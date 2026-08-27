# Zenodo and Git release guide

## 1. Use the existing integration

The GitHub account is already linked with Zenodo. Do not reconnect it. Confirm
the exact enabled repository, apply its public URL with
`scripts/apply_repository_url.py`, and preserve that repository identity across
the release.

## 2. Verify before pushing

```bash
python scripts/prepare_v8_0_2_metadata.py
python scripts/rebuild_release_artifacts.py
python scripts/verify_release.py
```

Inspect the first-page contact sheet and PDF preflight report. The verifier
checks scientific inventory, source separation, nested archives, every
checksum ledger, and the package manifest.

## 3. Push the corrected Git release

Push the verified `main` branch and annotated tag `v8.0.2` to the repository
already enabled in Zenodo. The tag-triggered `publish-release` workflow verifies
the immutable tree and creates the GitHub release from that tag.
Do not reuse or move `v8.0.1`.

Attach:

1. complete repository ZIP;
2. portable Git bundle;
3. combined paper-series PDF;
4. master scientific atlas PDF;
5. individual submission-package collection;
6. external `SHA256SUMS.txt` covering the GitHub release attachments.

## 4. Let Zenodo archive the GitHub release

The existing integration should archive the GitHub release and assign the DOI.
Verify the Zenodo record against `.zenodo.json`: title, sole creator Abhijit
Singh, version 8.0.2, open access, CC BY 4.0 record license, files, repository
URL, and DOI. Project-created code remains additionally available under MIT as
declared in `LICENSES/README.md`.

Because Zenodo assigns the DOI after archiving, the immutable `v8.0.2` tag does
not contain its own DOI. If a source back-reference is desired, use
`scripts/apply_doi.py` in a later patch release.

## 5. Optional separate research records

The manual-entry template `zenodo/master_record_metadata.json` and the nineteen
individual templates are optional follow-on records, distinct from the linked
software/source archive. After a master DOI exists, use
`scripts/apply_master_doi.py` to populate only the parent relations, rebuild the
archives and ledgers, and publish each paper with its matching ZIP.
