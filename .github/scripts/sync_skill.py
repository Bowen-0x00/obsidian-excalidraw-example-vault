"""Synchronize obsidian-excalidraw skill into Example Vault (.omp and .claude).

Copies skills/obsidian-excalidraw from upstream to:
- .omp/skills/obsidian-excalidraw
- .claude/skills/obsidian-excalidraw
Maintains a lock file at .github/skill-sync.lock.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCK = ".github/skill-sync.lock.json"
SOURCE_REPO = "Bowen-0x00/obsidian-excalidraw-agent-skill"
TARGET_DIRS = [
    ".omp/skills/obsidian-excalidraw",
    ".claude/skills/obsidian-excalidraw",
]


def git(directory: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(directory), *args], check=True,
                          capture_output=True, encoding="utf-8").stdout.strip()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scan_dir(base_dir: Path) -> dict[str, bytes]:
    """Scan directory recursively and return relative_path -> file_bytes."""
    res = {}
    if not base_dir.is_dir():
        return res
    for root, _, files in os.walk(base_dir):
        for f in files:
            p = Path(root, f)
            rel = p.relative_to(base_dir).as_posix()
            res[rel] = p.read_bytes()
    return res


def synchronize(vault_root: Path, upstream_dir: Path, source_commit: str, *, apply: bool = False) -> dict:
    source_skill_dir = upstream_dir / "skills" / "obsidian-excalidraw"
    if not source_skill_dir.is_dir():
        raise FileNotFoundError(f"Upstream skill directory missing: {source_skill_dir}")

    source_files = scan_dir(source_skill_dir)
    lock_file = vault_root / LOCK
    old_lock = {}
    if lock_file.is_file():
        try:
            old_lock = json.loads(lock_file.read_text(encoding="utf-8"))
        except Exception:
            old_lock = {}

    changes = []
    staged_paths = set()
    records = {}

    for rel_path, src_bytes in sorted(source_files.items()):
        src_sha = digest(src_bytes)
        records[rel_path] = src_sha

        for target_base in TARGET_DIRS:
            target_path = vault_root / target_base / rel_path
            dst_sha = digest(target_path.read_bytes()) if target_path.is_file() else ""
            vault_rel = f"{target_base}/{rel_path}"

            if src_sha != dst_sha:
                changes.append({
                    "target": vault_rel,
                    "file": rel_path,
                    "oldSha": dst_sha[:12] if dst_sha else "none",
                    "newSha": src_sha[:12],
                })
                staged_paths.add(vault_rel)

    # Check for removed files in targets
    for target_base in TARGET_DIRS:
        target_dir = vault_root / target_base
        existing_targets = scan_dir(target_dir)
        for existing_rel in existing_targets:
            if existing_rel not in source_files:
                vault_rel = f"{target_base}/{existing_rel}"
                changes.append({
                    "target": vault_rel,
                    "file": existing_rel,
                    "oldSha": digest(existing_targets[existing_rel])[:12],
                    "newSha": "deleted",
                })
                staged_paths.add(vault_rel)

    result = {
        "repository": SOURCE_REPO,
        "sourceCommit": source_commit,
        "changes": changes,
        "changed": bool(changes),
        "paths": sorted(list(staged_paths)),
    }

    if apply and changes:
        # Write files into each target
        for target_base in TARGET_DIRS:
            dest_dir = vault_root / target_base
            # Remove deleted files
            for c in changes:
                if c["newSha"] == "deleted" and c["target"].startswith(target_base):
                    p = vault_root / c["target"]
                    if p.is_file():
                        p.unlink()
            # Copy all current files
            for rel_path, src_bytes in source_files.items():
                p = dest_dir / rel_path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(src_bytes)

        new_lock = {
            "schemaVersion": 1,
            "source": {
                "repository": SOURCE_REPO,
                "commit": source_commit,
            },
            "files": records,
        }
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.write_text(json.dumps(new_lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["paths"].append(LOCK)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "apply"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--source-commit", default="")
    args = parser.parse_args()

    commit = args.source_commit
    if not commit:
        try:
            commit = git(args.upstream, "rev-parse", "HEAD")
        except Exception:
            commit = "unknown"

    res = synchronize(args.root, args.upstream, commit, apply=(args.command == "apply"))
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
