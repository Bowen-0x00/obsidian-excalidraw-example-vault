"""Synchronize plugin build artifacts from obsidian-excalidraw-plugin-ymjr to Example Vault.

Copies only:
- main.js
- manifest.json
- styles.css
Explicitly NEVER touches data.json or other configuration files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_PLUGIN_DIR = ".obsidian/plugins/obsidian-excalidraw-plugin-ymjr"
SOURCE_REPO = "Bowen-0x00/obsidian-excalidraw-plugin-ymjr"
SYNCED_FILES = ["main.js", "manifest.json", "styles.css"]


def git(directory: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(directory), *args], check=True,
                          capture_output=True, encoding="utf-8").stdout.strip()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def synchronize(vault_root: Path, upstream_dir: Path, source_commit: str, *, apply: bool = False) -> dict:
    target_dir = vault_root / TARGET_PLUGIN_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    changes = []
    staged: dict[str, bytes] = {}

    # Read upstream manifest for version
    upstream_manifest_file = upstream_dir / "manifest.json"
    if not upstream_manifest_file.is_file():
        raise FileNotFoundError(f"Upstream manifest.json not found in {upstream_dir}")

    manifest_data = json.loads(upstream_manifest_file.read_text(encoding="utf-8"))
    version = manifest_data.get("version", "unknown")

    for filename in SYNCED_FILES:
        if filename == "data.json":
            # Extra safety check: NEVER touch data.json
            continue

        src_file = upstream_dir / filename
        if not src_file.is_file():
            raise FileNotFoundError(f"Required upstream file missing: {filename}")

        src_bytes = src_file.read_bytes()
        src_sha = digest(src_bytes)

        dst_file = target_dir / filename
        dst_bytes = dst_file.read_bytes() if dst_file.is_file() else b""
        dst_sha = digest(dst_bytes) if dst_bytes else ""

        rel_dst = f"{TARGET_PLUGIN_DIR}/{filename}"

        if src_sha != dst_sha:
            changes.append({
                "file": filename,
                "path": rel_dst,
                "oldSha": dst_sha[:12] if dst_sha else "none",
                "newSha": src_sha[:12],
            })
            staged[rel_dst] = src_bytes

    result = {
        "repository": SOURCE_REPO,
        "sourceCommit": source_commit,
        "version": version,
        "changes": changes,
        "changed": bool(changes),
        "paths": list(staged.keys()),
    }

    if apply and changes:
        for rel_path, content in staged.items():
            dest = vault_root / rel_path
            dest.write_bytes(content)

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
