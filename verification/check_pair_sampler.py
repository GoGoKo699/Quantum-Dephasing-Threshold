"""Finite diagnostics for the certified reflection-pair sampler.

Run from the repository root:
    python verification/check_pair_sampler.py

The sampler itself uses exact rational/integer arithmetic.  This diagnostic
uses NumPy/SciPy floating arithmetic for independent Bessel and matrix-
exponential comparisons.  These finite comparisons do not prove the theorem.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import ceil, sqrt
import json

import numpy as np
from scipy.linalg import expm
from scipy.special import ive

from pair_sampler import alternating_actions, build_pair_sampler


def _word(position: int, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    result = np.eye(a.shape[0], dtype=complex)
    for action in alternating_actions(position):
        result = (a if action == "A" else b) @ result
    return result


def _adjoint(unitary: np.ndarray) -> np.ndarray:
    # Column-major vectorization: vec(U rho U†) = (U* tensor U) vec(rho).
    return np.kron(unitary.conj(), unitary)


def _choi(superoperator: np.ndarray, dimension: int) -> np.ndarray:
    # Unnormalized Choi matrix sum_ij |i><j| tensor Phi(|i><j|).
    result = np.zeros((dimension**2, dimension**2), dtype=complex)
    for i in range(dimension):
        for j in range(dimension):
            column = superoperator[:, i+dimension*j]
            block = column.reshape((dimension, dimension), order="F")
            result[i*dimension:(i+1)*dimension,
                   j*dimension:(j+1)*dimension] = block
    return result


def _random_reflection(dimension: int, rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(dimension, dimension)) + 1j*rng.normal(size=(dimension, dimension))
    unitary, _ = np.linalg.qr(matrix)
    signs = np.ones(dimension)
    signs[dimension//2:] = -1
    return (unitary*signs) @ unitary.conj().T


def check_word_orientation() -> dict:
    rng = np.random.default_rng(52963)
    a, b = (_random_reflection(4, rng) for _ in range(2))
    maximum = 0.0
    count = 0
    for length in range(9):
        endpoint_counts: dict[int, int] = {}
        for letters in product(("A", "B"), repeat=length):
            position = 0
            matrix = np.eye(4, dtype=complex)
            for action in letters:
                parity = 1 if position % 2 == 0 else -1
                position += parity if action == "A" else -parity
                matrix = (a if action == "A" else b) @ matrix
            error = float(np.linalg.norm(matrix-_word(position, a, b)))
            maximum = max(maximum, error)
            endpoint_counts[position] = endpoint_counts.get(position, 0)+1
            count += 1
        # Fair letters must give the same endpoint multiplicities as fair ±1 steps.
        walk_counts: dict[int, int] = {}
        for steps in product((-1, 1), repeat=length):
            endpoint = sum(steps)
            walk_counts[endpoint] = walk_counts.get(endpoint, 0)+1
        assert endpoint_counts == walk_counts
    assert maximum < 1e-11
    return {"words_checked": count, "maximum_matrix_difference": maximum}


def check_distributions() -> list[dict]:
    cases = [(0, ".01"), (".00001", ".2"), (".01", ".1"),
             (1, ".01"), (20, ".001"), (1000, ".01"), (10000, ".05"),
             (Fraction(1, 3), "0.00000001")]
    rows = []
    for time, epsilon in cases:
        sampler = build_pair_sampler(time, epsilon)
        k, cert = sampler.modulus, sampler.certificate
        assert all(weight >= 0 for weight in sampler.weights)
        assert sum(sampler.weights) == sampler.denominator
        assert sampler.cumulative[-1] == sampler.denominator
        assert cert["total_diamond_bound"] <= sampler.epsilon
        if sampler.time:
            eta = cert["eta"]
            assert cert["root_coordinate_error_bound"] <= eta/4
            assert cert["characteristic_error_bound"] <= eta/4
            assert eta*(1 << cert["precision_bits"]) >= 8
        t = float(sampler.time)
        # At u=80 the omitted two-sided Bessel tail is <=2 exp(-80), far
        # below the floating comparison tolerance.  The reference uses the
        # Bessel series, not another evaluation of the sampler's FFT.
        radius = max(k, ceil(sqrt(2*t*80)+80))
        positions = np.arange(-radius, radius+1, dtype=np.int64)
        if t == 0:
            probabilities = np.asarray(positions == 0, dtype=float)
        else:
            probabilities = ive(np.abs(positions), t)
        wrapped = np.bincount(positions % k, weights=probabilities, minlength=k)
        computed = np.asarray(sampler.weights, dtype=float)/sampler.denominator
        l1_error = float(np.abs(computed-wrapped).sum())
        numerical_allowance = float(cert["arithmetic_l1_bound"]+cert["dyadic_l1_bound"])
        assert l1_error <= numerical_allowance+2e-12
        tail = float(probabilities[np.abs(positions) >= k//2].sum()) if t else 0.0
        assert 2*tail <= float(cert["alias_diamond_bound"])+2e-12
        # Test exact inverse-CDF interval boundaries, including zero weights.
        class FixedBits:
            def __init__(self, value: int):
                self.value = value
            def getrandbits(self, bits: int) -> int:
                assert bits == sampler.random_bits
                return self.value
        start = 0
        for residue, weight in enumerate(sampler.weights):
            if weight:
                signed = residue if residue < (k+1)//2 else residue-k
                assert sampler.sample_signed(FixedBits(start)) == signed
                assert sampler.sample_signed(FixedBits(start+weight-1)) == signed
                assert abs(signed) <= sampler.query_cap
            start += weight
        rows.append({
            "time": str(sampler.time), "epsilon": str(sampler.epsilon),
            "modulus": k, "query_cap": sampler.query_cap,
            "precision_bits": cert["precision_bits"],
            "precision_attempts": cert["precision_attempts"],
            "random_bits": sampler.random_bits,
            "l1_to_wrapped_bessel": l1_error,
            "two_sided_alias_tail": tail,
            "certified_diamond_error": float(cert["total_diamond_bound"]),
        })
    return rows


def check_channels() -> list[dict]:
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    z = np.diag([1, -1]).astype(complex)
    rng = np.random.default_rng(52964)
    random_a, random_b = (_random_reflection(4, rng) for _ in range(2))
    theta = 0.31
    tilted = np.cos(theta)*z + np.sin(theta)*x
    cases = [
        ("identical-qubit", z, z, "0.1", ".01"),
        ("anticommuting-qubit", z, x, "3", ".01"),
        ("tilted-qubit", z, tilted, "1", ".001"),
        ("tilted-qubit-long", z, tilted, "30", ".001"),
        ("complex-four-dimensional", random_a, random_b, "4", ".001"),
    ]
    rows = []
    for name, a, b, time, epsilon in cases:
        sampler = build_pair_sampler(time, epsilon)
        dimension = len(a)
        identity = np.eye(dimension**2, dtype=complex)
        target = expm(float(sampler.time)*(0.5*(_adjoint(a)+_adjoint(b))-identity))
        simulated = np.zeros_like(target)
        for residue, weight in enumerate(sampler.weights):
            position = residue if residue < sampler.modulus//2 else residue-sampler.modulus
            simulated += (weight/sampler.denominator)*_adjoint(_word(position, a, b))
        difference = simulated-target
        choi_difference = _choi(difference, dimension)
        # ||Phi||_diamond <= ||J(Phi)||_1 for the unnormalized Choi matrix.
        # The right side is evaluated numerically here, not as an interval.
        choi_bound = float(np.linalg.svd(choi_difference, compute_uv=False).sum())
        assert choi_bound < float(sampler.epsilon)
        trace_row = np.eye(dimension).reshape(dimension**2, order="F")
        tp_error = float(np.linalg.norm(trace_row @ simulated-trace_row))
        assert tp_error < 1e-11
        rows.append({
            "case": name, "dimension": dimension, "time": time,
            "query_cap": sampler.query_cap,
            "choi_trace_norm_diamond_upper_estimate": choi_bound,
            "trace_preservation_error": tp_error,
        })
    return rows


def main() -> None:
    report = {
        "status": "pass",
        "scope": "finite floating diagnostics plus exact certificate checks; not a proof",
        "word_identity": check_word_orientation(),
        "distributions": check_distributions(),
        "channels": check_channels(),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
