# Thirty milestones for the dephasing threshold

This map follows the question of how many calls to unknown reflections are needed to reproduce their continuous-time noise. Its route connects the physical output requirement to an accelerated simulator and then to lower bounds that apply to arbitrary quantum algorithms.

The threshold statements concern every real $`t\ge1`$ and a fixed accuracy $`0\lt\epsilon\le0.01`$, with the worst case taken over finite system dimensions. The pair construction also gives explicit bounds as accuracy varies.

The single educational anchor is **Andrew M. Childs, *Lecture Notes on Quantum Algorithms*, 17 April 2025**, in the [author-hosted edition][childs]. Section numbers below refer to that edition; PDF links open at the relevant starting page. The [source-to-project bridge](CHILDS_BRIDGE.md) translates the anchor into this model. Density operators, complete positivity, the diamond norm, Poissonization, and the certified finite-bit sampler are supplied in the bridge and scientific pages. Their Childs pointers identify the relevant circuit, approximation, walk, or query-method foundations.

## Allocation and dependency convention

| Phase | Milestones | Scientific purpose | Synthesis |
|---|---|---|---|
| Background/preliminaries | M01–M12 | Join quantum registers and channels, coherent oracle access, error accounting, and probabilistic trajectories into a precise simulation problem. | M12 states the complete task and the obligations of its upper and lower bounds. |
| Narrative/innovation | M13–M30 | Develop the cancellation mechanism, complete its algorithmic resources, and connect two distinct lower-bound arguments to the threshold. | M30 assembles the theorem, its physical meaning, and its limits. |

The allocation is **12 background milestones and 18 narrative milestones**. The foundations require three interfaces to be made explicit: a circuit must implement a channel on an existing input, a stochastic evolution must have a bounded query implementation, and a simulator must be convertible into a query algorithm for a lower bound. The longer narrative phase follows these interfaces through the pair sampler and the finite-tree reduction. Each phase proceeds from individual objects to the complete scientific account.

Every milestone belongs to the phase containing its heading. Dependencies name earlier IDs and may be transitive. They describe logical prerequisites, not a prescribed reading schedule. Understanding targets group related steps; the linked scientific pages retain the full calculations and specialist details.

## Phase I — Background/preliminaries

### M01 — Registers, operations, and observable outcomes

**Central question:** What does a quantum algorithm act on, and what can its output reveal?

**Understanding target:** Interpret basis states, superpositions, tensor-product registers, unitary operations, and measurement probabilities. Distinguish the system whose evolution is requested from extra registers used to carry out an algorithm.

**Dependencies and story role:** None. This supplies the concrete objects to which the channel and oracle definitions will apply.

**Conceptual connection:** A computational basis can label a qubit, a graph vertex, or an oracle address; the mathematical operation must be specified on all superpositions of those labels.

