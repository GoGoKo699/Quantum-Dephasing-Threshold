# Model and results

## The question

A single binary dephasing process can be simulated with one reflection-oracle call, however long it runs. Does this remain true when independently specified dephasing processes act simultaneously? This project determines the worst-case query cost when there are one, two, or three supplied reflection primitives, with their total jump rate held fixed.

The answer is a constant/square-root/linear hierarchy. The upper bounds simulate the full quantum channel, including its action on a reference-entangled input. The converse bounds hold against arbitrary quantum algorithms with coherent access to the supplied reflections. The three-reflection hard family has a dimension that grows with time; that qualification is essential.

## 1. The physical evolution

Let $`\mathcal H`$ be a finite-dimensional target Hilbert space. A reflection here means any Hermitian unitary, with no restriction on the dimensions of its two eigenspaces:

```math
R_j=R_j^\dagger,\qquad R_j^2=I,
\qquad j\in\{1,\ldots,k\}.
```

The supplied tuple may include repeated reflections and the identity. Define

```math
\operatorname{Ad}_{R_j}(\rho)=R_j\rho R_j,
\qquad
\mathcal L_k=\frac1k\sum_{j=1}^{k}
  \bigl(\operatorname{Ad}_{R_j}-\operatorname{Id}\bigr),
\qquad
\Phi_t=e^{t\mathcal L_k}.
```

This is a GKSL generator with jump operators $`R_j/\sqrt{k}`$ and no Hamiltonian term. The total jump rate is one. Time $`t`$ is therefore dimensionless: it is physical time multiplied by the total rate. A common physical rate $`\gamma`$ replaces $`t`$ everywhere by $`\gamma t_{\mathrm{phys}}`$.

The generator is autonomous, unital, and self-adjoint in the Hilbert–Schmidt inner product. Equivalently,

```math
\mathcal L_k(\rho)
=-\frac1{2k}\sum_{j=1}^{k}[R_j,[R_j,\rho]].
```

For one reflection, its eigenspace blocks remain fixed while coherence between the plus and minus eigenspaces decays as $`e^{-2t}`$. Thus these are binary dephasing primitives. The reflections may fail to commute, and no spatial locality is promised.

The integer $`k`$ counts the supplied primitives and their oracle interfaces. It is **not** an invariant of the channel or the minimum number of jumps in a GKSL representation. Changing a generator's representation may change the access required to implement its new jumps.

## 2. Access, output and error

The algorithm knows $`k`$, the target dimension, $`t`$, the desired error, and the reflection promise. It receives no classical description of the unknown matrix entries. Its oracle is

```math
S_R=\sum_{j=1}^{k}|j\rangle\langle j|\otimes R_j.
```

On any unused binary index labels, extend this oracle by the identity. One invocation of SELECT, its inverse, or a version with an additional coherent control costs one query. Since the reflections are involutions, SELECT is its own inverse. Calling an individual reflection is a permitted special case.

Algorithms may use arbitrary oracle-independent quantum operations, ancillas, measurements, classical randomness and adaptive control. Quantum operations may depend on prior outcomes. Query complexity counts the **total serial oracle calls**, with an upper bound on every branch; a small expected count is insufficient. Known gates and classical arithmetic are free only in this query measure. Their actual costs are accounted for separately in [Sampling and resources](sampling-and-resources.md).

The output must be a completely positive trace-preserving map $`\widetilde\Phi_t`$ satisfying

```math
\|\widetilde\Phi_t-\Phi_t\|_\diamond\le\epsilon.
```

We use the unhalved diamond norm. For two channels it is the maximum trace norm of their output difference on an input state with a sufficiently large reference system. In particular, an error of $`\epsilon`$ changes any measured event probability by at most $`\epsilon/2`$. There is no input-state restriction, conditioning on success, or normalized-amplitude output convention.

The algorithm must work uniformly for all allowed reflection tuples of its given dimension. Let $`Q_k(t,\epsilon)`$ be the supremum over finite target dimensions of the least worst-case number of queries for such an algorithm. Equivalently, an upper bound must hold for every dimension and tuple; a lower bound may choose a finite dimension and a hard family depending on $`t`$. The order of these quantifiers excludes giving the algorithm a classical description of the hard instance.

## 3. The query threshold

**Theorem.** Fix $`\epsilon_0=1/100`$. For every real $`t\ge1`$, the dimension-uniform worst-case query complexities obey

```math
Q_1(t,\epsilon_0)=1,
\qquad
Q_2(t,\epsilon_0)=\Theta(\sqrt t),
\qquad
Q_3(t,\epsilon_0)=\Theta(t).
```

