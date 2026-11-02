# The reflection threshold with coherent field output

The sister project [Quantum Environment Fast Forwarding](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding) studies the field emitted by a specified vacuum dilation. Combining its output contract with the reflection-word geometry here gives the same worst-case constant/square-root/linear hierarchy. The lower bounds need field measurements: a measurement on the final system cannot establish hardness after that system has been discarded.

This page states the complete receiving model, consequence and proof mechanisms. The sister repository owns the [authoritative field theorem](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding/blob/7ccf8fb54418b90a1142499472af81540946609e/science/reflection_threshold.md), [pair witness](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding/blob/7ccf8fb54418b90a1142499472af81540946609e/science/reflection_pair.md) and [three-reflection proof](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding/blob/7ccf8fb54418b90a1142499472af81540946609e/science/reflection_tree.md). This repository owns the [reduced-word geometry](pair-simulation.md), [system theorem](model-and-results.md) and original [tree parity construction](lower-bounds.md).

## Fixed microscopic target

Take the supplied Hermitian involutions $`R_j`$ with exactly specified jumps

```math
L_j=R_j/\sqrt{k},\qquad j=1,\ldots,k,\qquad H=0.
```

Every rate is $`1/k`$, so the total rate is one. Use vacuum in each labelled bosonic field, identity Hudson–Parthasarathy scattering, and the displayed positive real coupling coefficient. These phases are part of the task: multiplying a jump by a phase preserves its reduced generator but changes the emitted field.

