# From Watrous to the reflection threshold

A device applies unknown reflections when a random clock rings. To simulate the device, one must first decide which output is wanted: the system left inside it, or the coherent field that has left it. Both outputs are channels on the same initial quantum input, yet they retain different information. This bridge connects that distinction to the constant/square-root/linear reflection threshold.

The single common educational anchor is **John Watrous, [The Theory of Quantum Information, 2018 author draft](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)**. The [30 milestones](MILESTONES.md) organize this project's story. The [scientific account](../science/README.md) owns exact statements and full proofs; the [sister field account](../science/field-output.md) states the receiving model and points to its authoritative field proofs.

## 1. Targeted source route

| Watrous material | What it supplies | Project connection supplied here |
|---|---|---|
| Chapter 1, linear algebra, norms and probability | Operators, tensor products, spectral decomposition and probabilistic quantities | A reflection is an unknown Hermitian involution, and its supplied interface need not be a small local gate. |
| §2.2, quantum channels and their representations | Kraus and Stinespring descriptions, complete positivity and trace preservation | Random reflection histories implement a channel on an existing input; retaining their coherent purification defines a different field output. |
| §3.1, state discrimination | Observable event probabilities and trace distance | A bounded measurement of either output can turn simulation accuracy into a query lower bound. |
| §3.2, fidelity | Overlaps, purification comparisons and their operational meaning | An input-independent omitted probability gives a square-root error for a coherent output truncation. |
| §3.3, channel discrimination and completely bounded trace norm | A channel comparison that permits an untouched entangled reference | System and field simulators must work on every input; the two projects explicitly translate their factor-of-two conventions. |

The book supplies channel and distinguishability foundations. It does not contain this project's Poisson/Skellam identities, certified endpoint sampler, reflection-oracle compiler or parity proof. Those additional steps are developed below and in the linked science. Primary query-complexity research, including the polynomial method, remains attribution rather than a second educational anchor.

## 2. Translate the objects and conventions

| Book/channel language | Object used in this project |
|---|---|
| Input space | The unknown initial system, possibly correlated with an untouched reference. |
| A known quantum channel | An oracle-independent operation, which may use earlier measurement outcomes. |
| Stinespring isometry | The coherent trajectory expansion, with system and field as its two output factors. |
| One marginal channel | The reduced-system semigroup $`\Phi_t`$. |
| The other marginal for the specified dilation | The coherent field channel $`\Gamma_t`$. Its physical labels and phases must be fixed. |
| Completely bounded trace norm | The diamond norm $`\|\cdot\|_\diamond`$ in the scientific pages. |
| Event-probability error | At most $`\epsilon/2`$ for the system's unhalved error $`\epsilon`$; at most $`\epsilon`$ for a field half-diamond error $`\epsilon`$. |

A reflection obeys $`R=R^\dagger`$ and $`R^2=I`$. The simulator receives no matrix entries. Its supplied oracle is

```math
S_R=\sum_{j=1}^{k}|j\rangle\langle j|\otimes R_j.
```

One controlled SELECT, its inverse, or an individual reflection call costs one query. Unused binary labels act as identity. The count is serial calls capped on every branch, not elapsed circuit depth or an expectation. Known processing is free only in this query measure; sampling, compilation, memory, output registers and implementing the unknown operation remain resources.

## 3. From reflection noise to a channel and its dilation

Let $`\mathcal T=k^{-1}\sum_j\mathrm{Ad}_{R_j}`$. The generator is $`\mathcal L_k=\mathcal T-\mathrm{id}`$. Expanding its exponential gives

```math
\Phi_t=e^{-t}\sum_{N=0}^{\infty}\frac{t^N}{N!}\mathcal T^N.
```

Thus the device's reduced system can be reproduced by drawing a rate-one Poisson count, choosing independent uniform reflection labels, and applying the corresponding product. Every branch is unitary, so the mixture is CPTP on every reference-entangled input. There is no input-state preparation or postselection.

