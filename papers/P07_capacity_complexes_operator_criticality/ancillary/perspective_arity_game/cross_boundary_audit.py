from __future__ import annotations

import argparse
import json
from pathlib import Path

from cross_boundary_completion import audit


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit the generated cross-boundary completion"
    )
    parser.add_argument("--output", default="cross_boundary_audit.json")
    args = parser.parse_args()
    Path(args.output).write_text(json.dumps(audit(), indent=2) + "\n")


if __name__ == "__main__":
    main()
