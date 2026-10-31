# Lower bounds for simulation from reflection oracles

This page proves the converse bounds for the model in [Model and results](model-and-results.md). The bounds apply to arbitrary quantum simulation algorithms, including algorithms that use coherent selection, clean auxiliary registers, classical randomness, intermediate measurements, and adaptive control. The three-reflection result is a reduction from quantum query complexity; it does not assume that the simulator follows or explicitly generates a random trajectory.

Throughout, the simulation error is the **unhalved** diamond norm, the query count is a maximum on every branch, and the system dimension is allowed to depend on time. Fix a real time $`t\ge 1`$ and an error $`0<\epsilon\le 1/100`$.

## 1. Statements and oracle conventions

For unknown Hermitian involutions $`R_1,\ldots,R_k`$, define

```math
\mathcal L_k
=\frac1k\sum_{j=1}^{k}
  \bigl(\operatorname{Ad}_{R_j}-\operatorname{Id}\bigr),
\qquad
\operatorname{Ad}_{R_j}(\rho)=R_j\rho R_j,
\qquad
\Phi_t=e^{t\mathcal L_k}.
```

The supplied oracle is

```math
S_R=\sum_{j=1}^{k}|j\rangle\langle j|\otimes R_j.
```

An invocation of this oracle, its inverse, or its version with an additional coherent control costs one query. Since the reflections are involutions, $`S_R^{-1}=S_R`$. An individual reflection invocation is a special case of selection. The simulator receives no classical description of the unknown matrix entries. All other operations must be independent of those unknown entries, except through previous oracle use.

Let $`Q_k(t,\epsilon)`$ be the worst-case query complexity, taking the supremum over finite target dimensions and all supplied tuples of $`k`$ reflections. Tuples may contain repeated reflections. The required simulator is a completely positive trace-preserving map satisfying

```math
\|\widetilde\Phi_t-\Phi_t\|_\diamond\le\epsilon.
```

The following explicit bounds hold:

```math
\begin{aligned}
Q_1(t,\epsilon)&\ge 1,\\[2mm]
Q_2(t,\epsilon)&\ge
\frac{1-e^{-(1-\cos 1)}-2\epsilon}{2}\sqrt t,\\[2mm]
Q_3(t,\epsilon)&\ge\frac{t}{384}.
\end{aligned}
```

At $`\epsilon=1/100`$, the coefficient in the two-reflection bound is greater than $`0.1742`$. Together with the algorithms in [Pair simulation](pair-simulation.md) and [Sampling and resources](sampling-and-resources.md), these give the fixed-error worst-case orders

```math
Q_1=\Theta(1),\qquad
Q_2=\Theta(\sqrt t),\qquad
Q_3=\Theta(t).
```

The two-reflection lower bound uses a single-qubit target. The three-reflection construction uses target dimension $`\exp(\Theta(t))`$, or $`\Theta(t)`$ target qubits. Its dimension dependence is part of the statement.

## 2. A hybrid inequality for arbitrary adaptive simulators

For unitary oracles $`U,V`$, including any controls and selection registers in their definitions, their conjugation channels obey

```math
\|\operatorname{Ad}_U-\operatorname{Ad}_V\|_\diamond
\le 2\|U-V\|_{\mathrm{op}}.
```

To see this, insert and subtract $`V\rho U^\dagger`$ and use the triangle inequality and the operator-norm bound on multiplication. The same calculation holds after tensoring both unitaries with an arbitrary reference identity.

Replace the oracle calls of a $`q`$-query algorithm one at a time. Trace norm and diamond norm contract under the intervening known quantum channels. Consequently, the output states on any fixed input satisfy

```math
\|\rho_U^{\mathrm{out}}-\rho_V^{\mathrm{out}}\|_1
\le 2q\|U-V\|_{\mathrm{op}}.
```

