"""Score multilingual LLM benchmark rows from CSV."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Score multilingual benchmark outputs.")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    with args.csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    by_language: dict[str, list[int]] = defaultdict(list)
    by_category: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        score = int(row["score"])
        by_language[row["language"]].append(score)
        by_category[row["category"]].append(score)

    print("Language averages")
    print("-----------------")
    for language, scores in sorted(by_language.items()):
        print(f"{language:10} {sum(scores) / len(scores):.2f}")

    print("\nCategory averages")
    print("-----------------")
    for category, scores in sorted(by_category.items()):
        print(f"{category:24} {sum(scores) / len(scores):.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
