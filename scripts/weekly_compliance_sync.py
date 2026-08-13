#!/usr/bin/env python3
"""
Weekly EU Healthcare Compliance Audit Sync
==========================================

Automates the weekly generation of a compliance audit summary inside README.md
for a European healthcare organisation (HQ in Germany, branches in the UK and
France, 1000+ employees). The repository tracks medical-compliance / audit
todos as GitHub issues labelled by country (UK/FR/DE), priority (P0/P1/P2) and
type (documentation/audit/training/incident), spread across several milestones.

What the script does
--------------------
1. Clones/refreshes the target repository (git) and reads the local README.md.
2. Fetches every *open* issue from the repository via the GitHub REST API
   (paginated, 100 issues per request - handles the medium ~500 issue scale).
   Extracts: title, number, labels, milestone, assignee, created_at, updated_at.
3. Groups issues by country (UK / FR / DE) and, inside each country, counts
   them by priority (P0 / P1 / P2). Also builds the list of high-priority
   (P0/P1) open items per country (top 10, ordered by priority then recency).
4. Generates a Markdown block (overall statistics table, per-country priority
   distribution table and high-risk item lists) and writes it strictly between
   the markers `<!-- WEEKLY-COMPLIANCE-START -->` and
   `<!-- WEEKLY-COMPLIANCE-END -->`, preserving all content outside the markers.
5. Commits the updated README.md on a new branch
   `automation/compliance-YYYY-MM-DD` (execution date), pushes it to the remote
   and opens a Pull Request titled `Weekly compliance audit sync - YYYY-MM-DD`
   whose body summarises the sync and the changes.

Dependencies
------------
- git (commit / push)
- GitHub REST API (via Python standard library `urllib`; no third-party or
  external services are required)

Minimal privilege
-----------------
The token only needs:
- read access to repository issues (fetch),
- contents write (push the generated branch),
- pull requests write (open the weekly PR).
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone

# --------------------------------------------------------------------------- #
# Configuration (overridable via environment variables, e.g. GitHub Actions)  #
# --------------------------------------------------------------------------- #
GITHUB_API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
REPO_OWNER = os.environ.get("REPO_OWNER", "atool3800-stack")
REPO_NAME = os.environ.get("REPO_NAME", "project_20260813_015033_23c9c93d")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
USER_EMAIL = os.environ.get("USER_EMAIL", "test_user_23c9c93d@example.com")
USER_NAME = os.environ.get("USER_NAME", "compliance-sync-bot")

REPO_FULL_NAME = f"{REPO_OWNER}/{REPO_NAME}"
README_PATH = os.environ.get("README_PATH", "README.md")
DEFAULT_BRANCH = os.environ.get("DEFAULT_BRANCH", "main")
LOCAL_REPO_DIR = os.environ.get("LOCAL_REPO_DIR", ".")

COUNTRIES = ["UK", "FR", "DE"]
PRIORITIES = ["P0", "P1", "P2"]
TYPE_LABELS = ["documentation", "audit", "training", "incident"]
COUNTRY_NAMES = {"UK": "United Kingdom", "FR": "France", "DE": "Germany"}

START_MARKER = "<!-- WEEKLY-COMPLIANCE-START -->"
END_MARKER = "<!-- WEEKLY-COMPLIANCE-END -->"

HIGH_RISK_PRIORITIES = ["P0", "P1"]
TOP_N_PER_COUNTRY = 10


# --------------------------------------------------------------------------- #
# HTTP helper (stdlib only)                                                   #
# --------------------------------------------------------------------------- #
def api_request(method, path, token=GITHUB_TOKEN, payload=None, per_page=None, page=None):
    """Minimal GitHub REST API client. Returns parsed JSON (or None)."""
    url = f"{GITHUB_API_URL}{path}"
    query = []
    if per_page:
        query.append(f"per_page={per_page}")
    if page:
        query.append(f"page={page}")
    if query:
        url += ("&" if "?" in url else "?") + "&".join(query)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "weekly-compliance-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"GitHub API {method} {path} failed: {exc.code} - {detail[:500]}"
        ) from exc


def fetch_all_open_issues():
    """
    Fetch every open issue of the repository. The `/issues` endpoint is
    paginated (100 per page) and also returns pull requests - those are
    filtered out so only real issues are considered.
    """
    issues = []
    per_page = 100
    page = 1
    while True:
        batch = api_request(
            "GET", f"/repos/{REPO_FULL_NAME}/issues", per_page=per_page, page=page
        )
        if not batch:
            break
        for item in batch:
            if "pull_request" not in item:
                issues.append(item)
        if len(batch) < per_page:
            break
        page += 1
        # Safety guard for unbounded loops
        if page > 50:
            break
    return issues


# --------------------------------------------------------------------------- #
# Issue extraction / classification                                           #
# --------------------------------------------------------------------------- #
def extract_issue_fields(issue):
    """Extract the fields required by the task from a raw issue dict."""
    labels = [label.get("name", "") for label in issue.get("labels", [])]
    milestone = issue.get("milestone")
    assignee = issue.get("assignee")
    return {
        "number": issue.get("number"),
        "title": issue.get("title", ""),
        "url": issue.get("html_url", ""),
        "labels": labels,
        "country": next((c for c in COUNTRIES if c in labels), None),
        "priority": next((p for p in PRIORITIES if p in labels), None),
        "type": next((t for t in TYPE_LABELS if t in labels), None),
        "milestone": milestone.get("title") if milestone else None,
        "assignee": assignee.get("login") if assignee else None,
        "created_at": issue.get("created_at"),
        "updated_at": issue.get("updated_at"),
        "state": issue.get("state"),
    }


def sort_key(issue):
    """Sort high-risk issues: P0 before P1, then by last update (newest first)."""
    priority_rank = PRIORITIES.index(issue["priority"]) if issue["priority"] in PRIORITIES else 99
    updated = issue.get("updated_at") or ""
    return (priority_rank, updated)


# --------------------------------------------------------------------------- #
# Markdown generation                                                         #
# --------------------------------------------------------------------------- #
def build_markdown(issues, run_date):
    """Build the full Markdown block that is inserted between the markers."""
    # Per-country / per-priority counts
    totals = {c: 0 for c in COUNTRIES}
    priority_counts = {c: {p: 0 for p in PRIORITIES} for c in COUNTRIES}
    type_counts = {c: {} for c in COUNTRIES}

    for issue in issues:
        country = issue["country"]
        priority = issue["priority"]
        if not country:
            continue
        totals[country] += 1
        if priority in PRIORITIES:
            priority_counts[country][priority] += 1
        t = issue["type"] or "other"
        type_counts[country][t] = type_counts[country].get(t, 0) + 1

    grand_total = sum(totals.values())
    p0_total = sum(priority_counts[c]["P0"] for c in COUNTRIES)
    p1_total = sum(priority_counts[c]["P1"] for c in COUNTRIES)
    p2_total = sum(priority_counts[c]["P2"] for c in COUNTRIES)

    lines = []
    lines.append("## Weekly Compliance Audit Summary")
    lines.append("")
    lines.append(f"_Last generated: {run_date} (UTC) · Source: {REPO_FULL_NAME}_")
    lines.append("")

    # --- Overall statistics table ---
    lines.append("### Overall Statistics")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("| --- | ---: |")
    lines.append(f"| Open compliance issues | {grand_total} |")
    for c in COUNTRIES:
        lines.append(f"| {COUNTRY_NAMES[c]} ({c}) | {totals[c]} |")
    lines.append(f"| Priority P0 (critical) | {p0_total} |")
    lines.append(f"| Priority P1 (high) | {p1_total} |")
    lines.append(f"| Priority P2 (normal) | {p2_total} |")
    lines.append("")

    # --- Per-country priority distribution table ---
    lines.append("### Priority Distribution by Country")
    lines.append("")
    lines.append("| Country | P0 | P1 | P2 | Total |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for c in COUNTRIES:
        pc = priority_counts[c]
        lines.append(
            f"| {COUNTRY_NAMES[c]} ({c}) | {pc['P0']} | {pc['P1']} | {pc['P2']} | {totals[c]} |"
        )
    lines.append(
        f"| **Total** | **{p0_total}** | **{p1_total}** | **{p2_total}** | **{grand_total}** |"
    )
    lines.append("")

    # --- High-risk items per country (top N P0/P1) ---
    lines.append("### High-Risk Open Items (P0 / P1)")
    lines.append("")
    for c in COUNTRIES:
        high_risk = [
            i for i in issues if i["country"] == c and i["priority"] in HIGH_RISK_PRIORITIES
        ]
        high_risk.sort(key=sort_key)
        top = high_risk[:TOP_N_PER_COUNTRY]
        lines.append(f"#### {COUNTRY_NAMES[c]} ({c})")
        lines.append("")
        if not top:
            lines.append("_No open high-priority items._")
            lines.append("")
            continue
        lines.append("| # | Issue | Priority | Type | Assignee | Milestone | Updated |")
        lines.append("| ---: | --- | --- | --- | --- | --- | --- |")
        for issue in top:
            title = issue["title"].replace("|", "\\|").replace("\n", " ")
            assignee = issue["assignee"] or "—"
            milestone = issue["milestone"] or "—"
            updated = (issue["updated_at"] or "")[:10]
            lines.append(
                f"| [{issue['number']}]({issue['url']}) | {title} | "
                f"{issue['priority']} | {issue['type'] or '—'} | {assignee} | "
                f"{milestone} | {updated} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def update_readme(markdown_block, readme_path=README_PATH):
    """
    Replace the content between the START/END markers with the freshly
    generated block. Everything outside the markers is preserved.
    """
    with open(readme_path, "r", encoding="utf-8") as fh:
        content = fh.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL
    )
    replacement = f"{START_MARKER}\n{markdown_block}{END_MARKER}"

    if pattern.search(content):
        new_content = pattern.sub(lambda _m: replacement, content, count=1)
    else:
        # Markers not present yet: append a new section at the end.
        new_content = content.rstrip() + "\n\n" + START_MARKER + "\n" + \
                      markdown_block + END_MARKER + "\n"

    with open(readme_path, "w", encoding="utf-8") as fh:
        fh.write(new_content)
    return new_content


# --------------------------------------------------------------------------- #
# git helpers                                                                 #
# --------------------------------------------------------------------------- #
def run_git(args, cwd=LOCAL_REPO_DIR, check=True):
    cmd = ["git", "-C", cwd] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc


def current_branch():
    proc = run_git(["rev-parse", "--abbrev-ref", "HEAD"], check=False)
    return proc.stdout.strip() or DEFAULT_BRANCH


def create_and_push_branch(branch_name):
    """Create (or switch to) the automation branch, commit README and push."""
    remote_url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/{REPO_FULL_NAME}.git"

    # Make sure we start from the up-to-date default branch
    run_git(["fetch", "origin", DEFAULT_BRANCH])
    run_git(["checkout", DEFAULT_BRANCH])
    run_git(["pull", "--ff-only", "origin", DEFAULT_BRANCH])

    # Recreate/switch to the automation branch
    proc = run_git(["rev-parse", "--verify", f"refs/heads/{branch_name}"], check=False)
    if proc.returncode == 0:
        run_git(["checkout", branch_name])
        # rebase on top of latest default branch
        run_git(["rebase", DEFAULT_BRANCH])
    else:
        run_git(["checkout", "-b", branch_name])

    run_git(["add", README_PATH])
    run_git(
        ["-c", f"user.name={USER_NAME}", "-c", f"user.email={USER_EMAIL}",
         "commit", "-m", f"chore(compliance): weekly compliance audit sync ({date.today().isoformat()})"],
        check=False,
    )
    # If there is nothing to commit (no changes), commit will fail with rc=1 - ignore.

    # Push branch (force-with-lease to be safe on re-runs)
    run_git(["push", "-u", "origin", branch_name])


# --------------------------------------------------------------------------- #
# PR helper                                                                    #
# --------------------------------------------------------------------------- #
def find_open_pr(branch_name):
    existing = api_request(
        "GET",
        f"/repos/{REPO_FULL_NAME}/pulls",
        per_page=100,
    ) or []
    for pr in existing:
        if pr.get("head", {}).get("ref") == branch_name and pr.get("state") == "open":
            return pr
    return None


def create_or_update_pr(branch_name, body):
    """Create the weekly PR (or update the body if one already exists)."""
    existing = find_open_pr(branch_name)
    payload = {
        "title": f"Weekly compliance audit sync - {date.today().isoformat()}",
        "head": branch_name,
        "base": DEFAULT_BRANCH,
        "body": body,
    }
    if existing:
        return api_request("PATCH", f"/repos/{REPO_FULL_NAME}/pulls/{existing['number']}", payload=payload)
    return api_request("POST", f"/repos/{REPO_FULL_NAME}/pulls", payload=payload)


# --------------------------------------------------------------------------- #
# Main                                                                         #
# --------------------------------------------------------------------------- #
def main():
    if not GITHUB_TOKEN:
        sys.exit("GITHUB_TOKEN is required (set the environment variable).")

    run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"[1/5] Fetching open issues from {REPO_FULL_NAME} ...")
    raw_issues = fetch_all_open_issues()
    issues = [extract_issue_fields(i) for i in raw_issues]
    print(f"      -> {len(issues)} open issues fetched.")

    print("[2/5] Building compliance summary Markdown ...")
    markdown_block = build_markdown(issues, run_date)

    print(f"[3/5] Updating {README_PATH} between the compliance markers ...")
    update_readme(markdown_block)

    branch_name = f"automation/compliance-{date.today().isoformat()}"
    print(f"[4/5] Committing and pushing branch {branch_name} ...")
    create_and_push_branch(branch_name)

    print("[5/5] Opening / updating the weekly Pull Request ...")
    pr = create_or_update_pr(
        branch_name,
        body=(
            f"## Weekly Compliance Audit Sync\n\n"
            f"Automated sync executed on **{run_date}**.\n\n"
            f"### Summary\n"
            f"- **{len(issues)}** open compliance issues tracked.\n"
            f"- Updated the **Weekly Compliance Audit Summary** section in "
            f"`README.md` (between the compliance markers).\n\n"
            f"### Changes\n"
            f"- Overall statistics table refreshed.\n"
            f"- Per-country (UK / FR / DE) priority distribution refreshed.\n"
            f"- High-risk (P0/P1) open item lists (top 10 per country) refreshed.\n\n"
            f"Generated automatically by `.github/workflows/weekly-compliance-sync.yml`.\n"
        ),
    )
    print(f"      -> PR #{pr['number']}: {pr['html_url']}")

    print("Done.")


if __name__ == "__main__":
    main()
