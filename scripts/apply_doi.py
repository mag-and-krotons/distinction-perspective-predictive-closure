#!/usr/bin/env python3
"""Apply the DOI assigned to this source/reproducibility Git release."""

from pathlib import Path
import json
import re
import sys

import yaml


if len(sys.argv) != 2:
    raise SystemExit("usage: apply_doi.py 10.5281/zenodo.XXXXXXX")
doi = sys.argv[1].strip()
if not re.fullmatch(r"10\.5281/zenodo\.\d+", doi):
    raise SystemExit("expected a Zenodo DOI in the form 10.5281/zenodo.XXXXXXX")

root = Path(__file__).resolve().parents[1]
(root / "DOI.txt").write_text(doi + "\n", encoding="utf-8", newline="\n")

citation_path = root / "CITATION.cff"
citation = yaml.safe_load(citation_path.read_text(encoding="utf-8")) or {}
citation["doi"] = doi
citation_path.write_text(
    yaml.safe_dump(citation, sort_keys=False, allow_unicode=True),
    encoding="utf-8",
    newline="\n",
)

codemeta_path = root / "codemeta.json"
codemeta = json.loads(codemeta_path.read_text(encoding="utf-8"))
codemeta["identifier"] = f"https://doi.org/{doi}"
codemeta_path.write_text(
    json.dumps(codemeta, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)

bib_path = root / "citation.bib"
bib_text = bib_path.read_text(encoding="utf-8")
bib_text = re.sub(r"\n\s*note\s*=\s*\{[^}]*\},?", "", bib_text)
if "doi =" in bib_text:
    bib_text = re.sub(r"doi\s*=\s*\{[^}]*\}", f"doi = {{{doi}}}", bib_text)
else:
    bib_text = bib_text.replace("\n}", f",\n  doi = {{{doi}}}\n}}", 1)
bib_path.write_text(bib_text, encoding="utf-8", newline="\n")

readme_path = root / "README.md"
readme = readme_path.read_text(encoding="utf-8")
marker = f"**Zenodo DOI:** [{doi}](https://doi.org/{doi})"
if "**Zenodo DOI:**" in readme:
    readme = re.sub(r"\*\*Zenodo DOI:\*\*.*", marker, readme)
else:
    readme = readme.replace("**Date:** 27 August 2026", f"**Date:** 27 August 2026  \n{marker}")
readme_path.write_text(readme, encoding="utf-8", newline="\n")

print(doi)
print("Run scripts/rebuild_release_artifacts.py before committing a DOI back-reference.")
