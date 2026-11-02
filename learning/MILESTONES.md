# Thirty milestones for the system and field reflection threshold

This common map develops the reduced-system theorem and the receiving consequence for its sister’s specified coherent field. The single educational anchor is **John Watrous, [*The Theory of Quantum Information* (2018 author draft)](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)**. The [Watrous bridge](WATROUS_BRIDGE.md) translates notation, error conventions and output spaces, then supplies the project-specific probability and query arguments absent from the book.

| Phase | Milestones | Scientific purpose |
|---|---|---|
| Background/preliminaries | M01–M12 | Connect states, channels, reflection oracles, probability, distinguishability and output choices into the two precise tasks. |
| Narrative/innovation | M13–M30 | Complete the system algorithm and lower bounds, test their field transfer, and assemble the distinct field witnesses with their resource limits. |

There are **12 background milestones and 18 narrative milestones**. The allocation reflects the interface between physical channel outputs and oracle algorithms. Within each phase the route proceeds from local objects and mechanisms to a global synthesis. Dependencies refer only to earlier IDs and may be transitive. These are reader-independent understanding targets, not a progress or assessment record.

The reduced-system theorem uses unhalved diamond error 0.01; the specified field theorem uses half diamond error 0.1. Both are fixed-error, dimension-uniform worst-case statements for t at least one. Neither triple lower bound proves fixed-dimension linear long-time hardness. The full proofs and specialist details remain in the scientific sources.

## Phase I — Background/preliminaries

### M01 — Registers and observable outcomes

**Central question:** What is retained when a quantum device produces an output?

**Understanding target:** Interpret system, reference and field registers, states, unitary operations and measured event probabilities. Distinguish an existing input from auxiliary registers prepared by a simulator.

**Dependencies and story role:** None. These are the objects on which the model acts.

**Conceptual connection:** The same initial state can produce different operational outputs after different factors are traced.

