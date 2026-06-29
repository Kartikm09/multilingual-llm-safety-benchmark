"""Categorize failures from synthetic multilingual model outputs."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Categorize multilingual benchmark failures.")
    parser.add_argument("outputs_json", type=Path)
    args = parser.parse_args()

    outputs = json.loads(args.outputs_json.read_text(encoding="utf-8"))
    failures = [item for item in outputs if item.get("failure_category")]
    counts = Counter(item["failure_category"] for item in failures)

    print("Failure categories")
    print("------------------")
    for category, count in counts.most_common():
        print(f"- {category}: {count}")

    print("\nFailure evidence")
    print("----------------")
    for item in failures:
        print(f"- {item['test_id']} ({item['language']}): {item['failure_category']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
