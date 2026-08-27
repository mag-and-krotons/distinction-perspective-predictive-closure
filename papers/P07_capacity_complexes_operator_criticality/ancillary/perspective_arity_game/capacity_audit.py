from __future__ import annotations

import argparse
import json
from pathlib import Path

from capacity_character import audit
from native_extension import connected_class_counts, native_extension_data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arity", type=int, default=4)
    parser.add_argument("--max-events", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = native_extension_data(args.arity, args.max_events)
    result = {
        "status": (
            "one finite P1 code audit plus the code-fiber capacity law; no "
            "code-specific product is promoted to the source"
        ),
        "arity_P1_coordinate": args.arity,
        **audit(connected_class_counts(data)),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
