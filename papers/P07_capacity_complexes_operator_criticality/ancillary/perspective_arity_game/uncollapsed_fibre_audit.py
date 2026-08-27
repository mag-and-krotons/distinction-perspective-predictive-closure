from __future__ import annotations

import argparse
import json
from pathlib import Path

from uncollapsed_fibre_duality import audit


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit carry-coupled uncollapsed character fibres"
    )
    parser.add_argument("--output", default="uncollapsed_fibre_audit.json")
    args = parser.parse_args()
    Path(args.output).write_text(json.dumps(audit(), indent=2) + "\n")


if __name__ == "__main__":
    main()
