"""Run the finite P1 audit of native P1 and hypothetical native P4."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from primitive import (
    binary_fiber,
    binary_tree_shape,
    complete_binary_tree_orbits,
    complete_binary_trees_of_four,
    exact_layers,
    isolated_binary_tree_automorphisms,
    isolated_native_automorphisms,
    native_classes,
)


def audit_arity(arity: int, max_events: int) -> dict:
    layers = exact_layers(arity, max_events)
    rows = []
    class_maps: dict[int, dict] = {}
    for event_count, histories in layers.items():
        classes = native_classes(histories, arity)
        class_maps[event_count] = classes
        rows.append(
            {
                "event_horizon_P1_coordinate": event_count,
                "raw_P1_histories": len(histories),
                "native_incidence_classes": len(classes),
                "source_histories_retained": sum(len(fiber) for fiber in classes.values()),
                "discarded_histories": 0,
            }
        )
    return {"arity_P1_coordinate": arity, "layers": rows, "_classes": class_maps}


def audit_p4_binary_fibers(max_events: int) -> dict:
    p4 = audit_arity(4, max_events)
    layers = []
    for event_count, classes in p4["_classes"].items():
        complete_fiber_sizes: list[int] = []
        complete_presentation_counts: list[int] = []
        balanced_subview_sizes: list[int] = []
        for histories in classes.values():
            representative = histories[0]
            representatives, orbit_sizes = complete_binary_tree_orbits(representative)
            complete_fiber_sizes.append(len(representatives))
            complete_presentation_counts.append(sum(orbit_sizes))
            balanced_subview_sizes.append(len(binary_fiber(representative)))

        split_histogram = Counter(complete_fiber_sizes)
        layers.append(
            {
                "event_horizon_P1_coordinate": event_count,
                "native_P4_classes": len(classes),
                "complete_P1_binary_presentations_before_isomorphism": sum(
                    complete_presentation_counts
                ),
                "complete_P1_binary_shadow_classes": sum(complete_fiber_sizes),
                "native_classes_split_by_P1": sum(
                    size > 1 for size in complete_fiber_sizes
                ),
                "maximum_shadow_classes_over_one_native_class": max(
                    complete_fiber_sizes
                ),
                "shadow_split_histogram": {
                    str(key): value for key, value in sorted(split_histogram.items())
                },
                "all_complete_binary_presentations_retained": all(
                    count == 15**event_count
                    for count in complete_presentation_counts
                ),
                "equal_depth_subview_shadow_classes": sum(balanced_subview_sizes),
            }
        )

    del p4["_classes"]
    return {
        "semantic_index": {
            "P0": "no distinction; not a program state",
            "P1": "our native two-resultant distinction and all program notation",
            "P4": "hypothetical atomic four-resultant distinction",
        },
        "isolated_event": {
            "native_P4_automorphisms_seen_by_P1": isolated_native_automorphisms(4),
            "balanced_binary_hierarchy_automorphisms": (
                isolated_binary_tree_automorphisms()
            ),
            "unbalanced_binary_hierarchy_automorphisms": 2,
            "complete_binary_presentations_retained": 15,
            "balanced_presentations": sum(
                binary_tree_shape(tree) == "balanced"
                for tree in complete_binary_trees_of_four((0, 1, 2, 3))
            ),
            "unbalanced_presentations": sum(
                binary_tree_shape(tree) == "unbalanced"
                for tree in complete_binary_trees_of_four((0, 1, 2, 3))
            ),
            "interpretation": (
                "every binary hierarchy inserts intermediate distinctions absent "
                "from atomic P4; all fifteen complete hierarchies are retained"
            ),
        },
        "native_P4_closure": p4,
        "binary_presentation_fibers": layers,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-events", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    p1 = audit_arity(2, min(args.max_events, 4))
    del p1["_classes"]
    result = {
        "status": "P1 audit; no claim of entering or reproducing P4",
        "native_P1_closure": p1,
        **audit_p4_binary_fibers(args.max_events),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
