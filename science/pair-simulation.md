# Why two reflection baths can be simulated in square-root time

Two noncommuting reflections can produce a long sequence of jumps. Their accumulated action nevertheless has a short description: cancel adjacent repetitions, and the remaining letters alternate. The length of this reduced word is the distance traveled by a symmetric random walk on a line. It typically grows as the square root of the physical time.

This page proves the exact channel identity behind that statement, then converts it into a simulation with a deterministic query cap. The [model and results](model-and-results.md) specify the oracle contract and the fixed-error complexity theorem. The [sampling and resource account](sampling-and-resources.md) supplies a finite-bit implementation without generating a time-length jump trajectory. The matching lower bound is in [lower bounds](lower-bounds.md).

## 1. Model and exact Poisson expansion

Let $`A`$ and $`B`$ be Hermitian involutions on an arbitrary finite-dimensional system:

```math
A=A^\dagger,\qquad B=B^\dagger,\qquad A^2=B^2=I.
```

Write $`\operatorname{Ad}_U(\rho)=U\rho U^\dagger`$. The normalized generator is

```math
\mathcal L_2
=\frac12\bigl(\operatorname{Ad}_A+\operatorname{Ad}_B\bigr)
-\operatorname{id}.
```

The total jump rate is one. Put $`\mathcal P=(\operatorname{Ad}_A+\operatorname{Ad}_B)/2`$. Since the identity superoperator commutes with every superoperator,

```math
e^{t\mathcal L_2}
=e^{-t}\sum_{n=0}^{\infty}\frac{t^n}{n!}\mathcal P^n.
\tag{1}
```

