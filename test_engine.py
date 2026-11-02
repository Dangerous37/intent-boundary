import json
import subprocess
import sys
import unittest
from pathlib import Path

from engine import evaluate


def example():
    return json.loads(Path(__file__).with_name("example.json").read_text(encoding="utf-8"))


class AcceptanceTests(unittest.TestCase):
    def test_example_cli(self):
        proc = subprocess.run([sys.executable, "cli.py", "example.json"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), evaluate(example()))

    def test_frozen_threshold_and_abstention(self):
        result = evaluate(example())
        self.assertEqual(result["threshold"], 2/3)
        self.assertEqual(result["correct"], 3)
        self.assertEqual(result["false_accepts"], 0)

    def test_holdout_labels_do_not_change_threshold(self):
        data = example()
        data["test"][0]["intent"] = None
        self.assertEqual(evaluate(data)["false_accepts"], 1)
        self.assertEqual(evaluate(data)["threshold"], evaluate(example())["threshold"])

    def test_leakage_after_normalization(self):
        data = example()
        data["test"][0]["text"] = "PASSWORD reset ACCOUNT!"
        with self.assertRaisesRegex(ValueError, "overlapping"):
            evaluate(data)
