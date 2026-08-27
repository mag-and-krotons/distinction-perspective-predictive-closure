#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess
import sys
import zipfile

import yaml


ROOT = Path(__file__).resolve().parents[1]
RELEASE = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
errors: list[str] = []

IGNORED_PARTS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "_latex_build",
    "_renders",
}
IGNORED_NAMES = {".DS_Store", "Thumbs.db"}


def is_ignored(path: Path, base: Path) -> bool:
    relative = path.relative_to(base)
    return (
        any(part in IGNORED_PARTS for part in relative.parts)
        or path.name in IGNORED_NAMES
        or path.suffix == ".pyc"
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pdfinfo(path: Path) -> str:
    result = subprocess.run(
        ["pdfinfo", str(path)], capture_output=True, text=True, check=False
    )
    if result.returncode:
        errors.append(f"pdfinfo failed: {path.relative_to(ROOT)}")
    return result.stdout


def packaged_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if is_ignored(path, ROOT):
            continue
        files.append(path)
    return sorted(files, key=lambda value: value.relative_to(ROOT).as_posix())


def parse_checksum_ledger(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            errors.append(f"malformed checksum row {path.relative_to(ROOT)}:{line_number}")
            continue
        digest, name = match.groups()
        if name in rows:
            errors.append(f"duplicate checksum path in {path.relative_to(ROOT)}: {name}")
        rows[name] = digest
    return rows


def verify_checksum_ledger(
    ledger: Path, base: Path, expected_names: set[str]
) -> None:
    if not ledger.exists():
        errors.append(f"missing checksum ledger: {ledger.relative_to(ROOT)}")
        return
    rows = parse_checksum_ledger(ledger)
    missing = sorted(expected_names - set(rows))
    extra = sorted(set(rows) - expected_names)
    if missing:
        errors.append(
            f"checksum ledger missing {ledger.relative_to(ROOT)}: {', '.join(missing)}"
        )
    if extra:
        errors.append(
            f"checksum ledger has extra {ledger.relative_to(ROOT)}: {', '.join(extra)}"
        )
    for name in sorted(expected_names & set(rows)):
        target = base / name
        if not target.is_file():
            errors.append(f"checksum target missing: {target.relative_to(ROOT)}")
        elif sha256(target) != rows[name]:
            errors.append(f"checksum mismatch: {target.relative_to(ROOT)}")


def verify_root_integrity() -> None:
    files = packaged_files()
    relative_names = {path.relative_to(ROOT).as_posix() for path in files}
    expected_ledger = relative_names - {"SHA256SUMS.txt"}
    verify_checksum_ledger(ROOT / "SHA256SUMS.txt", ROOT, expected_ledger)

    manifest_path = ROOT / "PACKAGE_MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"package manifest is not valid JSON: {exc}")
        return

    records = manifest.get("files") or []
    by_name = {record.get("path"): record for record in records}
    expected_manifest = relative_names - {"SHA256SUMS.txt", "PACKAGE_MANIFEST.json"}
    if set(by_name) != expected_manifest:
        missing = sorted(expected_manifest - set(by_name))
        extra = sorted(set(by_name) - expected_manifest)
        if missing:
            errors.append(f"package manifest missing: {', '.join(missing)}")
        if extra:
            errors.append(f"package manifest has extra: {', '.join(extra)}")
    for name in sorted(expected_manifest & set(by_name)):
        path = ROOT / name
        record = by_name[name]
        if record.get("bytes") != path.stat().st_size:
            errors.append(f"manifest byte count mismatch: {name}")
        if record.get("sha256") != sha256(path):
            errors.append(f"manifest hash mismatch: {name}")

    canonical = "".join(
        f"{by_name[name]['sha256']}  {name}\n" for name in sorted(expected_manifest)
    ).encode("utf-8")
    expected_root = hashlib.sha256(canonical).hexdigest()
    if manifest.get("root_sha256") != expected_root:
        errors.append("package manifest root hash mismatch")
    if manifest.get("version") != RELEASE:
        errors.append("package manifest version mismatch")
    if manifest.get("author") != "Abhijit Singh":
        errors.append("package manifest author mismatch")


def verify_release_and_submission_ledgers(papers: list[tuple[str, Path]]) -> None:
    paper_by_directory = {directory.name: (paper_id, directory) for paper_id, directory in papers}
    expected_directories = set(paper_by_directory)
    submissions_root = ROOT / "submissions"
    actual_directories = {
        path.name for path in submissions_root.iterdir() if path.is_dir()
    }
    if actual_directories != expected_directories:
        missing = sorted(expected_directories - actual_directories)
        extra = sorted(actual_directories - expected_directories)
        if missing:
            errors.append(f"submission directories missing: {', '.join(missing)}")
        if extra:
            errors.append(f"orphan submission directories: {', '.join(extra)}")

    expected_aggregates = {
        f"{directory}_submission_package.zip" for directory in expected_directories
    }
    actual_aggregates = {
        path.name
        for path in submissions_root.glob("*_submission_package.zip")
        if path.is_file()
    }
    if actual_aggregates != expected_aggregates:
        missing = sorted(expected_aggregates - actual_aggregates)
        extra = sorted(actual_aggregates - expected_aggregates)
        if missing:
            errors.append(f"aggregate submission ZIPs missing: {', '.join(missing)}")
        if extra:
            errors.append(f"orphan aggregate submission ZIPs: {', '.join(extra)}")

    expected_top_files = expected_aggregates | {"INDEX.csv"}
    actual_top_files = {
        path.name for path in submissions_root.iterdir() if path.is_file()
    }
    if actual_top_files != expected_top_files:
        missing = sorted(expected_top_files - actual_top_files)
        extra = sorted(actual_top_files - expected_top_files)
        if missing:
            errors.append(f"submission top-level files missing: {', '.join(missing)}")
        if extra:
            errors.append(f"unexpected submission top-level files: {', '.join(extra)}")

    release_dir = ROOT / "release"
    expected_release_names = {
        "COMPLETE_PAPER_SERIES.pdf",
        "INDIVIDUAL_SUBMISSION_INDEX.csv",
        "MASTER_SCIENTIFIC_ATLAS.pdf",
        "RELEASE_ASSETS.md",
        "SHA256SUMS.txt",
    }
    actual_release_names = {
        path.name for path in release_dir.iterdir() if path.is_file()
    }
    if actual_release_names != expected_release_names:
        missing = sorted(expected_release_names - actual_release_names)
        extra = sorted(actual_release_names - expected_release_names)
        if missing:
            errors.append(f"release files missing: {', '.join(missing)}")
        if extra:
            errors.append(f"unexpected release files: {', '.join(extra)}")
    release_names = {
        path.name
        for path in release_dir.iterdir()
        if path.is_file() and path.name != "SHA256SUMS.txt"
    }
    verify_checksum_ledger(
        release_dir / "SHA256SUMS.txt", release_dir, release_names
    )
    release_copies = {
        "COMPLETE_PAPER_SERIES.pdf": ROOT / "COMPLETE_PAPER_SERIES.pdf",
        "MASTER_SCIENTIFIC_ATLAS.pdf": ROOT / "atlas/MASTER_SCIENTIFIC_ATLAS.pdf",
        "INDIVIDUAL_SUBMISSION_INDEX.csv": submissions_root / "INDEX.csv",
    }
    for name, source in release_copies.items():
        target = release_dir / name
        if source.is_file() and target.is_file() and sha256(source) != sha256(target):
            errors.append(f"release copy mismatch: release/{name}")

    for directory_name in sorted(expected_directories):
        directory = submissions_root / directory_name
        if not directory.is_dir():
            continue
        paper_id, paper_directory = paper_by_directory[directory_name]
        expected_all_names = {
            f"{paper_id}_abstract.txt",
            f"{paper_id}_manuscript.pdf",
            f"{paper_id}_metadata.json",
            f"{paper_id}_source.zip",
            f"{paper_id}_submission_readme.md",
            "SHA256SUMS.txt",
        }
        actual_all_names = {
            path.name for path in directory.iterdir() if path.is_file()
        }
        if actual_all_names != expected_all_names:
            missing = sorted(expected_all_names - actual_all_names)
            extra = sorted(actual_all_names - expected_all_names)
            if missing:
                errors.append(f"submission files missing in {directory_name}: {', '.join(missing)}")
            if extra:
                errors.append(f"unexpected submission files in {directory_name}: {', '.join(extra)}")
        names = expected_all_names - {"SHA256SUMS.txt"}
        verify_checksum_ledger(directory / "SHA256SUMS.txt", directory, names)
        source_copy = directory / f"{paper_id}_source.zip"
        manuscript_copy = directory / f"{paper_id}_manuscript.pdf"
        if source_copy.is_file() and sha256(source_copy) != sha256(paper_directory / "source_package.zip"):
            errors.append(f"submission source copy mismatch: {directory_name}")
        if manuscript_copy.is_file() and sha256(manuscript_copy) != sha256(paper_directory / "main.pdf"):
            errors.append(f"submission manuscript copy mismatch: {directory_name}")

        archive = submissions_root / f"{directory.name}_submission_package.zip"
        if not archive.exists():
            errors.append(f"missing aggregate submission ZIP: {archive.name}")
            continue
        with zipfile.ZipFile(archive) as zipped:
            if zipped.testzip():
                errors.append(f"bad aggregate submission ZIP: {archive.name}")
            expected_archive_names = names | {"SHA256SUMS.txt"}
            if set(zipped.namelist()) != expected_archive_names:
                errors.append(f"aggregate submission ZIP inventory mismatch: {archive.name}")
            for name in expected_archive_names & set(zipped.namelist()):
                if hashlib.sha256(zipped.read(name)).hexdigest() != sha256(directory / name):
                    errors.append(f"aggregate submission ZIP byte mismatch: {archive.name}/{name}")

    index_rows = list(csv.DictReader((submissions_root / "INDEX.csv").open(encoding="utf-8")))
    indexed_directories = {row.get("directory", "") for row in index_rows}
    indexed_ids = {row.get("paper_id", "") for row in index_rows}
    expected_ids = {paper_id for paper_id, _ in papers}
    if len(index_rows) != 19 or indexed_directories != expected_directories or indexed_ids != expected_ids:
        errors.append("submission index does not exactly map the 19 paper/atlas units")


def version_metadata_checks() -> None:
    json_checks = [
        (ROOT / ".zenodo.json", "version"),
        (ROOT / "codemeta.json", "version"),
        (ROOT / "GIT_RELEASE_INFO.json", "release"),
        (ROOT / "zenodo/master_record_metadata.json", "version"),
    ]
    for path, key in json_checks:
        try:
            value = json.loads(path.read_text(encoding="utf-8")).get(key)
        except Exception as exc:
            errors.append(f"invalid JSON metadata {path.relative_to(ROOT)}: {exc}")
            continue
        if value != RELEASE:
            errors.append(f"version mismatch in {path.relative_to(ROOT)}")

    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8")) or {}
    if str(citation.get("version")) != RELEASE:
        errors.append("version mismatch in CITATION.cff")

    release_info = json.loads((ROOT / "GIT_RELEASE_INFO.json").read_text(encoding="utf-8"))
    repository_url = str(release_info.get("repository_url") or "")
    if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+", repository_url):
        errors.append("Git repository URL is unresolved or malformed")
    if release_info.get("tag") != f"v{RELEASE}":
        errors.append("Git release tag mismatch")


def paper_checks() -> list[tuple[str, Path]]:
    papers: list[tuple[str, Path]] = []
    banned = "(?i)(?<![A-Za-z])" + ("A" + "I") + "(?![A-Za-z])|" + ("AH" + "UVI")
    for directory in sorted((ROOT / "papers").iterdir()):
        if not directory.is_dir() or not (directory / "main.tex").exists():
            continue
        paper_id = directory.name.split("_", 1)[0]
        papers.append((paper_id, directory))
        text = (directory / "main.tex").read_text(encoding="utf-8", errors="ignore")
        if "Independent Researcher" in text or "\\affiliation" in text:
            errors.append(f"affiliation present: {paper_id}")
        if re.search(banned, text):
            errors.append(f"restricted terminology in manuscript: {paper_id}")
        for filename in ["main.pdf", "source_package.zip", "metadata.yaml", "00README.XXX"]:
            if not (directory / filename).exists():
                errors.append(f"missing {paper_id}/{filename}")

        metadata = yaml.safe_load((directory / "metadata.yaml").read_text(encoding="utf-8")) or {}
        if metadata.get("author") != "Abhijit Singh":
            errors.append(f"wrong metadata author: {paper_id}")
        if str(metadata.get("release")) != RELEASE:
            errors.append(f"wrong release metadata: {paper_id}")
        if not metadata.get("primary_category"):
            errors.append(f"primary category missing: {paper_id}")

        info = pdfinfo(directory / "main.pdf")
        if "A4" not in info:
            errors.append(f"non-A4 PDF: {paper_id}")
        author = re.search(r"^Author:\s*(.*)", info, re.MULTILINE)
        if not author or author.group(1).strip() != "Abhijit Singh":
            errors.append(f"wrong PDF author: {paper_id}")
        pdf_text = subprocess.run(
            ["pdftotext", str(directory / "main.pdf"), "-"],
            capture_output=True,
            text=True,
            check=False,
        ).stdout
        if "Independent Researcher" in pdf_text or re.search(r"(?im)^Affiliation\b", pdf_text):
            errors.append(f"affiliation printed: {paper_id}")
        if re.search(banned, pdf_text):
            errors.append(f"restricted terminology in PDF: {paper_id}")

        expected_source = {
            path.relative_to(directory).as_posix()
            for path in directory.rglob("*")
            if path.is_file()
            and not is_ignored(path, directory)
            and path.name not in {"main.pdf", "source_package.zip"}
        }
        with zipfile.ZipFile(directory / "source_package.zip") as zipped:
            if zipped.testzip():
                errors.append(f"bad source ZIP: {paper_id}")
            if set(zipped.namelist()) != expected_source:
                errors.append(f"source ZIP inventory mismatch: {paper_id}")
            for name in expected_source & set(zipped.namelist()):
                if hashlib.sha256(zipped.read(name)).hexdigest() != sha256(directory / name):
                    errors.append(f"source ZIP byte mismatch: {paper_id}/{name}")
    return papers


def scientific_and_pdf_checks(papers: list[tuple[str, Path]]) -> int:
    if len(papers) != 19:
        errors.append(f"expected 19 paper/atlas units, found {len(papers)}")
    index = list(csv.DictReader((ROOT / "ledgers/PAPER_INDEX.csv").open(encoding="utf-8")))
    if len(index) != 19:
        errors.append(f"paper index has {len(index)} rows")

    with (ROOT / "data/prime_observer_36_relations.csv").open(encoding="utf-8") as stream:
        relations = list(csv.DictReader(stream))
    if len(relations) != 36:
        errors.append("relation table is not 36 rows")
    result = subprocess.run(
        [sys.executable, str(ROOT / "code/verify_prime_observer_36.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        errors.append("prime-observer verifier failed")
    else:
        try:
            payload = json.loads(result.stdout)
            if payload.get("status") != "PASS" or payload.get("relations") != 36:
                errors.append("prime-observer verifier returned unexpected result")
        except Exception:
            errors.append("prime-observer verifier output is not JSON")

    clean = list(csv.DictReader((ROOT / "verification/CLEAN_SOURCE_COMPILE_V8.csv").open(encoding="utf-8")))
    if len(clean) != 19 or any(row["status"] != "PASS" for row in clean):
        errors.append("clean-source compilation report incomplete or failed")
    warnings = list(csv.DictReader((ROOT / "verification/LATEX_WARNING_AUDIT_V8.csv").open(encoding="utf-8")))
    if len(warnings) != 19:
        errors.append("LaTeX warning audit incomplete")
    if any(int(row["overfull_boxes"]) for row in warnings):
        errors.append("overfull boxes detected")
    if any(
        int(row["undefined_references"])
        or int(row["undefined_citations"])
        or int(row["multiply_defined_labels"])
        for row in warnings
    ):
        errors.append("reference/citation/label warnings detected")

    combined = ROOT / "COMPLETE_PAPER_SERIES.pdf"
    atlas = ROOT / "atlas/MASTER_SCIENTIFIC_ATLAS.pdf"
    for path in [combined, atlas]:
        if not path.exists():
            errors.append(f"missing {path.name}")
        elif "A4" not in pdfinfo(path):
            errors.append(f"non-A4 central PDF: {path.name}")
    combined_info = pdfinfo(combined)
    pages = re.search(r"^Pages:\s+(\d+)", combined_info, re.MULTILINE)
    if not pages or int(pages.group(1)) != 200:
        errors.append("combined series page count is not 200")
    return len(relations)


def source_separation_and_placeholder_checks() -> None:
    forbidden_assets = [
        "img_0735",
        "img_0736",
        "img_0737",
        "notebook_source_montage",
        "ancillary/source_notes",
        "sources/notebook",
    ]
    for path in packaged_files():
        relative = path.relative_to(ROOT).as_posix().lower()
        if any(token in relative for token in forbidden_assets):
            errors.append(f"handwritten-note asset remains in public release: {relative}")
        if path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path) as zipped:
                for name in zipped.namelist():
                    lowered = name.lower()
                    if any(token in lowered for token in forbidden_assets):
                        errors.append(f"handwritten-note asset in {relative}: {name}")

    for path in (ROOT / "zenodo/individual_records").glob("*.json"):
        if "[equation]" in path.read_text(encoding="utf-8"):
            errors.append(f"equation placeholder remains: {path.relative_to(ROOT)}")
    placeholder_tokens = [
        "GITHUB_REPOSITORY_URL_TO_BE_INSERTED",
        "TO_BE_SET_WITH_scripts/apply_repository_url.py",
    ]
    for path in packaged_files():
        if path.suffix.lower() not in {".json", ".md", ".cff", ".bib", ".txt", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in placeholder_tokens:
            if token in text:
                errors.append(f"publication placeholder remains in {path.relative_to(ROOT)}")


def restricted_terminology_check() -> None:
    banned = "(?i)(?<![A-Za-z])" + ("A" + "I") + "(?![A-Za-z])|" + ("AH" + "UVI")
    binary_suffixes = {".pdf", ".zip", ".jpg", ".jpeg", ".png", ".gif", ".bundle"}
    for path in packaged_files():
        if path.suffix.lower() in binary_suffixes:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(banned, text):
            errors.append(f"restricted terminology in {path.relative_to(ROOT)}")


def main() -> None:
    version_metadata_checks()
    papers = paper_checks()
    relation_rows = scientific_and_pdf_checks(papers)
    verify_release_and_submission_ledgers(papers)
    source_separation_and_placeholder_checks()
    restricted_terminology_check()
    verify_root_integrity()

    results = {
        "author": "Abhijit Singh",
        "combined_pages": 200,
        "individual_submission_packages": len(
            list((ROOT / "submissions").glob("*_submission_package.zip"))
        ),
        "paper_and_atlas_units": len(papers),
        "relation_rows": relation_rows,
        "release": RELEASE,
        "status": "PASS" if not errors else "FAIL",
    }
    print(json.dumps(results, indent=2, sort_keys=True))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
