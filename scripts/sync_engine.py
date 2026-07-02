"""
Sync engine for skills-and-plugins distribution.

Reads manifests/origins.json and manifests/destinations.json,
builds a prompt cache from skill folders, and distributes to
configured destinations using two methods:
  - markdown-boundary: injects skill prompts between HTML comment markers
  - skill-folder-copy: copies entire skill folders to discovery directories
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

BOUNDARY_START = "<!-- MANAGED-SKILLS:START -->"
BOUNDARY_END = "<!-- MANAGED-SKILLS:END -->"

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for p in [start, *start.parents]:
        if (p / "manifests" / "origins.json").is_file():
            return p
    raise FileNotFoundError(
        "manifests/origins.json not found in CWD or any parent."
    )


def load_env(repo_root: Path) -> dict[str, str]:
    env_file = repo_root / ".env"
    if load_dotenv is not None and env_file.is_file():
        load_dotenv(env_file)
    elif env_file.is_file():
        print("WARNING: python-dotenv not installed; .env file ignored. "
              "Install with: py -m pip install python-dotenv")
    return dict(os.environ)


def resolve_path(template: str, repo_root: Path | None = None) -> Path:
    expanded = template.replace("{HOME}", str(Path.home()))
    if repo_root:
        expanded = expanded.replace("{REPO_ROOT}", str(repo_root))
    return Path(expanded)


def load_origins(repo_root: Path) -> dict:
    path = repo_root / "manifests" / "origins.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format_version", 1) < 2:
        raise ValueError(
            f"origins.json format_version {data.get('format_version')} < 2; "
            "migration required"
        )
    return data


def load_destinations(repo_root: Path) -> dict:
    path = repo_root / "manifests" / "destinations.json"
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Fetch (reuses existing notebook pattern)
# ---------------------------------------------------------------------------

def _run_git(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        args, cwd=cwd, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git command failed: {' '.join(args)}\n{result.stderr.strip()}"
        )
    return result.stdout.strip()


_clone_cache: dict[tuple[str, str], tuple[Path, str]] = {}


def clone_upstream(
    repo: str, branch: str, cache_dir: Path
) -> tuple[Path, str]:
    key = (repo, branch)
    if key not in _clone_cache:
        import tempfile
        dest = Path(tempfile.mkdtemp(prefix="skillsrc_"))
        _run_git([
            "git", "clone", "--depth", "1", "--branch", branch,
            repo, str(dest)
        ])
        sha = _run_git(["git", "rev-parse", "HEAD"], cwd=dest)
        _clone_cache[key] = (dest, sha)
    return _clone_cache[key]


def extract_skill_content(
    clone_path: Path, subpath: str, ignore: set[str]
) -> dict[str, Path]:
    root = (clone_path / subpath) if subpath else clone_path
    out: dict[str, Path] = {}
    if root.is_dir():
        for p in root.rglob("*"):
            if p.is_file():
                rel = p.relative_to(root)
                if not any(part in ignore for part in rel.parts):
                    out[rel.as_posix()] = p
    return out


def fetch_skill(
    skill: dict, cache_dir: Path, ignore: set[str]
) -> dict[str, Any]:
    try:
        clone_path, head_sha = clone_upstream(
            skill["repo"], skill["branch"], cache_dir
        )
        up_files = extract_skill_content(
            clone_path, skill.get("subpath", ""), ignore
        )
        return {
            "skill": skill,
            "head_sha": head_sha,
            "up_files": up_files,
            "status": "fetched",
        }
    except Exception as e:
        cached = cache_dir / "prompts" / f"{skill['name']}.md"
        return {
            "skill": skill,
            "head_sha": None,
            "up_files": {},
            "status": "offline-fallback" if cached.is_file() else "failed",
            "error": str(e),
        }


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

def cache_skill_prompt(
    skill_name: str, skill_dir: Path, cache_dir: Path
) -> Path | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return None
    dest = cache_dir / "prompts" / f"{skill_name}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(skill_md, dest)
    return dest


def build_prompt_cache(repo_root: Path, origins: dict) -> list[str]:
    cache_dir = repo_root / ".cache"
    cached: list[str] = []

    for skill in origins["skills"]:
        skill_dir = repo_root / skill["local"]
        result = cache_skill_prompt(skill["name"], skill_dir, cache_dir)
        if result:
            cached.append(skill["name"])

    for entry in origins.get("excluded", []):
        skill_dir = repo_root / entry["local"]
        result = cache_skill_prompt(entry["name"], skill_dir, cache_dir)
        if result:
            cached.append(entry["name"])

    return cached


# ---------------------------------------------------------------------------
# Distribute
# ---------------------------------------------------------------------------

def render_skills_block(
    skill_names: list[str], cache_dir: Path
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    parts = [
        BOUNDARY_START,
        f"<!-- Generated by skills-and-plugins sync engine. "
        f"Do not edit between these markers. -->",
        f"<!-- Last synced: {now} -->",
        "",
    ]

    for i, name in enumerate(skill_names):
        prompt_file = cache_dir / "prompts" / f"{name}.md"
        if not prompt_file.is_file():
            parts.append(f"<!-- MISSING: {name} (not in cache) -->")
            parts.append("")
            continue
        content = prompt_file.read_text(encoding="utf-8").strip()
        if i > 0:
            parts.append("---")
            parts.append("")
        parts.append(content)
        parts.append("")

    parts.append(BOUNDARY_END)
    return "\n".join(parts)


def inject_markdown(
    target_file: Path,
    block: str,
    *,
    create_if_missing: bool = True,
) -> str:
    if not target_file.is_file():
        if create_if_missing:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(block + "\n", encoding="utf-8")
            return "created"
        return "skipped"

    content = target_file.read_text(encoding="utf-8")
    start_idx = content.find(BOUNDARY_START)
    end_idx = content.find(BOUNDARY_END)

    if start_idx != -1 and end_idx != -1:
        if start_idx > end_idx:
            raise ValueError(
                f"Boundary markers in {target_file} are in wrong order "
                f"(END before START). Fix manually."
            )
        end_idx += len(BOUNDARY_END)
        new_content = content[:start_idx] + block + content[end_idx:]
        if new_content == content:
            return "unchanged"
        target_file.write_text(new_content, encoding="utf-8")
        return "updated"

    if start_idx == -1 and end_idx == -1:
        new_content = content.rstrip() + "\n\n" + block + "\n"
        target_file.write_text(new_content, encoding="utf-8")
        return "appended"

    raise ValueError(
        f"Corrupted boundary markers in {target_file}: "
        f"found {'START' if start_idx != -1 else 'END'} but not "
        f"{'END' if start_idx != -1 else 'START'}. Fix manually."
    )


def copy_skill_folder(
    skill_name: str,
    src_dir: Path,
    target_dir: Path,
) -> str:
    """Copy an entire skill folder to target_dir/{skill_name}/.

    Returns: 'created', 'updated', or 'unchanged'.
    """
    dest = target_dir / skill_name

    if not src_dir.is_dir():
        raise FileNotFoundError(f"Source skill folder not found: {src_dir}")

    if not dest.is_dir():
        shutil.copytree(src_dir, dest)
        return "created"

    # Compare file-by-file for idempotency
    changed = False
    src_files = {p.relative_to(src_dir) for p in src_dir.rglob("*") if p.is_file()}
    dest_files = {p.relative_to(dest) for p in dest.rglob("*") if p.is_file()}

    # Files to add or update
    for rel in src_files:
        src_file = src_dir / rel
        dst_file = dest / rel
        if not dst_file.is_file():
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            changed = True
        elif src_file.read_bytes() != dst_file.read_bytes():
            shutil.copy2(src_file, dst_file)
            changed = True

    # Files to remove (exist in dest but not in source)
    for rel in dest_files - src_files:
        (dest / rel).unlink()
        changed = True

    # Clean up empty directories after removals
    for dirpath in sorted(dest.rglob("*"), reverse=True):
        if dirpath.is_dir() and not any(dirpath.iterdir()):
            dirpath.rmdir()

    return "updated" if changed else "unchanged"


def distribute_folder_copy(
    destination: dict,
    repo_root: Path,
) -> dict[str, Any]:
    """Distribute skills via folder copy for a single destination."""
    dest_id = destination["id"]
    target_dir = resolve_path(destination["target_dir"], repo_root)
    skills = destination.get("skills_assigned", [])

    if not skills:
        return {"id": dest_id, "status": "skipped", "detail": "no skills assigned"}

    target_dir.mkdir(parents=True, exist_ok=True)

    per_skill: list[dict] = []
    for name in skills:
        src = repo_root / "skills" / name
        try:
            status = copy_skill_folder(name, src, target_dir)
            per_skill.append({"name": name, "status": status})
        except Exception as e:
            per_skill.append({"name": name, "status": "error", "detail": str(e)})

    # Clean up skills no longer assigned
    removed: list[str] = []
    assigned_set = set(skills)
    for child in target_dir.iterdir():
        if child.is_dir() and child.name not in assigned_set:
            shutil.rmtree(child)
            removed.append(child.name)

    # Summarize
    counts = {}
    for ps in per_skill:
        counts[ps["status"]] = counts.get(ps["status"], 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in counts.items())
    if removed:
        summary += f", removed: {removed}"

    return {
        "id": dest_id,
        "status": "ok",
        "detail": f"{target_dir} — {summary}",
        "per_skill": per_skill,
        "removed": removed,
    }


def distribute_to_destination(
    destination: dict, cache_dir: Path, repo_root: Path
) -> dict[str, Any]:
    dest_id = destination["id"]

    if not destination.get("enabled", True):
        return {"id": dest_id, "status": "skipped", "detail": "disabled"}

    method = destination.get("method", "markdown-boundary")
    skills = destination.get("skills_assigned", [])

    if not skills:
        return {"id": dest_id, "status": "skipped", "detail": "no skills assigned"}

    if method == "markdown-boundary":
        target = resolve_path(destination["target_file"], repo_root)
        block = render_skills_block(skills, cache_dir)
        status = inject_markdown(target, block)
        return {"id": dest_id, "status": status, "detail": str(target)}

    if method == "skill-folder-copy":
        return distribute_folder_copy(destination, repo_root)

    return {
        "id": dest_id,
        "status": "skipped",
        "detail": f"unsupported method: {method}",
    }


def distribute_all(
    destinations: dict, cache_dir: Path, repo_root: Path
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for dest in destinations.get("destinations", []):
        try:
            result = distribute_to_destination(dest, cache_dir, repo_root)
        except Exception as e:
            result = {"id": dest.get("id", "?"), "status": "error", "detail": str(e)}
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

_STATUS_ICONS = {
    "created": "+",
    "updated": "~",
    "unchanged": "=",
    "appended": "+",
    "skipped": "-",
    "error": "!",
}


def format_report(
    fetch_results: list[dict] | None,
    distribute_results: list[dict],
) -> str:
    lines = ["", "=" * 60, "Sync Report", "=" * 60]

    if fetch_results:
        lines.append(f"\nFetch: {len(fetch_results)} skill(s) processed")
        for r in fetch_results:
            lines.append(f"  {r['status']:<20} {r['skill']['name']}")

    lines.append(f"\nDistribute: {len(distribute_results)} destination(s)")
    for r in distribute_results:
        icon = _STATUS_ICONS.get(r["status"], "?")
        lines.append(f"  [{icon}] {r['id']:<30} {r['status']} — {r.get('detail', '')}")

    lines.append("=" * 60)
    return "\n".join(lines)
