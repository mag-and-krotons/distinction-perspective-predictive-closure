# Release 8.0.2

Release 8.0.2 is an integrity and publication-workflow correction. It does not
alter the scientific claims, theorem statements, proofs, figures, or reported
computational results of release 8.0.1.

## Corrections

- Rebuilt all checksum ledgers and the package manifest from Git-canonical LF
  bytes so that a fresh clone verifies identically to the release ZIP.
- Extended the release verifier to validate the root ledger, package manifest,
  release-asset ledger, and all individual-submission ledgers.
- Added the clean-environment dependencies required by the verification
  workflow.
- Removed unresolved DOI strings from frozen publication metadata. Zenodo
  assigns the DOI after archiving the linked Git release.
- Repaired stale staging paths and documented the existing Zenodo--Git
  integration as the publication route.
- Replaced literal equation placeholders in individual-record descriptions
  with readable mathematical text.
- Kept every manuscript and combined-volume page byte-for-byte unchanged; the
  external citation and Zenodo metadata remain authoritative.
- Recreated the public Git history with a GitHub no-reply identity; no personal
  email address occurs in commit or tag metadata.

## Preserved scope

- Sole author: Abhijit Singh; no affiliation is asserted.
- Nineteen independently packaged paper/atlas units.
- Two hundred-page combined series.
- Nine-state, thirty-six-relation prime-observer theorem and executable audit.
- Raw handwritten research notes remain outside every manuscript, source
  package, public Git object, release asset, and Zenodo upload.

## Publication rule

Publish the annotated tag `v8.0.2`. Do not move or reuse `v8.0.1`.
