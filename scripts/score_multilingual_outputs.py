"""Score multilingual LLM benchmark rows from CSV."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from score_validation import load_scored_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Score multilingual benchmark outputs.")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    try:
        rows = load_scored_rows(args.csv_path, ["score"])
    except ValueError as error:
        parser.error(str(error))

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
