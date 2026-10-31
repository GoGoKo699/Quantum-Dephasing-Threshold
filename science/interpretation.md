# Why two reflections differ from three

The threshold comes from the geometry of reduced reflection words. For one supplied reflection, only the parity of its number of applications matters. For two, cancelling adjacent repeated letters leaves a word indexed by a point on a line. For three, the same cancellation rule allows a branching tree. Diffusive displacement on the line permits square-root compression; outward motion on a tree can carry a linearly long parity computation.

## 1. A dephasing process with a simple endpoint

Write a reflection as $`R=P_+-P_-`$, where $`P_+`$ and $`P_-`$ are its orthogonal spectral projectors. For the single-reflection generator, the diagonal blocks $`P_\pm\rho P_\pm`$ remain unchanged and the off-diagonal blocks are multiplied by $`e^{-2t}`$. The exact channel can therefore be implemented by choosing between the identity and one reflection with a known scalar probability.

The clock may ring many times, but those rings do not create many distinct net operations. This observation is already present in the related reflection-noise work cited in [Related work](../references/related-work.md). It supplies the one-primitive endpoint of the classification.

## 2. The line behind every pair

For a pair $`A,B`$, the only universally available relations are $`A^2=B^2=I`$. Every word reduces to an alternating word. The abstract group with these relations has a Cayley graph that is an infinite line. Independent, equally likely reflection choices therefore induce a symmetric random walk on that line, even when the actual matrices satisfy additional relations.

Additional relations can identify endpoints and make an instance easier. They do not invalidate the universal sampler: each sampled abstract word is still a well-defined product of the supplied matrices. After a rate-one Poisson number of steps, the signed endpoint has variance $`t`$. A bounded-length approximation therefore needs order $`\sqrt t`$ reflection applications at fixed error.

The algorithm uses an exact channel identity before truncation. It does not observe the target state, choose a favorable input, or discard a failed branch. Its classical random choice is made independently of the input, and its channel guarantee includes entanglement with any reference. The direct sampler in [Sampling and resources](sampling-and-resources.md) avoids spending order $`t`$ classical work on the original trajectory.

## 3. Reversible motion can move outward

With three involutions, reduced words form a three-regular tree before a finite boundary is imposed. Away from the root, two edge colors move outward and one moves inward. Each edge move is reversible, but the distance from the root has a positive drift. This is a geometric counting effect: there are more outward choices than inward choices.

The hard family labels every edge between depths $`\ell-1`$ and $`\ell`$ with the same input bit $`x_\ell`$. Moving across that edge flips an answer qubit by the bit. Backtracking flips it again and cancels. The answer at any vertex is therefore the parity of the bits up to its depth. At time proportional to the number of input bits, the endpoint reaches the required depth with constant probability.

This construction is still an autonomous, unital, Hilbert–Schmidt self-adjoint quantum semigroup. Its finite classical vertex walk is reversible with respect to the uniform distribution; boundary self-loops preserve symmetry. The lower bound requires neither an absorbing directed shift nor external resets of the target. The actual proof in [Lower bounds](lower-bounds.md) reduces every allowed controlled reflection query to two standard bit queries, so it applies to general coherent simulation strategies.

The tree has exponentially many vertices in its radius. That growth supports the long outward transient and is reflected in the $`\exp(\Theta(t))`$ system dimension. The result concerns the dimension-uniform worst case; it does not establish linear long-time hardness for a fixed finite system.

## 4. Representation and resource boundaries

Several distinctions are necessary when applying the theorem:

| Feature | Meaning for this result |
|---|---|
| Supplied primitive count | Counts the reflection interfaces that the simulator receives; it is not an intrinsic GKSL rank |
| Total jump rate | Fixed at one, so adding a primitive does not silently increase the overall clock rate |
| Target evolution | Autonomous sum of reflection conjugation generators; no interleaved target control |
| Simulation algorithm | May use known gates, ancillas, coherent controls, measurements and randomness |
| Output | Full CPTP channel on arbitrary inputs and references, with unhalved diamond error |
| Charged resource | Serial unknown-oracle calls; implementation costs are stated separately |
| Hard-system size | A qubit for the pair lower bound; a growing system for the three-reflection lower bound |

A physical implementation must still build the reflections. If one call costs $`G`$ gates, applying a sampled word of length $`Q`$ costs at least the corresponding $`QG`$ gate work, in addition to control and sampling. The theorem neither supplies a free matrix description nor converts a nonlocal reflection into a local gate.

Likewise, a classical Markov-chain amplitude state is a different output object. The normalized vector proportional to a walk distribution's amplitudes is not the physical mixture generated by the channel. Existing reversible-chain fast-forwarding results retain their normalization costs and do not automatically supply a full channel simulator. [Related work](../references/related-work.md) makes this comparison at the level of the published output and resource contracts.

## 5. Consequence and remaining questions

An arbitrary pair of binary dephasing primitives admits universal sublinear query growth, even when the reflections do not commute. A triple need not. The sharp distinction is therefore a property of combining supplied noise primitives, with their total rate fixed.

The present theorem leaves several natural parameters open: a dimension-dependent sharp law for triples, additional spatial-locality restrictions, and optimal joint dependence on time and very small error. The proofs settle the stated fixed-error, dimension-uniform classification without assuming answers to those extensions.
