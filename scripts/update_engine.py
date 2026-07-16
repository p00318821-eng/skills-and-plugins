"""
Update engine: check each tracked skill in manifests/origins.json against its
upstream repo, diff subpath vs. local skills/<name>, and apply chosen updates.

Supersedes update-sourced-skills.ipynb's inline helpers AND scripts/sync_engine.py's
formerly-unused clone_upstream/extract_skill_content/fetch_skill (removed from
sync_engine.py — this is now the single implementation of "clone upstream, diff
vs. local, apply selected updates, stamp last_synced_sha").

Skills with "forked": true (e.g. domain-modeling, caveman) are intentionally
modified vendor forks: a plain local-vs-HEAD diff would permanently flag every
forked line as "changed" even though nothing new happened upstream. For these,
scan_forked_skill() does a three-way diff instead: it also fetches upstream at
the historical "last_synced_sha" anchor (via clone_upstream_at_sha, a single
commit fetched by full SHA rather than a branch-tip shallow clone) and reports
anchor-vs-HEAD as genuine upstream drift (has_update-driving) and local-vs-anchor
as the known, expected fork_delta (informational only, never auto-applied).
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
_head_sha_cache: dict[tuple[str, str], str] = {}


def get_remote_head_sha(repo: str, branch: str, cache: dict | None = None) -> str:
    """Cheap ref-only check (git ls-remote, no tree data transferred) so
    check_all() can skip a full shallow clone for anything whose HEAD hasn't
    moved since last_synced_sha. Memoized per (repo, branch) like clone_upstream,
    since several manifest entries often share one upstream repo."""
    cache = _head_sha_cache if cache is None else cache
    key = (repo, branch)
    if key not in cache:
        out = _run(["git", "ls-remote", repo, f"refs/heads/{branch}"])
        if not out:
            raise RuntimeError(f"branch not found on remote: {repo}@{branch}")
        cache[key] = out.split()[0]
    return cache[key]


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


_sha_clone_cache: dict[tuple[str, str], Path] = {}


def clone_upstream_at_sha(repo: str, sha: str, cache: dict | None = None) -> Path:
    """Fetch a single historical commit by full SHA — the three-way-diff anchor
    for forked skills. Distinct from clone_upstream's branch-tip shallow clone:
    requires the full 40-char SHA (GitHub's smart-HTTP want-by-SHA support
    rejects abbreviated forms), fetched via `git fetch --depth 1 origin <sha>`
    into a bare init'd repo rather than `git clone --branch`."""
    cache = _sha_clone_cache if cache is None else cache
    key = (repo, sha)
    if key not in cache:
        dest = Path(tempfile.mkdtemp(prefix="skillsrc_sha_"))
        _run(["git", "init", str(dest)])
        _run(["git", "remote", "add", "origin", repo], cwd=dest)
        _run(["git", "fetch", "--depth", "1", "origin", sha], cwd=dest)
        _run(["git", "checkout", "FETCH_HEAD"], cwd=dest)
        cache[key] = dest
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
    skipped_clone: bool = False
    fork_delta: list[str] = field(default_factory=list)
    base_files: dict[str, Path] | None = None
    base_dir: Path | None = None


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


def scan_forked_skill(repo_root: Path, skill: dict, ignore: set[str]) -> UpdateReport:
    """Three-way diff for a forked skill. added/modified/local_only mean
    upstream drift (anchor last_synced_sha vs upstream HEAD) here, not
    local vs HEAD — has_update is driven by drift alone. fork_delta (local
    vs anchor) is the known, expected fork edit, reported separately and
    never treated as an update."""
    up_root, head_sha = clone_upstream(skill["repo"], skill["branch"])
    base_root = clone_upstream_at_sha(skill["repo"], skill["last_synced_sha"])

    up_dir = (up_root / skill["subpath"]) if skill["subpath"] else up_root
    base_dir = (base_root / skill["subpath"]) if skill["subpath"] else base_root
    local_dir = repo_root / skill["local"]

    up_files = list_upstream_files(up_dir, ignore)
    base_files = list_upstream_files(base_dir, ignore)
    local_files = list_upstream_files(local_dir, ignore)

    added, modified, local_only = [], [], []
    for rel, up_path in sorted(up_files.items()):
        bp = base_files.get(rel)
        if bp is None:
            added.append(rel)
        elif up_path.read_bytes() != bp.read_bytes():
            modified.append(rel)
    for rel in sorted(base_files):
        if rel not in up_files:
            local_only.append(rel)

    fork_delta = []
    for rel, base_path in sorted(base_files.items()):
        lp = local_files.get(rel)
        if lp is None or lp.read_bytes() != base_path.read_bytes():
            fork_delta.append(rel)
    for rel in sorted(local_files):
        if rel not in base_files:
            fork_delta.append(rel)

    return UpdateReport(
        skill=skill, head_sha=head_sha, up_files=up_files, local_dir=local_dir,
        added=added, modified=modified, local_only=local_only,
        has_update=bool(added or modified), fork_delta=sorted(set(fork_delta)),
        base_files=base_files, base_dir=base_dir,
    )


