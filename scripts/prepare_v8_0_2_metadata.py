#!/usr/bin/env python3
"""Apply the publication-metadata corrections specific to release 8.0.2."""

from __future__ import annotations

from pathlib import Path
import json
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]
RELEASE = "8.0.2"
RESEARCH_TITLE = (
    "Distinction, Perspective, and Predictive Closure: "
    "Complete Research Release 8.0.2"
)
CODE_TITLE = (
    "Distinction, Perspective, and Predictive Closure: "
    "Research Verification Code and Source Packages"
)

EQUATIONS = {
    "P02": ["m/d"],
    "P05": ["|z|²"],
    "P06": ["n", "n−1", "t^(n−1)", "n−1"],
    "P07": ["m", "[m, 2m)"],
    "P08": ["A_N", "A_N/N → ∞", "N/A_N → 0"],
    "P14": [
        "z_acc = 0.587401052",
        "z_eq = 0.259921050",
        "H_0t_0 = 0.9358813101",
        "ΔN = 0.4620981204",
        "q_0 = −1/2",
        "j_0 = 1",
    ],
    "P17": [
        "p·1 = p",
        "ℤ₁₀",
        "σ(d) = 1−d (mod 10)",
        "C(9,2) = 36",
        "2, 3, 5, 7",
        "6",
        "4, 8, 9",
    ],
}


def dump_json(path: Path, data: object) -> None:
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def replace_equations(text: str, values: list[str], label: str) -> str:
    actual = text.count("[equation]")
    if actual == 0:
        return text
    if actual != len(values):
        raise RuntimeError(
            f"{label}: expected {len(values)} equation markers, found {actual}"
        )
    for value in values:
        text = text.replace("[equation]", value, 1)
    return text


def update_primary_metadata() -> None:
    zenodo_path = ROOT / ".zenodo.json"
    zenodo = json.loads(zenodo_path.read_text(encoding="utf-8"))
    zenodo["title"] = RESEARCH_TITLE
    zenodo["upload_type"] = "publication"
    zenodo["publication_type"] = "other"
    zenodo["version"] = RELEASE
    dump_json(zenodo_path, zenodo)

    citation_path = ROOT / "CITATION.cff"
    citation = yaml.safe_load(citation_path.read_text(encoding="utf-8")) or {}
    citation["title"] = RESEARCH_TITLE
    citation["version"] = RELEASE
    citation["preferred-citation"] = {
        "type": "generic",
        "title": RESEARCH_TITLE,
        "authors": [{"family-names": "Singh", "given-names": "Abhijit"}],
        "year": 2026,
    }
    citation_path.write_text(
        yaml.safe_dump(citation, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
        newline="\n",
    )

    codemeta_path = ROOT / "codemeta.json"
    codemeta = json.loads(codemeta_path.read_text(encoding="utf-8"))
    codemeta["name"] = CODE_TITLE
    codemeta["version"] = RELEASE
    dump_json(codemeta_path, codemeta)

    bib_path = ROOT / "citation.bib"
    bib = bib_path.read_text(encoding="utf-8")
    bib = re.sub(r"title\s*=\s*\{[^}]*\}", f"title = {{{RESEARCH_TITLE}}}", bib)
    bib = re.sub(r",?\n\s*note\s*=\s*\{Zenodo DOI to be assigned\}", "", bib)
    bib_path.write_text(bib, encoding="utf-8", newline="\n")

    release_info_path = ROOT / "GIT_RELEASE_INFO.json"
    release_info = json.loads(release_info_path.read_text(encoding="utf-8"))
    release_info["release"] = RELEASE
    release_info["tag"] = f"v{RELEASE}"
    release_info["history"] = (
        "I publish the complete research programme with its formal papers, "
        "scientific atlas, data, executable audits, source packages, and "
        "provenance ledgers."
    )
    dump_json(release_info_path, release_info)


def clear_unassigned_dois() -> None:
    placeholder_tokens = ("TO_BE", "RESERVE", "MASTER_RELEASE_DOI")

    def is_unassigned(value: object) -> bool:
        return value is None or not str(value).strip() or any(
            token in str(value) for token in placeholder_tokens
        )

    for path in sorted((ROOT / "papers").glob("*/metadata.yaml")):
        metadata = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        metadata["release"] = RELEASE
        if is_unassigned(metadata.get("doi")):
            metadata["doi"] = None
        path.write_text(
            yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
            newline="\n",
        )

    for path in sorted((ROOT / "submissions").glob("*/*_metadata.json")):
        metadata = json.loads(path.read_text(encoding="utf-8"))
        metadata["release_version"] = RELEASE
        if is_unassigned(metadata.get("doi")):
            metadata["doi"] = None
        if is_unassigned(metadata.get("related_master_release")):
            metadata["related_master_release"] = None
        dump_json(path, metadata)

    for path in sorted((ROOT / "zenodo/individual_records").glob("*_zenodo_metadata.json")):
        metadata = json.loads(path.read_text(encoding="utf-8"))
        metadata["related_identifiers"] = [
            item
            for item in metadata.get("related_identifiers", [])
            if "MASTER_RELEASE_DOI" not in str(item.get("identifier", ""))
        ]
        dump_json(path, metadata)

    master_path = ROOT / "zenodo/master_record_metadata.json"
    master = json.loads(master_path.read_text(encoding="utf-8"))
    if "RESERVE_ON_ZENODO" in str(master.get("doi", "")):
        master.pop("doi", None)
    master["version"] = RELEASE
    master["record_creation_mode"] = "linked-github-release"
    master["title"] = (
        "Distinction, Perspective, and Predictive Closure: "
        f"Complete Research Release {RELEASE}"
    )
    dump_json(master_path, master)


def replace_equation_markers() -> None:
    for paper_id, values in EQUATIONS.items():
        zenodo_path = ROOT / "zenodo/individual_records" / f"{paper_id}_zenodo_metadata.json"
        metadata = json.loads(zenodo_path.read_text(encoding="utf-8"))
        metadata["description"] = replace_equations(
            metadata["description"], values, zenodo_path.as_posix()
        )
        dump_json(zenodo_path, metadata)

        matches = list((ROOT / "submissions").glob(f"{paper_id}_*/{paper_id}_abstract.txt"))
        if len(matches) != 1:
            raise RuntimeError(f"{paper_id}: expected one submission abstract, found {len(matches)}")
        abstract_path = matches[0]
        abstract = replace_equations(
            abstract_path.read_text(encoding="utf-8"), values, abstract_path.as_posix()
        )
        abstract_path.write_text(abstract, encoding="utf-8", newline="\n")


def repair_operational_paths() -> None:
    for name in ["NEXT_STEPS.md", "ZENODO_GIT_RELEASE_GUIDE.md", "zenodo/README.md"]:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r"Abhijit_Singh_Zenodo_Upload_v[0-9_]+",
            "Abhijit_Singh_Zenodo_Upload_v8_0_2",
            text,
        )
        text = text.replace(
            "verification/FIRST_PAGE_CONTACT_SHEET.png",
            "verification/FIRST_PAGE_CONTACT_SHEET_V8.png",
        )
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    (ROOT / "VERSION").write_text(RELEASE + "\n", encoding="utf-8", newline="\n")
    update_primary_metadata()
    clear_unassigned_dois()
    replace_equation_markers()
    repair_operational_paths()
    print(json.dumps({"release": RELEASE, "status": "METADATA_PREPARED"}, indent=2))


if __name__ == "__main__":
    main()
