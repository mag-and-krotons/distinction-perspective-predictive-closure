#!/usr/bin/env python3
"""Build the external GitHub/Zenodo attachments for an immutable tag."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
ZIP_TIME = (2026, 8, 27, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--tag", default=f"v{VERSION}")
    args = parser.parse_args()

    expected_tag = f"v{VERSION}"
    if args.tag != expected_tag:
        raise SystemExit(f"expected immutable tag {expected_tag}, received {args.tag}")

    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise SystemExit("output directory must be outside the repository")
    output.mkdir(parents=True, exist_ok=True)

    tag_ref = f"refs/tags/{args.tag}"
    if git("cat-file", "-t", tag_ref) != "tag":
        raise SystemExit(f"{args.tag} must be an annotated tag")
    tag_commit = git("rev-parse", f"{tag_ref}^{{commit}}")
    head_commit = git("rev-parse", "HEAD")
    if tag_commit != head_commit:
        raise SystemExit(
            f"tag {args.tag} resolves to {tag_commit}, not HEAD {head_commit}"
        )

    archive = f"Abhijit_Singh_Zenodo_Git_Release_v{VERSION}"
    repository_zip = output / f"{archive}.zip"
    repository_bundle = output / f"{archive}.bundle"
    individual_zip = output / f"Abhijit_Singh_Individual_Submission_Packages_v{VERSION}.zip"

    main_result = subprocess.run(
        ["git", "rev-parse", "--verify", "refs/heads/main"],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if main_result.returncode:
        git("branch", "main", tag_commit)
    elif main_result.stdout.strip() != tag_commit:
        raise SystemExit(
            "local main does not point to the immutable tagged release commit"
        )
    subprocess.run(
        [
            "git",
            "archive",
            "--format=zip",
            f"--prefix={archive}/",
            f"--output={repository_zip}",
            f"{args.tag}^{{}}",
        ],
        cwd=ROOT,
        check=True,
    )
    # Keep Git's transient ``.bundle.lock`` outside the release directory so
    # even concurrent builds cannot leave non-asset files beside the output.
    with tempfile.TemporaryDirectory(prefix="release-bundle-") as temporary:
        temporary_bundle = Path(temporary) / repository_bundle.name
        subprocess.run(
            [
                "git",
                "-c",
                "pack.threads=1",
                "bundle",
                "create",
                str(temporary_bundle),
                "HEAD",
                "refs/heads/main",
                tag_ref,
            ],
            cwd=ROOT,
            check=True,
        )
        temporary_bundle.replace(repository_bundle)

    submission_members = [
        (path, path.name)
        for path in sorted((ROOT / "submissions").glob("*_submission_package.zip"))
    ]
    submission_members.append((ROOT / "submissions/INDEX.csv", "INDEX.csv"))
    if len(submission_members) != 20:
        raise SystemExit("expected 19 individual packages plus INDEX.csv")
    write_zip(individual_zip, submission_members)

    copies = {
        ROOT / "COMPLETE_PAPER_SERIES.pdf": output / "COMPLETE_PAPER_SERIES.pdf",
        ROOT / "atlas/MASTER_SCIENTIFIC_ATLAS.pdf": output / "MASTER_SCIENTIFIC_ATLAS.pdf",
    }
    for source, destination in copies.items():
        shutil.copyfile(source, destination)

    assets = [
        repository_zip,
        repository_bundle,
        individual_zip,
        copies[ROOT / "COMPLETE_PAPER_SERIES.pdf"],
        copies[ROOT / "atlas/MASTER_SCIENTIFIC_ATLAS.pdf"],
    ]
    checksum_path = output / "RELEASE_ASSET_SHA256SUMS.txt"
    checksum_path.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in assets),
        encoding="utf-8",
        newline="\n",
    )

    print(
        json.dumps(
            {
                "assets": [path.name for path in assets] + [checksum_path.name],
                "commit": tag_commit,
                "output": str(output),
                "status": "BUILT",
                "tag": args.tag,
                "version": VERSION,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
