#!/usr/bin/env python3
"""Rebuild nested archives and integrity ledgers from Git-canonical bytes."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]
RELEASE = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
ZIP_TIME = (2026, 8, 27, 0, 0, 0)
IGNORED_PARTS = {".git", ".pytest_cache", "__pycache__", "_latex_build", "_renders"}
IGNORED_NAMES = {".DS_Store", "Thumbs.db"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def is_ignored(path: Path, base: Path) -> bool:
    relative = path.relative_to(base)
    return (
        any(part in IGNORED_PARTS for part in relative.parts)
        or path.name in IGNORED_NAMES
        or path.suffix == ".pyc"
    )


def write_ledger(path: Path, base: Path, names: list[str]) -> None:
    rows = [f"{sha256(base / name)}  {name}\n" for name in sorted(names)]
    write_text(path, "".join(rows))


def write_zip(path: Path, members: list[tuple[Path, str]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with zipfile.ZipFile(
        temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for source, name in sorted(members, key=lambda pair: pair[1]):
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
    temporary.replace(path)


def rebuild_paper_and_submission_archives() -> None:
    paper_dirs = [
        directory
        for directory in sorted((ROOT / "papers").iterdir())
        if directory.is_dir() and (directory / "main.tex").exists()
    ]
    for paper_dir in paper_dirs:
        paper_id = paper_dir.name.split("_", 1)[0]
        source_members: list[tuple[Path, str]] = []
        for source in paper_dir.rglob("*"):
            if (
                not source.is_file()
                or is_ignored(source, paper_dir)
                or source.name in {"main.pdf", "source_package.zip"}
            ):
                continue
            source_members.append((source, source.relative_to(paper_dir).as_posix()))
        source_archive = paper_dir / "source_package.zip"
        write_zip(source_archive, source_members)

        submission_dir = ROOT / "submissions" / paper_dir.name
        submission_source = submission_dir / f"{paper_id}_source.zip"
        shutil.copyfile(source_archive, submission_source)
        shutil.copyfile(paper_dir / "main.pdf", submission_dir / f"{paper_id}_manuscript.pdf")

        submission_names = [
            path.name
            for path in submission_dir.iterdir()
            if path.is_file()
            and not is_ignored(path, submission_dir)
            and path.name != "SHA256SUMS.txt"
        ]
        write_ledger(
            submission_dir / "SHA256SUMS.txt", submission_dir, submission_names
        )
        all_submission_names = sorted(submission_names + ["SHA256SUMS.txt"])
        aggregate = ROOT / "submissions" / f"{paper_dir.name}_submission_package.zip"
        write_zip(
            aggregate,
            [(submission_dir / name, name) for name in all_submission_names],
        )


def rebuild_release_directory() -> None:
    release_dir = ROOT / "release"
    shutil.copyfile(ROOT / "COMPLETE_PAPER_SERIES.pdf", release_dir / "COMPLETE_PAPER_SERIES.pdf")
    shutil.copyfile(
        ROOT / "atlas/MASTER_SCIENTIFIC_ATLAS.pdf",
        release_dir / "MASTER_SCIENTIFIC_ATLAS.pdf",
    )
    shutil.copyfile(
        ROOT / "submissions/INDEX.csv",
        release_dir / "INDIVIDUAL_SUBMISSION_INDEX.csv",
    )
    names = [
        path.name
        for path in release_dir.iterdir()
        if path.is_file()
        and not is_ignored(path, release_dir)
        and path.name != "SHA256SUMS.txt"
    ]
    write_ledger(release_dir / "SHA256SUMS.txt", release_dir, names)


def packaged_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if is_ignored(path, ROOT):
            continue
        files.append(path)
    return sorted(files, key=lambda value: value.relative_to(ROOT).as_posix())


def rebuild_root_integrity() -> None:
    excluded = {"PACKAGE_MANIFEST.json", "SHA256SUMS.txt"}
    entries = []
    for path in packaged_files():
        name = path.relative_to(ROOT).as_posix()
        if name in excluded:
            continue
        entries.append(
            {"bytes": path.stat().st_size, "path": name, "sha256": sha256(path)}
        )
    canonical = "".join(
        f"{entry['sha256']}  {entry['path']}\n" for entry in entries
    ).encode("utf-8")
    manifest = {
        "author": "Abhijit Singh",
        "files": entries,
        "generated_at_utc": "2026-08-27T00:00:00+00:00",
        "package": "Abhijit Singh Zenodo and Git Release",
        "root_sha256": hashlib.sha256(canonical).hexdigest(),
        "version": RELEASE,
    }
    write_text(
        ROOT / "PACKAGE_MANIFEST.json",
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
    )

    ledger_names = [
        path.relative_to(ROOT).as_posix()
        for path in packaged_files()
        if path.relative_to(ROOT).as_posix() != "SHA256SUMS.txt"
    ]
    write_ledger(ROOT / "SHA256SUMS.txt", ROOT, ledger_names)


def main() -> None:
    rebuild_paper_and_submission_archives()
    rebuild_release_directory()
    rebuild_root_integrity()
    print(
        json.dumps(
            {
                "release": RELEASE,
                "root_files": len(packaged_files()),
                "submission_packages": len(
                    list((ROOT / "submissions").glob("*_submission_package.zip"))
                ),
                "status": "REBUILT",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
