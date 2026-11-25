#!/usr/bin/env python3
"""Check for new Drips Wave 11 assignments for devbigaiizen.

Reads the GitHub token from the GITHUB_TOKEN environment variable (never
from chat, never from a file in this repo). Lists open issues assigned to
devbigaiizen in the Wave repos, compares against seen.json, and prints any
new assignments. Exits 0 when nothing is new.

Usage:
    GITHUB_TOKEN=*** python3 scripts/check-assignment.py
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error

ASSIGNEE = "devbigaiizen"
REPOS = [
    "Stellar-Agent-Guard/stellar-agent-guard-sdk",
    "wraith-protocol/demo",
]
SEEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "seen.json")
BASE = "https://api.github.com"


def github_get(path, token):
    req = urllib.request.Request(BASE + path, method="GET")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("GitHub API error: HTTP %s on %s" % (e.code, path), file=sys.stderr)
        return None


def load_seen():
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("seen", []))
    except (OSError, ValueError):
        return set()


def find_prs(repo, token):
    """Return PRs authored by ASSIGNEE in repo (any state)."""
    query = "author:%s+repo:%s+type:pr" % (ASSIGNEE, repo)
    result = github_get("/search/issues?q=" + query, token)
    if result is None:
        return []
    return result.get("items", [])


def references_issue(pr, number):
    text = "%s\n%s" % (pr.get("title") or "", pr.get("body") or "")
    return re.search(r"(?<![\w/])#%s(?!\d)" % number, text) is not None


def classify(number, prs):
    """Return (status, pr_url) for an issue given candidate PRs."""
    matches = [p for p in prs if references_issue(p, number)]
    merged = [p for p in matches if (p.get("pull_request") or {}).get("merged_at")]
    if merged:
        return "pr_merged", merged[0]["html_url"]
    opened = [p for p in matches if p.get("state") == "open"]
    if opened:
        return "pr_open", opened[0]["html_url"]
    return "assigned_no_pr", None


STATUS_TEXT = {
    "assigned_no_pr": "assigned, no PR yet",
    "pr_open": "PR open",
    "pr_merged": "PR merged",
}


def build_report(token, seen):
    issues = []
    for repo in REPOS:
        query = "assignee:%s+repo:%s+type:issue+state:open" % (ASSIGNEE, repo)
        result = github_get("/search/issues?q=" + query, token)
        if result is None:
            continue
        items = result.get("items", [])
        prs = find_prs(repo, token) if items else []
        for item in items:
            key = "%s#%s" % (repo, item["number"])
            status, pr_url = classify(item["number"], prs)
            issues.append({
                "key": key,
                "number": item["number"],
                "title": item["title"],
                "url": item["html_url"],
                "new": key not in seen,
                "status": status,
                "pr_url": pr_url,
            })
    return {
        "assignee": ASSIGNEE,
        "new_count": sum(1 for i in issues if i["new"]),
        "issues": issues,
    }


def print_report(report):
    new = [i for i in report["issues"] if i["new"]]
    if not new:
        print("No new Wave 11 assignment for %s." % ASSIGNEE)
    else:
        print("New assignment(s) for %s:" % ASSIGNEE)
        for item in new:
            print("- %s: %s (%s)" % (item["key"], item["title"], item["url"]))
        print("Vet each one with the malware rule in AGENT.md before starting work.")
    if report["issues"]:
        print("Status of assigned open issues:")
        for i in report["issues"]:
            line = "- %s: %s" % (i["key"], STATUS_TEXT[i["status"]])
            if i["pr_url"]:
                line += " (%s)" % i["pr_url"]
            print(line)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--json", action="store_true",
                        help="print the report as JSON")
    args = parser.parse_args(argv)

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("GITHUB_TOKEN is not set. Export it first, never paste it in chat.",
              file=sys.stderr if args.json else sys.stdout)
        return 2

    report = build_report(token, load_seen())
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
