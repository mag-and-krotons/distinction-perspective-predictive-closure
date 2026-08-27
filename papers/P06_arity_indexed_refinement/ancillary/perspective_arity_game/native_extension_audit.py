from __future__ import annotations

import argparse
import json
from pathlib import Path

from native_extension import audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arity", type=int, default=4)
    parser.add_argument("--max-events", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = audit(args.arity, args.max_events)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
