"""Publish synchronized skill updates into Example Vault as an automated PR."""
from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from sync_skill import LOCK, ROOT, digest, git, synchronize

BRANCH = "automation/sync-skill"
BOT_NAME = "github-actions[bot]"
BOT_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"


def api(method: str, path: str, payload=None, token: str | None = None):
    token = token or os.environ.get("GH_TOKEN") or os.environ.get("VAULT_SYNC_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("Missing GitHub API token (GH_TOKEN or VAULT_SYNC_TOKEN)")
    req = urllib.request.Request(
        "https://api.github.com" + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "vault-skill-sync",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            body = resp.read()
            return json.loads(body) if body else None
    except urllib.error.HTTPError as err:
        body = json.loads(err.read())
        raise RuntimeError(f"GitHub {err.code}: {body.get('message', 'request failed')}") from None


def run(*args: str, cwd: Path = ROOT):
    subprocess.run(args, cwd=str(cwd), check=True)


def main():
    root = ROOT
    upstream_dir = root / ".upstream-skill"
    if not upstream_dir.is_dir():
        raise ValueError(f"Upstream skill directory not found: {upstream_dir}")

    target_repo = os.environ.get("GITHUB_REPOSITORY", "Bowen-0x00/obsidian-excalidraw-example-vault")
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    event = json.loads(Path(event_path).read_text(encoding="utf-8")) if event_path and Path(event_path).is_file() else {}

    commit = git(upstream_dir, "rev-parse", "HEAD")
    if os.environ.get("GITHUB_EVENT_NAME") == "repository_dispatch":
        payload = event.get("client_payload", {})
        requested = payload.get("sha")
        if requested and len(requested) == 40 and all(c in "0123456789abcdef" for c in requested):
            try:
                git(upstream_dir, "merge-base", "--is-ancestor", requested, "HEAD")
                commit = requested
            except Exception:
                pass

    print(f"Synchronizing skill from upstream commit: {commit}")
    result = synchronize(root, upstream_dir, commit, apply=True)
    if not result["changed"]:
        print("No skill file changes detected; no PR churn.")
        return

    prefix = f"/repos/{target_repo}"
    owner = target_repo.split("/")[0]
    pulls = api("GET", f"{prefix}/pulls?state=open&head={owner}:{BRANCH}")
    remote_heads = git(root, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    previous_sha = remote_heads.split()[0] if remote_heads else ""

    if previous_sha:
        git(root, "fetch", "origin", BRANCH)
        branch_tip = git(root, "rev-parse", "FETCH_HEAD")
        authors = set(git(root, "log", "--format=%ae", f"origin/main..{branch_tip}").splitlines())
        if authors and not authors <= {BOT_EMAIL}:
            raise ValueError("Sync branch has non-bot edits; refusing to overwrite")

    run("git", "config", "user.name", BOT_NAME)
    run("git", "config", "user.email", BOT_EMAIL)

    run("git", "checkout", "-B", BRANCH)
    run("git", "add", "--", *result["paths"])

    staged = git(root, "diff", "--cached", "--name-only").splitlines()
    if not staged:
        print("Working tree clean after staging; no changes to commit.")
        return

    commit_msg = f"chore(skill): sync obsidian-excalidraw skill updates ({commit[:7]})\n\nSource: https://github.com/{result['repository']}/commit/{commit}"
    run("git", "commit", "-m", commit_msg)

    token = os.environ.get("GH_TOKEN") or os.environ.get("VAULT_SYNC_TOKEN") or os.environ.get("GITHUB_TOKEN")
    remote_url = f"https://x-access-token:{token}@github.com/{target_repo}.git"

    if previous_sha:
        run("git", "push", f"--force-with-lease=refs/heads/{BRANCH}:{previous_sha}", remote_url, f"HEAD:refs/heads/{BRANCH}")
    else:
        run("git", "push", "-u", remote_url, f"HEAD:refs/heads/{BRANCH}")

    rows = [
        f"| `{c['target']}` | `{c['oldSha']}` | `{c['newSha']}` |"
        for c in result["changes"][:30]
    ]
    truncated_msg = f"\n*...and {len(result['changes']) - 30} more files.*" if len(result['changes']) > 30 else ""

    body = (
        f"Automated skill synchronization from [{result['repository']}@{commit[:7]}](https://github.com/{result['repository']}/commit/{commit}).\n\n"
        "### Sync Targets\n"
        "- `.omp/skills/obsidian-excalidraw/`\n"
        "- `.claude/skills/obsidian-excalidraw/`\n\n"
        "### Changes Summary\n"
        "| File Path | Previous SHA (12) | New SHA (12) |\n"
        "|---|---|---|\n" + "\n".join(rows) + truncated_msg + "\n\n"
        f"Source commit: `{commit}`\n"
    )
    title = f"chore(skill): sync obsidian-excalidraw skill ({commit[:7]})"

    if pulls:
        pr_number = pulls[0]["number"]
        pull = api("PATCH", f"{prefix}/pulls/{pr_number}", {"title": title, "body": body})
        print(f"Updated existing PR #{pr_number}: {pull['html_url']}")
    else:
        pull = api("POST", f"{prefix}/pulls", {"title": title, "body": body, "head": BRANCH, "base": "main"})
        print(f"Created new PR #{pull['number']}: {pull['html_url']}")

    # Auto-merge verified skill PR once mergeable
    pr_id = pulls[0]["number"] if pulls else pull["number"]
    for attempt in range(6):
        time.sleep(3)
        try:
            pr_info = api("GET", f"{prefix}/pulls/{pr_id}")
            if pr_info.get("mergeable") is True:
                merge_res = api("PUT", f"{prefix}/pulls/{pr_id}/merge", {
                    "merge_method": "merge",
                    "commit_title": f"chore(skill): auto-merge sync PR #{pr_id} ({commit[:7]})"
                })
                print(f"Successfully auto-merged skill PR #{pr_id}: {merge_res.get('message', 'success')}")
                break
            elif pr_info.get("merged") is True:
                print(f"PR #{pr_id} is already merged.")
                break
        except Exception as err:
            print(f"Auto-merge attempt {attempt + 1}: {err}")

    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as s:
            s.write(f"### Skill Sync PR\n{pull['html_url']}\n\nUpstream Commit: `{commit}`\n")


if __name__ == "__main__":
    main()
