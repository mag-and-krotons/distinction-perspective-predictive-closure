# Global Scientific-Readiness Audit — Current Release Lineage

## Decision

The current release lineage is quarantined and blocked from a new Zenodo deposit/update, GitHub release publication, journal submission, and arXiv submission until paper-specific evidence gates are cleared.

P02 is a confirmed reproducibility failure, but it is not the only one. The audit found blockers in every research-paper package P00–P17. A00 is retained only as repository navigation and an archive map.

## Release-wide defects

1. **Claim-level citation failure.** The paper set carries bibliographies without attaching citations to the claims, imported results, data sources, and novelty comparisons they are meant to support.
2. **No pinned reproduction environment.** No complete dependency lock or equivalent environment recipe is present for the numerical work.
3. **Packaging verification was mistaken for scientific verification.** Compilation, A4 conformance, author strings, ZIP integrity, hashes, and selected finite scripts do not prove that a paper contains its required data, matrices, proof artifacts, uncertainty, or complete code path.
4. **Metadata is not ready for archival ingestion.** DOI/repository placeholders, literal equation placeholders, and unsuitable record-type assumptions remain in the release metadata.
5. **Coverage is file-level rather than claim-level.** Assigning a long source document to a paper does not establish that its theorems, derivations, values, corrections, failed routes, and figures were transmitted.
6. **Several verification programs start from final outputs.** Hard-coded eigenvalues, transition matrices, prediction tables, or imposed model values check downstream arithmetic but do not reproduce the result from source inputs.
7. **Paper-specific evidence is missing or mismatched.** Examples include the absent P02 numerical instrument, the missing P03 full test corpus, the absent P07 chain-complex computation, the incomplete P10 empirical pipeline, and P16 code that does not implement the architecture described.
8. **Readiness language is overstated.** The current README and bound-volume declarations use “complete” and “reproducible” beyond what the supplied evidence establishes.
9. **Mixed-resource provenance and licensing need a fresh file-level audit.** Manuscripts, first-party code, third-party data, and archive metadata cannot be treated as one undifferentiated resource.
10. **Every individual submission package inherits its paper's evidence gap.** A readable ZIP and a compiling PDF do not clear scientific submission.

## Machine findings from the audit

- Research papers blocked: **18/18**
- Atlas disposition: **archive only**
- Paper/atlas units requiring claim-level citation repair: **19/19**
- Individually staged metadata records requiring correction: **19/19**
- Reproducible environment lock: **absent**
- Individual package ZIPs structurally readable: **19/19**, which is a packaging result only

## Clearance rule

A paper clears only when all of the following are true:

1. every imported or prior result is cited at the claim;
2. every paper-internal theorem has a complete proof or exact proof dependency;
3. every numerical result is regenerated from supplied source inputs rather than restated outputs;
4. uncertainty and covariance status are explicit;
5. dependencies and execution commands are pinned;
6. the individual paper package contains the evidence required for its own claims;
7. a field-specific adversarial review has been resolved.

See `AUDIT/PAPER_READINESS_MATRIX.csv` and `AUDIT/REBUILD_SEQUENCE.md`.
