#!/usr/bin/env python3
"""Link optional individual-record templates to a separately published master DOI."""

from pathlib import Path
import json
import re
import sys


if len(sys.argv) != 2:
    raise SystemExit("usage: apply_master_doi.py 10.5281/zenodo.XXXXXXX")
doi = sys.argv[1].strip()
if not re.fullmatch(r"10\.5281/zenodo\.\d+", doi):
    raise SystemExit("expected a Zenodo DOI in the form 10.5281/zenodo.XXXXXXX")

root = Path(__file__).resolve().parents[1]
master_path = root / "zenodo/master_record_metadata.json"
master = json.loads(master_path.read_text(encoding="utf-8"))
master["doi"] = doi
master_path.write_text(
    json.dumps(master, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)

for path in sorted((root / "submissions").glob("*/*_metadata.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    data["related_master_release"] = doi
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

for path in sorted((root / "zenodo/individual_records").glob("*_zenodo_metadata.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    related = [
        item
        for item in data.get("related_identifiers", [])
        if item.get("relation") != "isPartOf"
    ]
    related.append({"identifier": doi, "relation": "isPartOf", "scheme": "doi"})
    data["related_identifiers"] = related
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

print(doi)
print("Run scripts/rebuild_release_artifacts.py before committing or uploading.")