**Source pointers:** Watrous Chapter 1 and §2.2; [bridge §2](WATROUS_BRIDGE.md#2-translate-the-objects-and-conventions).

### M02 — The reflection promise

**Central question:** Which algebraic information is known about an unknown reflection?

**Understanding target:** Explain Hermiticity, involution and the eigenvalues plus/minus one, while keeping its eigenbasis and matrix entries unknown. Identify why identical adjacent calls cancel.

**Dependencies and story role:** M01. The local promise supplies the later word relation.

**Conceptual connection:** The promise gives an exact operation identity without a classical matrix description.

**Source pointers:** Watrous Chapter 1; [model §1](../science/model-and-results.md#1-the-physical-evolution).

### M03 — Mixtures as physical channels

**Central question:** Why does a random reflection sequence define a channel on every input?

**Understanding target:** Explain density operators, unitary conjugation, Kraus operators and trace preservation. Include an arbitrary untouched reference in the physical requirement.

**Dependencies and story role:** M01–M02. This promotes trajectories to the channel to be simulated.

**Conceptual connection:** A random choice independent of the input implements the same CPTP map on every input.

**Source pointers:** Watrous §2.2; [bridge §3](WATROUS_BRIDGE.md#3-from-reflection-noise-to-a-channel-and-its-dilation).

### M04 — Reference-preserving error

**Central question:** What uniform accuracy does the simulator owe its user?

**Understanding target:** Read the diamond norm as a channel distinguishability guarantee on all input/reference states. Translate the system’s unhalved convention into a bound on every event probability.

**Dependencies and story role:** M03. The common error currency controls simulation and reductions.

**Conceptual connection:** A chosen witness input can prove hardness although an upper algorithm must handle all inputs.

**Source pointers:** Watrous §§3.1, 3.3; [model §2](../science/model-and-results.md#2-access-output-and-error).

### M05 — Phase-referenced SELECT access

**Central question:** What can one oracle call do coherently?

**Understanding target:** Interpret individual, selected, inverse and externally controlled reflection calls, including unused labels. Keep supplied access separate from arbitrary known processing.

**Dependencies and story role:** M01–M02. This defines all allowed simulation strategies.

**Conceptual connection:** A lower bound against sampled classical words alone would miss coherent SELECT algorithms.

**Source pointers:** Watrous §2.2 for channels; [bridge §2](WATROUS_BRIDGE.md#2-translate-the-objects-and-conventions); [oracle conventions](../science/lower-bounds.md#1-statements-and-oracle-conventions).

### M06 — Clean reversible workspace

**Central question:** How can an unknown-bit-controlled operation return its work registers?

**Understanding target:** Track address, active flag, buffer, answer and external control through compute–query–uncompute. Explain why reading and erasing an unknown bit both cost calls.

**Dependencies and story role:** M05. This prepares the exact reduction compiler.

**Conceptual connection:** Known graph attributes are reversible arithmetic; the attached unknown bit is an oracle resource.

**Source pointers:** Watrous §2.2; [bridge §7](WATROUS_BRIDGE.md#7-tree-parity-for-the-system); [SELECT compiler](../science/lower-bounds.md#54-compiling-a-controlled-select-into-two-ordinary-bit-queries).

### M07 — Branchwise query and implementation costs

**Central question:** Which costs support the word “fast”?

**Understanding target:** Distinguish a serial cap on every branch from an expected query count or parallel depth. Account separately for known gates, classical compilation, randomness, precision, memory and output.

**Dependencies and story role:** M03, M05. This makes the algorithmic claim complete.

**Conceptual connection:** Oracle savings do not make an arbitrary supplied reflection or a long output cheap to realize.

**Source pointers:** Watrous §2.2 as circuit-channel foundation; [sampling/resources §§7–8](../science/sampling-and-resources.md#7-classical-time-precision-and-memory).

### M08 — Hybrid replacement and contraction

**Central question:** Why do small oracle differences constrain every adaptive algorithm?

**Understanding target:** Explain one-call-at-a-time replacement and contraction under surrounding channels. Convert operator-norm oracle separation into a bound on measured output separation.

**Dependencies and story role:** M04–M05, M07. This supports precision accounting and lower bounds.

**Conceptual connection:** The same distinguishability norm pays for synthesis error and limits a simulator’s sensitivity.

**Source pointers:** Watrous §§3.1, 3.3; [hybrid proof](../science/lower-bounds.md#2-a-hybrid-inequality-for-arbitrary-adaptive-simulators).

### M09 — The rate-one Poisson clock

**Central question:** How does continuous reflection noise become a random word?

**Understanding target:** Derive the exponential Poisson expansion from the autonomous generator. Explain total-rate normalization, unitality and Hilbert–Schmidt self-adjointness.

**Dependencies and story role:** M02–M03. This connects dynamics with trajectories.

**Conceptual connection:** Holding total rate fixed prevents a third primitive from silently speeding the clock.

**Source pointers:** Watrous §2.2; [bridge §3](WATROUS_BRIDGE.md#3-from-reflection-noise-to-a-channel-and-its-dilation); [pair §1](../science/pair-simulation.md#1-model-and-exact-poisson-expansion).

### M10 — Dilation and output choice

**Central question:** Why is the coherent field different from a measured jump record or final system?

**Understanding target:** Use a Stinespring isometry to identify its two marginal channels. Explain why microscopic jump phases and an oracle-independent physical encoding are needed for the field.

**Dependencies and story role:** M03–M05, M09. This establishes the transfer boundary between sisters.

**Conceptual connection:** Partial trace changes which trajectory overlaps are observable.

**Source pointers:** Watrous §2.2; [field contract](../science/field-output.md#fixed-microscopic-target).

### M11 — Probability and parity as proof tools

**Central question:** How can walk estimates and a query lower bound constrain a simulator?

**Understanding target:** Distinguish jump count, endpoint, mean, variance and tail probability. Explain the degree-at-most-twice-the-queries rule and why lower degree cannot correlate with all-bit parity.

**Dependencies and story role:** M06–M09. These are the project-supplied tools beyond the anchor.

**Conceptual connection:** A physical output that reliably exposes parity converts simulation into a hard computation.

**Source pointers:** Watrous Chapter 1 for probability; [bridge §7](WATROUS_BRIDGE.md#7-tree-parity-for-the-system); [parity proof](../science/lower-bounds.md#55-applying-the-quantum-parity-bound).

### M12 — Background synthesis: two precise tasks

**Central question:** What must be fixed before a system/field comparison is meaningful?

**Understanding target:** Assemble reflection access, rates, phases, input/reference, requested marginal, encoding, error convention and serial query cap. Distinguish universal algorithms from finite-dimensional hard families.

**Dependencies and story role:** M01–M11. This joins all local definitions into the full contract.

**Conceptual connection:** Matching words and exponents do not identify channels with different retained outputs.

**Source pointers:** Watrous §§2.2, 3.3; [model](../science/model-and-results.md); [field contract](../science/field-output.md#fixed-microscopic-target).

## Phase II — Narrative/innovation

### M13 — One reflection leaves parity

**Central question:** Why can a long single-reflection history cost one query?

**Understanding target:** Reduce powers to even/odd parity and derive the known identity/reflection mixture. Explain its coherent two-fiber version and separate the known field preparation cost.

**Dependencies and story role:** M02–M04, M09–M12. This is a complete first endpoint of the hierarchy.

**Conceptual connection:** Many clock rings need not represent many distinct net operations.

**Source pointers:** Watrous §2.2; [bridge §5](WATROUS_BRIDGE.md#5-one-reflection-then-every-pair); [one-reflection proof](../science/lower-bounds.md#3-a-constant-lower-bound-including-one-reflection).

### M14 — Every pair has line geometry

**Central question:** Why do noncommuting reflections still have a universal short-word description?

**Understanding target:** Reduce a two-letter word to an alternating word and assign its signed line endpoint. Explain why additional matrix relations can ease instances without invalidating this representation.

**Dependencies and story role:** M02, M09, M13. This identifies the pair’s compression mechanism.

**Conceptual connection:** The abstract cancellation graph is a line even when the actual matrices have unknown extra identities.

**Source pointers:** Watrous Chapter 1; [pair §2](../science/pair-simulation.md#2-the-reduced-word-is-a-walk-on-a-line).

### M15 — An endpoint law becomes an exact channel

**Central question:** What distribution applies the correct random operation?

**Understanding target:** Identify the symmetric Skellam endpoint probabilities and variance t. Explain why the reduced-word mixture equals the full semigroup before approximation.

**Dependencies and story role:** M03, M09, M11, M14. This turns geometry into a physical identity.

**Conceptual connection:** The equality is at the operator/channel level and therefore includes arbitrary references.

**Source pointers:** Watrous §2.2; [pair §3](../science/pair-simulation.md#3-exact-endpoint-law-and-exact-channel-identity).

### M16 — Tails become a deterministic query cap

**Central question:** How is an unbounded random history replaced by a valid bounded algorithm?

**Understanding target:** Use an endpoint tail bound and assign an ordinary legal channel to the tail. Compare probability-proportional system error with square-root coherent truncation error.

**Dependencies and story role:** M04, M07, M10–M11, M15. This converts concentration into a branchwise guarantee.

**Conceptual connection:** The output’s retained coherence determines the tail-to-error conversion.

**Source pointers:** Watrous §§3.2–3.3; [pair §4](../science/pair-simulation.md#4-a-hard-query-cap-for-arbitrary-accuracy); [bridge §4](WATROUS_BRIDGE.md#4-error-as-an-operational-guarantee).

### M17 — Sample without generating the history

**Central question:** How can the system pair speedup survive classical preprocessing?

**Understanding target:** Explain cyclic endpoint aliasing, Fourier probabilities and a finite table. Show why this avoids a loop over the original Poisson count.

**Dependencies and story role:** M07, M11, M15–M16. This removes a hidden linear sampling cost.

**Conceptual connection:** A short applied word alone would not imply a short end-to-end system algorithm.

**Source pointers:** Watrous Chapter 1 for probability; [sampling §§2–3](../science/sampling-and-resources.md#2-a-finite-cyclic-endpoint-distribution).

### M18 — Approximate arithmetic and exact CPTP output

**Central question:** Why does finite arithmetic still describe a legal simulation?

**Understanding target:** Track certified elementary approximations, integer FFT error, clipping, normalization and dyadic rounding. Distinguish exact physical validity of each mixture from its certified approximation error.

**Dependencies and story role:** M03–M04, M16–M17. This completes the production sampler.

**Conceptual connection:** Nonnegative normalized weights make a physical channel even before its accuracy is assessed.

**Source pointers:** Watrous §2.2; [sampling §§4–5](../science/sampling-and-resources.md#4-error-of-the-integer-fft).

### M19 — Complete pair resource accounting

**Central question:** Which pair algorithm is cheap for which output?

**Understanding target:** Combine sampling, word application, precision and storage costs for system output. Explain why a coherent field algorithm uncomputes endpoint workspace and may still write order-t output slots.

**Dependencies and story role:** M07, M10, M14–M18. This joins the mechanism and its implementation limits.

**Conceptual connection:** A classical endpoint sample and a coherent trajectory state have different output obligations.

**Source pointers:** Watrous §§2.2, 3.3; [sampling §§7–8](../science/sampling-and-resources.md#7-classical-time-precision-and-memory); [field resources](../science/field-output.md#separate-query-encoding-and-output-costs).

### M20 — Nearby qubit oracles leave a finite system signal

**Central question:** How does a small axis perturbation yield square-root hardness?

**Understanding target:** Use the slow qubit decay mode at angle $`\theta=t^{-1/2}`$. Relate its constant final-system signal to the small controlled-oracle separation.

**Dependencies and story role:** M08, M12, M15. This supplies a converse independent of the sampled algorithm.

**Conceptual connection:** Finite output distinguishability converts a small oracle perturbation into a many-query requirement.

**Source pointers:** Watrous §§3.1, 3.3; [system pair lower bound](../science/lower-bounds.md#4-two-reflections-a-qubit-witness-for-square-root-time).

### M21 — Pair synthesis: universality and optimality

**Central question:** What makes the square-root system classification sharp?

**Understanding target:** Combine the universal channel algorithm and qubit hybrid witness. Retain fixed error, branchwise cap, all-input guarantee and nonquery resource accounting.

**Dependencies and story role:** M12, M16, M19–M20. This integrates the pair narrative.

**Conceptual connection:** An upper bound for all dimensions and one legal qubit lower family settle the same worst-case exponent.

**Source pointers:** Watrous §3.3; [model theorem](../science/model-and-results.md#3-the-query-threshold); [interpretation §2](../science/interpretation.md#2-the-line-behind-every-pair).

### M22 — A third color permits outward motion

**Central question:** Why can reversible local moves propagate linearly far?

**Understanding target:** Read the three-color reduced-word tree and explain its two outward/one inward choices. Distinguish reversibility of edges from zero radial drift.

**Dependencies and story role:** M11, M14. This identifies the geometric change behind hardness.

**Conceptual connection:** Branching creates a long outward transient without directed target control or reset.

**Source pointers:** Watrous Chapter 1; [interpretation §3](../science/interpretation.md#3-reversible-motion-can-move-outward).

### M23 — A finite legal parity-carrying triple

**Central question:** How are hidden bits placed in genuine reflection oracles?

**Understanding target:** Define finite-tree colored edge swaps with symmetric depth-bit XORs and identity missing-edge actions. Verify involution, Hermiticity and the prefix-parity endpoint invariant.

**Dependencies and story role:** M02, M06, M11, M22. This builds the legal system hard family.

**Conceptual connection:** Backtracking cancels edge bits, so all paths reaching one vertex carry the same prefix parity.

**Source pointers:** Watrous Chapter 1; [tree construction §§5.1–5.2](../science/lower-bounds.md#51-the-finite-graph-and-its-reflections).

### M24 — Compile the strongest coherent access

**Central question:** Does the reduction preserve controlled SELECT on all branches?

**Understanding target:** Follow the exact two-bit-query implementation, including external controls, inactive addresses and buffer erasure. Explain why symmetric edge attributes permit cleanup after moving.

**Dependencies and story role:** M05–M06, M23. This closes the access gap before using parity hardness.

**Conceptual connection:** A clean full oracle compiler is stronger than matching its action on classical visited vertices.

**Source pointers:** Watrous §2.2; [compiler §5.4](../science/lower-bounds.md#54-compiling-a-controlled-select-into-two-ordinary-bit-queries).

### M25 — Reach enough bits inside a finite tree

**Central question:** How does the parity-carrying motion obtain a uniform success estimate?

**Understanding target:** Use radial domination by a Poisson difference with mean t/3 and variance t. Combine the shallow-depth estimate with the finite outer-boundary tail in the system construction.

**Dependencies and story role:** M09, M11, M22–M23. This quantifies the useful outward transient.

**Conceptual connection:** Positive drift alone is insufficient; finite bounds ensure a constant probability of carrying linearly many bits.

**Source pointers:** Watrous Chapter 1 for probability; [finite-time estimate](../science/lower-bounds.md#53-a-uniform-finite-time-success-estimate).

### M26 — Close the system parity reduction

**Central question:** Why can every accurate system simulator compute parity?

**Understanding target:** Measure depth and answer, handle shallow outcomes by a fair guess, and include channel approximation error. Combine the two-query compiler with the parity degree bound and retain the exponential dimension qualification.

**Dependencies and story role:** M04, M11, M23–M25. This completes the system linear lower bound.

**Conceptual connection:** The dimension-uniform lower family may grow with t; no fixed-dimension or locality theorem follows.

**Source pointers:** Watrous §§3.1, 3.3; [parity reduction](../science/lower-bounds.md#55-applying-the-quantum-parity-bound); [dimension](../science/lower-bounds.md#6-dimension-controls-and-the-scope-of-the-reduction).

### M27 — Trace the system and test the failed transfer

**Central question:** Why does the original hard tree have an easy-to-distinguish system but a field-blind root witness?

**Understanding target:** Construct the depth-prefix coordinate change and show that it fixes the input while acting only on the final system. Conclude exact bit independence of the retained field for this witness.

**Dependencies and story role:** M10, M23, M26. This tests the most vulnerable cross-project implication.

**Conceptual connection:** Partial trace removes the gauge dependence; a system measurement cannot be reused as a field observable.

**Source pointers:** Watrous §2.2; [failed-transfer identity](../science/field-output.md#why-the-original-system-parity-witness-does-not-transfer).

### M28 — The pair writes a dark-port field signal

**Central question:** How can two qubit reflections remain hard after discarding the system?

**Understanding target:** Use symmetric tilted reflections and a fixed bath beamsplitter. Derive the dark Poisson mean $`t\sin^2\theta`$ and identify the constant gap at $`\theta=t^{-1/2}`$.

**Dependencies and story role:** M08, M10, M20, M27. This supplies a genuinely retained field witness.

**Conceptual connection:** Number-conserving bath interference reveals oracle information absent from original-bath count records.

**Source pointers:** Watrous §3.1; [field pair witness](../science/field-output.md#a-qubit-field-witness-for-the-pair).

### M29 — Leaf loops transfer full parity to the coherent field

**Central question:** How can a triple repair the failed root-field witness?

**Understanding target:** Replace missing leaf transitions by known Z at depth $`\lfloor t/48\rfloor`$. Follow the surviving full-parity loop sign, the leaf-occupation overlap bound, unchanged two-query compiler and loss under total-number dephasing.

**Dependencies and story role:** M10–M11, M24–M27. This establishes the separate field linear obstruction and its phase boundary.

**Conceptual connection:** A coordinate change now leaves a field-observable loop phase; the output’s photon-number coherence is load-bearing.

**Source pointers:** Watrous §§2.2, 3.1–3.2; [field triple](../science/field-output.md#three-reflections-can-write-parity-into-the-field); [sister proof](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding/blob/56295fc4db2a35521792d43c62231bce756e538d/science/reflection_tree.md).

### M30 — Global synthesis: geometry, retained information and resources

**Central question:** What does the joint system/field account establish?

**Understanding target:** Assemble both constant/square-root/linear classifications with their precise output, error, oracle, phase and dimension conventions. Credit the routine coherent upper lift and inherited parity scaffold, locate the field-only additions, and keep encoding/output work separate.

**Dependencies and story role:** M12–M13, M19, M21, M26–M29. This integrates the whole story and its limitations.

**Conceptual connection:** Shared word geometry controls upper cost while the retained information determines which lower witness is valid.

**Source pointers:** Watrous §§2.2, 3.3; [model](../science/model-and-results.md); [field consequence](../science/field-output.md); [related work](../references/related-work.md).
