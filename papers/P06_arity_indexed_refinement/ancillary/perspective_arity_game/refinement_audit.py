from __future__ import annotations

import argparse
import json
from pathlib import Path

from refinement_invariant import audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-arity", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "status": (
            "P1 audit of the complete refinement shadow; generated before "
            "arithmetic or RH comparison"
        ),
        "arities": [audit(arity) for arity in range(2, args.max_arity + 1)],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
