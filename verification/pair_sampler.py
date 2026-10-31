"""Certified finite-bit sampler for two reflection Lindbladians.

The production path uses only Python integers and fractions.  It computes a
wrapped Skellam law by a radix-2 FFT, with interval-certified elementary
functions and a proved FFT rounding allowance.  No Poisson trajectory is
generated.  NumPy and SciPy are deliberately not dependencies of this module.

See science/sampling-and-resources.md for the error proof and bit complexity.
The requested time and error are interpreted as exact rational numbers;
floats, if passed, are interpreted by their decimal ``str`` representation.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction
from math import factorial, isqrt
from random import SystemRandom
from typing import Iterator


Interval = tuple[int, int]  # Endpoints divided by the common scale 2**p.
ComplexInt = tuple[int, int]


def _fraction(value: Fraction | int | str | float) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(str(value))


def _ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def _ceil_log2(x: Fraction) -> int:
    """Smallest integer n with 2**n >= x, for positive rational x."""
    if x <= 0:
        raise ValueError("logarithm argument must be positive")
    n = x.numerator.bit_length() - x.denominator.bit_length()
    if n >= 0:
        return n if x.numerator <= x.denominator << n else n + 1
    return n if x.numerator << (-n) <= x.denominator else n + 1


def _ceil_sqrt(x: Fraction) -> int:
    if x < 0:
        raise ValueError("square-root argument must be nonnegative")
    n = isqrt(x.numerator // x.denominator)
    return n if n * n * x.denominator == x.numerator else n + 1


class _FixedIntervals:
    """Outward-rounded interval arithmetic at one dyadic precision."""

    def __init__(self, bits: int):
        self.bits = bits
        self.scale = 1 << bits
        # Taylor remainder bounds use |theta| < 4 and 0 <= y <= 1/4.
        n = 0
        while (4 ** (2 * n + 2) * self.scale > factorial(2 * n + 2)
               or 4 ** (2 * n + 3) * self.scale > factorial(2 * n + 3)):
            n += 1
        self.trig_terms = n
        n = 0
        while self.scale > (4 ** (n + 1)) * factorial(n + 1):
            n += 1
        self.exp_terms = n
        self.pi = self._pi()

    @staticmethod
    def add(a: Interval, b: Interval) -> Interval:
        return a[0] + b[0], a[1] + b[1]

    @staticmethod
    def neg(a: Interval) -> Interval:
        return -a[1], -a[0]

    @staticmethod
    def div_int(a: Interval, n: int) -> Interval:
        if n <= 0:
            raise ValueError("positive divisor required")
        return a[0] // n, _ceil_div(a[1], n)

    @staticmethod
    def times_rational(a: Interval, x: Fraction) -> Interval:
        lo, hi = (a if x >= 0 else (a[1], a[0]))
        return ((lo * x.numerator) // x.denominator,
                _ceil_div(hi * x.numerator, x.denominator))

    def mul(self, a: Interval, b: Interval) -> Interval:
        products = (a[0] * b[0], a[0] * b[1],
                    a[1] * b[0], a[1] * b[1])
        return (min(products) // self.scale,
                _ceil_div(max(products), self.scale))

    @staticmethod
    def clip(a: Interval, lo: int, hi: int) -> Interval:
        result = max(a[0], lo), min(a[1], hi)
        if result[0] > result[1]:
            raise ArithmeticError("empty certified interval")
        return result

    def _atan_reciprocal(self, q: int) -> Interval:
        # Alternating series; after n terms the remainder has the sign of
        # term n and magnitude at most 1 / ((2*n+1)*q**(2*n+1)).
        result = (0, 0)
        power, n = q, 0
        while True:
            denominator = (2 * n + 1) * power
            if denominator >= self.scale:
                tail = (0, 1) if n % 2 == 0 else (-1, 0)
                return self.add(result, tail)
            term = (self.scale // denominator,
                    _ceil_div(self.scale, denominator))
            result = self.add(result, term if n % 2 == 0 else self.neg(term))
            power *= q * q
            n += 1

    def _pi(self) -> Interval:
        # Machin's identity: pi = 16 atan(1/5) - 4 atan(1/239).
        return self.add(
            self.times_rational(self._atan_reciprocal(5), Fraction(16)),
            self.times_rational(self._atan_reciprocal(239), Fraction(-4)),
        )

    def sin_cos(self, index: int, modulus: int) -> tuple[Interval, Interval]:
        """Enclose sin(2*pi*index/modulus), cos(...), 0 <= index <= K/2."""
        q = self.scale
        if index == 0:
            return (0, 0), (q, q)
        if 2 * index == modulus:
            return (0, 0), (-q, -q)
        if 4 * index == modulus:
            return (q, q), (0, 0)
        theta = self.times_rational(self.pi, Fraction(2 * index, modulus))
        if not (0 <= theta[0] <= theta[1] < 4 * q):
            raise ArithmeticError("trigonometric range reduction failed")
        theta2 = self.mul(theta, theta)
        cterm, sterm = (q, q), theta
        cosine, sine = cterm, sterm
        for k in range(1, self.trig_terms + 1):
            cterm = self.neg(self.div_int(self.mul(cterm, theta2), (2*k-1)*(2*k)))
            sterm = self.neg(self.div_int(self.mul(sterm, theta2), (2*k)*(2*k+1)))
            cosine = self.add(cosine, cterm)
            sine = self.add(sine, sterm)
        # Lagrange remainders are at most one unit in the last place.
        return (self.clip((sine[0]-1, sine[1]+1), -q, q),
                self.clip((cosine[0]-1, cosine[1]+1), -q, q))

    def exp_minus_point(self, x: int, cutoff: int) -> Interval:
        """Enclose exp(-x/scale) for a nonnegative integer x."""
        q = self.scale
        if x == 0:
            return q, q
        if x >= cutoff * q:
            # exp(-h) <= 2**(-h), using e >= 2.
            return 0, _ceil_div(q, 1 << cutoff)
        shifts = max(0, (4*x).bit_length() - q.bit_length())
        while 4*x > q << shifts:
            shifts += 1
        y = x // (1 << shifts), _ceil_div(x, 1 << shifts)
        if y[1] > q // 4:
            # Outward rounding may put the upper endpoint one ulp above 1/4.
            shifts += 1
            y = x // (1 << shifts), _ceil_div(x, 1 << shifts)
        term, result = (q, q), (q, q)
        for k in range(1, self.exp_terms + 1):
            term = self.div_int(self.mul(term, y), k)
            result = self.add(result, term if k % 2 == 0 else self.neg(term))
        result = self.clip((result[0]-1, result[1]+1), 0, q)
        for _ in range(shifts):
            result = self.clip(self.mul(result, result), 0, q)
        return result

    def exp_minus(self, x: Interval, cutoff: int) -> Interval:
        if x[0] < 0:
            raise ValueError("negative exponential argument")
        low = self.exp_minus_point(x[1], cutoff)[0]
        high = self.exp_minus_point(x[0], cutoff)[1]
        return low, high


def _midpoint_and_radius(interval: Interval) -> tuple[int, int]:
    midpoint = (interval[0] + interval[1]) // 2
    return midpoint, max(midpoint-interval[0], interval[1]-midpoint)


def _integer_fft(values: list[int], roots: list[ComplexInt], scale: int) -> list[ComplexInt]:
    """Unnormalized negative-sign DFT, with one floor per output coordinate."""
    k = len(values)
    data = [(v, 0) for v in values]
    j = 0
    for i in range(1, k):
        bit = k >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            data[i], data[j] = data[j], data[i]
    length = 2
    while length <= k:
        half, stride = length // 2, k // length
        for start in range(0, k, length):
            for j in range(half):
                ur, ui = data[start+j]
                vr, vi = data[start+j+half]
                wr, wi = roots[j*stride]
                pr = (vr*wr - vi*wi) // scale
                pi = (vr*wi + vi*wr) // scale
                data[start+j] = ur+pr, ui+pi
                data[start+j+half] = ur-pr, ui-pi
        length *= 2
    return data


@dataclass(frozen=True)
class PairSampler:
    """A fixed-bit probability table and its deterministic error certificate."""

    time: Fraction
    epsilon: Fraction
    modulus: int
    random_bits: int
    weights: tuple[int, ...]
    cumulative: tuple[int, ...]
    certificate: dict[str, int | Fraction]

    @property
    def query_cap(self) -> int:
        return self.modulus // 2

    @property
    def denominator(self) -> int:
        return 1 << self.random_bits

    def sample_signed(self, rng=None) -> int:
        """Use exactly random_bits unbiased bits, then ordinary binary search."""
        if rng is None:
            rng = SystemRandom()
        residue = bisect_right(self.cumulative, rng.getrandbits(self.random_bits))
        return residue if residue < (self.modulus+1)//2 else residue-self.modulus

    def probabilities(self) -> tuple[Fraction, ...]:
        return tuple(Fraction(w, self.denominator) for w in self.weights)


def alternating_actions(position: int) -> Iterator[str]:
    """Chronological gates: positive starts A, negative starts B, then alternates."""
    first = "A" if position > 0 else "B"
    second = "B" if position > 0 else "A"
    for step in range(abs(position)):
        yield first if step % 2 == 0 else second


def build_pair_sampler(
    time: Fraction | int | str | float,
    epsilon: Fraction | int | str | float,
) -> PairSampler:
    """Construct a sampler whose reflection channel error is at most epsilon.

    The cap is K/2, where K is a power of two of order
    sqrt(t*log(1/epsilon)) + log(1/epsilon).  The certificate bounds the full
    diamond norm, not half the diamond norm.  Inputs describe exact oracles;
    input-time rounding and gate synthesis are separate errors.
    """
    t, eps = _fraction(time), _fraction(epsilon)
    if t < 0 or not 0 < eps <= 1:
        raise ValueError("require time >= 0 and 0 < epsilon <= 1")
    if t == 0:
        return PairSampler(t, eps, 1, 0, (1,), (1,), {
            "precision_bits": 0, "precision_attempts": 0,
            "alias_diamond_bound": Fraction(0),
            "arithmetic_l1_bound": Fraction(0),
            "dyadic_l1_bound": Fraction(0),
            "total_diamond_bound": Fraction(0),
        })
    u = _ceil_log2(8 / eps)
    radius = _ceil_sqrt(2*t*u) + u
    k = 1 << (2*radius-1).bit_length()
    levels = k.bit_length()-1
    eta = eps / (128*k*(levels+2))
    elementary_bits = _ceil_log2(1/eta)
    bits = max(32, elementary_bits + max(0, _ceil_log2(1+t))
               + 16 + 2*(elementary_bits+1).bit_length())
    cutoff = _ceil_log2(16/eta)
    attempts = 0
    while True:
        attempts += 1
        ctx = _FixedIntervals(bits)
        scale = ctx.scale
        phi, roots = [0]*k, []
        max_root_radius = max_phi_radius = 0
        for j in range(k//2+1):
            sin_iv, cos_iv = ctx.sin_cos(j, k)
            sine, sradius = _midpoint_and_radius(sin_iv)
            cosine, cradius = _midpoint_and_radius(cos_iv)
            if j < k//2:
                roots.append((cosine, -sine))
                max_root_radius = max(max_root_radius, sradius, cradius)
            argument = ctx.times_rational((scale-cos_iv[1], scale-cos_iv[0]), t)
            interval = ctx.exp_minus(argument, cutoff)
            midpoint, radius_phi = _midpoint_and_radius(interval)
            max_phi_radius = max(max_phi_radius, radius_phi)
            phi[j] = midpoint
            if 0 < j < k//2:
                phi[k-j] = midpoint
        # These are exact rational comparisons.  Each root coordinate and
        # characteristic value has error <= eta/4; sqrt(2)/scale <= eta/4.
        if (4*max(max_root_radius, max_phi_radius) <= eta*scale
                and eta*scale >= 8):
            break
        bits *= 2
    transformed = _integer_fft(phi, roots, scale)
    masses = [max(0, z[0]) for z in transformed]
    mass = sum(masses)
    if mass <= 0:
        raise ArithmeticError("nonpositive Fourier normalization")
    random_bits = _ceil_log2(32*k/eps)
    denominator = 1 << random_bits
    weights = [(denominator*m)//mass for m in masses]
    deficit = denominator-sum(weights)
    if not 0 <= deficit < k:
        raise ArithmeticError("invalid dyadic remainder")
    for j in range(deficit):
        weights[j] += 1
    cumulative, running = [], 0
    for weight in weights:
        running += weight
        cumulative.append(running)
    alias_bound = Fraction(4, 1 << u)
    arithmetic_bound = 4*k*eta*(levels+2)
    dyadic_bound = Fraction(k, denominator)
    total_bound = alias_bound+arithmetic_bound+dyadic_bound
    if total_bound > eps:
        raise ArithmeticError("requested error budget was exceeded")
    return PairSampler(t, eps, k, random_bits, tuple(weights), tuple(cumulative), {
        "tail_exponent": u,
        "tail_radius": radius,
        "precision_bits": bits,
        "precision_attempts": attempts,
        "fft_levels": levels,
        "root_coordinate_error_bound": Fraction(max_root_radius, scale),
        "characteristic_error_bound": Fraction(max_phi_radius, scale),
        "eta": eta,
        "alias_diamond_bound": alias_bound,
        "arithmetic_l1_bound": arithmetic_bound,
        "dyadic_l1_bound": dyadic_bound,
        "total_diamond_bound": total_bound,
        "fft_butterflies": k*levels//2,
    })
