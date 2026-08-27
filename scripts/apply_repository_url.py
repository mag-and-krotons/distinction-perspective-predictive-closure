#!/usr/bin/env python3
"""Apply one public GitHub repository URL to every release metadata surface."""

from pathlib import Path
import json
import re
import sys

import yaml


if len(sys.argv) != 2:
    raise SystemExit("usage: apply_repository_url.py https://github.com/OWNER/REPOSITORY")
url = sys.argv[1].strip().rstrip("/")
if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+", url):
    raise SystemExit("repository URL must be https://github.com/OWNER/REPOSITORY")

root = Path(__file__).resolve().parents[1]

citation_path = root / "CITATION.cff"
citation = yaml.safe_load(citation_path.read_text(encoding="utf-8")) or {}
citation["repository-code"] = url
citation_path.write_text(
    yaml.safe_dump(citation, sort_keys=False, allow_unicode=True),
    encoding="utf-8",
    newline="\n",
)

codemeta_path = root / "codemeta.json"
codemeta = json.loads(codemeta_path.read_text(encoding="utf-8"))
codemeta["codeRepository"] = url
codemeta_path.write_text(
    json.dumps(codemeta, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)

zenodo_path = root / ".zenodo.json"
zenodo = json.loads(zenodo_path.read_text(encoding="utf-8"))
related = [
    item
    for item in zenodo.get("related_identifiers", [])
    if not (
        item.get("scheme") == "url"
        and str(item.get("identifier", "")).startswith("https://github.com/")
    )
]
related.append({"identifier": url, "relation": "isSupplementTo", "scheme": "url"})
zenodo["related_identifiers"] = related
zenodo_path.write_text(
    json.dumps(zenodo, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)

release_info_path = root / "GIT_RELEASE_INFO.json"
release_info = json.loads(release_info_path.read_text(encoding="utf-8"))
release_info["repository_url"] = url
release_info_path.write_text(
    json.dumps(release_info, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)

bib_path = root / "citation.bib"
bib = bib_path.read_text(encoding="utf-8")
if re.search(r"(?m)^\s*url\s*=", bib):
    bib = re.sub(r"(?m)^\s*url\s*=\s*\{[^}]*\},?", f"  url = {{{url}}}", bib)
else:
    bib = re.sub(r"\n\}\s*$", f",\n  url = {{{url}}}\n}}\n", bib)
bib_path.write_text(bib, encoding="utf-8", newline="\n")

master_path = root / "zenodo/master_record_metadata.json"
master = json.loads(master_path.read_text(encoding="utf-8"))
master_related = [
    item
    for item in master.get("related_identifiers", [])
    if item.get("scheme") != "url"
]
master_related.append(
    {"identifier": url, "relation": "isSupplementedBy", "scheme": "url"}
)
master["related_identifiers"] = master_related
master_path.write_text(
    json.dumps(master, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)

print(url)
print("Run scripts/rebuild_release_artifacts.py before committing or tagging.")
