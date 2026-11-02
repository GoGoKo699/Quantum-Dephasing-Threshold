# Quantum Dephasing Threshold

**How does combining binary dephasing processes change the cost of quantum simulation?** At fixed total jump rate and fixed channel error, one supplied reflection costs constant queries, every pair admits square-root scaling, and three can require linear scaling.

The generator is

```math
\mathcal L_k=\frac1k\sum_{j=1}^{k}
\bigl(\mathrm{Ad}_{R_j}-\mathrm{Id}\bigr),
\qquad R_j=R_j^\dagger,
\qquad R_j^2=I.
```

Here $`\mathrm{Ad}_{R_j}(\rho)=R_j\rho R_j`$. The task is to implement the full channel $`e^{t\mathcal L_k}`$ on arbitrary inputs and reference systems. For fixed unhalved diamond error $`\epsilon=1/100`$ and real $`t\ge1`$, its dimension-uniform worst-case serial query cost is

```math
Q_1(t)=1,\qquad
Q_2(t)=\Theta(\sqrt t),\qquad
Q_3(t)=\Theta(t).
```

| Supplied reflections | Mechanism | Scope of the matching lower bound |
|---|---|---|
| One | Sample the parity of the jump count | A qubit already needs one query |
| Two | Reduce the random word to an endpoint on a line | A qubit gives square-root hardness |
| Three | Branching trajectories can carry a long parity computation | The hard family uses dimension $`\exp(\Theta(t))`$ |

The count is the number of **supplied reflection primitives**, not an intrinsic Lindblad rank. The three-reflection result concerns a growing system and does not establish linear long-time hardness at fixed dimension. All target generators are autonomous, unital and Hilbert–Schmidt self-adjoint. The lower bounds allow general coherent and adaptive simulation algorithms, including controlled SELECT access.

## Sister result: the coherent output field

**[Quantum Environment Fast Forwarding](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding) is this project's sister.** Here the authoritative result concerns the reduced system; there the specified vacuum field is retained after discarding that system. The same one/two/three-reflection query hierarchy holds for the coherent field, with new field-only lower-bound witnesses. This repository owns the reflection-word geometry and original branching parity scaffold; the sister owns the field theorem and its proof.

The [self-contained field consequence](science/field-output.md) fixes phases, rates, oracle access, physical embedding and error conventions. It explains why the original system parity witness is exactly field-blind, how known leaf-$`Z`$ loops repair that failure, and why the new triple witness loses its signal under total-photon-number dephasing. The pair's dark-port count witness survives that dephasing. Separate field encoding and output work remain charged.

## Read the science

Start with [Model and results](science/model-and-results.md) for the exact oracle, error and quantifier conventions. Then follow the question that interests you:

| Reader's question | Route |
|---|---|
| Why is every pair simulable in square-root time? | [Pair simulation](science/pair-simulation.md) |
| Is linear classical trajectory generation hidden in that speedup? | [Direct sampling and resource accounting](science/sampling-and-resources.md) |
| Why can coherent algorithms not evade the converse bounds? | [Lower bounds](science/lower-bounds.md) |
| What changes when the system is discarded and the field is retained? | [Coherent field consequence](science/field-output.md) |
| What causes the difference between two and three? | [Physical and algorithmic interpretation](science/interpretation.md) |
| What is inherited from earlier work? | [Related work](references/related-work.md) and [bibliography](references/references.bib) |
| Where is the complete connected account? | [Scientific reading route](science/README.md) |

The one-reflection endpoint, Poisson trajectories and parity lower-bound method are established ingredients. The contribution studied here is the universal pair algorithm together with a linear obstruction using only three autonomous reflection types. The related-work account compares exact access models, output requirements, dimensions and source versions.

## Learn the project

The common educational anchor for both sisters is **John Watrous, [*The Theory of Quantum Information* (2018 author draft)](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)**. The [Watrous bridge](learning/WATROUS_BRIDGE.md) connects channels, dilations, reference-preserving distance and distinguishability to this project's reflection geometry, certified sampler and parity reductions. It also explains the extra work needed to compare system and field outputs.

The [30-milestone map](learning/MILESTONES.md) develops the project's understanding targets through background/preliminaries and narrative/innovation. It is a common scientific route, with explicit dependencies and source pointers. The [learning entrypoint](learning/README.md) explains how to use the bridge and map alongside the authoritative proof pages.

## Reproduce the finite checks

From the repository root, install the pinned numerical dependencies and run:

```bash
python -m pip install -r verification/requirements.txt
python verification/run_all.py
```

The suite checks reduced words and direct endpoint sampling, compares small full-channel matrices, verifies the exact qubit signal, and tests finite-tree parity and radial-motion identities. The certified sampler itself uses Python's standard library and integer arithmetic; NumPy and SciPy are used for independent numerical diagnostics. The new field-only diagnostics are maintained with the [sister field proof](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding/blob/main/verification/README.md), separately from this system suite. See [Verification](verification/README.md) for requirements, output, tested cases and the distinction between finite checks and analytic proof.

## Resource boundaries

The headline theorem counts serial unknown-oracle calls with a maximum on every branch. Classical preprocessing, random bits, workspace, time representation and approximate oracle synthesis are discussed separately. A supplied reflection can be a costly physical operation; the theorem makes no free-data-loading or spatial-locality assumption and does not claim a hardware runtime advantage. The fixed-error law also leaves optimal joint time-and-precision dependence open.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
