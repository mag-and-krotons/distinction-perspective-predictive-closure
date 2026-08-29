# RELEASE-WIDE HOLD — DO NOT PUBLISH OR DEPOSIT

The current release is blocked pending a paper-by-paper scientific-content and reproducibility rebuild.

P02 has a confirmed missing-numerical-instrument defect, but it is not an isolated failure. The release-wide audit found blocking defects in every research-paper package P00–P17. A00 is retained only as an archive/navigation object.

## Global blockers

1. Bibliographies are present but claim-level in-text citations are absent across the paper set.
2. No pinned, reproducible software environment is supplied for the numerical packages.
3. The release verifier checks compilation, layout, hashes, ZIP integrity, and selected finite outputs; it does not establish scientific completeness.
4. Several numerical verifiers begin from already reported output constants instead of raw inputs.
5. Multiple papers omit the data, matrices, proof artifacts, covariance status, preprocessing, or complete code needed by their claims.
6. Zenodo metadata still contains unresolved placeholders and unsuitable record-type assumptions.
7. The repository and bound-volume language overstate completeness and reproducibility.

## Disposition

- P00–P17: **BLOCKED**
- A00: **ARCHIVE ONLY**
- GitHub release: **BLOCKED**
- Zenodo deposit/update: **BLOCKED**
- Journal/arXiv submission packages: **BLOCKED**

The detailed readiness matrix and evidence-gated rebuild sequence are in `AUDIT/` on this branch.
