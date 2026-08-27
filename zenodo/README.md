# Zenodo publication preparation

## Linked GitHub source record

The GitHub account is already connected to Zenodo. Publish tag `v8.0.2` in the
repository already enabled in that integration; Zenodo then archives the
release and assigns its DOI. `.zenodo.json` is the authoritative metadata for
this source/reproducibility record.

Do not create a duplicate connection or move a published tag.

## Optional master research record

The external folder `Abhijit_Singh_Zenodo_Upload_v8_0_2` contains the six-file
manual upload set:

1. complete repository ZIP;
2. combined paper-series PDF;
3. master scientific atlas PDF;
4. portable Git bundle;
5. `ZENODO_SHA256SUMS.txt`, covering the other five files;
6. master metadata JSON.

`master_record_metadata.json` is a manual-UI template, not a direct API request
body. It represents a separate research record and should be cross-linked to
the source record only after both identifiers exist.

## Optional individual records

Each archive under `submissions/` contains one independent manuscript, clean
source, abstract, metadata, and checksums. Matching manual-entry metadata is
under `zenodo/individual_records/`. An individual record receives its own DOI;
the master DOI is only an `isPartOf` relation.
