# tests/test_github_pr.py
# Tests the GitHub adapter WITHOUT touching the real internet:
# unittest.mock replaces req.get / req.post with fake responses.

import unittest
from unittest.mock import patch, MagicMock

import requests as real_requests
from src.ingestion import github_pr


def fake_response(status=200, json_data=None, headers=None, text=""):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = json_data if json_data is not None else {}
    r.headers = headers or {}
    r.text = text
    return r


class TestFetchPr(unittest.TestCase):
    @patch("src.ingestion.github_pr.req.get")
    def test_404_returns_none(self, get):
        get.return_value = fake_response(404, {"message": "Not Found"})
        self.assertIsNone(github_pr.fetch_pr_safely("o", "r", 1))

    @patch("src.ingestion.github_pr.req.get")
    def test_rate_limit_returns_none(self, get):
        get.return_value = fake_response(403, {"message": "rate limit"}, {"X-RateLimit-Remaining": "0"})
        self.assertIsNone(github_pr.fetch_pr_safely("o", "r", 1))

    @patch("src.ingestion.github_pr.req.get")
    def test_network_error_returns_none(self, get):
        get.side_effect = real_requests.exceptions.ConnectionError("down")
        self.assertIsNone(github_pr.fetch_pr_safely("o", "r", 1))

    @patch("src.ingestion.github_pr.req.get")
    def test_timeout_returns_none(self, get):
        get.side_effect = real_requests.exceptions.Timeout("slow")
        self.assertIsNone(github_pr.fetch_pr_safely("o", "r", 1))

    @patch("src.ingestion.github_pr.req.get")
    def test_files_endpoint_failure_returns_none(self, get):
        get.side_effect = [fake_response(200, {"title": "t"}), fake_response(500)]
        self.assertIsNone(github_pr.fetch_pr_safely("o", "r", 1))

    @patch("src.ingestion.github_pr.req.get")
    def test_success_returns_detail_and_files(self, get):
        get.side_effect = [fake_response(200, {"title": "t"}), fake_response(200, [{"filename": "a.py"}])]
        result = github_pr.fetch_pr_safely("o", "r", 1)
        self.assertEqual(result["detail"]["title"], "t")
        self.assertEqual(result["files"][0]["filename"], "a.py")


class TestFileContent(unittest.TestCase):
    @patch("src.ingestion.github_pr.req.get")
    def test_missing_file_returns_empty_string(self, get):
        get.return_value = fake_response(404)
        self.assertEqual(github_pr.get_file_content_from_github("o", "r", "x.py", "sha"), "")


class TestSummaryAndComment(unittest.TestCase):
    def test_summary_has_disclaimer_and_overall_level(self):
        rows = [{"function_name": "f", "file": "a.py", "risk": "HIGH", "minutes": 3.0}]
        text = github_pr.format_pr_summary_markdown(7, "title", rows)
        self.assertIn("HIGH", text)
        self.assertIn("does not prove", text)

    @patch("src.ingestion.github_pr.req.post")
    def test_no_token_means_no_post(self, post):
        with patch.dict("os.environ", {}, clear=True):
            self.assertFalse(github_pr.post_pr_comment("o", "r", 1, "hi"))
        post.assert_not_called()

    @patch("src.ingestion.github_pr.req.post")
    def test_token_is_sent_in_header(self, post):
        post.return_value = fake_response(201)
        self.assertTrue(github_pr.post_pr_comment("o", "r", 1, "hi", token="abc"))
        self.assertEqual(post.call_args.kwargs["headers"]["Authorization"], "Bearer abc")

    @patch("src.ingestion.github_pr.req.post")
    def test_rejected_comment_returns_false(self, post):
        post.return_value = fake_response(403)
        self.assertFalse(github_pr.post_pr_comment("o", "r", 1, "hi", token="abc"))


if __name__ == "__main__":
    unittest.main()
