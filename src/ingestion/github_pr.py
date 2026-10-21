# src/ingestion/github_pr.py
# GitHub adapter: all GitHub-specific code lives here, so the core analyzer
# never depends on one external service.
# Reads PUBLIC data without credentials. Posting a comment needs a token,
# which is read from the GITHUB_TOKEN environment variable and is NEVER hard-coded.

import os
import requests as req

API = "https://api.github.com"
TIMEOUT = 15  # seconds, so a slow API can't hang the analyzer


def _get(url):
    # Wraps req.get so a network failure returns None instead of crashing
    try:
        return req.get(url, timeout=TIMEOUT)
    except req.exceptions.RequestException as e:
        print(f"ERROR: network problem calling {url}: {e}")
        return None


def _explain_error(response, what):
    # Rate limit gets its own clear message, other errors show GitHub's text
    if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
        print(f"ERROR: GitHub rate limit reached while fetching {what}. Wait, or use a token.")
        return
    try:
        msg = response.json().get("message", "Unknown error")
    except ValueError:
        msg = "Unknown error"
    print(f"ERROR: could not fetch {what}. Status: {response.status_code}. GitHub says: {msg}")


def fetch_pr_safely(owner, repo, pr_number):
    """Returns {"detail":..., "files":...} or None (with a printed reason)."""
    detail = _get(f"{API}/repos/{owner}/{repo}/pulls/{pr_number}")
    if detail is None:
        return None
    if detail.status_code != 200:
        _explain_error(detail, f"PR #{pr_number}")
        return None

    files = _get(f"{API}/repos/{owner}/{repo}/pulls/{pr_number}/files")
    if files is None:
        return None
    if files.status_code != 200:
        _explain_error(files, f"files of PR #{pr_number}")
        return None

    return {"detail": detail.json(), "files": files.json()}


def get_file_content_from_github(owner, repo, filepath, commit_sha):
    """Full file text at a commit. Returns "" if the file is missing (e.g. newly added)."""
    response = _get(f"https://raw.githubusercontent.com/{owner}/{repo}/{commit_sha}/{filepath}")
    if response is None or response.status_code != 200:
        return ""
    return response.text


def format_pr_summary_markdown(pr_number, title, rows):
    """
    Builds a SHORT comment body. rows = list of dicts with
    function_name, file, risk, minutes (already sorted by priority).
    """
    levels = [r["risk"] for r in rows]
    overall = "HIGH" if "HIGH" in levels else "MEDIUM" if "MEDIUM" in levels else "LOW"
    lines = [f"### Review risk summary for PR #{pr_number}: {title}",
             f"**Overall review attention: {overall}**", ""]
    for i, r in enumerate(rows[:5], 1):
        lines.append(f"{i}. `{r['function_name']}()` in `{r['file']}` - {r['risk']} (~{r['minutes']:.1f} min)")
    if len(rows) > 5:
        lines.append(f"...and {len(rows) - 5} more functions.")
    lines += ["", "_This is a review-attention signal from measured code metrics. "
                  "It does not prove that a bug exists._"]
    return "\n".join(lines)


def post_pr_comment(owner, repo, pr_number, body, token=None):
    """Posts a comment. Token comes from the argument or GITHUB_TOKEN env var, never from code."""
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: no GITHUB_TOKEN set, comment not posted.")
        return False
    try:
        response = req.post(
            f"{API}/repos/{owner}/{repo}/issues/{pr_number}/comments",
            headers={"Authorization": f"Bearer {token}"},
            json={"body": body},
            timeout=TIMEOUT,
        )
    except req.exceptions.RequestException as e:
        print(f"ERROR: network problem while posting: {e}")
        return False
    if response.status_code != 201:
        print(f"ERROR: comment rejected. Status: {response.status_code}")
        return False
    return True