Thus an exact trajectory description first draws $`N\sim\operatorname{Poisson}(t)`$ and then applies $`N`$ independent fair choices of $`A`$ and $`B`$. Equation (1) follows directly from the exponential series; it is an identity of channels, including on inputs entangled with an untouched reference. The constant-rate trajectory viewpoint also appears in the general simulation framework of [Borras and Marvian, Section 4](https://arxiv.org/html/2509.10425v2).

Directly generating and applying all these letters has expected cost $`t`$. The following reduction acts on their product before it is applied to the system.

## 2. The reduced word is a walk on a line

Represent a word in **chronological order**, so the first listed letter is the first gate applied. Delete every adjacent pair $`AA`$ or $`BB`$. The operator product is unchanged because $`A^2=B^2=I`$. A stack implements this reduction: a new letter cancels the top letter if they agree, and otherwise is pushed onto the stack. Every surviving nonempty word alternates.

Index alternating words by signed integers. Let $`W_0=I`$. For $`s>0`$, apply $`s`$ alternating gates beginning with $`A`$. For $`s<0`$, apply $`|s|`$ alternating gates beginning with $`B`$. For example,

| Coordinate | Chronological gates | Resulting operator |
|---|---|---|
| $`-3`$ | $`B,A,B`$ | $`BAB`$ |
| $`-2`$ | $`B,A`$ | $`AB`$ |
| $`-1`$ | $`B`$ | $`B`$ |
| $`0`$ | none | $`I`$ |
| $`1`$ | $`A`$ | $`A`$ |
| $`2`$ | $`A,B`$ | $`BA`$ |
| $`3`$ | $`A,B,A`$ | $`ABA`$ |

Appending a gate chronologically means multiplying the operator on the left. Its action on the coordinate is

```math
A W_s=W_{T_A(s)},\qquad
B W_s=W_{T_B(s)},
```

```math
T_A(s)=s+(-1)^s,\qquad
T_B(s)=s-(-1)^s.
\tag{2}
```

Each map swaps disjoint neighboring pairs of integers and is itself an involution. At every coordinate, a fair choice of $`A`$ or $`B`$ therefore moves right or left with equal probability. Conditional on the entire past, the next increment is a fair sign; consequently the increments are independent fair signs.

The abstract graph in this argument is the Cayley graph of $`\mathbb Z_2*\mathbb Z_2`$, which is a line. No infinite-dimensional register is used by the simulator. The graph only records a classical word. Particular matrices may obey additional relations and identify several $`W_s`$; these relations cannot invalidate (2) or the resulting channel identity.

## 3. Exact endpoint law and exact channel identity

Let $`S_t`$ be the coordinate after the Poisson number of steps in (1). Splitting a rate-one Poisson process into independent fair right and left events gives

```math
S_t=N_+-N_-,\qquad
N_+,N_-\ \text{independent},\qquad
N_+,N_-\sim\operatorname{Poisson}(t/2).
\tag{3}
```

The signed endpoint has the symmetric Skellam distribution. Its probabilities can be defined without special-function notation by

```math
p_s(t)
=e^{-t}\sum_{j=0}^{\infty}
\frac{(t/2)^{2j+|s|}}{j!(j+|s|)!}
=e^{-t}I_{|s|}(t),
\qquad s\in\mathbb Z,
\tag{4}
```

where the last equality defines the relevant modified Bessel function. Equivalently, the characteristic and moment-generating functions are

```math
\mathbb E e^{i\theta S_t}=e^{t(\cos\theta-1)},
\qquad
\mathbb E e^{\lambda S_t}=e^{t(\cosh\lambda-1)}.
\tag{5}
```

**Exact pair identity.** For every $`t\ge 0`$ and every pair of Hermitian involutions,

```math
e^{t\mathcal L_2}
=\sum_{s\in\mathbb Z}p_s(t)\operatorname{Ad}_{W_s}.
\tag{6}
```

**Proof.** Expand the semigroup by (1). For each chronological word, (2) identifies a coordinate $`s`$ with the same operator product $`W_s`$. Summing probabilities of all words with that coordinate gives (3)–(4). Since every substitution is an exact operator identity, the resulting equality holds on the system tensored with any reference. The weights sum to one, and the series converges in diamond norm. ∎

An ideal exact draw from (4) requires $`|S_t|`$ reflection queries. Its first two moments satisfy

```math
\mathbb E S_t=0,\qquad
\mathbb E S_t^2=t,\qquad
\mathbb E|S_t|\le\sqrt t.
\tag{7}
```

The final inequality is Cauchy–Schwarz. It is an expected-cost statement. A worst-case query theorem additionally needs a cap, and a finite implementation additionally needs an efficient endpoint sampler. Those are separate steps below and in the [resource account](sampling-and-resources.md).

## 4. A hard query cap for arbitrary accuracy

Throughout this project, an error $`\epsilon`$ means **full diamond norm**, without the factor of one half sometimes used in channel-distance conventions.

For $`x>0`$ and $`t>0`$, the endpoint obeys the two-sided Bernstein bound

```math
\Pr\{|S_t|\ge x\}
\le 2\exp\!\left[-\frac{x^2}{2(t+x/3)}\right].
\tag{8}
```

Here is a direct proof that also fixes the constants. For $`0\le\lambda<3`$,

```math
\cosh\lambda-1
\le e^\lambda-1-\lambda
\le\frac{\lambda^2}{2(1-\lambda/3)}.
```

The last inequality follows term by term from $`n!\ge2\cdot3^{n-2}`$ for $`n\ge2`$. Apply the exponential Markov inequality to (5) and set $`\lambda=x/(t+x/3)`$. This gives the upper-tail exponent in (8). Symmetry gives the lower tail and the factor two.

In particular, for every $`u>0`$,

```math
x\ge\sqrt{2tu}+u
\quad\Longrightarrow\quad
\Pr\{|S_t|\ge x\}\le2e^{-u}.
\tag{9}
```

Indeed, substituting $`x=\sqrt{2tu}+u`$ into $`x^2-2u(t+x/3)`$ gives a nonnegative expression, and the exponent in (8) increases with $`x`$.

For a simple capped construction, choose

```math
u=\ln(4/\epsilon),\qquad
M=\left\lceil\sqrt{2tu}+u\right\rceil,
\qquad 0<\epsilon\le1.
```

Draw the exact endpoint. Apply $`W_{S_t}`$ if $`|S_t|<M`$; otherwise apply the identity. If $`\mathcal F_{t,M}`$ denotes this channel, then

```math
\begin{aligned}
\bigl\|\mathcal F_{t,M}-e^{t\mathcal L_2}\bigr\|_\diamond
&\le\sum_{|s|\ge M}p_s(t)
\bigl\|\operatorname{id}-\operatorname{Ad}_{W_s}\bigr\|_\diamond\\
&\le2\Pr\{|S_t|\ge M\}\\
&\le\epsilon.
\end{aligned}
\tag{10}
```

This uses at most $`M-1`$ queries on every run. There is no postselection, failure flag, or conditioning on an unobserved event: the tail is assigned an ordinary output channel. All branches implement a unitary channel, so their classical mixture is a physical trace-preserving map.

At fixed nonzero accuracy, (10) gives an $`O(\sqrt t)`$ query cap for $`t\ge1`$. Its general-accuracy form is

```math
O\!\left(\sqrt{t\log(1/\epsilon)}+\log(1/\epsilon)\right),
```

with $`\log(1/\epsilon)`$ understood as $`\log(4/\epsilon)`$ when a formula uniform up to $`\epsilon=1`$ is needed. The special case $`t=0`$ is the identity and uses no query.

## 5. Turning the endpoint description into an algorithm

Drawing a Poisson trajectory and reducing it after the fact would still spend expected classical time proportional to $`t`$. To preserve the improvement in the complete resource account, the implementation samples the endpoint through a finite cyclic distribution.

For an even power of two $`K`$, sample the residue of $`S_t`$ modulo $`K`$ and choose its representative in $`[-K/2,K/2-1]`$. Its exact probabilities are

```math
q_r=
\frac1K\sum_{j=0}^{K-1}
e^{t(\cos(2\pi j/K)-1)}e^{-2\pi i jr/K},
\qquad r=0,\ldots,K-1.
\tag{11}
```

The discrete Fourier orthogonality identity gives

```math
q_r=\sum_{\ell\in\mathbb Z}p_{r+\ell K}(t).
```

Consequently the probabilities in (11) are nonnegative despite their Fourier representation. Coupling the cyclic sample to the same $`S_t`$ changes the selected word only outside the representative interval. Choosing $`K`$ using (9) bounds this aliasing error and caps the number of queries by $`K/2`$.

The [finite-bit construction](sampling-and-resources.md) computes (11) by an integer FFT, certifies the elementary-function approximation, and rounds the resulting distribution to a fixed-bit probability table. It has

```math
K=O\!\left(\sqrt{t\log(1/\epsilon)}+\log(1/\epsilon)\right)
```

and classical preprocessing $`O(K\log K\,\operatorname{poly}(b))`$, where $`b`$ counts input length and required arithmetic precision. There is no loop over the Poisson jump count and no coherent probability-loading operation.

## 6. Interpretation and limits

The reduction is available to every supplied pair of involutions, including noncommuting pairs. It does not require simultaneous diagonalization, spectral estimates, a controlled unknown unitary, inverse access beyond the supplied involutions, or a prepared data state. It acts correctly on whatever system state is presented to the channel simulator.

The result concerns the cost of applying a randomly selected operator word. It does not claim that a classical description of the complete output density matrix is inexpensive. Nor does the word length alone prove a query lower bound: a more general quantum algorithm could in principle exploit the oracles coherently. The [two-reflection lower bound](lower-bounds.md) separately excludes a better worst-case time exponent by comparing nearby qubit reflections.

With three supplied reflections, reduced words can branch on a tree rather than moving on a line. The linear lower bound in [lower bounds](lower-bounds.md) makes this geometric difference operational by encoding a query-hard parity problem. The count is the number of supplied binary dephasing primitives in the specified oracle representation; it is not an intrinsic rank classification of all Lindblad representations.

## Verification route

Run from the repository root:

```bash
python verification/check_pair_sampler.py
```

The check enumerates all two-letter words of length at most eight, confirms the endpoint multiplicities and chronological operator convention, compares finite-bit probability tables with independently evaluated Bessel probabilities, and compares the implemented mixed channel with a direct matrix exponential on several noncommuting examples. Its floating matrix comparisons are finite diagnostics. Equations (1)–(11) establish the dimension-independent statement.
