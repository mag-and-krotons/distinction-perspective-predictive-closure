# Immediate release sequence

This release uses the existing Zenodo--GitHub connection. Do not create a
second connection.

1. Identify the exact repository already enabled in the Zenodo GitHub
   integration and confirm that it is the intended research repository.
2. Apply that repository URL once:
   `python scripts/apply_repository_url.py <URL>`.
3. Run `python scripts/prepare_v8_0_2_metadata.py`, followed by
   `python scripts/rebuild_release_artifacts.py`.
4. Run `python scripts/verify_release.py` and inspect
   `verification/FIRST_PAGE_CONTACT_SHEET_V8.png` plus
   `verification/PDF_PREFLIGHT_V8.txt`.
5. Commit the verified tree, create the annotated tag `v8.0.2`, and push
   branch `main` plus that tag to the enabled repository.
6. The tag-triggered `publish-release` workflow verifies the immutable tree,
   builds the repository ZIP, portable Git bundle, combined paper series,
   scientific atlas, individual submission collection, and external checksum
   ledger, then publishes the GitHub release.
7. Allow the existing Zenodo integration to archive the GitHub release. Verify
   the issued DOI, record title, creator, version, license, files, and related
   repository URL before treating publication as complete.
8. A DOI back-reference belongs in a later patch commit; never move the
   already published `v8.0.2` tag.
9. Optional separate master and individual research records use the templates
   under `zenodo/` only after their identifiers are assigned.

For field submission, use one archive under `submissions/`; the bound series is
not a substitute for an individual paper package.

No scientific manuscript is changed by this publication workflow.

## Academic-source separation

Raw handwritten research notes are not part of any academic manuscript, paper
source archive, individual submission package, public release asset, or Zenodo
upload. Only formal typeset exposition, proofs, data, code, and
publication-grade figures are included.