The same orders hold for any other fixed $`0<\epsilon\le1/100`$, with constants allowed to depend on that fixed error. This is a statement about time dependence at fixed accuracy, not an optimal joint time-and-precision theorem.

| Supplied reflections | Universal simulation | Converse and dimension |
|---|---|---|
| One | Exact parity mixture; at most one query | One query is necessary in the worst case; a qubit suffices |
| Two | Sample a reduced alternating word; bounded query cost $`O(\sqrt t)`$ | $`\Omega(\sqrt t)`$ even for a qubit |
| Three | Truncate the ordinary Poisson trajectory; cost $`O(t)`$ | $`\Omega(t)`$ for a family with $`\exp(\Theta(t))`$ target dimension |

The upper proofs are in [Pair simulation](pair-simulation.md), with the direct finite-bit implementation in [Sampling and resources](sampling-and-resources.md). The lower proofs and explicit constants are in [Lower bounds](lower-bounds.md). In particular, that page proves

```math
Q_2(t,\epsilon)
\ge \frac{1-e^{-(1-\cos1)}-2\epsilon}{2}\sqrt t,
\qquad
Q_3(t,\epsilon)\ge\frac{t}{384}
\quad (0<\epsilon\le1/100).
```

The one-reflection endpoint and general parity lower-bound method are inherited ingredients. The fixed two-versus-three classification is the contribution studied here; [Related work](../references/related-work.md) identifies the relevant existing results and exact model distinctions.

### Every fixed larger number

For each fixed $`k\ge3`$, the worst-case order is also $`\Theta(t)`$. Pad a three-reflection hard instance with $`k-3`$ identity primitives. Its generator becomes $`(3/k)\mathcal L_3`$, so a time-$`t`$ simulation contains the three-reflection problem at time $`3t/k`$. The small-time part follows from the constant lower bound, and the general trajectory upper bound is unchanged. Constants may depend on $`k`$; this does not claim a uniform joint law in $`k`$ and $`t`$.

## 4. The general linear upper bound

Set $`\mathcal T=k^{-1}\sum_j\operatorname{Ad}_{R_j}`$. Since the identity superoperator commutes with $`\mathcal T`$,

```math
\Phi_t=e^{-t}\sum_{n=0}^{\infty}\frac{t^n}{n!}\mathcal T^n.
```

Thus draw $`N\sim\operatorname{Poisson}(t)`$ and apply $`N`$ independently uniform reflection labels. This exact mixture has an unbounded query count, so it does not alone meet the model's branchwise cap.

Choose

```math
n_{\max}=\left\lceil2t+2\log(4/\epsilon)\right\rceil.
```

On a branch with $`N>n_{\max}`$, apply the identity instead. This replacement is trace preserving and uses at most $`n_{\max}`$ oracle calls. The exponential-moment bound with parameter $`\log2`$ gives

```math
\Pr(N>n_{\max})
\le e^{t-n_{\max}\log2}
\le\epsilon/4.
```

The diamond distance between any two channels is at most two. Replacing a mixture of total probability at most $`\epsilon/4`$ therefore changes the channel by at most $`\epsilon/2`$, including on reference-entangled inputs. Reserve the remaining $`\epsilon/2`$ for finite-bit approximation of the truncated probability law. This proves $`O(t+\log(1/\epsilon))`$ oracle cost for every fixed $`k`$. There are only $`O(t+\log(1/\epsilon))`$ retained counts; their probabilities can be computed by the Poisson recurrence with sufficient precision, and rounded to a normalized dyadic table. This requires one scalar recurrence step per retained count, with the precision cost charged separately; no optimal classical bit-complexity claim is needed for this general query bound. The pair algorithm uses a different direct sampler to retain its square-root advantage in the complete resource account.

## 5. What the theorem establishes

The classification concerns uniform simulation of full autonomous quantum channels from supplied reflection oracles. It shows that the guarantee of sublinear time dependence survives an arbitrary pair, while a third primitive can destroy that guarantee. Many particular triples can still be easy; the third line is a worst-case obstruction.

The three-reflection construction uses $`\Theta(t)`$ target qubits and need not be geometrically local. The theorem gives no linear lower bound at fixed target dimension and no practical hardware speedup. It also does not charge every reflection as one elementary gate: a reflection may be costly to realize physically. These qualifications connect the oracle statement to its physical meaning, developed in [Interpretation](interpretation.md).

The finite checks in [Verification](../verification/README.md) independently exercise the channel identities, direct sampler, qubit signal and finite tree construction. Their numerical results are diagnostics; the asymptotic and full diamond-norm claims rest on the analytic arguments above and in the linked proof pages.
