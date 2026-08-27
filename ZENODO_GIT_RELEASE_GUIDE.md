# Zenodo and Git publication guide

## Primary record

The existing GitHub–Zenodo integration archives the complete research release.
The resulting Zenodo record is the primary publication record for the research
series, not a software deposit and not a secondary source-only record.

Before publishing a tag, verify that `.zenodo.json` identifies:

- resource type: **Publication — Other**;
- title: **Distinction, Perspective, and Predictive Closure: Complete Research
  Release 8.0.2**;
- creator: **Abhijit Singh**;
- open access and CC BY 4.0 record licence;
- the GitHub repository as a supporting related resource; and
- a substantive research abstract written in my authorial voice.

## Verification before publication

```bash
python scripts/prepare_v8_0_2_metadata.py
python scripts/rebuild_release_artifacts.py
python scripts/verify_release.py
```

The verifier checks the research inventory, package manifests, checksums,
nested archives, submission packages, and release assets.

## Release assets

The GitHub release contains:

1. the complete repository archive;
2. the portable Git bundle;
3. the complete paper-series PDF;
4. the master scientific atlas PDF;
5. the individual submission-package collection; and
6. the external SHA-256 ledger for those attachments.

## After Zenodo archives the release

Verify the live title, creator, resource type, abstract, version, access,
licence, files, repository relation, and DOI. Zenodo permits published metadata
to be corrected in place without changing the DOI; such a correction should be
used for metadata errors rather than creating a duplicate deposit.

The templates under `zenodo/individual_records/` are reserved for any later,
deliberate decision to publish individual papers with separate DOIs.
