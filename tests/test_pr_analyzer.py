import unittest
from unittest.mock import patch
from src.analysis import pr_analyzer as pa

SRC_OLD = "def f(x):\n    return x\n"
SRC_NEW = "def f(x):\n    for i in x:\n        if i:\n            for j in i:\n                if j:\n                    pass\n    return x\n"

class T(unittest.TestCase):
    def test_label_high(self):
        self.assertEqual(pa.risk_label({"loc": 5, "complexity": 21, "max_nesting": 0}), "HIGH")

    def test_label_medium_by_nesting(self):
        self.assertEqual(pa.risk_label({"loc": 5, "complexity": 1, "max_nesting": 4}), "MEDIUM")

    def test_label_low(self):
        self.assertEqual(pa.risk_label({"loc": 5, "complexity": 1, "max_nesting": 0}), "LOW")

    def test_bad_syntax_returns_empty(self):
        self.assertEqual(pa.functions_from_source("def ("), {})

    @patch("src.analysis.pr_analyzer.github_pr")
    def test_fetch_failure_returns_none(self, gp):
        gp.fetch_pr_safely.return_value = None
        self.assertIsNone(pa.analyze_pr("o", "r", 1))

    @patch("src.analysis.pr_analyzer.github_pr")
    def test_changed_function_detected(self, gp):
        gp.fetch_pr_safely.return_value = {
            "detail": {"title": "t", "base": {"sha": "a"}, "head": {"sha": "b"}},
            "files": [{"filename": "x.py"}, {"filename": "notes.txt"}]}
        gp.get_file_content_from_github.side_effect = [SRC_OLD, SRC_NEW]
        r = pa.analyze_pr("o", "r", 1)
        self.assertEqual(len(r["rows"]), 1)
        self.assertEqual(r["policy"], "REVIEW ADVISED")

    @patch("src.analysis.pr_analyzer.github_pr")
    def test_main_exit_2_on_failure(self, gp):
        gp.fetch_pr_safely.return_value = None
        self.assertEqual(pa.main(["o", "r", "1"]), 2)

if __name__ == "__main__":
    unittest.main()
