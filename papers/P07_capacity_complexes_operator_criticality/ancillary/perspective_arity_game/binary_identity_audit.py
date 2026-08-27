from __future__ import annotations

import argparse
import json
from pathlib import Path

from binary_identity_carrier import audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-bits", type=int, default=14)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = audit(args.max_bits)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
