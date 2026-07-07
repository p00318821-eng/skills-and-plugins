"""
Update engine: check each tracked skill in manifests/origins.json against its
upstream repo, diff subpath vs. local skills/<name>, and apply chosen updates.

Supersedes update-sourced-skills.ipynb's inline helpers AND scripts/sync_engine.py's
formerly-unused clone_upstream/extract_skill_content/fetch_skill (removed from
sync_engine.py — this is now the single implementation of "clone upstream, diff
vs. local, apply selected updates, stamp last_synced_sha").
"""

from __future__ import annotations

import difflib
import json
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for p in [start, *start.parents]:
        if (p / "manifests" / "origins.json").is_file():
            return p
    raise FileNotFoundError("manifests/origins.json not found in CWD or any parent.")


def _run(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout.strip()


_clone_cache: dict[tuple[str, str], tuple[Path, str]] = {}


def clone_upstream(repo: str, branch: str, cache: dict | None = None) -> tuple[Path, str]:
    """Shallow-clone a repo once per session; returns (path, head_sha).
    `cache` defaults to a module-level dict so callers don't have to manage
    the process-lifetime clone cache themselves."""
    cache = _clone_cache if cache is None else cache
    key = (repo, branch)
    if key not in cache:
        dest = Path(tempfile.mkdtemp(prefix="skillsrc_"))
        _run(["git", "clone", "--depth", "1", "--branch", branch, repo, str(dest)])
        sha = _run(["git", "rev-parse", "HEAD"], cwd=dest)
        cache[key] = (dest, sha)
    return cache[key]


def list_upstream_files(root: Path, ignore: set[str]) -> dict[str, Path]:
    out: dict[str, Path] = {}
    if root.is_dir():
        for p in root.rglob("*"):
            if p.is_file():
                rel = p.relative_to(root)
                if not any(part in ignore for part in rel.parts):
                    out[rel.as_posix()] = p
    return out


@dataclass
class UpdateReport:
    skill: dict
    head_sha: str
    up_files: dict[str, Path]
    local_dir: Path
    added: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    local_only: list[str] = field(default_factory=list)
    has_update: bool = False


def scan_skill(repo_root: Path, skill: dict, ignore: set[str]) -> UpdateReport:
    up_root, head_sha = clone_upstream(skill["repo"], skill["branch"])
    up_dir = (up_root / skill["subpath"]) if skill["subpath"] else up_root
    local_dir = repo_root / skill["local"]
    up_files = list_upstream_files(up_dir, ignore)
    local_files = list_upstream_files(local_dir, ignore)

    added, modified, local_only = [], [], []
    for rel, up_path in sorted(up_files.items()):
        lp = local_files.get(rel)
        if lp is None:
            added.append(rel)
        elif up_path.read_bytes() != lp.read_bytes():
            modified.append(rel)
    for rel in sorted(local_files):
        if rel not in up_files:
            local_only.append(rel)

    return UpdateReport(
        skill=skill, head_sha=head_sha, up_files=up_files, local_dir=local_dir,
        added=added, modified=modified, local_only=local_only,
        has_update=bool(added or modified),
    )


def unified_diff_for(up_path: Path, local_path: Path, rel: str) -> str:
    try:
        up = up_path.read_text(encoding="utf-8").splitlines(keepends=True)
        lo = local_path.read_text(encoding="utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        return f"(binary file '{rel}' differs)\n"
    return "".join(difflib.unified_diff(lo, up, fromfile=f"local/{rel}", tofile=f"upstream/{rel}"))


def check_all(repo_root: Path) -> dict[str, UpdateReport]:
    """Loads origins.json fresh, calls scan_skill for every tracked skill."""
    origins_path = repo_root / "manifests" / "origins.json"
    manifest = json.loads(origins_path.read_text(encoding="utf-8"))
    ignore = set(manifest.get("ignore", []))

    results: dict[str, UpdateReport] = {}
    for skill in manifest["skills"]:
        try:
            results[skill["name"]] = scan_skill(repo_root, skill, ignore)
        except Exception as e:
            results[skill["name"]] = UpdateReport(
                skill=skill, head_sha="", up_files={}, local_dir=repo_root / skill["local"],
            )
            results[skill["name"]].error = str(e)  # type: ignore[attr-defined]
    return results


def format_update_report(results: dict[str, UpdateReport], show_diffs: bool = True) -> str:
    lines = []
    for name, rep in results.items():
        lines.append("=" * 78)
        lines.append(f"{name}   (last synced: {rep.skill.get('last_synced_sha') or 'never'})")
        error = getattr(rep, "error", None)
        if error:
            lines.append(f"  !! could not check: {error}")
            continue
        lines.append(f"  upstream HEAD: {rep.head_sha}")
        if not rep.has_update:
            lines.append("  up to date — no changes to apply.")
        else:
            lines.extend(f"      + (new)      {r}" for r in rep.added)
            lines.extend(f"      ~ (modified) {r}" for r in rep.modified)
        if rep.local_only:
            lines.append(f"  local-only (kept, never deleted): {', '.join(rep.local_only)}")
        if show_diffs and rep.modified:
            for r in rep.modified:
                lines.append("-" * 70)
                lines.append(unified_diff_for(rep.up_files[r], rep.local_dir / r, r))

    lines.append("=" * 78)
    updatable = [n for n, r in results.items() if r.has_update]
    lines.append(f"Skills with updates available: {updatable or 'none'}")
    return "\n".join(lines)


def apply_update(repo_root: Path, report: UpdateReport) -> list[str]:
    """Copies added+modified files into local_dir. Returns list of copied paths."""
    copied = []
    for rel in report.added + report.modified:
        dst = report.local_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(report.up_files[rel].read_bytes())
        copied.append(rel)
    return copied


def apply_decisions(
    repo_root: Path, results: dict[str, UpdateReport], decisions: dict[str, str],
) -> dict[str, list[str]]:
    """For each 'apply' decision, copies files + stamps last_synced_sha; writes
    origins.json once at the end (loaded fresh inside this call). Returns
    {'applied': [...], 'skipped': [...]}."""
    origins_path = repo_root / "manifests" / "origins.json"
    manifest = json.loads(origins_path.read_text(encoding="utf-8"))

    applied: list[str] = []
    skipped: list[str] = []
    for name, decision in decisions.items():
        rep = results.get(name)
        if str(decision).strip().lower() != "apply" or not rep or not rep.has_update:
            skipped.append(name)
            continue
        apply_update(repo_root, rep)
        for s in manifest["skills"]:
            if s["name"] == name:
                s["last_synced_sha"] = rep.head_sha
        applied.append(name)

    if applied:
        origins_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
        )

    return {"applied": applied, "skipped": skipped}
