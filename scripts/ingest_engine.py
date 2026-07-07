"""
Ingest engine: scan a project's skill directory, compare against the central
repo, and apply classify/reconcile decisions into manifests/origins.json and
manifests/destinations.json.

Pure logic, no ipywidgets import — widget construction and display stay in the
notebook cells that call these functions. Supersedes the inline helpers in
ingest-project.ipynb and the CLI logic in the now-retired scripts/ingest-destination.py.
"""

from __future__ import annotations

import difflib
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for p in [start, *start.parents]:
        if (p / "manifests" / "origins.json").is_file():
            return p
    raise FileNotFoundError("manifests/origins.json not found in CWD or any parent.")


# ---------------------------------------------------------------------------
# Scan / compare
# ---------------------------------------------------------------------------

@dataclass
class ScanResult:
    source: Path
    dest_id: str
    repo_skills: dict[str, Path]
    project_skills: dict[str, Path]
    diff: dict[str, list[str]]
    changed: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)


def scan_skills_directory(path: Path) -> dict[str, Path]:
    """Scan directory for skill folders. Returns {skill_name: skill_path}."""
    skills: dict[str, Path] = {}
    if not path.is_dir():
        return skills
    for skill_dir in path.iterdir():
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file():
            skills[skill_dir.name] = skill_dir
    return skills


def compare_skills(repo_skills: dict[str, Path], project_skills: dict[str, Path]) -> dict:
    """Compare repo vs. project. Returns {status: [skill_names]}."""
    repo_names = set(repo_skills.keys())
    project_names = set(project_skills.keys())
    return {
        "new": sorted(project_names - repo_names),
        "existing": sorted(project_names & repo_names),
        "removed": sorted(repo_names - project_names),
    }


def check_skill_changed(repo_path: Path, project_path: Path) -> bool:
    repo_md = (repo_path / "SKILL.md").read_bytes()
    project_md = (project_path / "SKILL.md").read_bytes()
    return repo_md != project_md


def show_diff(repo_path: Path, project_path: Path, skill_name: str) -> str:
    """Unified diff of SKILL.md between central and project versions."""
    repo_lines = (repo_path / "SKILL.md").read_text(encoding="utf-8").splitlines(keepends=True)
    project_lines = (project_path / "SKILL.md").read_text(encoding="utf-8").splitlines(keepends=True)
    diff = list(difflib.unified_diff(
        repo_lines, project_lines,
        fromfile=f"central/{skill_name}/SKILL.md",
        tofile=f"project/{skill_name}/SKILL.md",
        n=1,
    ))
    lines = ["".join(diff[:30])]
    if len(diff) > 30:
        lines.append(f"... ({len(diff) - 30} more lines)")
    return "".join(lines)


def scan_project(repo_root: Path, source: Path, dest_id: str) -> ScanResult:
    """Scan a project's skill directory vs. the central repo's skills/."""
    skills_dir = repo_root / "skills"
    repo_skills = scan_skills_directory(skills_dir)
    project_skills = scan_skills_directory(source)
    diff = compare_skills(repo_skills, project_skills)

    changed: list[str] = []
    unchanged: list[str] = []
    for name in diff["existing"]:
        if check_skill_changed(repo_skills[name], project_skills[name]):
            changed.append(name)
        else:
            unchanged.append(name)

    return ScanResult(
        source=source, dest_id=dest_id,
        repo_skills=repo_skills, project_skills=project_skills,
        diff=diff, changed=changed, unchanged=unchanged,
    )


def format_scan_report(result: ScanResult) -> str:
    lines = [
        "=" * 70,
        "PHASE 1: Initial Intake & Reconciliation",
        f"Project: {result.dest_id}",
        "=" * 70,
        f"Source:  {result.source}",
        f"Central: (repo)/skills",
        "",
    ]

    if result.diff["new"]:
        lines.append(f"NEW SKILLS ({len(result.diff['new'])})")
        lines.extend(f"    {name}" for name in result.diff["new"])
        lines.append("")

    if result.changed:
        lines.append(f"CHANGED SKILLS ({len(result.changed)})")
        lines.extend(f"    {name}" for name in result.changed)
        lines.append("")

    if result.unchanged:
        lines.append(f"UNCHANGED SKILLS ({len(result.unchanged)})")
        lines.extend(f"    {name}" for name in result.unchanged[:5])
        if len(result.unchanged) > 5:
            lines.append(f"    ... and {len(result.unchanged) - 5} more")
        lines.append("")

    if result.diff["removed"]:
        lines.append(f"NOT IN PROJECT ({len(result.diff['removed'])})")
        lines.extend(f"    {name}" for name in result.diff["removed"][:5])
        if len(result.diff["removed"]) > 5:
            lines.append(f"    ... and {len(result.diff['removed']) - 5} more")
        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Classify / apply
# ---------------------------------------------------------------------------

