# From Childs's Quantum Algorithms to the dephasing threshold

Suppose a device applies a reflection whenever a random clock rings. One reflection type is easy to simulate for a long time: only the parity of the number of rings matters. With two reflection types, cancellations leave a word whose typical length grows as the square root of time. Three types can carry a computation that requires linearly many oracle calls. The purpose of this bridge is to explain how those physical statements become a quantum query-complexity theorem.

The educational anchor is **Andrew M. Childs, [Lecture Notes on Quantum Algorithms](https://www.cs.umd.edu/~amchilds/qa/qa.pdf), edition dated 17 April 2025**. The notes supply the circuit, oracle, error-accumulation, and lower-bound foundations. This page develops the additional channel and probability arguments needed for this project. The [milestone map](MILESTONES.md) organizes the learning route; the [scientific account](../science/README.md) remains the authoritative home of the complete theorem statements and proofs.

## 1. Selected source and reading route

The page references in this table are **printed page numbers** in the selected edition. PDF page numbers include eight pages of front matter: printed page 1 is PDF page 9. The author-hosted edition has 191 PDF pages.

| Childs section | Printed pages | Connection to this project |
|---|---|---|
| §§1.1–1.2 and §1.4 | 1–3 | Registers, circuits, and reversible computation support coherent oracle access and clean workspace. |
| §2.1 | 7–8 | The operator-norm telescoping argument is extended below to channels and reference systems. |
| §17.3 | 75 | The classical walk on a line supplies useful context for the two-reflection endpoint law. Its clock normalization must be translated. |
| §§21.1–21.3 and §21.5 | 97–100 | The bit-query model and polynomial method supply the parity obstruction. Section 21.4 is optional context; the parity-correlation proof below does not need symmetrization. |
| §§27.1–27.4 | 133–136 | Simulation is formulated as an oracle task with an explicit input representation. |
| §28.1 | 139 | The parity-transport reduction suggests the structure of the three-reflection converse; this project's dissipative construction supplies different dynamics and access. |
| §18.2, optional | begins on 82 | Coherent constructions from Markov chains help identify why the requested output object must be specified. |

Reading the listed sections does not by itself establish the threshold. The additional steps are the definition of full-channel accuracy, an exact Poisson channel expansion, cancellation of reflection words, a bounded finite-bit sampler, and reductions that preserve the reflection-oracle interface. The following sections supply those connections in the order they are used.

## 2. Translating the oracle model

A reflection is a Hermitian unitary:

```math
R=R^\dagger,\qquad R^2=I.
```

Its two eigenspaces have eigenvalues plus and minus one; either eigenspace may have any dimension. There is no promise that a reflection is a one-qubit gate or acts locally on a few qubits.

The simulator receives a tuple $`R_1,\ldots,R_k`$ through the coherent selection oracle

```math
S_R=\sum_{j=1}^{k}|j\rangle\langle j|\otimes R_j.
```

A label in superposition selects the corresponding reflection coherently. Unused binary labels act as the identity. One invocation of SELECT, its inverse, or a version with an additional coherent control costs one query. Here $`S_R^{-1}=S_R`$, because each supplied reflection is an involution. The upper algorithms only need classical choices of individual reflections; the lower bounds also allow the stronger coherent interface.

The translation from the anchor is explicit:

| Quantity | Meaning here |
|---|---|
| A non-query operation in Childs's query model | A known operation independent of the unknown reflection entries; it can depend on recorded outcomes from earlier queries. |
| An input string of length $`n`$ in Chapter 21 | The $`m`$ unknown bits used to construct the hard reflection family. |
| Childs's bit-flip oracle $`\widehat O_x`$ in §21.2 | This project's $`O_x\lvert i,z\rangle=\lvert i,z\oplus x_i\rangle`$. The notation $`O_x`$ here always denotes this bit-flip interface. |
| Childs's phase-oracle notation $`O_x`$ | A different notation from ours; no free controlled phase oracle is imported into the reduction. |
| Query count | A bound on total serial oracle invocations on every branch, including branches selected by measurements or randomness. |
| Simulation time $`t`$ | The requested physical evolution time multiplied by the total jump rate; it is separate from the simulator's query count. |

Known gates, classical calculations, and workspace are free only in the query measure. They remain real resources, accounted for in [Sampling and resources](../science/sampling-and-resources.md). A simulator also receives an existing quantum input; it is not given a classical description of that state or of the unknown reflection matrices.

The theorem is uniform over allowed reflection tuples. At fixed dimension, the algorithm must work for every such tuple using only the supplied access. The worst case is then taken over finite dimensions. Consequently a lower bound may choose a dimension depending on $`t`$, while an upper bound must work in every dimension. This order of quantifiers will matter for the tree construction.

## 3. From state vectors to full quantum channels

State-vector circuit language must be extended to describe random jumps and discarded classical information. A density matrix $`\rho`$ is positive semidefinite and has trace one. A pure state has $`\rho=|\psi\rangle\langle\psi|`$; a probabilistic preparation gives

```math
\rho=\sum_a p_a|\psi_a\rangle\langle\psi_a|.
```

An operation on density matrices is a **quantum channel** when it is completely positive and trace preserving, abbreviated CPTP. A finite-dimensional channel has a Kraus representation

```math
\Phi(\rho)=\sum_a K_a\rho K_a^\dagger,
\qquad
\sum_a K_a^\dagger K_a=I.
```

The second identity preserves total probability. Complete positivity ensures that the operation remains physical when the input is entangled with another system. In particular, choosing a unitary $`U_a`$ with classical probability $`p_a`$ implements the channel with Kraus operators $`K_a=\sqrt{p_a}U_a`$. Forgetting which choice was made is part of this channel, not a conditioning step.

### Reference systems and operational error

Let $`F`$ be an external reference register, possibly entangled with the simulated system $`S`$. A full-channel simulator must reproduce the action on every joint input while acting as the identity on $`F`$. The reference can represent information stored elsewhere in a larger quantum computation.

For two channels, their diamond distance can be written as

```math
\|\Phi-\Psi\|_\diamond
=\max_{\sigma_{SF}}
\left\|\bigl((\Phi-\Psi)\otimes\mathrm{Id}_F\bigr)(\sigma_{SF})\right\|_1.
```

The maximum is over density matrices, and a reference of the same dimension as the input suffices. The trace norm is $`\|X\|_1=\mathrm{Tr}\sqrt{X^\dagger X}`$. This project uses the **unhalved** diamond norm: error at most $`\epsilon`$ changes the probability of any measured event by at most $`\epsilon/2`$.

This condition is stronger than checking a few basis inputs. A proposed simulator must preserve the relevant coherences and correlations as well as populations. The upper algorithms below satisfy that requirement because they establish exact operator identities before introducing a controlled error in the classical mixture.

### The channel version of telescoping

Childs §2.1 bounds the operator-norm error of a product of approximate unitaries. For channels, replacing one component at a time gives

```math
\|\Phi_q\circ\cdots\circ\Phi_1
-\Psi_q\circ\cdots\circ\Psi_1\|_\diamond
\le\sum_{j=1}^{q}\|\Phi_j-\Psi_j\|_\diamond.
```

The surrounding channels have diamond norm one, so they do not amplify an individual replacement error. For unitary conjugation, write $`\mathrm{Ad}_U(\rho)=U\rho U^\dagger`$. Inserting and subtracting $`V\rho U^\dagger`$ yields

```math
\|\mathrm{Ad}_U-\mathrm{Ad}_V\|_\diamond
\le2\|U-V\|_{\mathrm{op}}.
```

Thus $`q`$ unitary calls with individual operator-norm error at most $`\delta`$ contribute at most $`2q\delta`$ channel error. The same argument compares algorithms using two different unknown oracles. Measurement outcomes and random choices can be retained in registers; later adaptive operations become known controlled operations. The hybrid comparison therefore covers the adaptive model in [Lower bounds](../science/lower-bounds.md), not only a circuit with a fixed classical query schedule.

## 4. Reflection noise and the Poisson clock

A Lindblad generator describes continuous-time evolution of a density matrix. In general its jump terms have the form

```math
L_j\rho L_j^\dagger
-\frac12\bigl(L_j^\dagger L_j\rho+\rho L_j^\dagger L_j\bigr).
```

Set $`L_j=R_j/\sqrt{k}`$ and take the Hamiltonian term to be zero. Since $`R_j^\dagger R_j=I`$, the generator becomes

```math
\mathcal L_k(\rho)
=\frac1k\sum_{j=1}^{k}(R_j\rho R_j-\rho),
\qquad
\Phi_t=e^{t\mathcal L_k}.
```

The coefficient $`1/k`$ holds the total jump rate at one. Adding a third primitive does not increase the overall rate. If the physical rate is $`\gamma`$, the dimensionless time in the theorem is $`t=\gamma t_{\mathrm{phys}}`$.

Define the single-jump channel $`\mathcal P=k^{-1}\sum_j\mathrm{Ad}_{R_j}`$. The identity superoperator commutes with $`\mathcal P`$, so the exponential series gives

```math
\Phi_t=e^{-t}\sum_{n=0}^{\infty}\frac{t^n}{n!}\mathcal P^n.
```

This is an exact channel identity. Draw $`N\sim\mathrm{Poisson}(t)`$, then draw $`N`$ independent uniform labels and apply their reflections in order. Every branch is a unitary channel, so the averaged map is CPTP on arbitrary inputs and references. This argument directly establishes physicality for the restricted family used here; the broader theory of Lindblad generators is not required for the algorithm.

The target is autonomous because its generator is fixed in time. It is unital because $`\mathcal L_k(I)=0`$. It is self-adjoint for the Hilbert–Schmidt inner product $`\langle X,Y\rangle=\mathrm{Tr}(X^\dagger Y)`$, because conjugation by a Hermitian unitary is self-adjoint. An equivalent expression is

```math
\mathcal L_k(\rho)
=-\frac1{2k}\sum_j[R_j,[R_j,\rho]].
```

These properties restrict the physical family, but they do not determine its query complexity. The relevant additional structure is how products of the supplied reflections simplify.

## 5. One reflection: only jump parity matters

For one primitive, a history of $`N`$ jumps applies $`R^N`$. The identities $`R^{2a}=I`$ and $`R^{2a+1}=R`$ remove every detail except whether $`N`$ is odd. The Poisson generating function gives $`\mathbb E(-1)^N=e^{-2t}`$, hence

```math
\Phi_t=(1-p_t)\mathrm{Id}+p_t\mathrm{Ad}_R,
\qquad
p_t=\frac{1-e^{-2t}}2.
```

Sample this one classical bit and apply $`R`$ only on the odd branch. The cap is one query for any time. Approximating the scalar probability to accuracy $`\epsilon/2`$ costs no additional reflection query and changes the channel by at most $`\epsilon`$.

The dephasing interpretation follows by writing $`R=P_+-P_-`$. Blocks within the two eigenspaces stay fixed; cross blocks $`P_+\rho P_-`$ and $`P_-\rho P_+`$ acquire the factor $`e^{-2t}`$. A long physical jump history can therefore have an extremely short implementation of its averaged action.

A qubit already shows that zero queries cannot always suffice: the $`X`$- and $`Z`$-reflection channels act differently on $`|+\rangle`$. The exact worst-case value for $`t\ge1`$ and the stated small fixed error is consequently $`Q_1=1`$. See [Lower bounds, one-reflection argument](../science/lower-bounds.md#3-a-constant-lower-bound-including-one-reflection).

## 6. Two reflections: cancellation produces diffusion

Write the two reflections as $`A`$ and $`B`$. Every adjacent $`AA`$ or $`BB`$ cancels. A surviving nonempty word must alternate. No commutation assumption is used.

### A complete cancellation example

Consider the **chronological** sequence

```math
A,\ B,\ B,\ A,\ B,\ A.
```

Cancel the second and third gates, then the now adjacent first and fourth gates. The remaining chronological sequence is $`B,A`$, requiring two oracle calls. Since the last applied gate acts on the left, the original operator and its reduced form satisfy

```math
A B A B B A=A B.
```

Thus the channel for this branch is $`\rho\mapsto AB\rho BA`$. The order is observable. With $`A=Z`$, $`B=(Z+X)/\sqrt2`$, and input $`|0\rangle`$, the output is $`AB|0\rangle=|{-}\rangle`$; measuring $`X`$ returns minus one with certainty. Reversing the surviving gate order would produce $`|{+}\rangle`$. This small example fixes the convention used in the entire algorithm.

### Signed endpoints

Index the empty word by zero. A positive coordinate $`s`$ means $`s`$ chronological gates alternating from $`A`$; a negative coordinate means $`|s|`$ gates alternating from $`B`$. Denote the resulting operator by $`W_s`$. In particular, $`W_2=BA`$ and $`W_{-2}=AB`$.

Appending one chronological gate changes the coordinate by

```math
\begin{aligned}
T_A(s)&=s+(-1)^s,\\
T_B(s)&=s-(-1)^s.
\end{aligned}
```

The six-letter example follows coordinates $`0,1,2,1,0,-1,-2`$. At every coordinate, a fair choice of gate is a fair choice between the two neighboring integers. The reduced-word coordinate is therefore a symmetric classical walk on a line.

After a rate-one Poisson number of steps,

```math
S_t=N_+-N_-,
\qquad
N_+,N_-\ \text{independent with distribution }\mathrm{Poisson}(t/2).
```

Its probabilities are $`p_s(t)=e^{-t}I_{|s|}(t)`$, where $`I_{|s|}`$ is a modified Bessel function. The central channel identity is

```math
e^{t\mathcal L_2}
=\sum_{s\in\mathbb Z}p_s(t)\mathrm{Ad}_{W_s}.
```

It follows by replacing each Poisson word with its exactly equal reduced operator and collecting the weights. Specific matrices may have additional relations that identify several endpoints; the identity remains valid for them. The abstract line is a classical description of words, not an extra quantum register.

Childs §17.3 uses a classical path walk with rate one along each of its two directions, hence total rate two. Its probability formula has the form $`e^{-2\tau}I_{|s|}(2\tau)`$. This project's clock corresponds to **$`\tau=t/2`$**. With that normalization,

```math
\mathbb E S_t=0,
\qquad
\mathbb E S_t^2=t,
\qquad
\mathbb E|S_t|\le\sqrt t.
```

The classical diffusion determines how many quantum oracle calls the sampled word needs. The chosen word still acts coherently on the existing input and its correlations with a reference. The exact proof and chronological conventions are in [Pair simulation](../science/pair-simulation.md).

## 7. From diffusion to a bounded finite-bit simulator

An expected word length at most $`\sqrt t`$ does not yet meet a query model that caps every branch. The endpoint moment-generating function is

```math
\mathbb E e^{\lambda S_t}=e^{t(\cosh\lambda-1)}.
```

Exponential Markov bounds give

```math
\Pr(|S_t|\ge M)
\le2\exp\!\left[-\frac{M^2}{2(t+M/3)}\right].
```

Choosing $`M`$ of order $`\sqrt{t\log(4/\epsilon)}+\log(4/\epsilon)`$ makes the tail small enough. Replace every excessive-length branch by the identity. Since two channels differ by at most two in diamond norm, replacing a mixture of total probability $`\tau`$ changes the channel by at most $`2\tau`$. The replacement produces an ordinary output on every branch and preserves trace, including on reference-entangled inputs.

### Sampling the endpoint directly

Generating all $`N`$ jumps before reducing them would still require expected classical work proportional to $`t`$. The implementation instead uses the endpoint modulo an even power of two $`K`$ and selects its representative in $`[-K/2,K/2-1]`$. The residue probabilities are

```math
q_a=\frac1K\sum_{j=0}^{K-1}
e^{t(\cos(2\pi j/K)-1)}e^{-2\pi i ja/K}.
```

Finite Fourier orthogonality identifies this as the wrapped Skellam distribution. It is nonnegative and normalized. Aliasing affects the selected word only when the integer endpoint lies outside the representative interval, so the same tail reasoning controls its channel error.

The Fourier transform here is a **classical FFT**. The implementation encloses its elementary-function inputs with integer interval arithmetic, uses an integer FFT, clips and normalizes the result, and rounds it to a dyadic probability table. A fixed number of random bits and a classical cumulative-table search then produce the sample. There is no coherent probability-loading operation or QRAM assumption.

For the exact rational inputs $`t=1000`$ and $`\epsilon=0.01`$, the documented implementation uses a table of $`512`$ residues, a cap of $`256`$ reflection queries, and $`21`$ random bits per sample. The arithmetic certificate is below the requested error. These are concrete parameters of the supplied algorithm, rather than a claim that its constants are optimal.

The complete [sampling proof and resource account](../science/sampling-and-resources.md) establishes classical preprocessing $`O(K\log K\,\mathrm{poly}(b))`$, with input length and precision included in $`b`$. It also gives the total implementation-error budget

```math
\frac{9\epsilon}{16}
+2|t-\widetilde t|
+2Q\delta,
```

where $`\widetilde t`$ is the supplied rational time, $`Q`$ is the query cap, and $`\delta`$ is an optional operator-norm synthesis error per oracle call. The ideal theorem uses exact reflection oracles; building those oracles has its own physical cost.

## 8. Why the square-root cost is necessary

The walk interpretation proves an algorithm. A query lower bound must also exclude coherent strategies that never generate a reduced word. A single qubit is enough for that converse.

Compare the pairs $`(Z,Z)`$ and $`(Z,B_\theta)`$, where

```math
B_\theta=\cos\theta\,Z+\sin\theta\,X,
\qquad
\theta=t^{-1/2}.
```

Their SELECT oracles differ by operator norm at most $`\theta`$, including when an external coherent control is added. A $`q`$-query algorithm therefore produces output states differing by trace norm at most $`2q\theta`$ on a fixed input, by the hybrid argument of Section 3.

The ideal channels have a larger, time-amplified distinction. Starting from $`|0\rangle`$, the final $`Z`$ expectation for the tilted pair is

```math
z_\theta(t)
=\cos^2(\theta/2)e^{-t(1-\cos\theta)}
+\sin^2(\theta/2)e^{-t(1+\cos\theta)}.
```

The untilted pair leaves that expectation equal to one. The slow decay rate is $`1-\cos\theta`$, which scales as $`\theta^2/2`$. A time of order $`\theta^{-2}`$ therefore gives a constant change even though each oracle call differs by only order $`\theta`$.

For the stated choice of angle and every $`t\ge1`$, the exact expression gives a trace-norm separation at least

```math
\delta_*=1-e^{-(1-\cos1)}\gt0.3685.
```

If the same simulator approximates both channels with error at most $`\epsilon`$, its two approximation errors and its oracle distinguishability must account for this signal:

```math
\delta_*\le2\epsilon+2q\theta,
\qquad
q\ge\frac{\delta_*-2\epsilon}{2}\sqrt t.
```

Thus the pair upper bound has the optimal fixed-error time exponent. The comparison uses genuinely different conjugation channels, so the signal is not an unknown global phase. [Lower bounds](../science/lower-bounds.md#4-two-reflections-a-qubit-witness-for-square-root-time) gives the Bloch-vector derivation and the uniform inequality. The hybrid method is a standard tool; its role here is to turn a small angular change in a reflection into a lower bound for the noisy evolution.

## 9. Three reflections: a tree can compute parity

The algebra of three involutions allows a new reduced letter at each step in two directions and cancellation in one. Away from the root, the corresponding tree walk therefore moves outward with probability $`2/3`$ and inward with probability $`1/3`$. Reversibility of each move coexists with positive radial drift.

A drifting word by itself is still not a lower bound against general quantum algorithms. To make the drift operational, encode an unknown bit string $`x_1,\ldots,x_m`$ into three reflection oracles. For $`t\ge48`$, use

```math
m=\lfloor t/48\rfloor,
\qquad
R=\lceil4t\rceil.
```

Vertices are reduced words of length at most $`R`$ over colors $`1,2,3`$, with adjacent colors unequal. The empty word is the root. The color-$`j`$ permutation $`T_j`$ deletes the last letter if it is $`j`$, appends $`j`$ otherwise when space remains, and becomes a self-loop at the outer boundary when the append is unavailable. Each $`T_j`$ is an involution on this finite set.

Label every edge between depths $`\ell-1`$ and $`\ell`$ by $`x_\ell`$ for $`\ell\le m`$. Deeper edges and self-loops carry zero. If $`\eta_j^{(x)}(v)`$ denotes this bit, define a reflection on the vertex and an answer qubit by

```math
R_j^{(x)}|v,a\rangle
=|T_j(v),a\oplus\eta_j^{(x)}(v)\rangle.
```

The bit is the same from either endpoint of an edge. Applying the operation twice restores both registers, so this permutation unitary is Hermitian and squares to the identity. Its three types fit the promised oracle family exactly.

Starting from the root with answer zero, every trajectory obeys the invariant

```math
a=x_1\oplus\cdots\oplus x_{\min\{|v|,m\}}.
```

For example, going from depth one to two adds $`x_2`$, and returning to depth one adds it again and cancels it. Consequently any endpoint of depth at least $`m`$ contains the full parity. The vertex walk depends on the chosen colors, while the unknown string only determines the answer register.

### A finite success probability

Before the boundary is reached, the radial distance dominates a difference of independent Poisson variables with means $`2t/3`$ and $`t/3`$. That comparison variable has mean $`t/3`$ and variance $`t`$. The parity depth $`m\le t/48`$ lies well below the mean. Chebyshev's inequality bounds shallow endpoints, and a Poisson tail bounds any encounter with the radius-$`R`$ boundary. The explicit result is

```math
\Pr(|v|\ge m)
\ge1-\frac{256}{25t}-e^{-c_Pt},
\qquad
c_P=4\log4-3\gt0.
```

Measure the depth and answer. Return the answer when the depth is at least $`m`$, and return a fresh fair bit otherwise. A channel simulation with diamond error at most $`\epsilon`$ then gives parity success at least

```math
1-\frac{128}{25t}-\frac12e^{-c_Pt}-\frac\epsilon2
\gt\frac78
```

for $`t\ge48`$ and $`\epsilon\le1/100`$. The proof in [Lower bounds](../science/lower-bounds.md#5-three-reflections-a-finite-tree-parity-reduction) keeps the root, finite boundary, and all constants explicit. The tree is finite throughout the actual reduction.

Childs §28.1 provides the general simulation-to-parity strategy for sparse Hamiltonians. Here the transport is supplied by an autonomous random-unitary channel with three Hermitian jumps. Establishing that channel, its finite success probability, and its exact oracle compiler is the additional work required for this theorem.

## 10. Compiling the coherent oracle

The parity reduction must turn every query allowed to the channel simulator into a bounded number of ordinary bit queries. Otherwise the reflection oracle might hide an expensive read of the input string.

Use the standard bit-flip oracle

```math
O_x|i,z\rangle=|i,z\oplus x_i\rangle,
\qquad 1\le i\le m.
```

For a color $`j`$, vertex $`v`$, and external control $`c`$, compute the symmetric edge depth $`\ell=\max\{|v|,|T_j(v)|\}`$. Form an active flag $`f`$ that is one exactly when the control is active, the edge is not a self-loop, and $`1\le\ell\le m`$. Use address $`i=\ell`$ on an active branch and the valid address $`i=1`$ otherwise. The assumption $`m\ge1`$ makes the latter well defined.

The following operations implement one full controlled SELECT call:

| Step | Operation | Ordinary bit queries |
|---|---|---:|
| 1 | Reversibly compute $`f`$ and $`i`$ using the known graph rules. Initialize a buffer qubit to zero. | 0 |
| 2 | Apply $`O_x`$ to the address and buffer. | 1 |
| 3 | Flip the target answer only when both $`f`$ and the buffer are one. | 0 |
| 4 | Apply $`O_x`$ again at the same address, returning the buffer to zero. | 1 |
| 5 | Apply the known vertex permutation $`T_j`$ when $`c=1`$. | 0 |
| 6 | Uncompute the address and active flag. | 0 |

Step 6 remains valid after the vertex moves because the edge depth and active condition are symmetric between its endpoints. On an inactive branch, the two calls at address one cancel and the answer is unchanged. Both calls are ordinary, uncontrolled invocations of $`O_x`$; the controlled operation occurs between them. No fixed-zero sentinel address is assumed.

The argument holds in superposition over vertices, colors, and external controls. Every work register is restored, so there is no information left in an auxiliary register that would disturb coherence. Invalid binary encodings and unused selection labels are fixed and inactive. Inverse SELECT has the same implementation because the reflections are involutions.

This is where the reversible-computation ideas of Childs §1.4 enter the proof. The graph has a succinct word encoding, so its known moves and edge-depth calculations use reversible computation on $`O(R)`$ bits with polynomial resources. The input-dependent part remains exactly **two bit queries per controlled reflection SELECT**, with no data-dependent table or QRAM access.

## 11. Closing the parity reduction

The polynomial method explains why even a coherent strategy cannot evade the reduction. After $`T`$ bit queries, an output probability is a multilinear polynomial in the input bits of degree at most $`2T`$. A query increases amplitude degree by at most one; forming a probability doubles the bound. The statement survives known gates, auxiliary registers, deferred measurements, and averaging over classical randomness. This is the standard degree bound developed in Childs §§21.2–21.3 and in the primary lower-bound literature cited in [Lower bounds](../science/lower-bounds.md).

A short parity argument avoids symmetrization. Let $`p(x)`$ be the probability of returning zero, and let $`\chi(x)=(-1)^{x_1+\cdots+x_m}`$. Uniform success greater than one half implies

```math
\chi(x)\bigl(2p(x)-1\bigr)\gt0
\quad\text{for every }x.
```

Its average over all Boolean strings is therefore positive. But every multilinear polynomial of degree below $`m`$ has zero correlation with $`\chi`$: each monomial omits at least one bit, and averaging over that omitted bit cancels the character. Thus the degree must be at least $`m`$, giving $`T\ge m/2`$.

Now suppose a channel simulator uses at most $`q`$ reflection queries on every branch. The compiler converts it into a parity algorithm with at most $`2q`$ bit queries and success greater than $`7/8`$. Therefore

```math
2q\ge m/2,
\qquad
q\ge m/4\ge t/384
\quad(t\ge48).
```

The constant one-query obstruction covers $`1\le t\lt48`$. This is a lower bound on every algorithm in the stated interface, including algorithms that never sample a trajectory. Conversely, the ordinary Poisson expansion, truncated at a count of order $`t`$ at fixed accuracy, supplies a universal linear-query upper bound. Together these establish $`Q_3(t,1/100)=\Theta(t)`$.

## 12. What the theorem says about physical simulation

The complete fixed-error statement, for every real $`t\ge1`$, is

```math
Q_1(t,1/100)=1,
\qquad
Q_2(t,1/100)=\Theta(\sqrt t),
\qquad
Q_3(t,1/100)=\Theta(t).
```

The two-reflection upper bound holds in every finite dimension and already needs square-root cost for an appropriate qubit pair. The three-reflection hard family has

```math
|V_R|=3\cdot2^R-2,
\qquad
\dim\mathcal H=2|V_R|=6\cdot2^R-4.
```

With $`R=\lceil4t\rceil`$, that is dimension $`\exp(\Theta(t))`$, represented using $`\Theta(t)`$ target qubits. The large state space supports a long outward transient. The theorem does not supply a linear long-time lower bound for a fixed finite-dimensional target.

The primitive count refers to the supplied oracle representation. It is not a minimal Lindblad rank, and a different representation can require different access. The normalization fixes the total rate. A hard triple is a worst-case possibility; particular triples can simplify further. The target itself has no imposed measurements, resets, or time-dependent control, even though the simulation algorithm is allowed those standard computational resources.

Finally, the output is a physical CPTP channel. A coherent walk state, or a normalized amplitude encoding of a classical probability vector, comes with a different output and normalization contract. Optional reading in Childs §18.2 provides useful context for that distinction, while [Related work](../references/related-work.md) compares the research-level guarantees. The query theorem also leaves the cost of physically realizing each reflection explicit; it claims neither a spatially local implementation nor an automatic hardware runtime advantage.

The [model](../science/model-and-results.md), [pair proof](../science/pair-simulation.md), [finite-bit resource proof](../science/sampling-and-resources.md), and [converse proofs](../science/lower-bounds.md) provide the complete technical route. The [verification guide](../verification/README.md) identifies which finite calculations exercise those arguments and which conclusions require the analytic proofs. Together, these connections explain how familiar query-complexity tools apply to autonomous dephasing dynamics while retaining the physical channel, access, and dimension assumptions that make the result precise.
