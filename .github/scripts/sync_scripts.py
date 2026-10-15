"""Synchronize upstream Excalidraw scripts into Example Vault.

Preserves vault folder hierarchy (whether flattened or categorized).
Only updates scripts that ALREADY exist in the vault; skips new/missing scripts.
Tracks source commit, versions, and SHA-256 hashes in .github/scripts-sync.lock.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
LOCK = ".github/scripts-sync.lock.json"
SOURCE_REPO = "Bowen-0x00/obsidian-excalidraw-scripts"


def git(directory: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(directory), *args], check=True,
                          capture_output=True, encoding="utf-8").stdout.strip()


def normalized(raw: bytes) -> bytes:
    if len(raw) > 5 * 1024 * 1024 or b"\0" in raw:
        raise ValueError("Script file is binary or exceeds 5 MiB")
    return raw.decode("utf-8").replace("\r\n", "\n").encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(normalized(raw)).hexdigest()


def extract_version(raw: bytes) -> str:
    try:
        text = normalized(raw).decode("utf-8")
        header = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
        if header:
            found = re.search(r"^version:\s*(\S.*?)\s*$", header[1], re.M)
            if found:
                return found[1]
    except Exception:
        pass
    return "unknown"


def discover_vault_scripts(vault_root: Path) -> dict[str, list[str]]:
    """Scan vault for existing script markdown files, indexed by filename."""
    vault_scripts: dict[str, list[str]] = {}
    ignored_dirs = {".git", ".obsidian", ".upstream-scripts", ".upstream-plugin", "node_modules"}
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        rel_root = Path(root).relative_to(vault_root).as_posix()
        # Look for scripts inside directories containing 'Scripts' or 'scripts'
        parts = [p.lower() for p in PurePosixPath(rel_root).parts]
        if "scripts" in parts:
            for f in files:
                if f.endswith(".md"):
                    rel_path = (Path(root, f).relative_to(vault_root)).as_posix()
                    vault_scripts.setdefault(f, []).append(rel_path)
    return vault_scripts


def discover_upstream_scripts(upstream_dir: Path) -> dict[str, tuple[str, Path]]:
    """Scan upstream Scripts directory for script files, indexed by filename."""
    upstream_scripts: dict[str, tuple[str, Path]] = {}
    scripts_dir = upstream_dir / "Scripts" if (upstream_dir / "Scripts").is_dir() else upstream_dir
    for root, _, files in os.walk(scripts_dir):
        for f in files:
            if f.endswith(".md") and f != "index.md" and f != "temp.md":
                abs_path = Path(root, f)
                rel_path = abs_path.relative_to(upstream_dir).as_posix()
                upstream_scripts[f] = (rel_path, abs_path)
    return upstream_scripts


def synchronize(vault_root: Path, upstream_dir: Path, source_commit: str, *, apply: bool = False) -> dict:
    lock_file = vault_root / LOCK
    old_lock = {}
    if lock_file.is_file():
        try:
            old_lock = json.loads(lock_file.read_text(encoding="utf-8"))
        except Exception:
            old_lock = {}

    vault_scripts = discover_vault_scripts(vault_root)
    upstream_scripts = discover_upstream_scripts(upstream_dir)

    changes = []
    staged_files: dict[str, bytes] = {}
    new_records: dict[str, dict] = {}

    # Match existing scripts in vault with upstream scripts
    for filename, vault_paths in sorted(vault_scripts.items()):
        if filename not in upstream_scripts:
            # Script exists in vault but not in upstream - keep as is, do not touch
            continue

        src_rel, src_abs = upstream_scripts[filename]
        upstream_raw = src_abs.read_bytes()
        upstream_norm = normalized(upstream_raw)
        upstream_sha = digest(upstream_norm)
        upstream_ver = extract_version(upstream_norm)

        for v_path in vault_paths:
            target_file = vault_root / v_path
            current_raw = target_file.read_bytes() if target_file.is_file() else b""
            current_sha = digest(current_raw) if current_raw else ""
            current_ver = extract_version(current_raw) if current_raw else "missing"

            new_records[v_path] = {
                "source": src_rel,
                "sha256": upstream_sha,
                "version": upstream_ver,
            }

            if current_sha != upstream_sha:
                changes.append({
                    "source": src_rel,
                    "target": v_path,
                    "oldVersion": current_ver,
                    "newVersion": upstream_ver,
                    "oldSha": current_sha[:12],
                    "newSha": upstream_sha[:12],
                })
                staged_files[v_path] = upstream_norm

            # Also check for companion .svg icon
            svg_name = Path(filename).stem + ".svg"
            upstream_svg = src_abs.with_name(svg_name)
            target_svg = target_file.with_name(svg_name)
            target_svg_rel = Path(v_path).with_name(svg_name).as_posix()
            if target_svg.is_file() and upstream_svg.is_file():
                up_svg_raw = upstream_svg.read_bytes()
                up_svg_norm = normalized(up_svg_raw)
                up_svg_sha = digest(up_svg_norm)
                cur_svg_sha = digest(target_svg.read_bytes())
                if cur_svg_sha != up_svg_sha:
                    changes.append({
                        "source": upstream_svg.relative_to(upstream_dir).as_posix(),
                        "target": target_svg_rel,
                        "oldVersion": "svg",
                        "newVersion": "svg",
                        "oldSha": cur_svg_sha[:12],
                        "newSha": up_svg_sha[:12],
                    })
                    staged_files[target_svg_rel] = up_svg_norm

    result = {
        "repository": SOURCE_REPO,
        "sourceCommit": source_commit,
        "matchedCount": len(new_records),
        "changes": changes,
        "changed": bool(changes),
        "paths": list(staged_files.keys()),
    }

    if apply and changes:
        for rel_path, content in staged_files.items():
            dest = vault_root / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)

        new_lock = {
            "schemaVersion": 1,
            "source": {
                "repository": SOURCE_REPO,
                "commit": source_commit,
            },
            "matchedCount": len(new_records),
            "files": new_records,
        }
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.write_text(json.dumps(new_lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["paths"].append(LOCK)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "plan", "apply"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--upstream", type=Path)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    if args.command == "check":
        lock_file = args.root / LOCK
        if not lock_file.is_file():
            print(json.dumps({"valid": True, "locked": False, "message": "No lock file present"}))
            return 0
        lock_data = json.loads(lock_file.read_text(encoding="utf-8"))
        mismatched = []
        for v_path, info in lock_data.get("files", {}).items():
            target_path = args.root / v_path
            if not target_path.is_file():
                mismatched.append({"path": v_path, "error": "file missing"})
                continue
            sha = digest(target_path.read_bytes())
            if sha != info["sha256"]:
                mismatched.append({"path": v_path, "error": f"hash mismatch ({sha[:12]} != {info['sha256'][:12]})"})
        if mismatched:
            print(json.dumps({"valid": False, "mismatched": mismatched}, indent=2))
            return 1
        print(json.dumps({"valid": True, "filesChecked": len(lock_data.get("files", {}))}, indent=2))
        return 0

    if not args.upstream:
        parser.error("plan and apply require --upstream directory")

    commit = args.source_commit
    if not commit:
        try:
            commit = git(args.upstream, "rev-parse", "HEAD")
        except Exception:
            commit = "unknown"

    result = synchronize(args.root, args.upstream, commit, apply=(args.command == "apply"))
    report = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.write_text(report, encoding="utf-8")
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
