# Finite-bit sampling and complete resource accounting

The [pair identity](pair-simulation.md) replaces a Poisson sequence of reflection jumps by one signed endpoint. This only becomes an efficient algorithm if the endpoint can be sampled without first generating the entire sequence. This page gives such a sampler, proves its finite-precision error bound, and accounts for its classical and quantum resources.

The implementation is [verification/pair_sampler.py](../verification/pair_sampler.py). Its construction path uses Python integers and exact rational numbers. Floating-point elementary functions are used only by the separate [diagnostic program](../verification/check_pair_sampler.py), not by the sampler or its error certificate.

## 1. Contract and parameters

Let $`A`$ and $`B`$ be exact Hermitian-involution oracles, with normalized generator

```math
\mathcal L_2=\frac12(\mathrm{Ad}_A+\mathrm{Ad}_B)-\mathrm{id}.
```

Supply a nonnegative rational time $`t`$ and a rational accuracy $`0\lt \epsilon\le1`$. The target norm is the full diamond norm, on arbitrary system inputs and arbitrary untouched references. The case $`t=0`$ returns the identity with no query and no random bit.

For $`t\gt 0`$, define the following integers:

```math
\begin{aligned}
u&=\left\lceil\log_2\frac8\epsilon\right\rceil,\qquad\\
m&=\left\lceil\sqrt{2tu}\right\rceil+u,\qquad\\
K&=2^{\lceil\log_2(2m)\rceil},\qquad\\
L&=\log_2 K.
\end{aligned}
\tag{1}
```

All ceilings in (1) can be computed by integer comparisons and integer square roots. No floating logarithm or square root is needed. The simulator applies at most

```math
Q=K/2\lt 2m
```

reflection queries on every run. In particular,

```math
\begin{aligned}
Q&=O\!\left(\sqrt{t\log(4/\epsilon)}+\log(4/\epsilon)\right).
\end{aligned}
\tag{2}
```

**Finite-bit sampling theorem.** The implementation below constructs a dyadic probability table, samples it using a fixed number of unbiased classical bits, and applies one alternating word. The resulting channel $`\widetilde{\mathcal E}_{t,\epsilon}`$ satisfies

```math
\begin{aligned}
\left\|\widetilde{\mathcal E}_{t,\epsilon}-e^{t\mathcal L_2}\right\|_\diamond
&\le\frac4{2^u}+\frac\epsilon{32}+\frac K{2^r}\\
&\le\frac{9\epsilon}{16},\qquad\\
r&=\left\lceil\log_2\frac{32K}{\epsilon}\right\rceil.
\end{aligned}
\tag{3}
```

Its classical preprocessing uses $`O(K\log K\,\mathrm{poly}(b))`$ bit operations, where $`b`$ accounts for the rational input length and $`\log((2+t)K/\epsilon)`$. Ordinary classical storage is $`O(K\mathrm{poly}(b))`$ bits. The cost is charged even for a single use; repeated uses at the same time and accuracy can reuse the table. The proof and the more explicit accounting follow.

## 2. A finite cyclic endpoint distribution

Let $`S_t=N_+-N_-`$ with independent $`N_\pm\sim\mathrm{Poisson}(t/2)`$. The exact pair channel applies $`W_{S_t}`$, as proved in [pair simulation](pair-simulation.md). Define

```math
\begin{aligned}
\phi_j&=e^{t(\cos(2\pi j/K)-1)},\qquad\\
q_a&=\frac1K\sum_{j=0}^{K-1}\phi_j e^{-2\pi i ja/K},\qquad\\
0&\le a\lt K.
\end{aligned}
\tag{4}
```

By finite Fourier orthogonality,

```math
\begin{aligned}
q_a&=\Pr\{S_t\equiv a\pmod K\}\\
&=\sum_{\ell\in\mathbb Z}\Pr\{S_t=a+\ell K\}.
\end{aligned}
\tag{5}
```

Thus $`q`$ is an ordinary probability distribution. Send residue $`a`$ to its signed representative

```math
\sigma(a)=
\begin{cases}
a,&0\le a\lt K/2,\\
a-K,&K/2\le a\lt K.
\end{cases}
```