**Source pointers:** [Childs §§1.1–1.2][childs-1]; [bridge §3](CHILDS_BRIDGE.md#3-from-state-vectors-to-full-quantum-channels); [model §2](../science/model-and-results.md#2-access-output-and-error).

### M02 — What the reflection promise gives

**Central question:** Which consequences follow from supplying a Hermitian involution?

**Understanding target:** Explain why $`R^\dagger=R`$ and $`R^2=I`$ make the same operation its own inverse and restrict its eigenvalues to $`\pm1`$. Separate these known algebraic properties from the unknown eigenbasis and matrix entries.

**Dependencies and story role:** M01. The local oracle promise supplies the cancellation relation used throughout the project.

**Conceptual connection:** Reflection geometry becomes an algorithmic resource because consecutive equal calls cancel exactly, even when two supplied reflections fail to commute.

**Source pointers:** [Childs §1.2][childs-1]; [bridge §2](CHILDS_BRIDGE.md#2-translating-the-oracle-model); [model §1](../science/model-and-results.md#1-the-physical-evolution).

### M03 — From random operations to full quantum channels

**Central question:** How can classical randomness describe a quantum evolution on an unknown input?

**Understanding target:** Interpret a density operator and a convex mixture of unitary conjugations. Explain complete positivity and trace preservation through the implemented random branches, including an arbitrary entangled reference register on which the simulator acts trivially.

**Dependencies and story role:** M01–M02. This replaces a description of one state trajectory by the physical map that must be simulated.

**Conceptual connection:** Sampling a classical word and applying it to the existing system implements the same channel for every input; no preparation or knowledge of that input is required.

**Source pointers:** [Childs §§1.1–1.2][childs-1] for the register foundations; [bridge §3](CHILDS_BRIDGE.md#3-from-state-vectors-to-full-quantum-channels); [pair simulation §1](../science/pair-simulation.md#1-model-and-exact-poisson-expansion).

### M04 — Operational error with a reference

**Central question:** What does it mean to approximate the requested evolution uniformly?

**Understanding target:** Explain the unhalved diamond-norm convention, its maximization over inputs and references, and why channel error at most $`\epsilon`$ changes any final event probability by at most $`\epsilon/2`$. Identify the stronger obligation of a channel guarantee compared with a calculation for one chosen input.

**Dependencies and story role:** M03. This fixes the common error currency for upper bounds, implementation accuracy, and lower-bound measurements.

**Conceptual connection:** The same norm certifies a random-word simulator and limits the loss of success when that simulator is used to solve a hidden-bit problem.

**Source pointers:** [Childs §2.1][childs-2] for the approximation starting point; [bridge §3](CHILDS_BRIDGE.md#3-from-state-vectors-to-full-quantum-channels); [model §2](../science/model-and-results.md#2-access-output-and-error).

### M05 — The supplied oracle interface

**Central question:** What information about the reflections can an algorithm obtain in one query?

**Understanding target:** Interpret individual reflection calls, coherent $`\mathrm{SELECT}`$, and external controlled calls. Distinguish unknown operations from arbitrary known processing, and understand that coherent access, including its phases, is part of the supplied interface.

**Dependencies and story role:** M01–M02. This defines the algorithms against which the lower bounds must hold.

**Conceptual connection:** An algorithm may keep the choice of reflection in superposition. Proving hardness only for a sampled sequence of classical labels would leave that access unaddressed.

**Source pointers:** [Childs §§21.1–21.2][childs-21]; [bridge §2](CHILDS_BRIDGE.md#2-translating-the-oracle-model); [lower bounds §1](../science/lower-bounds.md#1-statements-and-oracle-conventions).

### M06 — Reversible access and returned workspace

**Central question:** How can a query-dependent action be carried out without leaving unwanted information behind?

**Understanding target:** Explain compute–query–uncompute using an ordinary input-bit oracle. Track address, answer, control, and work registers separately, including branches on which the intended operation is inactive. Identify which cleanup operations must themselves query the input.

**Dependencies and story role:** M01, M05. This prepares the exact oracle compiler needed to turn a hypothetical simulator into an ordinary bit-query algorithm.

**Conceptual connection:** Classical knowledge of a graph edge can be computed reversibly; the unknown bit attached to that edge must be read and erased through the allowed oracle.

**Source pointers:** [Childs §1.4][childs-reversible] and [§21.2][childs-queries]; [bridge §10](CHILDS_BRIDGE.md#10-compiling-the-coherent-oracle); [lower bounds §5.4](../science/lower-bounds.md#54-compiling-a-controlled-select-into-two-ordinary-bit-queries).

### M07 — A resource bound that holds on every branch

**Central question:** Which costs are included when a stochastic simulation is called fast?

**Understanding target:** Distinguish the maximum serial number of oracle calls from an expected count. Account separately for classical preprocessing, random bits, memory, known gates, input representation, and any synthesis cost for a supplied oracle.

**Dependencies and story role:** M03, M05. This prevents a distributional description from being mistaken for a complete bounded-cost algorithm.

**Conceptual connection:** A short typical trajectory is useful only after its tails and the work of sampling it have been brought into the resource contract.

**Source pointers:** [Childs §21.1][childs-21] and [Chapter 27][childs-27]; [model §2](../science/model-and-results.md#2-access-output-and-error); [sampling and resources §§7–8](../science/sampling-and-resources.md#7-classical-time-precision-and-memory).

### M08 — Errors and oracle differences under composition

**Central question:** Why can local approximation errors be accumulated through an adaptive algorithm?

**Understanding target:** Trace a telescoping replacement of one oracle call at a time. Connect an operator-norm difference of unitaries to a factor-two channel bound, and use contractivity under intervening physical processing to cover measurements, randomness, ancillas, and adaptive control.

**Dependencies and story role:** M04–M05, M07. This provides the common tool for gate-accuracy accounting and the qubit lower bound.

**Conceptual connection:** Childs §2.1 supplies unitary operator-norm telescoping; the local argument extends the comparison to full channels and their observable outputs.

**Source pointers:** [Childs §2.1][childs-2]; [lower bounds §2](../science/lower-bounds.md#2-a-hybrid-inequality-for-arbitrary-adaptive-simulators); [sampling and resources §8](../science/sampling-and-resources.md#8-quantum-gates-and-implementation-accuracy).

### M09 — The autonomous generator and its rate-one clock

**Central question:** How does the generator determine a distribution of jump histories?

**Understanding target:** Read $`\mathcal L_k=\frac1k\sum_j(\mathrm{Ad}_{R_j}-\mathrm{id})`$ as a time-independent generator with total jump rate one. Derive its Poisson expansion and identify why reflection conjugations make the evolution unital and the generator self-adjoint in the Hilbert–Schmidt inner product.

**Dependencies and story role:** M02–M03. This connects the physical differential equation to a concrete random-word representation.

**Conceptual connection:** Time normalization fixes how many opportunities for oracle-dependent motion occur; the generator exponential makes that clock exact.

**Source pointers:** [Childs §§27.1–27.2][childs-27] for the simulation setting; [bridge §4](CHILDS_BRIDGE.md#4-reflection-noise-and-the-poisson-clock); [pair simulation §1](../science/pair-simulation.md#1-model-and-exact-poisson-expansion).

### M10 — From walk statistics to reliable events

**Central question:** Which probabilistic information is needed to control a simulation?

**Understanding target:** Distinguish endpoint position, jump count, mean, variance, and tail probability for a continuous-time walk. Explain how Poissonization, a moment bound, and an exponential-moment bound answer different questions about typical motion and rare events.

**Dependencies and story role:** M07, M09. This supplies the probability tools shared by the line upper bound and the finite-tree lower bound.

**Conceptual connection:** Diffusive displacement can give a short endpoint description, while biased radial motion can make a distant computational label likely to be reached.

**Source pointers:** [Childs §17.3][childs-walk]; [bridge §§6–7](CHILDS_BRIDGE.md#6-two-reflections-cancellation-produces-diffusion); [pair simulation §§3–4](../science/pair-simulation.md#3-exact-endpoint-law-and-exact-channel-identity).

### M11 — Why parity forces many quantum queries

**Central question:** How can a lower bound rule out every bounded-error quantum query algorithm?

**Understanding target:** Explain why an algorithm with $`T`$ ordinary bit queries has acceptance probabilities of degree at most $`2T`$. Connect the full-parity Fourier character to the lower bound $`T\ge m/2`$ for parity of $`m`$ bits, including classical randomness and adaptive processing.

**Dependencies and story role:** M05–M08. This supplies the external hardness statement into which the three-reflection simulation problem will be reduced.

**Conceptual connection:** A physical output carrying parity can turn a fast simulator into an impossible low-degree algorithm. The project's parity-correlation proof uses no symmetrization step; Childs §21.4 is optional context.

**Source pointers:** [Childs §§21.2–21.3 and §21.5][childs-queries]; [lower bounds §5.5](../science/lower-bounds.md#55-applying-the-quantum-parity-bound); [standard-tool references](../science/lower-bounds.md#references-for-the-standard-lower-bound-tools).

### M12 — Background synthesis: the complete simulation contract

**Central question:** What exactly must a simulator achieve, and what would establish its optimal cost?

**Understanding target:** Assemble the unknown reflection tuple, total rate, arbitrary system and reference input, full diamond error, and maximum branch query count into one task. Distinguish an upper bound valid for every tuple from a lower bound witnessed by a legal family, with a supremum over finite dimensions.

**Dependencies and story role:** M02, M04–M05, M07–M11. This integrates the foundations into the framework used by both sides of the theorem.

**Conceptual connection:** The physical output requirement, access model, probability estimates, and query lower-bound tools now have compatible meanings. A witness input can prove hardness even though a simulator must handle all inputs.

**Source pointers:** [Childs §21.1][childs-21] and [Chapter 27][childs-27]; [model §§1–3](../science/model-and-results.md#1-the-physical-evolution); [interpretation §4](../science/interpretation.md#4-representation-and-resource-boundaries).

## Phase II — Narrative/innovation

### M13 — One reflection leaves only jump parity

**Central question:** How much of a long history survives when every jump is the same involution?

**Understanding target:** Reduce a history to even or odd parity and obtain a mixture of the identity channel and one reflection conjugation. Combine the one-query implementation with the all-$`X`$/all-$`Z`$ witness to explain $`Q_1=1`$ for $`t\ge1`$ and fixed $`\epsilon\le0.01`$.

**Dependencies and story role:** M02–M04, M09, M12. This is the smallest complete instance of algebraic compression and matching query necessity.

**Conceptual connection:** The sampled jump count grows with time, but the operation it represents has only two possibilities.

**Source pointers:** [Childs §1.2][childs-1] and [§21.1][childs-21]; [bridge §5](CHILDS_BRIDGE.md#5-one-reflection-only-jump-parity-matters); [lower bounds §3](../science/lower-bounds.md#3-a-constant-lower-bound-including-one-reflection).

### M14 — Two reflections turn words into a line

**Central question:** What information remains after all adjacent equal letters cancel?

**Understanding target:** Represent every reduced two-letter word by a signed integer, with its sign choosing the first chronological gate. Explain the alternating-word convention and why appending either reflection moves the abstract endpoint by one step.

**Dependencies and story role:** M02, M09–M10, M13. This identifies the mechanism that compresses every pair, including noncommuting pairs.

**Conceptual connection:** The algebraic relation $`A^2=B^2=I`$ turns a history problem into endpoint motion on a line. Additional relations between the actual matrices preserve the validity of this representation.

**Source pointers:** [Childs §17.3][childs-walk]; [bridge §6](CHILDS_BRIDGE.md#6-two-reflections-cancellation-produces-diffusion); [pair simulation §2](../science/pair-simulation.md#2-the-reduced-word-is-a-walk-on-a-line).

### M15 — The exact endpoint law is already a channel identity

**Central question:** Which distribution of reduced words reproduces the entire pair evolution?

**Understanding target:** Derive $`S_t=N_+-N_-`$ with independent $`N_\pm\sim\mathrm{Poisson}(t/2)`$, its characteristic function, and the mixture of conjugations by $`W_{S_t}`$. Explain why equality of the random operations gives an exact identity on arbitrary inputs and references.

**Dependencies and story role:** M03–M04, M09–M10, M14. This upgrades word cancellation to the universal pair simulation formula.

**Conceptual connection:** Childs §17.3 uses total rate two; its time $`t/2`$ matches the project's time $`t`$. The resulting Skellam law has variance $`t`$, which identifies the square-root length scale.

**Source pointers:** [Childs §17.3, Eq. (17.20)][childs-walk]; [pair simulation §3](../science/pair-simulation.md#3-exact-endpoint-law-and-exact-channel-identity); [bridge §6](CHILDS_BRIDGE.md#6-two-reflections-cancellation-produces-diffusion).

### M16 — Tail probability becomes a physical query cap

**Central question:** How can an unbounded random description yield a simulator with a fixed maximum cost?

**Understanding target:** Use the Skellam exponential-moment bound to choose a radius of order $`\sqrt{t\log(4/\epsilon)}+\log(4/\epsilon)`$. Replace rare branches by the identity channel and explain both complete positivity and the factor-two tail-to-diamond bound. Apply the same principle to the Poisson count to obtain the general linear upper bound.

**Dependencies and story role:** M04, M07, M10, M15. This converts endpoint statistics into the required worst-branch resource guarantee.

**Conceptual connection:** A controlled change to rare outcomes preserves a valid trace-preserving map and supplies the upper bounds against which both lower bounds will be compared.

**Source pointers:** [Childs §2.1][childs-2] for error composition; [pair simulation §4](../science/pair-simulation.md#4-a-hard-query-cap-for-arbitrary-accuracy); [model §4](../science/model-and-results.md#4-the-general-linear-upper-bound).

### M17 — Sample the endpoint without generating the history

**Central question:** How is the square-root query saving retained in the classical preparation?

**Understanding target:** Interpret the finite Fourier formula for the law of $`S_t\bmod K`$. Map each residue to a short signed representative and bound the aliasing error by the endpoint tail, while avoiding generation of the underlying Poisson sequence.

**Dependencies and story role:** M07, M15–M16. This closes the gap between an endpoint existence formula and a directly computable distribution.

**Conceptual connection:** Classical Fourier inversion gives a finite probability table whose size follows the endpoint scale. The table is used by a classical sampler, without coherent data loading.

**Source pointers:** [Childs §17.3][childs-walk] for the walk starting point; [pair simulation §5](../science/pair-simulation.md#5-turning-the-endpoint-description-into-an-algorithm); [sampling and resources §2](../science/sampling-and-resources.md#2-a-finite-cyclic-endpoint-distribution).

### M18 — Approximate arithmetic, exact physical validity

**Central question:** How can finite-precision probabilities define an exactly valid quantum channel?

**Understanding target:** Connect outward-rounded elementary-function intervals, the integer FFT error, clipping, normalization, and dyadic rounding into a certified probability calculation. Explain why the final weights are nonnegative and sum exactly to one, and how their $`\ell_1`$ error becomes full diamond error.

**Dependencies and story role:** M03–M04, M08, M17. This supplies the finite-bit implementation behind the ideal pair formula.

**Conceptual connection:** Numerical approximation affects closeness to the target, while exact sampling of the normalized dyadic law preserves complete positivity and trace preservation. The combined aliasing and arithmetic certificate is at most $`9\epsilon/16`$.

**Source pointers:** [Childs §2.1][childs-2] for additive error accounting; [sampling and resources §§3–5](../science/sampling-and-resources.md#3-certified-elementary-function-inputs); [bridge §7](CHILDS_BRIDGE.md#7-from-diffusion-to-a-bounded-finite-bit-simulator).

### M19 — The complete pair implementation and its cost

**Central question:** Which resources accompany the reduced number of reflection calls?

**Understanding target:** Account for $`O(K\log K\,\mathrm{poly}(b))`$ preprocessing bit operations, where $`b`$ includes rational input length and logarithmic precision. Track classical storage, fixed random-bit sampling, and the query cap; add time-rounding and oracle-synthesis errors and the conditional gate cost of implemented reflections.

**Dependencies and story role:** M07–M08, M16–M18. This completes the pair upper bound as an algorithm with charged preparation and implementation resources.

**Conceptual connection:** Efficient oracle use remains meaningful when the endpoint table is constructed for a single use, the unknown input is left in place, and oracle synthesis is charged separately. Analytic certificates and finite numerical diagnostics have distinct evidential roles.

**Source pointers:** [Childs §2.1][childs-2] and [§§27.1–27.2][childs-27]; [sampling and resources §§7–9](../science/sampling-and-resources.md#7-classical-time-precision-and-memory); [verification: certificate scope](../verification/README.md#what-makes-the-sampler-certificate-different).

### M20 — Nearby qubit oracles leave a finite channel signal

**Central question:** Can a pair of almost indistinguishable reflection oracles generate observably different long-time channels?

**Understanding target:** Analyze $`A=Z`$ and $`B_\theta=\cos\theta\,Z+\sin\theta\,X`$ with $`\theta=t^{-1/2}`$. Connect the exact Bloch-coordinate evolution to a constant output separation for every real $`t\ge1`$, while the oracle difference is only of order $`t^{-1/2}`$.

**Dependencies and story role:** M02–M04, M09, M12. This constructs the witness that makes the square-root upper bound necessary already in dimension two.

**Conceptual connection:** A small tilt of the noise axes can accumulate an observable effect even though each query reveals only a small difference.

**Source pointers:** [Childs §§1.1–1.2][childs-1] and [§2.1][childs-2]; [lower bounds: exact channel signal](../science/lower-bounds.md#exact-channel-signal); [bridge §8](CHILDS_BRIDGE.md#8-why-the-square-root-cost-is-necessary).

### M21 — Pair synthesis: optimality beyond sampled trajectories

**Central question:** Why can coherent access and adaptive quantum processing not beat the square-root cost?

**Understanding target:** Apply the hybrid inequality to the qubit witness, charge both channel-approximation errors, and infer $`\Omega(\sqrt t)`$ queries. Combine this lower bound with the finite-bit construction to state the optimal pair cost at fixed $`\epsilon\le0.01`$.

**Dependencies and story role:** M05, M08, M12, M19–M20. This closes the pair argument across its physical, algorithmic, and oracle-complexity formulations.

**Conceptual connection:** The short reduced word gives an upper bound; distinguishability of nearby legal oracles proves optimality for arbitrary simulators, including controlled queries and reference registers.

**Source pointers:** [Childs §2.1][childs-2] and [§§21.1–21.2][childs-21]; [lower bounds: oracle distance and query bound](../science/lower-bounds.md#oracle-distance-and-query-bound); [model §3](../science/model-and-results.md#3-the-query-threshold).

### M22 — A third reflection creates outward radial motion

**Central question:** How can individually reversible moves carry information a distance proportional to time?

**Understanding target:** Compare the two-letter reduced-word line with the three-letter tree. At a non-root interior vertex, identify two colors that increase depth and one that decreases it, yielding radial drift $`1/3`$ at total rate one despite symmetric traversal of every edge.

**Dependencies and story role:** M02, M09–M10, M14, M21. This identifies the geometric mechanism available to a hard triple after the universal pair case is closed.

**Conceptual connection:** Branching changes the number of outward options. Reversibility of individual transitions and self-adjointness of the generator remain compatible with outward motion from the root.

**Source pointers:** [Childs §17.3][childs-walk] for the line comparison and [§28.1][childs-noff] for the reduction setting; [interpretation §3](../science/interpretation.md#3-reversible-motion-can-move-outward); [lower bounds §5.3](../science/lower-bounds.md#53-a-uniform-finite-time-success-estimate).

### M23 — A finite legal triple of reflection oracles

**Central question:** How is the tree mechanism realized by actual finite-dimensional Hermitian involutions?

**Understanding target:** Construct the truncated tree of reduced three-letter words, color its edges, and use identity loops for missing boundary moves. Attach an input-bit label symmetrically to each edge and include its XOR action on an answer qubit, so each colored permutation squares to the identity.

**Dependencies and story role:** M02, M05–M06, M12, M22. This turns the geometric picture into a legal hard-instance family.

**Conceptual connection:** A boundary convention and symmetric edge labels are essential to obtaining exact finite oracles, with definite phases and no irreversible move hidden in the model.

**Source pointers:** [Childs §1.4][childs-reversible] and [§28.1][childs-noff]; [lower bounds §5.1](../science/lower-bounds.md#51-the-finite-graph-and-its-reflections); [bridge §9](CHILDS_BRIDGE.md#9-three-reflections-a-tree-can-compute-parity).

### M24 — Every trajectory carries the same prefix-parity invariant

**Central question:** Why does a sufficiently deep endpoint reveal all the hidden input bits?

**Understanding target:** Explain why crossing depth $`\ell`$ toggles bit $`x_\ell`$ when $`\ell\le m`$, and why immediate or later backtracking cancels the corresponding contribution. Establish that a vertex at depth $`d`$ carries the parity of the first $`\min(d,m)`$ bits.

**Dependencies and story role:** M11, M23. This supplies the computational information transported by the physical walk.

**Conceptual connection:** The tree's unique root-to-vertex path converts edgewise reversible updates into an endpoint invariant, so parity can be recovered without observing the jump history.

**Source pointers:** [Childs §21.5][childs-parity] and [§28.1][childs-noff]; [lower bounds §5.2](../science/lower-bounds.md#52-the-answer-bit-along-every-trajectory); [bridge §9](CHILDS_BRIDGE.md#9-three-reflections-a-tree-can-compute-parity).

### M25 — The full controlled SELECT costs two bit queries

**Central question:** Does the hidden-bit reduction preserve the simulator's strongest permitted oracle access?

**Understanding target:** Follow the exact two-query compiler for coherent color selection and an external control. Compute the active edge flag and address, read the bit into a clean buffer, update the answer conditionally, erase the buffer, and uncompute the edge data after moving the vertex. Track inactive branches using an ordinary valid address whose two queries cancel.

**Dependencies and story role:** M05–M06, M23–M24. This closes the oracle-access gap before invoking a general query lower bound.

**Conceptual connection:** Symmetric edge attributes make workspace cleanup possible from either endpoint. The construction needs no free controlled bit oracle, promised zero address, residual work, or uncontrolled global phase.

**Source pointers:** [Childs §1.4][childs-reversible] and [§21.2][childs-queries]; [lower bounds §5.4](../science/lower-bounds.md#54-compiling-a-controlled-select-into-two-ordinary-bit-queries); [bridge §10](CHILDS_BRIDGE.md#10-compiling-the-coherent-oracle).

### M26 — The finite tree reaches enough bits with high probability

**Central question:** Can the outward-motion argument survive finite time and a finite boundary?

**Understanding target:** Use $`m=\lfloor t/48\rfloor`$ and $`R=\lceil4t\rceil`$ for $`t\ge48`$. Couple radial depth to a difference of Poisson variables with mean $`t/3`$ and variance $`t`$, control shallow endpoints by Chebyshev's inequality, and bound boundary contact through the total Poisson jump count.

**Dependencies and story role:** M09–M10, M22–M24. This supplies a uniform finite-instance success estimate for the encoded computation.

**Conceptual connection:** Positive drift alone is qualitative. The two probability bounds show that a constant fraction of the simulated time can reliably expose a linear number of bits inside the legal finite system.

**Source pointers:** [Childs §17.3][childs-walk] and [§28.1][childs-noff] for the walk and reduction foundations; [lower bounds §5.3](../science/lower-bounds.md#53-a-uniform-finite-time-success-estimate); [bridge §9](CHILDS_BRIDGE.md#9-three-reflections-a-tree-can-compute-parity).

### M27 — Close the reduction to a linear quantum lower bound

**Central question:** How does accurate channel simulation become a bounded-error parity algorithm?

**Understanding target:** Measure endpoint depth, use the answer at depth at least $`m`$, and guess fairly otherwise. Include the $`\epsilon/2`$ success loss, obtain success above $`7/8`$, and combine the two-bit-query compiler with the parity bound to infer $`q\ge t/384`$. Use the constant lower bound to cover $`1\le t\lt48`$.

**Dependencies and story role:** M04, M11–M13, M16, M24–M26. This completes the three-reflection lower bound against arbitrary adaptive controlled-query algorithms.

**Conceptual connection:** The channel's output distribution becomes an operational computation. Together with the generic upper bound from M16, the reduction yields $`Q_3=\Theta(t)`$ at fixed accuracy.

**Source pointers:** [Childs §21.5][childs-parity] and [§28.1][childs-noff]; [lower bounds §5.5](../science/lower-bounds.md#55-applying-the-quantum-parity-bound); [model §§3–4](../science/model-and-results.md#3-the-query-threshold).

### M28 — The dimension and representation qualifications

**Central question:** Over which families of physical systems does the threshold theorem hold?

**Understanding target:** Interpret the supremum over finite dimensions and the hard-tree size $`D=6\cdot2^R-4=\exp(\Theta(t))`$, which has an $`O(t)`$-qubit encoding. Distinguish a worst-case triple from every triple, a supplied reflection count from intrinsic dissipative rank, and the proved regime from fixed-dimension long-time or locality claims.

**Dependencies and story role:** M05, M07, M12, M21, M23, M27. This reconciles the upper and lower quantifiers before stating the global conclusion.

**Conceptual connection:** Identity padding extends hardness to each fixed $`k\ge3`$ after a time rescaling, with constants depending on $`k`$. The hard family needs no explicit exponentially large graph table, but its growing system size remains part of the theorem.

**Source pointers:** [Childs §21.1][childs-21] and [§28.1][childs-noff]; [lower bounds §6](../science/lower-bounds.md#6-dimension-controls-and-the-scope-of-the-reduction); [model: fixed larger numbers](../science/model-and-results.md#every-fixed-larger-number); [interpretation §4](../science/interpretation.md#4-representation-and-resource-boundaries).

### M29 — What is new, and which comparisons preserve the task

**Central question:** Which contribution remains after inherited tools and nearby simulation results are accounted for?

**Understanding target:** Separate the standard parity method and known single-involution compression from the universal pair algorithm and fixed-three-involution hardness result. Compare prior growing-number reflection hardness, general dissipative lower bounds, and reversible-chain acceleration using their actual oracle, normalization, and output requirements.

**Dependencies and story role:** M03–M05, M11, M13, M19, M21, M27–M28. This places the theorem within its research context without broadening its novelty claim.

**Conceptual connection:** Childs §28.1 concerns sparse-Hamiltonian parity transport; the present reduction supplies finite undirected reflection noise. Coherent Markov-chain state preparation also has a different output contract from a full trace-preserving channel on an arbitrary input.

**Source pointers:** [Childs §28.1][childs-noff] and optional [§18.2][childs-markov]; [related work: comparison criteria](../references/related-work.md#problem-and-comparison-criteria), [prior reflection-noise research](../references/related-work.md#related-unpublished-reflection-noise-research), and [contribution](../references/related-work.md#contribution-separated-from-its-ingredients).

### M30 — Global synthesis: the constant, square-root, and linear law

**Central question:** Why does the complete argument establish a sharp change between two and three supplied reflections?

**Understanding target:** Connect single-reflection parity, the pair's diffusive endpoint and certified sampler, the qubit hybrid witness, and finite-tree parity transport to $`Q_1=1`$, $`Q_2=\Theta(\sqrt t)`$, and $`Q_3=\Theta(t)`$. State the fixed-accuracy, real-time, channel, oracle, and dimension qualifications alongside the result and its charged implementation resources.

**Dependencies and story role:** M12–M13, M16, M19, M21, M27–M29. This integrates the full narrative, including what each proof establishes and what remains outside its scope.

**Conceptual connection:** The number of supplied reflections changes the possible geometry of reduced histories. Full-channel error and unrestricted oracle lower bounds turn that geometry into an optimal simulation classification; the analytical proofs establish universality, while the finite checks support the implementation and conventions.

**Source pointers:** [Childs §§21.1–21.5][childs-21] and [§28.1][childs-noff]; [model §3](../science/model-and-results.md#3-the-query-threshold); [interpretation §5](../science/interpretation.md#5-consequence-and-remaining-questions); [verification: proof routes and limits](../verification/README.md#proof-routes-and-limits).

[childs]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf
[childs-1]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=9
[childs-reversible]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=10
[childs-2]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=15
[childs-walk]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=83
[childs-markov]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=90
[childs-21]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=105
[childs-queries]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=106
[childs-parity]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=107
[childs-27]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=141
[childs-noff]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=147