def apply_new_skill(
    repo_root: Path, origins: dict, skill_name: str,
    project_skill_dir: Path, classification: str,
    *, repo: str = "", branch: str = "main", subpath: str = "",
    author: str = "", license_: str = "", reason: str = "",
) -> str:
    """Copies the skill folder into skills/, mutates `origins` in place.
    Returns 'imported-tracked' | 'imported-fork' | 'imported-own' | 'skipped'.
    Does NOT write origins.json — caller writes once after processing all skills.
    """
    if classification == "skip":
        return "skipped"

    dst = repo_root / "skills" / skill_name
    shutil.copytree(project_skill_dir, dst, dirs_exist_ok=True)

    if classification == "tracked":
        if not any(s["name"] == skill_name for s in origins["skills"]):
            origins["skills"].append({
                "name": skill_name,
                "local": f"skills/{skill_name}",
                "repo": repo,
                "branch": branch,
                "subpath": subpath,
                "type": "skill",
                "format": "skill-folder",
                "author": author,
                "license": license_,
                "last_synced_sha": None,
            })
        return "imported-tracked"

    if classification in ("fork", "own"):
        if not any(e["name"] == skill_name for e in origins["excluded"]):
            origins["excluded"].append({
                "name": skill_name,
                "local": f"skills/{skill_name}",
                "reason": reason,
            })
        return "imported-fork" if classification == "fork" else "imported-own"

    raise ValueError(f"Unknown classification: {classification!r}")


def apply_changed_skill(
    repo_root: Path, repo_skill_dir: Path, project_skill_dir: Path, choice: str,
) -> str:
    """choice: 'central' | 'project' | 'skip'. Overwrites repo_skill_dir from
    project_skill_dir when choice == 'project'. Returns a status string."""
    if choice == "central":
        return "kept-central"
    if choice == "project":
        shutil.rmtree(repo_skill_dir)
        shutil.copytree(project_skill_dir, repo_skill_dir)
        return "updated-from-project"
    if choice == "skip":
        return "skipped"
    raise ValueError(f"Unknown reconciliation choice: {choice!r}")


def apply_ingest(
    repo_root: Path, scan: ScanResult,
    classifications: dict[str, dict], reconciliations: dict[str, str],
    target_dir: str,
) -> dict:
    """Top-level orchestrator: loads origins.json + destinations.json fresh
    from disk, applies classify/reconcile decisions, writes both manifests
    once, appends a disabled destination entry. Returns a summary dict."""
    origins_path = repo_root / "manifests" / "origins.json"
    destinations_path = repo_root / "manifests" / "destinations.json"
    origins = json.loads(origins_path.read_text(encoding="utf-8"))
    destinations = json.loads(destinations_path.read_text(encoding="utf-8"))

    skills_assigned = list(scan.unchanged)
    imported_new = 0
    imported_changed = 0

    for skill_name in scan.diff["new"]:
        cls = classifications.get(skill_name)
        if cls is None:
            continue
        status = apply_new_skill(
            repo_root, origins, skill_name, scan.project_skills[skill_name],
            cls["choice"],
            repo=cls.get("repo", ""), branch=cls.get("branch", "main"),
            subpath=cls.get("subpath", ""), author=cls.get("author", ""),
            license_=cls.get("license", ""), reason=cls.get("reason", ""),
        )
        if status != "skipped":
            imported_new += 1
            skills_assigned.append(skill_name)

    for skill_name in scan.changed:
        choice = reconciliations.get(skill_name, "skip")
        status = apply_changed_skill(
            repo_root, scan.repo_skills[skill_name], scan.project_skills[skill_name], choice,
        )
        if status != "skipped":
            skills_assigned.append(skill_name)
        if status == "updated-from-project":
            imported_changed += 1

    origins_path.write_text(
        json.dumps(origins, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )

    new_dest = {
        "id": scan.dest_id,
        "environment": scan.dest_id.replace("_", "-"),
        "type": "skill-folder",
        "method": "skill-folder-copy",
        "target_dir": target_dir,
        "skills_assigned": sorted(skills_assigned),
        "enabled": False,
    }
    existing_dest = next(
        (d for d in destinations["destinations"] if d["id"] == scan.dest_id), None
    )
    if existing_dest is not None:
        existing_dest.update(new_dest)
    else:
        destinations["destinations"].append(new_dest)
    destinations_path.write_text(
        json.dumps(destinations, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )

    return {
        "imported_new": imported_new,
        "imported_changed": imported_changed,
        "skills_assigned": sorted(skills_assigned),
        "destination_id": scan.dest_id,
    }


# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------

def verify_ledger(repo_root: Path) -> dict:
    """Re-reads origins.json + scans skills/ dir fresh from disk."""
    origins_path = repo_root / "manifests" / "origins.json"
    origins = json.loads(origins_path.read_text(encoding="utf-8"))
    skills_dir = repo_root / "skills"

    on_disk = {
        skill_dir.name for skill_dir in skills_dir.iterdir()
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file()
    }
    in_manifest = {s["name"] for s in origins.get("skills", [])}
    in_manifest |= {s["name"] for s in origins.get("excluded", [])}

    orphaned = on_disk - in_manifest
    missing = in_manifest - on_disk
    return {"orphaned": orphaned, "missing": missing, "ok": not orphaned and not missing}


def format_verify_report(result: dict) -> str:
    lines = ["=" * 70, "PHASE 1e: Verify Skills Ledger", "=" * 70, ""]
    if result["ok"]:
        lines.append("Ledger clean: all skills on disk are in origins.json")
    else:
        if result["orphaned"]:
            lines.append("Orphaned skills (on disk, not in manifest):")
            lines.extend(f"    {name}" for name in sorted(result["orphaned"]))
        if result["missing"]:
            lines.append("Missing skills (in manifest, not on disk):")
            lines.extend(f"    {name}" for name in sorted(result["missing"]))
    return "\n".join(lines)
