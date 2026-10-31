# Scientific reading route

The question is how the number of supplied binary dephasing primitives changes the worst-case cost of simulating their autonomous sum. At fixed total jump rate and fixed diamond-norm error, one reflection costs constant queries, every pair admits square-root scaling, and three can force linear scaling.

| Question | Canonical page |
|---|---|
| What is the exact channel, oracle model and theorem? | [Model and results](model-and-results.md) |
| Why can every pair be compressed? | [Pair simulation](pair-simulation.md) |
| How is the endpoint sampled without generating a linear-length trajectory? | [Sampling and resources](sampling-and-resources.md) |
| Why can arbitrary coherent algorithms do no better in the worst case? | [Lower bounds](lower-bounds.md) |
| What causes the threshold, and what are its physical limits? | [Interpretation](interpretation.md) |
| Which ingredients and comparison results are prior work? | [Related work](../references/related-work.md) |
| Which finite calculations can be reproduced? | [Verification](../verification/README.md) |

Read the model before the proofs: the count is the number of supplied reflection oracles, the simulation target is a full trace-preserving channel, and the three-reflection hard family has dimension exponential in time. The lower bounds permit coherent selection, ancillas, randomness and adaptive control. The implementation pages separately account for classical preprocessing, randomness, oracle precision and workspace.
