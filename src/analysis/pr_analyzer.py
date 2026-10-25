# src/analysis/pr_analyzer.py
# Command-line analyzer: fetch a PR from GitHub, find changed functions,
# measure them, label risk, and print a short markdown summary.
# Usage: python -m src.analysis.pr_analyzer OWNER REPO PR_NUMBER
# Exit codes: 0 = analysis finished (any risk level), 2 = analysis FAILED.

import ast
import argparse
import sys

from src.ingestion import github_pr

NEST_NODES = (ast.If, ast.For, ast.While, ast.Try, ast.With)
BRANCH_NODES = (ast.If, ast.For, ast.While, ast.Try, ast.BoolOp, ast.ExceptHandler)


def functions_from_source(text):
    # {function name: AST node}; empty dict if the file can't be parsed
    try:
        tree = ast.parse(text)
    except Exception:
        return {}
    return {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}


def max_nesting(node, depth=0):
    best = depth
    for child in ast.iter_child_nodes(node):
        d = depth + 1 if isinstance(child, NEST_NODES) else depth
        best = max(best, max_nesting(child, d))
    return best


def measure(node):
    lines = [c.lineno for c in ast.walk(node) if hasattr(c, "lineno")]
    loc = max(lines) - node.lineno + 1
    complexity = 1 + sum(isinstance(c, BRANCH_NODES) for c in ast.walk(node))
    return {"loc": loc, "complexity": complexity, "max_nesting": max_nesting(node)}


def risk_label(m):
    # Same thresholds as V1 (a proxy rule, not proof of a bug)
    if m["complexity"] > 20 or m["max_nesting"] > 5 or m["loc"] > 100:
        return "HIGH"
    if m["complexity"] > 10 or m["max_nesting"] > 3 or m["loc"] > 50:
        return "MEDIUM"
    return "LOW"


def analyze_pr(owner, repo, pr_number):
    """Returns a result dict, or None if the PR data could not be fetched."""
    pr = github_pr.fetch_pr_safely(owner, repo, pr_number)
    if pr is None:
        return None
    base, head = pr["detail"]["base"]["sha"], pr["detail"]["head"]["sha"]

    weight = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    rows = []
    for f in pr["files"]:
        path = f["filename"]
        if not path.endswith(".py"):
            continue
        old = functions_from_source(github_pr.get_file_content_from_github(owner, repo, path, base))
        new = functions_from_source(github_pr.get_file_content_from_github(owner, repo, path, head))
        for name, node in new.items():
            if name in old and ast.dump(old[name]) == ast.dump(node):
                continue  # unchanged
            m = measure(node)
            change = abs(m["loc"] - measure(old[name])["loc"]) if name in old else m["loc"]
            label = risk_label(m)
            rows.append({
                "function_name": name, "file": path, "risk": label,
                "minutes": round(m["loc"] * 0.05 + m["complexity"] * 0.3, 1),
                # risk tier always wins; change size (capped at 9) only breaks ties
                "priority": weight[label] * 10 + min(change, 9),
            })
    rows.sort(key=lambda r: r["priority"], reverse=True)
    levels = [r["risk"] for r in rows]
    policy = ("HIGH REVIEW ATTENTION" if "HIGH" in levels
              else "REVIEW ADVISED" if "MEDIUM" in levels else "LOW")
    return {"title": pr["detail"]["title"], "rows": rows, "policy": policy}


def main(argv=None):
    p = argparse.ArgumentParser(description="Review-risk summary for a GitHub PR")
    p.add_argument("owner")
    p.add_argument("repo")
    p.add_argument("pr_number", type=int)
    p.add_argument("--out", help="also write the summary to this file")
    a = p.parse_args(argv)

    result = analyze_pr(a.owner, a.repo, a.pr_number)
    if result is None:
        print("ANALYSIS FAILED: could not fetch the PR.")
        return 2  # a crash is NOT the same as "high risk"

    text = github_pr.format_pr_summary_markdown(a.pr_number, result["title"], result["rows"])
    text += f"\n\nPolicy result: **{result['policy']}** (advisory only)"
    print(text)
    if a.out:
        with open(a.out, "w") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