The phase-referenced controlled SELECT oracle is the same interface as in [the system model](model-and-results.md#2-access-output-and-error). Its inverse is identical because the primitives are involutions. Queries count serial calls with a cap on every branch; no supplied matrix description, power oracle, QRAM or free decoder is assumed.

Let $`\mathcal F_t`$ be the full labelled output Fock space. For a chronological word $`w=(j_1,\ldots,j_N)`$, fix the normalized physical field ket

```math
|N,w\rangle_{\mathcal F}
=\sqrt{N!/t^N}\int_{0\lt s_1\lt\cdots\lt s_N\lt t}
|s_1,j_1;\ldots;s_N,j_N\rangle\,d^N\mathbf s.
```

Different count/word labels are orthonormal. The embedding is independent of the unknown reflections and has no time-grid approximation. It generally does not factor into separate bath registers; deleting bath labels from a word register is not a physical partial trace.

The exact vacuum isometry and the requested field channel are

```math
\begin{aligned}
V_t|\psi\rangle
&=\sum_{N=0}^{\infty}\sum_{w\in[k]^N}
\sqrt{e^{-t}t^N/(N!k^N)}\,
R_{j_N}\cdots R_{j_1}|\psi\rangle\otimes|N,w\rangle_{\mathcal F},\\
\Gamma_t(\rho)&=\operatorname{Tr}_S[V_t\rho V_t^\dagger].
\end{aligned}
```

The simulator returns the field, discards the final system, and preserves its correlations with every untouched input reference. For an encoded output with declared isometry $`J_t`$ into this physical field, compare $`J_t\mathcal A(\rho)J_t^\dagger`$ with $`\Gamma_t(\rho)`$. Define the physical output channel $`\widetilde\Gamma_t(\rho)=J_t\mathcal A(\rho)J_t^\dagger`$ and use half diamond error

```math
d_\diamond(\widetilde\Gamma_t,\Gamma_t)
=\tfrac12\|\widetilde\Gamma_t-\Gamma_t\|_\diamond.
```

The system theorem uses unhalved error $`0.01`$; the field theorem below uses half diamond error $`0.1`$. These are distinct fixed-accuracy conventions. Their time exponents agree without identifying the two output channels.

## Field-only classification

At half diamond error $`0.1`$, for real $`t\ge1`$ and a supremum over finite input-system dimensions,

```math
Q^F_1(t)=1,\qquad Q^F_2(t)=\Theta(\sqrt t),\qquad
Q^F_3(t)=\Theta(t).
```

The same exponents hold at smaller fixed error. The pair lower bound needs one qubit; the triple lower bound has dimension $`\exp(\Theta(t))`$. No linear long-time bound at a fixed dimension is proved.

The upper bound is a routine coherent lift of this repository's cancellation identity. Keep the original trajectory amplitudes and labels while applying the reduced operator word. One reflection needs only its parity. For two, the signed endpoint has the Skellam law already derived in [Pair simulation](pair-simulation.md); concentration gives a reduced-word query cap of order $`\sqrt t`$ at fixed error. For three, coherent Poisson-word truncation gives order $`t`$. Measuring the endpoint or discarding reduction garbage would dephase the field and would not implement this upper bound.

## A qubit field witness for the pair

Use two phase-fixed reflections

```math
R_\pm(\theta)=\cos\theta\,Z\pm\sin\theta\,X.
```

A fixed 50:50 mixing of the two bath labels transforms their couplings into $`L_b=\cos\theta Z`$ and $`L_d=\sin\theta X`$. Since $`L_d^\dagger L_d=\sin^2\theta I`$, the dark-port count is exactly Poisson with mean $`t\sin^2\theta`$, independently of the input.

At $`\theta=0`$ the dark port is vacuum. At $`\theta=t^{-1/2}`$ its nonvacuum probability is at least $`1-e^{-\sin^2 1}`$, while the controlled-SELECT distance is at most $`t^{-1/2}`$. The hybrid argument therefore forces $`\Omega(\sqrt t)`$ queries. This measurement keeps only the field and preserves total photon number. Its signal survives dephasing between different total-number sectors. The [full pair proof](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding/blob/7ccf8fb54418b90a1142499472af81540946609e/science/reflection_pair.md) supplies the exact count law and error constants.

## Why the original system parity witness does not transfer

For the original tree construction with identity boundary loops, put

```math
D_x|v,a\rangle
=|v,a\oplus(x_1\oplus\cdots\oplus x_{\min(|v|,m)})\rangle.
```

Then $`R_j^{(x)}=D_xR_j^{(0)}D_x`$, and $`D_x`$ fixes $`|\varnothing,0\rangle`$. Hence

```math
V_t^{(x)}|\varnothing,0\rangle
=(D_x\otimes I_{\mathcal F})V_t^{(0)}|\varnothing,0\rangle.
```

Tracing the final system makes the complete coherent field exactly independent of $`x`$ on this input. The answer measured in the [system proof](lower-bounds.md#52-the-answer-bit-along-every-trajectory) has been discarded. This is an exact failed transfer of that witness, while the original system theorem remains valid.

## Three reflections can write parity into the field

Modify the tree by truncating it at depth $`m=\lfloor t/48\rfloor`$ for $`t\ge48`$. Retain the depth-bit XOR on every non-loop edge, and let each missing leaf-color transition act by the known $`Z`$ on the answer qubit. Each color remains a Hermitian involution, each rate remains $`1/3`$, and no fourth observer is added.

Conjugation by $`D_x`$ removes all edge bits and replaces each leaf loop by $`(-1)^PZ`$, where $`P=x_1\oplus\cdots\oplus x_m`$. From the root with answer zero, a word acquires phase $`(-1)^{P K}`$, with $`K`$ its number of leaf loops. These phases remain in the field after the final system is traced.

The field proof groups words by their known terminal vertex. Conditional on the vertex-moving skeleton, the loop count is Poisson with mean $`(2/3)\ell_t`$, where $`\ell_t`$ is total leaf occupation time. Its field trace-distance calculation gives

```math
D(\rho_F^0,\rho_F^1)
\ge 1-\mathbb E e^{-4\ell_t/3}
\ge\frac{1513}{1936}\frac45(1-e^{-5/3})
=0.5071203359\ldots.
```

The last estimate combines a constant probability of hitting a leaf by $`t-1`$ with its first exponential dwell time. The original two-bit-query controlled-SELECT compiler still works; leaf $`Z`$ costs no input-bit queries. The standard parity lower bound then yields $`q\ge m/4\ge t/384`$. The [authoritative tree proof](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding/blob/7ccf8fb54418b90a1142499472af81540946609e/science/reflection_tree.md) gives the full finite-time estimate and an explicit early-count/late-coherence field measurement.

This triple witness needs the stipulated phase reference. Because $`K\equiv N-|v|\pmod2`$ within an endpoint block, its two parity outputs differ by the total-number phase $`e^{i\pi N_{\mathrm{tot}}}`$. Dephasing between total-photon-number sectors makes them identical. The construction proves no phase-insensitive linear field lower bound.

## Separate query, encoding and output costs

At fixed accuracy an explicit count/word circuit uses $`O(t)`$ chronological output slots. It prepares coherent counts and labels, computes the pair endpoint reversibly, applies the reduced word, and uncomputes that endpoint. Known arithmetic, preparation and gate synthesis are charged separately; a conservative fixed-primitive bound is $`O(t\,\mathrm{polylog}(t/\epsilon))`$ when classical parameter descriptions have polylogarithmic size.

A compressed endpoint-fiber encoding is oracle independent, but declaring it does not supply cheap physical decoding. The physical field still has mean photon number $`t`$ and emission interval $`t`$. Neither the oracle upper bound nor the field measurement eliminates output-writing, optical energy or encoding-conversion work.

The distinct ownership is useful: this project supplies reflection geometry and the original system parity scaffold; its sister supplies the fixed field contract and the new field-only lower bounds. Coherent Poisson preparation, the parity method and the coordinate-change invariance are inherited tools. Reproducible new field diagnostics live with the [field proof and verification](https://github.com/GoGoKo699/Quantum-Environment-Fast-Forwarding/blob/main/verification/README.md); this repository's existing tests continue to check its system theorem and certified sampler.