The coupling $`a=S_t\bmod K`$ produces exactly the original word whenever $`-K/2\le S_t\lt K/2`$. Outside that interval, the two output channels can differ by at most two in diamond norm. The endpoint bound from [pair simulation, Eq. (9)](pair-simulation.md#4-a-hard-query-cap-for-arbitrary-accuracy) gives

```math
\begin{aligned}
\left\|
\sum_a q_a\mathrm{Ad}_{W_{\sigma(a)}}-e^{t\mathcal L_2}
\right\|_\diamond
&\le2\Pr\{|S_t|\ge K/2\}\\
&\le4e^{-u}\\
&\le\frac4{2^u}\le\frac\epsilon2.
\end{aligned}
\tag{6}
```

The inequality $`e^{-u}\le2^{-u}`$ lets the certificate use rational numbers throughout. The boundary event in (6) is a harmless enlargement: the representative $`-K/2`$ itself is preserved.

This construction approximates an endpoint distribution. It never generates the underlying $`\mathrm{Poisson}(t)`$ count or an individual jump history.

## 3. Certified elementary-function inputs

The Fourier transform must also be computed at finite precision. Set

```math
\begin{aligned}
\eta&=\frac{\epsilon}{128K(L+2)}.
\end{aligned}
\tag{7}
```

Use fixed-point numbers with scale $`D=2^p`$. An interval is a pair of integers $`(\ell,h)`$ representing $`[\ell/D,h/D]`$. Addition is exact; multiplication and division round the lower endpoint down and the upper endpoint up. Consequently each arithmetic operation preserves enclosure. Python's unbounded integers avoid machine overflow.

The required roots of unity and values $`\phi_j`$ are enclosed as follows.

**The constant $`\pi`$.** Use Machin's identity

```math
\pi=16\arctan(1/5)-4\arctan(1/239).
```

Each arctangent is evaluated by its alternating series. Stop when the next term is at most $`1/D`$, and include that signed remainder in the interval.

**Sine and cosine.** Reduce the indices to angles in $`[0,\pi]`$, using reflection symmetry for the remaining Fourier values. Taylor polynomials are evaluated by interval recurrences. Since the argument is smaller than four in magnitude, after cosine degree $`2n`$ and sine degree $`2n+1`$ the remainders are bounded by

```math
\frac{4^{2n+2}}{(2n+2)!},\qquad
\frac{4^{2n+3}}{(2n+3)!},
```

respectively. The next zero Taylor coefficient has been included when applying the Lagrange remainder theorem. Choose $`n`$ so that both bounds are at most $`1/D`$. Intersect the resulting intervals with $`[-1,1]`$. The special angles zero, $`\pi/2`$, and $`\pi`$ are represented exactly.

**The negative exponential.** For an enclosed nonnegative value $`x=t(1-\cos\theta)`$, evaluate $`e^{-x}`$ monotonically at its two interval endpoints. Put

```math
h=\left\lceil\log_2\frac{16}{\eta}\right\rceil.
```

If an endpoint is at least $`h`$, the enclosure $`[0,2^{-h}]`$ is valid. For an endpoint below $`h`$, divide by a power of two until the argument is at most $`1/4`$, evaluate the alternating exponential series there, and repeatedly square its enclosing interval. A degree-$`n`$ polynomial has remainder at most

```math
\frac{4^{-(n+1)}}{(n+1)!}.
```

Intersect each intermediate result with $`[0,1]`$. The number of squarings is $`O(\log h)`$, even when the original physical time is large.

Each midpoint is a fixed-point integer. Increase $`p`$ by doubling it until exact rational comparisons certify that every root coordinate and every $`\phi_j`$ midpoint has error at most $`\eta/4`$, and that $`D\ge8/\eta`$. No unverifiable rounding assumption enters this acceptance test. A termination and bit-complexity bound is given in Section 7.

The exponential cutoff itself has width at most $`2^{-h}`$ before outward rounding. Because $`2^{-h}\le\eta/16`$, it is safely below the midpoint tolerance and does not prevent precision refinement from terminating.

## 4. Error of the integer FFT

Compute the unnormalized negative-sign discrete Fourier transform of the fixed-point $`\phi_j`$ values by a radix-two FFT. The factorization requires $`KL/2`$ butterflies, as in the classical [Cooley–Tukey algorithm](https://doi.org/10.1090/S0025-5718-1965-0178586-1). The implementation contains its own integer butterfly loop; it does not call a floating FFT library.

A complex multiplication has the form

```math
\frac{(a+ib)(c+id)}{D}.
```

Each resulting integer coordinate is rounded down once. In physical fixed-point units, the complex rounding error is less than $`\sqrt2/D\le\eta/4`$. The interval certificate gives coordinate error at most $`\eta/4`$ for each root, hence complex root error less than $`\eta`$. The input-value error is also below $`\eta`$.

Let $`E_j`$ be the largest complex error after FFT stage $`j`$, before the final normalization by $`K`$. Exact stage-$`j`$ values have magnitude at most $`2^j`$ because the initial values satisfy $`|\phi_j|\le1`$. A butterfly therefore obeys the conservative recurrence

```math
\begin{aligned}
E_0&\le\eta,\\
\qquad E_{j+1}&\le(2+\eta)E_j+\eta\,2^j+\eta.
\end{aligned}
\tag{8}
```

The terms account, respectively, for previous errors in both butterfly inputs, the approximate unit root multiplying an exact value, and the fixed-point multiplication roundoff. Set $`F_j=E_j/2^j`$. Then

```math
F_{j+1}\le(1+\eta/2)F_j+\eta/2+\eta/2^{j+1},
```

so

```math
\begin{aligned}
F_L&\le e^{\eta L/2}\eta(2+L/2)\\
&\le2\eta(L+2).
\end{aligned}
\tag{9}
```

The last bound uses $`\eta L\le1`$, which follows amply from (7). Taking the real part cannot increase the error. Thus the real Fourier output divided by $`KD`$, denoted $`\widehat q`$, satisfies

```math
\begin{aligned}
\|\widehat q-q\|_1&\le\delta,\\
\qquad\delta&=2K\eta(L+2)=\epsilon/64.
\end{aligned}
\tag{10}
```

There is no extra division roundoff: the raw real FFT outputs are retained as integers, and the common factor $`KD`$ cancels in the subsequent exact normalization.

Some approximate outputs can be slightly negative. Clip them at zero to obtain $`a`$, and let $`Z=\sum_j a_j`$. Since $`q_j\ge0`$, clipping moves every coordinate toward its allowed range and cannot increase the error in (10). Hence

```math
\|a-q\|_1\le\delta,
\qquad |Z-1|\le\delta,
\qquad Z\gt 0.
```

The normalized probabilities $`v=a/Z`$ obey

```math
\begin{aligned}
\|v-q\|_1&\le\|v-a\|_1+\|a-q\|_1\\
&=|1-Z|+\|a-q\|_1\\
&\le2\delta=\epsilon/32.
\end{aligned}
\tag{11}
```

In the code, normalization is represented by the exact nonnegative integer masses and their sum. No approximate division is needed to define $`v`$.

## 5. Exact sampling from a dyadic table

Choose $`r`$ as in (3), let $`T=2^r`$, and initially set $`w_j=\lfloor Tv_j\rfloor`$. The integer deficit

```math
d=T-\sum_j w_j
```

lies between zero and $`K-1`$. Add one to each of the first $`d`$ entries. This produces nonnegative integer weights summing exactly to $`T`$, with

```math
\begin{aligned}
\left|\frac{w_j}{T}-v_j\right|&\le\frac1T,\qquad\\
\left\|\frac wT-v\right\|_1&\le\frac K{2^r}\le\frac\epsilon{32}.
\end{aligned}
\tag{12}
```

Draw exactly $`r`$ unbiased bits to obtain a uniform integer in $`\{0,\ldots,T-1\}`$. A binary search in the classical cumulative-weight table returns its interval and therefore an exactly distributed dyadic sample. Zero-weight entries are skipped by the same rule. There is no rejection loop and no random upper bound on preprocessing or oracle calls.

Apply the alternating word corresponding to $`\sigma(a)`$. Its first gate is $`A`$ when the signed coordinate is positive and $`B`$ when it is negative; the gates then alternate. Only its signed length is retained. An array containing the full word need not be stored.

For any fixed set of channels $`\mathcal U_j`$,

```math
\begin{aligned}
\left\|\sum_j(p_j-q_j)\mathcal U_j\right\|_\diamond
&\le\sum_j|p_j-q_j|.
\end{aligned}
\tag{13}
```

Thus the probability $`\ell_1`$ errors in (11) and (12) are already full diamond-norm error bounds. Adding the aliasing term (6) proves (3):

| Source | Full diamond-norm allowance |
|---|---|
| Replacing the integer endpoint by its cyclic representative | $`4/2^u\le\epsilon/2`$ |
| Certified elementary inputs, integer FFT, clipping, and normalization | $`\epsilon/32`$ |
| Dyadic probability rounding | $`K/2^r\le\epsilon/32`$ |
| Total | $`\le9\epsilon/16`$ |

Every branch of the simulator is an ordinary unitary channel. Mixing the branches with the dyadic probabilities makes the implemented map exactly completely positive and trace preserving, even before comparing it with the target.

## 6. Using the implementation

For example, from the repository root:

```python
import sys
from fractions import Fraction
sys.path.insert(0, "verification")
from pair_sampler import build_pair_sampler, alternating_actions

sampler = build_pair_sampler(Fraction(1000), Fraction(1, 100))
signed_length = sampler.sample_signed()
for gate_name in alternating_actions(signed_length):
    # Invoke the supplied A or B oracle on the existing system register.
    pass

assert abs(signed_length) <= sampler.query_cap
assert sampler.certificate["total_diamond_bound"] <= sampler.epsilon
```

For these exact inputs, the table has $`K=512`$ entries, the cap is $`256`$ reflection queries, and a sample uses $`21`$ random bits. The implementation certifies the inputs at $`63`$ fixed-point fractional bits. Its full diamond error certificate is $`0.004462890625`$, below the requested $`0.01`$.

The module accepts integers, rational strings, and `Fraction` objects. If a Python float is supplied, its decimal `str` representation is interpreted as an exact rational input; any discrepancy between that rational and an intended physical time is charged separately below. The scientific contract does not presume an infinite-precision real input.

## 7. Classical time, precision, and memory

Let $`B`$ be the total bit length of the supplied rational numerators and denominators. Arithmetic involving the time necessarily includes this input length. Write

```math
b=B+O\!\left(\log(2+t)+\log(K/\epsilon)\right).
```

The precision-refinement procedure terminates at $`p=O(\log(2+t)+\log(K/\epsilon))`$, with constant factors absorbing logarithms of these logarithms. To see this without assuming a floating elementary-function oracle, track the interval widths of Section 3:

- The arctangent sums use $`O(p)`$ terms and produce width $`O(p/2^p)`$ for $`\pi`$.
- The trigonometric Taylor recurrences use $`O(p)`$ terms. Their factorial denominators bound the amplification of earlier errors, giving width $`O(p^2/2^p)`$ on $`[0,\pi]`$.
- Multiplication by the exact rational time increases the exponent-input width by at most a factor $`t`$, plus one outward-rounding unit. The function $`e^{-x}`$ is one-Lipschitz for nonnegative $`x`$.
- In the exponential routine, the reduced argument is at most $`1/4`$. The Taylor enclosure has width $`O(p/2^p)`$. There are $`O(\log h)`$ squarings, each with derivative at most two on $`[0,1]`$, so their total amplification is $`O(h)`$.

Consequently a characteristic-value interval has width at most

```math
\begin{aligned}
&O\!\left(\frac{(1+t)p^2+hp}{2^p}\right)+2^{-h},
\end{aligned}
\tag{14}
```

with fixed constants independent of $`t,K,\epsilon`$. Its cutoff contribution is at most $`\eta/16`$. A number of precision bits proportional to $`\log(2+t)+\log(1/\eta)`$ therefore satisfies the acceptance inequalities. Doubling the precision does not change the asymptotic bound on total work.

There are $`O(Kp)`$ elementary-function interval operations and $`KL/2`$ FFT butterflies. Every integer has $`O(b+\log K)`$ bits, including the input-dependent exponent arithmetic and the growing unnormalized FFT values. Ordinary integer multiplication and division suffice, so the bit cost is

```math
\begin{aligned}
&O\!\left(K\log K\,\mathrm{poly}(b)\right).
\end{aligned}
\tag{15}
```

This expression charges the elementary-function evaluation, the FFT, clipping, normalization, and dyadic table construction. A quadratic-length direct discrete Fourier transform would not give (15); the radix-two factorization is essential to the stated preprocessing cost.

During construction, the arrays require $`O(K\mathrm{poly}(b))`$ ordinary classical bits. After construction, the cumulative table requires $`O(Kr)`$ bits. Each sample uses exactly $`r=O(\log(K/\epsilon))`$ random bits and $`O(\log K)`$ comparisons of $`r`$-bit integers. Driving the alternating oracle sequence requires a counter of $`O(\log K)`$ bits and at most $`O(Q\log K)`$ classical bit operations under a simple binary-counter accounting.

The table is read by a classical processor before the gate sequence is applied. It is never queried in superposition, loaded into amplitudes, or assumed available through QRAM. Random bits may be classical; if generated by measuring a reusable qubit, their gates and measurements can instead be charged explicitly.

## 8. Quantum gates and implementation accuracy

The exact-oracle theorem charges every call to $`A`$ or $`B`$. It requires no controlled unknown operation and no inverse operation other than the same supplied involution. A classical controller selects the gate for each step. With separately supplied oracles, the upper-bound algorithm needs no additional coherent register. With a supplied two-label `SELECT` oracle, a computational-basis label and its constant-size preparation suffice.

If implementations of the reflections use at most $`G`$ elementary gates and $`w`$ clean work qubits per call, the resulting simulation uses at most $`QG+O(Q)`$ quantum gates and $`w+O(1)`$ extra coherent work qubits, beyond the existing system. This is a conditional implementation statement: the black-box theorem does not provide a cheap synthesis of an arbitrary reflection. It does not prepare, load, or replace the unknown system input.

The exact rational time used by the sampler and the accuracy of the implemented oracles can be accounted for separately. For $`s,t\ge0`$,

```math
\begin{aligned}
\|e^{t\mathcal L_2}-e^{s\mathcal L_2}\|_\diamond
&\le2|t-s|,
\end{aligned}
\tag{16}
```

because $`\|\mathcal L_2\|_\diamond\le2`$ and every intervening semigroup channel has diamond norm one. If each implemented unitary differs from the corresponding ideal reflection by at most $`\delta`$ in operator norm, its conjugation channel differs by at most $`2\delta`$ in diamond norm. A hybrid argument along a word of length at most $`Q`$ then gives an additional $`2Q\delta`$ error. The synthesized gates need not themselves satisfy exact involution relations for this comparison; they are compared with the ideal gates actually used in the already reduced word.

Thus a sampler built for rational time $`\widetilde t`$ and accuracy parameter $`\epsilon`$ has total physical implementation error at most

```math
\begin{aligned}
&\frac{9\epsilon}{16}
+2|t-\widetilde t|
+2Q\delta.
\end{aligned}
\tag{17}
```

For example, $`|t-\widetilde t|\le\epsilon/16`$ and $`\delta\le\epsilon/(16\max\{1,Q\})`$ make (17) at most $`13\epsilon/16`$. Gate-synthesis costs needed to meet that $`\delta`$ belong in $`G`$. The actual certificate in (3) may be used instead of $`9\epsilon/16`$ for a tighter budget.

## 9. Verification and its scope

The construction module needs only the Python standard library. The independent numerical checks additionally need NumPy and SciPy. Run:

```bash
python verification/check_pair_sampler.py
```

The command prints one JSON object whose success field is:

```json
{"status": "pass"}
```

It checks exact normalization and nonnegativity of the dyadic weights, the rational certificate inequalities, and every nonempty inverse-CDF interval boundary. It also enumerates the $`511`$ words of length at most eight to verify chronological gate order and endpoint multiplicities.

For independent numerical comparisons, it evaluates the Skellam probabilities through scaled Bessel functions, rather than another FFT, on eight cases including zero time, a small rational time, $`t=10^4`$, and accuracy $`10^{-8}`$. The Bessel reference is truncated with its own exponentially small analytic tail allowance. Five channel examples compare the implemented mixture with a direct exponential of the full superoperator: identical reflections, anticommuting qubit reflections, two tilted-qubit times, and complex four-dimensional noncommuting reflections.

The channel diagnostic reports the trace norm of the **unnormalized** Choi matrix of the difference. That quantity upper-bounds the diamond norm, but it is evaluated in floating arithmetic and is labeled a numerical estimate. The tests also check trace preservation. These finite checks address implementation errors and conventions; the all-dimension, all-time error certificate follows from (6)–(13), and the resource bound follows from the arithmetic construction and (14)–(15).
