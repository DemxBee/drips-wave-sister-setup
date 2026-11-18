#!/usr/bin/env python3
"""Check for new Drips Wave 11 assignments for devbigaiizen.

Reads the GitHub token from the GITHUB_TOKEN environment variable (never
from chat, never from a file in this repo). Lists open issues assigned to
devbigaiizen in the Wave repos, compares against seen.json, and prints any
new assignments. Exits 0 when nothing is new.

Usage:
    GITHUB_TOKEN=<token> python3 scripts/check-assignment.py
"""
import json
import os
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


def main():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("GITHUB_TOKEN is not set. Export it first, never paste it in chat.")
        return 2

    seen = load_seen()
    new = []
    for repo in REPOS:
        query = "assignee:%s+repo:%s+type:issue+state:open" % (ASSIGNEE, repo)
        result = github_get("/search/issues?q=" + query, token)
        if result is None:
            continue
        for item in result.get("items", []):
            key = "%s#%s" % (repo, item["number"])
            if key not in seen:
                new.append({
                    "key": key,
                    "number": item["number"],
                    "title": item["title"],
                    "url": item["html_url"],
                })

    if not new:
        print("No new Wave 11 assignment for %s." % ASSIGNEE)
        return 0

    print("New assignment(s) for %s:" % ASSIGNEE)
    for item in new:
        print("- %s: %s (%s)" % (item["key"], item["title"], item["url"]))
    print("Vet each one with the malware rule in AGENT.md before starting work.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