def unified_diff_for(up_path: Path, local_path: Path, rel: str) -> str:
    try:
        up = up_path.read_text(encoding="utf-8").splitlines(keepends=True)
        lo = local_path.read_text(encoding="utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        return f"(binary file '{rel}' differs)\n"
    return "".join(difflib.unified_diff(lo, up, fromfile=f"local/{rel}", tofile=f"upstream/{rel}"))


def check_all(repo_root: Path) -> dict[str, UpdateReport]:
    """Loads origins.json fresh, checks each tracked skill for updates.
    Ref-only pre-check first (git ls-remote — no tree data): if the upstream
    branch HEAD still matches last_synced_sha, skip the full shallow clone
    entirely and report unchanged. Only clones for skills whose HEAD moved
    (or that have never been synced)."""
    origins_path = repo_root / "manifests" / "origins.json"
    manifest = json.loads(origins_path.read_text(encoding="utf-8"))
    ignore = set(manifest.get("ignore", []))

    results: dict[str, UpdateReport] = {}
    for skill in manifest["skills"]:
        name = skill["name"]
        try:
            last_sha = skill.get("last_synced_sha")
            if last_sha:
                head_sha = get_remote_head_sha(skill["repo"], skill["branch"])
                if head_sha == last_sha:
                    results[name] = UpdateReport(
                        skill=skill, head_sha=head_sha, up_files={},
                        local_dir=repo_root / skill["local"], skipped_clone=True,
                    )
                    continue
            if skill.get("forked"):
                results[name] = scan_forked_skill(repo_root, skill, ignore)
            else:
                results[name] = scan_skill(repo_root, skill, ignore)
        except Exception as e:
            results[name] = UpdateReport(
                skill=skill, head_sha="", up_files={}, local_dir=repo_root / skill["local"],
            )
            results[name].error = str(e)  # type: ignore[attr-defined]
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
            if rep.skipped_clone:
                lines.append("  up to date — HEAD unchanged since last sync, skipped clone.")
            else:
                lines.append("  up to date — no changes to apply.")
        else:
            lines.extend(f"      + (new)      {r}" for r in rep.added)
            lines.extend(f"      ~ (modified) {r}" for r in rep.modified)
        if rep.local_only:
            lines.append(f"  local-only (kept, never deleted): {', '.join(rep.local_only)}")
        if rep.fork_delta:
            lines.append(f"  known fork delta (expected, not an update): {', '.join(rep.fork_delta)}")
        if show_diffs and rep.modified:
            base_for_diff = rep.base_dir if rep.skill.get("forked") else rep.local_dir
            for r in rep.modified:
                lines.append("-" * 70)
                lines.append(unified_diff_for(rep.up_files[r], base_for_diff / r, r))

    lines.append("=" * 78)
    updatable = [n for n, r in results.items() if r.has_update]
    lines.append(f"Skills with updates available: {updatable or 'none'}")
    return "\n".join(lines)


def stamp_synced_shas(repo_root: Path, results: dict[str, UpdateReport]) -> list[str]:
    """For skills confirmed up to date this run (has_update=False, whether via
    the ref-only pre-check or a full clone+diff that found no changes), record
    last_synced_sha so the NEXT check_all() can skip the clone via
    get_remote_head_sha. Without this, a skill that's simply unchanged never
    accumulates a last_synced_sha (apply_decisions only stamps skills it
    actually applied), so the ref pre-check would never fire for it. Skills
    with a pending update are left untouched — apply_decisions() stamps those
    once the user actually applies the change."""
    origins_path = repo_root / "manifests" / "origins.json"
    manifest = json.loads(origins_path.read_text(encoding="utf-8"))

    stamped: list[str] = []
    for s in manifest["skills"]:
        rep = results.get(s["name"])
        if not rep or getattr(rep, "error", None) or rep.has_update or not rep.head_sha:
            continue
        if s.get("last_synced_sha") != rep.head_sha:
            s["last_synced_sha"] = rep.head_sha
            stamped.append(s["name"])

    if stamped:
        origins_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
        )
    return stamped


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
        if rep.skill.get("forked"):
            skipped.append(
                f"{name} (forked skill — merge upstream drift by hand, then call "
                "acknowledge_upstream_drift() instead of applying)"
            )
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


def acknowledge_upstream_drift(repo_root: Path, name: str, results: dict[str, UpdateReport]) -> bool:
    """For a forked skill: after a human has manually merged whatever upstream
    drift they wanted from the report, reset the three-way-diff anchor by
    stamping last_synced_sha = head_sha — without touching any local files.
    This is the only way a forked skill's last_synced_sha ever advances;
    apply_decisions() deliberately refuses to do it via a normal 'apply'.
    Returns True if stamped, False if there was nothing to acknowledge."""
    rep = results.get(name)
    if not rep or not rep.skill.get("forked") or not rep.has_update or not rep.head_sha:
        return False

    origins_path = repo_root / "manifests" / "origins.json"
    manifest = json.loads(origins_path.read_text(encoding="utf-8"))
    for s in manifest["skills"]:
        if s["name"] == name:
            s["last_synced_sha"] = rep.head_sha
    origins_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    return True
