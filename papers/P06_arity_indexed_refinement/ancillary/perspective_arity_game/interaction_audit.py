from __future__ import annotations

import argparse
import json
from pathlib import Path

from interaction_closure import audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-arity", type=int, default=8)
    parser.add_argument("--max-events", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = {
        "status": (
            "P1 audit of complete atomic-interaction closure; generated before "
            "any arithmetic or RH comparison"
        ),
        "arities": [
            audit(arity, args.max_events)
            for arity in range(1, args.max_arity + 1)
        ],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
