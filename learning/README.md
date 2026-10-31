# Learning the dephasing threshold

One reflection reduces a long jump history to its parity. Two reflections reduce it to a position on a line. Three can generate an outward-moving history on a tree. Understanding why these descriptions give different simulation costs requires connecting quantum channels, probability and oracle lower bounds.

The single educational anchor is **Andrew M. Childs, *Lecture Notes on Quantum Algorithms*, 17 April 2025**, available from the [author's page](https://www.cs.umd.edu/~amchilds/qa/qa.pdf). Its query-complexity and simulation chapters provide the main algorithmic foundations. The project supplies the additional connections in the [Childs bridge](CHILDS_BRIDGE.md).

| Reading purpose | Route |
|---|---|
| Connect the anchor's definitions and methods to this model | [Source-to-project bridge](CHILDS_BRIDGE.md) |
| Follow the full understanding route and its dependencies | [Exactly 30 milestones](MILESTONES.md) |
| Inspect the precise statement, quantifiers and error convention | [Model and results](../science/model-and-results.md) |
| Read complete proofs in their canonical order | [Scientific reading route](../science/README.md) |
| Reproduce the specified finite checks and inspect their limits | [Verification](../verification/README.md) |

The milestone map allocates M01–M12 to background/preliminaries and M13–M30 to narrative/innovation. Each develops local objects and mechanisms into a global account of the question or result. Its central questions, understanding targets, dependencies and references are defined by the science and are common to every reader. The bridge and the cited anchor sections can be used alongside a relevant milestone; reading the whole source first is unnecessary.

The scientific pages own the exact claims and detailed derivations. Throughout the learning route, the target remains a full trace-preserving channel on arbitrary input with a reference, and queries are capped on every branch. The two-reflection lower bound already has a qubit witness; the three-reflection lower-bound family has a dimension that grows exponentially with time. These distinctions connect the conceptual picture to the theorem actually proved.