For a coherent dilation, instead prepare count and labels in superposition. With the fixed physical word states from [the field contract](../science/field-output.md#fixed-microscopic-target),

```math
V_t|\psi\rangle=
\sum_{N,w}\sqrt{e^{-t}t^N/(N!k^N)}\,
W_w|\psi\rangle\otimes|N,w\rangle_{\mathcal F}.
```

Tracing the field gives the system channel. Tracing the system gives a field channel whose off-diagonal trajectory blocks contain overlaps of different products. A classical jump record has lost these blocks and is therefore a different output. This is the concrete Stinespring connection from Watrous §2.2.

The field further fixes $`L_j=R_j/\sqrt k`$, zero Hamiltonian, identity scattering and vacuum inputs. These microscopic choices are more information than the reduced generator alone. A phase on a jump rotates its bath's photon-number phase even if it leaves $`\mathrm{Ad}_{R_j}`$ unchanged.

## 4. Error as an operational guarantee

The system theorem requires $`\|\widetilde\Phi_t-\Phi_t\|_\diamond\le0.01`$. The field classification uses $`\frac12\|\widetilde\Gamma_t-\Gamma_t\|_\diamond\le0.1`$. Both suprema include arbitrary untouched references. They are not equal error values or equal targets; they give the same fixed-error time exponents.

Two truncation rules illustrate why the output matters. For a classical mixture, replacing trajectories of total probability $`\delta`$ by any legal channel costs at most $`2\delta`$ in unhalved diamond norm. For a coherent pure dilation, normalized restriction to a set of input-independent probability $`1-\delta`$ has overlap $`\sqrt{1-\delta}`$ with the original output. Its trace distance is $`\sqrt\delta`$, hence its half-diamond error is at most that amount after any partial trace. The latter is a purity/overlap argument using the foundation in Watrous §3.2, not a classical total-variation estimate.

A hybrid replaces oracle calls one at a time. Since

```math
\|\mathrm{Ad}_U-\mathrm{Ad}_V\|_\diamond\le2\|U-V\|_{\mathrm{op}},
```

a $`q`$-query algorithm's two outputs differ in trace distance by at most $`q\|U-V\|_{\mathrm{op}}`$. The surrounding known channels contract distinguishability. This covers measurements, randomness, references and adaptive control. The same operational norm connects the upper error budget to the lower-bound measurement.

## 5. One reflection, then every pair

One reflection leaves only even or odd count, because $`R^{2n}=I`$ and $`R^{2n+1}=R`$. The system is a known mixture of identity and reflection. The coherent field retains an even-count and an odd-count vector; one controlled reflection suffices for their joint isometry in that declared two-fiber code. Actual preparation or optical realization of the fibers has separate cost.

For two reflections, cancelling adjacent equal letters leaves an alternating word. Its abstract endpoint is a signed integer $`s`$ on a line. Extra relations of the actual matrices can identify endpoints but do not invalidate this universal representation. A rate-one Poisson number of equal-choice steps gives

```math
p_s(t)=e^{-t}I_{|s|}(t),\qquad\mathbb E S_t=0,\qquad
\operatorname{Var}S_t=t.
```

Concentration makes $`|S_t|=O(\sqrt t)`$ at fixed tail probability. For the system, sample that endpoint directly and apply its word. The finite cyclic FFT sampler avoids generating the order-$`t`$ history; its probabilities are compiled into an explicitly stored classical dyadic table, without coherent memory access.

For the field, the same operator cancellation must be applied coherently while keeping trajectory amplitudes. In an explicit count/word code, compute $`s`$, apply its reduced word, then uncompute $`s`$. Measuring or discarding that workspace would expose which trajectory occurred and dephase the field. This upper lift is routine; it is not a new independent discovery.

## 6. Why the square-root order is necessary

A lower bound can use one legal input even though an upper simulator must handle all inputs. For the system, compare nearby qubit axes $`A=Z`$ and $`B_\theta=\cos\theta Z+\sin\theta X`$. At $`\theta=t^{-1/2}`$ a slow mode decays by a constant, while the oracle changes by only order $`t^{-1/2}`$. The hybrid therefore requires order $`\sqrt t`$ queries.

For the field, the measured system coordinate is unavailable. Use instead

```math
R_\pm(\theta)=\cos\theta Z\pm\sin\theta X.
```

A known beamsplitter maps their baths to bright/dark couplings $`\cos\theta Z`$ and $`\sin\theta X`$. The dark count is Poisson with mean $`t\sin^2\theta`$. It is zero at $`\theta=0`$ and nonzero with constant probability at $`\theta=t^{-1/2}`$. This bounded field event supplies the required gap. It preserves total photon number, so the pair lower bound survives total-number dephasing. The [field account](../science/field-output.md#a-qubit-field-witness-for-the-pair) links to the detailed proof.

## 7. Tree parity for the system

Three reflection types allow a branching reduced-word tree. At a nonroot vertex, two colors move outward and one inward. Although every edge move is reversible, the radius has positive drift. Put input bit $`x_\ell`$ on every edge between depths $`\ell-1`$ and $`\ell`$, and XOR it into an answer qubit when crossing. Backtracking cancels that XOR. An endpoint at depth at least $`m`$ therefore carries all-$`m`$ parity.

The finite source construction chooses $`m=\lfloor t/48\rfloor`$ and outer radius $`\lceil4t\rceil`$. A difference of independent Poisson counts has mean $`t/3`$ and variance $`t`$ and is dominated by radial depth. This controls shallow endpoints; the total jump-count tail controls the outer boundary. Measuring depth and answer then returns parity with a constant success advantage.

To preserve coherent SELECT access in the reduction, reversibly compute the symmetric edge-depth address, query its bit into a buffer, update the answer, query again to erase the buffer, then move the vertex and erase known workspace. Inactive branches use one ordinary valid address twice. This costs two bit queries, without a free controlled bit oracle or a zero sentinel. The standard polynomial argument says $`T`$ bit queries have acceptance degree at most $`2T`$; a polynomial of degree less than $`m`$ cannot correlate with the full-parity character. Thus bounded-error parity requires $`T\ge m/2`$, giving a linear reflection-query lower bound.

This probability and query-reduction material is supplied by the project and its cited primary literature; it is not a theorem imported from Watrous.

## 8. Why the field needs a different triple

For the original identity-loop tree, the coordinate change that XORs the depth-prefix parity into the answer fixes the root and conjugates every unknown reflection to its zero-bit version. It acts only on the final discarded system. The field on the root input is therefore exactly independent of the bits. A system theorem cannot pass through that trace without a new witness.

Truncate instead at depth $`m`$, and make each missing leaf-color transition act by known $`Z`$. The same coordinate change now leaves the full parity as a sign on leaf emissions. A field word carries $`(-1)^{P K}`$, with $`P`$ the full parity and $`K`$ its leaf-loop count. The field's overlap can be bounded through leaf occupation time, giving a constant separation greater than $`0.5071`$. The two-query oracle compiler is unchanged, so field simulation still needs order $`t`$ queries.

The new trace has a sharp boundary: within a terminal-vertex block, $`K\equiv N-|v|\pmod2`$. The two parity fields therefore differ by the total-number phase $`e^{i\pi N_{\mathrm{tot}}}`$ and become identical after dephasing total photon number. This proves coherent-field hardness with a specified phase reference; it does not prove a phase-insensitive linear lower bound. Both tree constructions use dimension exponential in time.

## 9. Assemble the result without conflating resources

The system and specified coherent field share the same worst-case exponents: one, square-root time, then linear time. Their upper mechanisms share reflection-word algebra; their converse measurements retain different information. The source's system proofs remain here; the sister owns the new field-only proof, with the definitions and consequence stated [locally](../science/field-output.md).

The system pair sampler has near-square-root preprocessing at fixed error. An explicit field word output uses order-$`t`$ slots and roughly linear known preparation/processing work, despite its square-root number of unknown calls. A compressed endpoint code needs an explicit known physical embedding, and declaring it supplies no cheap optical decoder. The physical field still has order-$`t`$ photons and interval $`t`$. The classification concerns oracle calls and fixed error in the dimension-uniform worst case, leaving sharp dimension dependence, locality and joint time/precision laws open.
