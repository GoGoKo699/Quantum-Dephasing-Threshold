# Verification

The analytical proofs establish the asymptotic query bounds and the full diamond-norm guarantees. This directory supplies a certified finite-bit endpoint sampler and independent finite diagnostics of the identities and hard instances used in those proofs.

## Reproduce

Use Python **3.11 or later** for the pinned numerical dependencies. The recorded run used Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0. From the repository root:

```bash
python -m pip install -r verification/requirements.txt
python verification/run_all.py
```

The runner executes both check programs, stops on a failed command, and prints one JSON object with `"status": "pass"` when both succeed. To retain a fresh report:

```bash
python verification/run_all.py --output verification/results/latest.json
```

An actual representative output is committed at [expected/results.json](expected/results.json). Compare the tested domains, status and tolerance assertions; floating-point values can vary slightly across platforms. The suite does not require byte-for-byte equality with that example.

The construction module [pair_sampler.py](pair_sampler.py) uses only Python's standard library. NumPy and SciPy are needed by the diagnostic programs, not by its sampling or certification path. The tests use Python assertions, so run the documented commands without the optimization flag `-O`.

## What is checked

| Program | Finite scope | What it can reveal |
|---|---|---|
| [check_pair_sampler.py](check_pair_sampler.py) | All 511 words of lengths zero through eight; eight rational-time/accuracy distribution cases; five direct channel comparisons | Word orientation, endpoint multiplicities, dyadic normalization, certificate arithmetic, inverse-CDF boundaries, and discrepancies with independent Bessel/exponential calculations |
| [check_channels.py](check_channels.py) | Twelve random pair channels in dimensions 2, 4 and 8; seven qubit signal cases; six finite radial chains; 9,120 colored-edge checks | Channel-identity errors, normalization conventions, the exact qubit formula, finite-tree boundary behavior, involution and prefix-parity invariants |

The random reflection seed in `check_channels.py` is fixed at `261031`. Pair times are 0.1, 1, 10 and 100. Qubit cases use exactly the lower-bound angle $`\theta=t^{-1/2}`$ at times 1, 1.5, 4, 16, 64, 256 and 1024. Radial times are 48, 60, 100, 192, 768 and 1536, with $`m=\lfloor t/48\rfloor`$ and $`R=\lceil4t\rceil`$ as in the proof. The structural tree has radius six and checks all sixteen four-bit strings.

The sampler diagnostics include zero time, small rational times, time $`10^4`$, and accuracy $`10^{-8}`$. Channel examples include identical reflections, anticommuting qubit reflections, tilted qubit axes and complex noncommuting four-dimensional reflections. See the JSON report for the full parameters.

## Representative observed results

The recorded aggregate run passed. Its largest reduced-word matrix discrepancy was about $`6.17\times10^{-15}`$. The maximum discrepancy between the independently exponentiated pair superoperator and the truncated exact endpoint mixture was about $`4.57\times10^{-14}`$. The sampler's five channel comparisons had maximum unnormalized-Choi trace-norm estimate about $`2.02\times10^{-5}`$, within their requested error budgets; their maximum trace-preservation discrepancy was about $`8.18\times10^{-16}`$.

These quantities answer different questions. A small superoperator spectral-norm error is an identity diagnostic, not itself the claimed dimension-independent diamond certificate. The trace norm of the unnormalized Choi matrix does upper-bound the diamond norm, but the reported value is evaluated in floating arithmetic and is therefore a numerical estimate. Neither is a replacement for a proof covering all dimensions or real times.

## What makes the sampler certificate different

The sampler's production path contains no floating exponential, trigonometric function or FFT. It uses exact rational inputs, outward-rounded integer intervals for elementary functions, an integer radix-two FFT, and a normalized table of dyadic probabilities. Exact rational comparisons enforce the stated elementary-input tolerance before the FFT runs. Its certificate bounds the remaining FFT, clipping, normalization, dyadic-rounding and aliasing errors using the inequalities proved in [Sampling and resources](../science/sampling-and-resources.md).

The certificate depends on the analytical correctness of those bounds and their implementation. Finite tests cannot independently prove that correctness. The separate diagnostics compare the implementation with a different evaluation method—scaled Bessel probabilities and direct small-matrix exponentiation—to expose likely convention or coding mistakes.

## Proof routes and limits

- [Model and results](../science/model-and-results.md) defines the target, query cap and norm convention.
- [Pair simulation](../science/pair-simulation.md) proves the exact word identity and the tail-to-channel conversion.
- [Sampling and resources](../science/sampling-and-resources.md) proves the finite-bit certificate, termination and bit-complexity bounds.
- [Lower bounds](../science/lower-bounds.md) proves the qubit hybrid argument, the controlled SELECT compiler and the parity reduction.

The suite does not test every quantum input, prove a query lower bound numerically, certify experimental noise, or establish optimal joint precision dependence. It also does not claim that the exponentially large hard tree is explicitly stored or simulated at its full Hilbert-space size: the radial check uses the exact reduced birth–death chain, while structural checks use a small finite tree. The analytical construction supplies the arbitrary-size result.
