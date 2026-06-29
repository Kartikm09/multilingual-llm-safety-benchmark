"""Generate a compact benchmark summary from CSV test cases and JSON outputs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate multilingual benchmark summary.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("outputs_json", type=Path)
    args = parser.parse_args()

    with args.csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    outputs = json.loads(args.outputs_json.read_text(encoding="utf-8"))

    scores = [int(row["score"]) for row in rows]
    languages = Counter(row["language"] for row in rows)
    failures = Counter(item["failure_category"] for item in outputs if item.get("failure_category"))

    print("Benchmark summary")
    print("-----------------")
    print(f"Test cases: {len(rows)}")
    print(f"Average score: {sum(scores) / len(scores):.2f}")
    print("Languages:")
    for language, count in sorted(languages.items()):
        print(f"- {language}: {count}")
    print("Failure categories:")
    for category, count in failures.most_common():
        print(f"- {category}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
