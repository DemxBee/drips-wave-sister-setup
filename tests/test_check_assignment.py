import contextlib
import importlib.util
import io
import json
import os
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "check_assignment", os.path.join(HERE, "..", "scripts", "check-assignment.py"))
ca = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ca)

REPO_A, REPO_B = ca.REPOS


def issue(n, title="t"):
    return {"number": n, "title": title, "html_url": "https://github.com/x/y/issues/%d" % n}


def pr(n, body, state="open", merged=False):
    return {
        "number": n, "title": "pr %d" % n, "body": body, "state": state,
        "html_url": "https://github.com/x/y/pull/%d" % n,
        "pull_request": {"merged_at": "2026-01-01T00:00:00Z" if merged else None},
    }


def fake_get(issues_by_repo, prs_by_repo):
    def _get(path, token):
        for repo in ca.REPOS:
            if "repo:" + repo in path:
                data = prs_by_repo if "type:pr" in path else issues_by_repo
                return {"items": data.get(repo, [])}
        return None
    return _get


def run(issues, prs, seen=(), args=()):
    out = io.StringIO()
    with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "tok"}), \
            mock.patch.object(ca, "github_get", fake_get(issues, prs)), \
            mock.patch.object(ca, "load_seen", return_value=set(seen)), \
            contextlib.redirect_stdout(out):
        code = ca.main(list(args))
    return code, out.getvalue()


class CheckAssignmentTests(unittest.TestCase):
    def test_new_assignment_reported(self):
        code, out = run({REPO_A: [issue(5, "Fix thing")]}, {})
        self.assertEqual(code, 0)
        self.assertIn("New assignment(s)", out)
        self.assertIn("%s#5" % REPO_A, out)
        self.assertIn("assigned, no PR yet", out)

    def test_no_new_assignments(self):
        code, out = run({REPO_A: [issue(5)]}, {}, seen=["%s#5" % REPO_A])
        self.assertEqual(code, 0)
        self.assertIn("No new Wave 11 assignment", out)

    def test_pr_matched_open_and_merged(self):
        issues = {REPO_A: [issue(1), issue(2), issue(3)]}
        prs = {REPO_A: [pr(10, "Fixes #1"), pr(11, "Closes #2", state="closed", merged=True),
                        pr(12, "unrelated #11")]}
        with mock.patch.object(ca, "github_get", fake_get(issues, prs)):
            report = ca.build_report("tok", set())
        by = {i["number"]: i for i in report["issues"]}
        self.assertEqual(by[1]["status"], "pr_open")
        self.assertEqual(by[1]["pr_url"], "https://github.com/x/y/pull/10")
        self.assertEqual(by[2]["status"], "pr_merged")
        self.assertEqual(by[3]["status"], "assigned_no_pr")
        self.assertIsNone(by[3]["pr_url"])

    def test_number_prefix_not_matched(self):
        self.assertEqual(ca.classify(1, [pr(10, "fixes #12")]), ("assigned_no_pr", None))

    def test_text_output_includes_pr_url(self):
        _, out = run({REPO_A: [issue(1)]}, {REPO_A: [pr(10, "Fixes #1")]})
        self.assertIn("PR open (https://github.com/x/y/pull/10)", out)

    def test_json_output(self):
        code, out = run({REPO_B: [issue(7, "Seven")]}, {REPO_B: [pr(20, "Fixes #7")]},
                        seen=["%s#7" % REPO_B], args=["--json"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["assignee"], ca.ASSIGNEE)
        self.assertEqual(data["new_count"], 0)
        self.assertEqual(data["issues"], [{
            "key": "%s#7" % REPO_B, "number": 7, "title": "Seven",
            "url": "https://github.com/x/y/issues/7", "new": False,
            "status": "pr_open", "pr_url": "https://github.com/x/y/pull/20"}])

    def test_missing_token(self):
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": ""}), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ca.main([]), 2)


if __name__ == "__main__":
    unittest.main()
