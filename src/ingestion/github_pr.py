# src/ingestion/github_pr.py
# Fetches real Pull Request data from GitHub's public REST API.
# Uses UNAUTHENTICATED, public read access only - no tokens, no
# credentials, no secrets involved. This is safe by design: we
# only ever read PUBLIC repository data that anyone could view
# in a browser, so there is nothing sensitive to leak or protect.
# Rate limits apply to unauthenticated requests (60/hour per IP),
# which is a known, documented limitation for heavier usage.

import requests as req

def fetch_pr_safely(owner, repo, pr_number):
    """
    Safely fetches a PR's detail and changed files from GitHub.
    Returns None (with a printed error) if the PR doesn't exist
    or the API call fails, instead of crashing the caller.
    """
    detail_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    detail_response = req.get(detail_url)

    if detail_response.status_code != 200:
        print(f"ERROR: Could not fetch PR #{pr_number}. Status: {detail_response.status_code}")
        print(f"GitHub says: {detail_response.json().get('message', 'Unknown error')}")
        return None

    pr_detail = detail_response.json()

    files_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    files_response = req.get(files_url)

    if files_response.status_code != 200:
        print(f"ERROR: Could not fetch files for PR #{pr_number}. Status: {files_response.status_code}")
        return None

    pr_files = files_response.json()

    return {"detail": pr_detail, "files": pr_files}


def get_file_content_from_github(owner, repo, filepath, commit_sha):
    """
    Fetches a file's full content at a specific commit, directly
    from GitHub's raw file server (not the API's JSON wrapper).
    """
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit_sha}/{filepath}"
    response = req.get(url)
    return response.text
