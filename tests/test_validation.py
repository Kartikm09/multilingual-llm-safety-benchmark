import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def cli(script, rows, *, options=(), extra_json=None):
    with tempfile.TemporaryDirectory() as temp:
        source = Path(temp) / "input.csv"
        if isinstance(rows, list) and (not rows or isinstance(rows[0], dict)):
            fields = list(rows[0]) if rows else ["score", "language"]
            with source.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
        args = [sys.executable, str(ROOT / "scripts" / script), str(source)]
        if extra_json is not None:
            output = Path(temp) / "outputs.json"
            output.write_text(json.dumps(extra_json), encoding="utf-8")
            args.append(str(output))
        return subprocess.run([*args, *options], text=True, capture_output=True, cwd=ROOT, timeout=10)

class BenchmarkTests(unittest.TestCase):
    def test_hand_computed_language_and_category_averages(self):
        rows = [{"test_id": "one", "score": "1", "language": "Hindi", "category": "safety"},
                {"test_id": "two", "score": "3", "language": "Hindi", "category": "safety"},
                {"test_id": "three", "score": "4", "language": "English", "category": "reasoning"}]
        result = cli("score_multilingual_outputs.py", rows)
        self.assertEqual(result.returncode, 0, result.stderr)
        values = dict(line.split() for line in result.stdout.splitlines() if line.startswith(("Hindi", "English", "safety", "reasoning")))
        self.assertEqual(values, {"Hindi": "2.00", "English": "4.00", "safety": "2.00", "reasoning": "4.00"})

    def test_both_score_commands_reject_invalid_scores(self):
        for script in ["score_multilingual_outputs.py", "generate_benchmark_summary.py"]:
            for score in ["", "0", "6", "100", "bad"]:
                with self.subTest(script=script, score=score):
                    kwargs = {"extra_json": []} if script.startswith("generate") else {}
                    result = cli(script, [{"score": score, "language": "Hindi", "category": "safety"}], **kwargs)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("score", result.stderr.lower())
                    self.assertNotIn("Traceback", result.stderr)

    def test_empty_summary_is_a_clear_data_error(self):
        result = cli("generate_benchmark_summary.py", [], extra_json=[])
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("at least one", result.stderr)

if __name__ == "__main__":
    unittest.main()