This is the standard hybrid method; see [Bennett, Bernstein, Brassard, and Vazirani](https://arxiv.org/abs/quant-ph/9701001). The argument above supplies the particular normalization used here. Intermediate measurements can be retained in outcome registers, and subsequent adaptive operations become known controlled operations. Classical randomness can likewise be retained as a register. A branch with fewer than $`q`$ calls can be padded with inactive controlled calls. Thus the inequality covers all the adaptive algorithms allowed by the model, rather than only fixed unitary circuits.

If an algorithm approximates each of two target channels to diamond error $`\epsilon`$, the ideal outputs on a chosen input can differ by at most

```math
2\epsilon+2q\|U-V\|_{\mathrm{op}}.
```

None of the lower bounds below needs an entangled input. The full diamond-norm requirement includes these particular unentangled witnesses and is therefore sufficient.

## 3. A constant lower bound, including one reflection

On a qubit, compare a tuple whose every reflection is $`X`$ with a tuple whose every reflection is $`Z`$. For any supplied tuple length $`k`$, the corresponding generators are respectively $`\operatorname{Ad}_X-\operatorname{Id}`$ and $`\operatorname{Ad}_Z-\operatorname{Id}`$.

Use the input $`|+\rangle\langle+|`$. The first evolution leaves this state fixed. The second evolves its Bloch $`x`$ coordinate to $`e^{-2t}`$. Hence the two output states have trace-norm separation

```math
1-e^{-2t}\ge 1-e^{-2}>0.86.
```

A zero-query procedure has the same output for both tuples. It cannot approximate both outputs within trace norm $`\epsilon`$, because $`2\epsilon\le 0.02`$. Thus

```math
Q_k(t,\epsilon)\ge 1
\qquad (k\ge 1,\ t\ge 1).
```

For one reflection, this bound is exact in the worst-case query model. Indeed,

```math
e^{t(\operatorname{Ad}_R-\operatorname{Id})}
=(1-p_t)\operatorname{Id}+p_t\operatorname{Ad}_R,
\qquad
p_t=\frac{1-e^{-2t}}2,
```

which uses at most one oracle invocation. Approximating the scalar probability $`p_t`$ to absolute error $`\epsilon/2`$ preserves the requested diamond accuracy without additional oracle calls. Here the randomness is part of a trace-preserving channel; no postselection is used.

## 4. Two reflections: a qubit witness for square-root time

Take

```math
A=Z,\qquad
B_\theta=\cos\theta\,Z+\sin\theta\,X,
\qquad
0\le\theta\le 1.
```

Both matrices are Hermitian involutions. Compare the supplied pair $`(A,B_\theta)`$ to $`(A,B_0)=(Z,Z)`$.

### Exact channel signal

Let $`a=(0,0,1)`$ and $`b=(\sin\theta,0,\cos\theta)`$ be their Bloch axes. Reflection conjugation acts on a Bloch vector by the matrix $`2aa^T-I`$ or $`2bb^T-I`$. Therefore the generator for the average of the two conjugations acts on the $`x`$-$`z`$ plane as

```math
aa^T+bb^T-2I.
```

The two eigenvalues are $`-(1-\cos\theta)`$ and $`-(1+\cos\theta)`$. The slow eigenvector is tilted through angle $`\theta/2`$ from the $`z`$ axis. Starting from $`|0\rangle\langle0|`$, the exact final expectation of $`Z`$ is consequently

```math
z_\theta(t)
=\cos^2(\theta/2)e^{-t(1-\cos\theta)}
 +\sin^2(\theta/2)e^{-t(1+\cos\theta)}.
```

In particular, $`z_0(t)=1`$. Choose

```math
\theta=t^{-1/2}.
```

This choice belongs to $`(0,1]`$ for every real $`t\ge1`$. The function

```math
\frac{1-\cos x}{x^2}
=\frac12\left(\frac{\sin(x/2)}{x/2}\right)^2
```

decreases on $`0<x\le1`$. For completeness, the derivative of $`\sin y/y`$ has the sign of $`y\cos y-\sin y`$, which is negative because this numerator vanishes at zero and has derivative $`-y\sin y<0`$. It follows that

```math
t(1-\cos\theta)\ge1-\cos1,
\qquad
z_\theta(t)\le e^{-(1-\cos1)}.
```

Measuring the bounded observable $`Z`$ therefore witnesses trace-norm separation at least

```math
\delta_*:=1-e^{-(1-\cos1)}>0.3685
```

between the two ideal outputs.

### Oracle distance and query bound

The selected oracles differ only in the block for $`B_\theta`$, and

```math
\|S_\theta-S_0\|_{\mathrm{op}}
=\|B_\theta-Z\|_{\mathrm{op}}
=2\sin(\theta/2)
\le\theta.
```

Adding an external control leaves this norm unchanged. Taking inverses also leaves it unchanged, since both selected oracles are involutions. The hybrid inequality now gives

```math
\delta_*\le2\epsilon+2q\theta,
```

and hence

```math
q\ge\frac{\delta_*-2\epsilon}{2}\sqrt t.
```

The comparison changes the physical conjugation channel, rather than only a choice of global phase for a reflection. It proves the claimed lower bound even when the simulator can use the stronger, externally controlled SELECT interface.

## 5. Three reflections: a finite-tree parity reduction

For now suppose $`t\ge48`$, and set

```math
m=\lfloor t/48\rfloor\ge1,
\qquad
R=\lceil4t\rceil.
```

The unknown data are arbitrary bits $`x_1,\ldots,x_m`$. We construct three reflection oracles such that simulating their autonomous semigroup for time $`t`$ computes the parity of those bits with a fixed success probability greater than $`7/8`$.

### 5.1 The finite graph and its reflections

Let $`V_R`$ consist of all words of length at most $`R`$ on the alphabet $`\{1,2,3\}`$ in which adjacent letters differ. Include the empty word as the root. The depth of a vertex $`v`$ is its word length $`|v|`$.

For a color $`j`$, define a known permutation $`T_j`$ as follows:

1. If the last letter of $`v`$ is $`j`$, delete that letter.
2. Otherwise, if $`|v|<R`$, append $`j`$.
3. Otherwise, leave $`v`$ unchanged.

Each $`T_j`$ is an involution. Its nontrivial edges join consecutive depths. At the outer boundary, its otherwise missing edges are self-loops.

For a non-loop edge $`v\leftrightarrow T_j(v)`$, let

```math
\ell_j(v)=\max\{|v|,|T_j(v)|\}.
```

Assign the bit $`x_{\ell_j(v)}`$ if $`1\le\ell_j(v)\le m`$, and assign zero to all deeper edges. Assign zero to every self-loop. Denote this edge bit by $`\eta_j^{(x)}(v)`$. It is symmetric between the endpoints:

```math
\eta_j^{(x)}(T_j(v))=\eta_j^{(x)}(v).
```

On the vertex register and an answer qubit define

```math
R_j^{(x)}|v,a\rangle
=|T_j(v),a\oplus\eta_j^{(x)}(v)\rangle.
```

This is a permutation unitary, and applying it twice restores both registers. Thus $`(R_j^{(x)})^2=I`$ and $`(R_j^{(x)})^\dagger=R_j^{(x)}`$. These are explicit oracle representatives with positive permutation entries; the construction introduces no unknown global phase.

### 5.2 The answer bit along every trajectory

Start from $`|\varnothing,0\rangle`$. Along every sequence of reflection applications, the answer at vertex $`v`$ satisfies

```math
a=x_1\oplus\cdots\oplus x_{\min\{|v|,m\}}.
```

This invariant follows by induction on moves. Traversing an edge at depth $`\ell\le m`$ adds or removes exactly the $`\ell`$th term of the prefix parity. Traversing a deeper edge changes neither side, and a self-loop changes neither register. In particular, any endpoint at depth at least $`m`$ contains the full parity.

For this basis input, the exact semigroup is a classical mixture of such trajectories. Indeed, writing

```math
\mathcal T=\frac13\sum_{j=1}^{3}\operatorname{Ad}_{R_j^{(x)}},
```

one has

```math
e^{t(\mathcal T-\operatorname{Id})}
=e^{-t}\sum_{n=0}^{\infty}\frac{t^n}{n!}\mathcal T^n.
```

Equivalently, draw $`N\sim\operatorname{Poisson}(t)`$ and then apply $`N`$ independent uniformly chosen colors. The vertex walk is independent of the bit string.

### 5.3 A uniform finite-time success estimate

First consider the infinite tree, before imposing the boundary at depth $`R`$. Away from the root its radial distance increases by one with probability $`2/3`$ and decreases by one with probability $`1/3`$. At the root it always increases by one.

Couple this process with independent increments that equal $`+1`$ with probability $`2/3`$ and $`-1`$ with probability $`1/3`$. Away from the root reuse the increment; at the root replace a negative increment by a positive one. Induction shows that the radial distance dominates the sum of the independent increments. Poisson thinning therefore gives

```math
D_N\ge Y=P_+-P_-,
\qquad
P_+\sim\operatorname{Poisson}(2t/3),
\quad
P_-\sim\operatorname{Poisson}(t/3),
```

with $`P_+`$ and $`P_-`$ independent. In particular,

```math
\mathbb EY=t/3,
\qquad
\operatorname{Var}(Y)=t.
```

Since $`m\le t/48`$, the distance between the mean and the parity threshold obeys

```math
t/3-m\ge5t/16.
```

Chebyshev's inequality yields

```math
\Pr(D_N<m)
\le\Pr(Y<m)
\le\frac{t}{(t/3-m)^2}
\le\frac{256}{25t}.
```

Couple the finite and infinite trees with the same colors. They agree unless the walk reaches the outer boundary and attempts to leave. A conservative bound on this discrepancy event is $`N\ge R`$. The exponential-moment bound with parameter $`\log4`$ gives

```math
\Pr(N\ge R)
\le\exp(3t-R\log4)
\le\exp[-t(4\log4-3)].
```

Writing $`c_P=4\log4-3>0`$, the finite-tree endpoint consequently satisfies

```math
\Pr(|v|\ge m)
\ge1-\frac{256}{25t}-e^{-c_Pt}.
```

Measure the final depth and answer. If the depth is at least $`m`$, return the answer; otherwise return a fresh fair bit. For every input string, the ideal success probability is at least

```math
1-\frac{128}{25t}-\frac12e^{-c_Pt}.
```

Replacing the ideal channel by one with unhalved diamond error $`\epsilon`$ decreases any measured event probability by at most $`\epsilon/2`$. The resulting parity algorithm therefore has success probability at least

```math
p_{\mathrm{succ}}
\ge1-\frac{128}{25t}-\frac12e^{-c_Pt}-\frac\epsilon2
>\frac78
\qquad (t\ge48,\ \epsilon\le1/100).
```

For an elementary numerical-free check of the last strict bound, use $`256/(25t)\le16/75`$ and $`e^{-c_Pt}<1/100`$. The displayed success probability is then greater than or equal to $`53/60>7/8`$. The sharper displayed expression is already greater than $`0.8883`$ at the smallest allowed time and largest allowed error.

### 5.4 Compiling a controlled SELECT into two ordinary bit queries

The ordinary input-bit oracle is

```math
O_x|i,z\rangle=|i,z\oplus x_i\rangle,
\qquad i\in\{1,\ldots,m\}.
```

We now implement one invocation of the full controlled SELECT oracle exactly, using two invocations of $`O_x`$. This includes arbitrary superpositions of the color, vertex, answer, and external control, and arbitrary entanglement with other registers.

Let $`c`$ be the external control. Using known reversible computation, form an active flag $`f`$ that is one precisely when $`c=1`$ and the selected edge is a non-loop edge with depth in $`\{1,\ldots,m\}`$. Compute an address $`i=\ell_j(v)`$ when $`f=1`$, and $`i=1`$ otherwise. The latter is always a valid address because $`m\ge1`$.

With a buffer qubit initially zero, perform these operations:

1. Invoke $`O_x`$ on the address and buffer.
2. Flip the target answer if both $`f`$ and the buffer equal one.
3. Invoke $`O_x`$ again on the same address and buffer, restoring the buffer to zero.
4. Apply the known vertex permutation $`T_j`$ if $`c=1`$.
5. Uncompute the address and active flag.

The last step is valid after the vertex move because the edge depth and active condition are symmetric between endpoints. On an inactive branch the address remains the valid address one; the two bit-oracle invocations cancel, and no answer flip occurs. Self-loops and out-of-range edge depths are inactive. If the graph or selection register is embedded in a larger binary register, invalid basis labels are defined to be fixed and inactive as well.

Thus every work register returns to its initial state, including on inactive coherent branches. The resulting unitary is exactly the controlled SELECT on the target and selection registers. No free controlled bit oracle and no fixed-zero sentinel address have been assumed. The same two-query implementation covers inverse SELECT, because the target SELECT is its own inverse.

All graph operations in this compiler are known independently of $`x`$. For example, vertices can be encoded by a length, a first color, and the binary choices of each subsequent different color, or by the rank of this description among words of depth at most $`R`$. Decoding, appending or deleting one letter, and computing the symmetric edge depth require only reversible computations on $`O(R)`$ bits. No data-dependent table or QRAM access is supplied for free.

### 5.5 Applying the quantum parity bound

The bounded-error quantum query complexity of parity on $`m`$ bits is at least $`m/2`$. The polynomial method of [Beals, Buhrman, Cleve, Mosca, and de Wolf](https://arxiv.org/abs/quant-ph/9802049) gives a short proof applicable here. With $`T`$ bit queries, the probability of output zero is a multilinear polynomial of degree at most $`2T`$ on Boolean inputs. If $`2T<m`$, its signed version has zero correlation with the full parity character. Success uniformly greater than one half on every bit string would make that correlation strictly positive, a contradiction.

This argument includes classical randomness, adaptive measurements, and auxiliary systems: keep their outcomes in registers, or average their acceptance probabilities, without increasing the degree bound. A uniform upper bound on the number of queries is essential; no statement about merely expected query cost is used here.

A $`q`$-query channel simulator, composed with the compiler and final measurement, would therefore give a parity algorithm using at most $`2q`$ bit queries. It follows that

```math
2q\ge\frac m2,
\qquad
q\ge\frac m4.
```

For $`t\ge48`$, the elementary bound $`\lfloor t/48\rfloor\ge t/96`$ gives

```math
q\ge\frac{t}{384}.
```

For $`1\le t<48`$, Section 3 gives $`q\ge1\ge t/384`$. This completes the uniform lower bound for every real $`t\ge1`$.

## 6. Dimension, controls, and the scope of the reduction

The finite tree has

```math
|V_R|=1+3(2^R-1)=3\cdot2^R-2
```

vertices. Including the answer qubit, the constructed target has dimension

```math
d_R=2|V_R|=6\cdot2^R-4.
```

Since $`R=\lceil4t\rceil`$, this dimension is $`\exp(\Theta(t))`$. Embedding in a binary register needs $`R+3`$ target qubits in the range used above. Extend each reflection by the identity on unused computational basis states. The known encoding and reversible graph operations can be performed with resources polynomial in $`R`$; the theorem does not assert a gate-optimal implementation.

The lower bound allows the simulator all clean work registers and adaptive operations described in the model. These resources do not evade the bit-query lower bound. The hard **target** remains an autonomous random-unitary semigroup: it has no Hamiltonian term, interleaved control, measurement, or reset. Each supplied reflection is Hermitian and unitary, so the generator is unital and self-adjoint in the Hilbert--Schmidt inner product.

There is no claim of linear-in-time hardness at a fixed target dimension, of geometrically local reflection primitives, or of a lower bound for preparing a normalized vector encoding a classical distribution. The task here is simulation of the full trace-preserving channel on arbitrary inputs, and the dimension-uniform worst case admits the finite instances just constructed. In particular, the three-reflection lower bound follows from parity against unrestricted query algorithms, rather than from a restriction to trajectory generation or a chosen elementary gate set.

For comparisons with other simulation tasks and previous lower bounds, see [Related work](../references/related-work.md).

## References for the standard lower-bound tools

- C. H. Bennett, E. Bernstein, G. Brassard, and U. Vazirani, **Strengths and Weaknesses of Quantum Computing**, *SIAM Journal on Computing* **26**(5), 1510–1523 (1997). [arXiv:quant-ph/9701001](https://arxiv.org/abs/quant-ph/9701001); [DOI:10.1137/S0097539796300933](https://doi.org/10.1137/S0097539796300933).
- R. Beals, H. Buhrman, R. Cleve, M. Mosca, and R. de Wolf, **Quantum Lower Bounds by Polynomials**. [arXiv:quant-ph/9802049](https://arxiv.org/abs/quant-ph/9802049). The parity bound used above is a standard consequence of the acceptance-probability degree bound.
