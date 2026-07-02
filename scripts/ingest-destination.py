#!/usr/bin/env python3
"""
Two-phase project intake: initial ingest + reconciliation, then ongoing distribution.

PHASE 1: Initial Intake (one-time)
  - Scan project directory for skills
  - Compare with central repo (find new, changed, removed)
  - User classifies each new/changed skill:
    [T] Tracked upstream — provide repo + subpath (auto-updated)
    [F] Fork — modified from upstream, don't auto-update
    [O] Own — no upstream source, project-specific
    [S] Skip — don't import this skill
  - Central becomes source of truth

PHASE 2: Ongoing Distribution (all subsequent runs)
  - Central repo distributes TO project
  - Generate CSV → edit → convert back → orchestrator distributes
  - No more scanning/importing

Usage:

  # Phase 1a: Dry-run (see what would change)
  py scripts/ingest-destination.py \
    --source C:/path/to/project/.agents/skills \
    --destination-id campus-profile

  # Phase 1b: Apply (import, classify, and set up destination)
  py scripts/ingest-destination.py \
    --source C:/path/to/project/.agents/skills \
    --destination-id campus-profile \
    --apply \
    --target-dir C:/path/to/project/.agents/skills

  # Phase 2: Use CSV + orchestrator for ongoing distribution
  py scripts/generate-destinations-csv.py
  # Edit CSV, then:
  py scripts/update-destinations-from-csv.py
  # Run sync_orchestrator.ipynb
"""

import json
import argparse
import shutil
import difflib
from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for p in [start, *start.parents]:
        if (p / "manifests" / "origins.json").is_file():
            return p
    raise FileNotFoundError("manifests/origins.json not found in CWD or any parent.")


def scan_skills_directory(path: Path) -> dict[str, Path]:
    """Scan directory for skill folders. Returns {skill_name: skill_path}."""
    skills = {}
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


def show_drift_detail(repo_path: Path, project_path: Path, skill_name: str) -> None:
    repo_lines = (repo_path / "SKILL.md").read_text(encoding="utf-8").splitlines(keepends=True)
    project_lines = (project_path / "SKILL.md").read_text(encoding="utf-8").splitlines(keepends=True)
    diff = list(difflib.unified_diff(
        repo_lines, project_lines,
        fromfile=f"central/{skill_name}/SKILL.md",
        tofile=f"project/{skill_name}/SKILL.md",
        n=1
    ))
    if diff:
        print(f"\n  Diff for {skill_name}:")
        for line in diff[:20]:
            print(f"    {line.rstrip()}")
        if len(diff) > 20:
            print(f"    ... ({len(diff) - 20} more lines)")


def classify_skill(name: str, context: str = "new") -> dict | None:
    """Interactive classification for a skill. Returns classification dict or None to skip."""
    print(f"\n  Classify '{name}' ({context}):")
    print(f"    [T] Tracked upstream (auto-updated from repo)")
    print(f"    [F] Fork (modified from upstream; don't auto-update)")
    print(f"    [O] Own skill (no upstream source)")
    print(f"    [S] Skip (don't import)")

    while True:
        choice = input(f"    Choice [T/F/O/S]: ").strip().upper()

        if choice == "S":
            return None

        if choice == "T":
            repo = input(f"    Upstream repo URL: ").strip()
            branch = input(f"    Branch [main]: ").strip() or "main"
            subpath = input(f"    Subpath to skill folder (e.g. .agents/skills/{name}): ").strip()
            author = input(f"    Author []: ").strip() or ""
            license_ = input(f"    License []: ").strip() or ""
            return {
                "classification": "tracked",
                "repo": repo,
                "branch": branch,
                "subpath": subpath,
                "author": author,
                "license": license_,
            }

        if choice == "F":
            upstream_note = input(f"    Upstream origin (e.g. repo URL or description): ").strip()
            return {
                "classification": "fork",
                "reason": f"Fork of {upstream_note}; locally modified, do not auto-update.",
            }

        if choice == "O":
            owner = input(f"    Owner/author []: ").strip()
            reason = f"Own skill ({owner})." if owner else "Own skill; no upstream source."
            return {
                "classification": "own",
                "reason": reason,
            }

        print(f"    Invalid choice. Enter T, F, O, or S.")


def classify_changed_skill(name: str) -> str:
    """Classify a changed skill: keep central, take project version, or skip."""
    print(f"\n  Skill '{name}' differs between central and project:")
    print(f"    [C] Keep central version (project drifted; ignore project changes)")
    print(f"    [P] Take project version (project has intentional edits)")
    print(f"    [S] Skip (leave as-is, don't assign to this destination)")

    while True:
        choice = input(f"    Choice [C/P/S]: ").strip().upper()
        if choice in ("C", "P", "S"):
            return choice
        print(f"    Invalid choice. Enter C, P, or S.")


def main():
    parser = argparse.ArgumentParser(
        description="Phase 1: Ingest project skills and reconcile with central repo"
    )
    parser.add_argument(
        "--source", required=True,
        help="Project skills directory (local path or git URL)",
    )
    parser.add_argument(
        "--destination-id", required=True,
        help="ID for the project destination (e.g., campus-profile)",
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Apply changes: classify, import, and set up destination (default: dry-run only)",
    )
    parser.add_argument(
        "--target-dir",
        help="Target directory for Phase 2 distribution",
    )
    args = parser.parse_args()

    repo_root = find_repo_root()
    skills_dir = repo_root / "skills"

    # Parse source
    if args.source.startswith(("http://", "https://", "git@")):
        print(f"Cloning {args.source}...")
        import tempfile
        import subprocess
        temp_dir = Path(tempfile.mkdtemp(prefix="ingest_"))
        subprocess.run(
            ["git", "clone", "--depth", "1", args.source, str(temp_dir)],
            check=True, capture_output=True
        )
        source_path = temp_dir / ".agents" / "skills"
        if not source_path.is_dir():
            source_path = temp_dir / "skills"
        if not source_path.is_dir():
            source_path = temp_dir
    else:
        source_path = Path(args.source).expanduser()

    if not source_path.is_dir():
        print(f"Error: Source not found: {source_path}")
        return

    # Scan both
    repo_skills = scan_skills_directory(skills_dir)
    project_skills = scan_skills_directory(source_path)
    diff = compare_skills(repo_skills, project_skills)

    # Print reconciliation report
    print(f"\n{'='*70}")
    print(f"PHASE 1: Initial Intake & Reconciliation")
    print(f"Project: {args.destination_id}")
    print(f"{'='*70}")
    print(f"Source:  {source_path}")
    print(f"Central: {skills_dir}\n")

    if diff["new"]:
        print(f"NEW SKILLS ({len(diff['new'])}) — require classification:")
        for name in diff["new"]:
            print(f"  + {name}")
        print()

    changed = []
    unchanged = []
    if diff["existing"]:
        for name in diff["existing"]:
            if check_skill_changed(repo_skills[name], project_skills[name]):
                changed.append(name)
            else:
                unchanged.append(name)

        if changed:
            print(f"CHANGED SKILLS ({len(changed)}) — need reconciliation:")
            for name in changed:
                print(f"  ~ {name}")
                show_drift_detail(repo_skills[name], project_skills[name], name)
            print()

        if unchanged:
            print(f"UNCHANGED SKILLS ({len(unchanged)}) — in sync:")
            for name in unchanged[:5]:
                print(f"  = {name}")
            if len(unchanged) > 5:
                print(f"  ... and {len(unchanged) - 5} more")
            print()

    if diff["removed"]:
        print(f"NOT IN PROJECT ({len(diff['removed'])}) — remain in central:")
        for name in diff["removed"][:5]:
            print(f"  - {name}")
        if len(diff["removed"]) > 5:
            print(f"  ... and {len(diff['removed']) - 5} more")
        print()

    # Dry-run: stop here
    if not args.apply:
        print(f"{'='*70}")
        print("DRY-RUN: No changes applied.")
        print("\nReview above, then run with --apply to classify and import each skill.")
        print("\nCommand:")
        print(f"  py scripts/ingest-destination.py \\")
        print(f"    --source {args.source} \\")
        print(f"    --destination-id {args.destination_id} \\")
        print(f"    --apply \\")
        print(f"    --target-dir '{args.target_dir or '...'}'")
        return

    # Apply: requires --target-dir
    if not args.target_dir:
        print("Error: --target-dir required for --apply")
        return

    print(f"{'='*70}")
    print("APPLYING Phase 1: Classify & Import")
    print(f"{'='*70}")

    origins_path = repo_root / "manifests" / "origins.json"
    origins = json.loads(origins_path.read_text(encoding="utf-8"))

    skills_assigned = list(unchanged)  # Unchanged skills auto-assigned
    imported_new = 0
    imported_changed = 0

    # --- Classify and import NEW skills ---
    if diff["new"]:
        print(f"\n--- Classify {len(diff['new'])} new skill(s) ---")

        for name in diff["new"]:
            result = classify_skill(name, context="new to central")
            if result is None:
                print(f"    Skipped {name}")
                continue

            # Copy to central
            src = project_skills[name]
            dst = skills_dir / name
            shutil.copytree(src, dst, dirs_exist_ok=True)
            imported_new += 1
            skills_assigned.append(name)

            if result["classification"] == "tracked":
                # Add to origins.skills
                if not any(s["name"] == name for s in origins["skills"]):
                    origins["skills"].append({
                        "name": name,
                        "local": f"skills/{name}",
                        "repo": result["repo"],
                        "branch": result["branch"],
                        "subpath": result["subpath"],
                        "type": "skill",
                        "format": "skill-folder",
                        "author": result["author"],
                        "license": result["license"],
                        "last_synced_sha": None,
                    })
                print(f"    ✓ {name} → tracked (upstream: {result['repo']})")

            elif result["classification"] in ("fork", "own"):
                # Add to origins.excluded
                if not any(e["name"] == name for e in origins["excluded"]):
                    origins["excluded"].append({
                        "name": name,
                        "local": f"skills/{name}",
                        "reason": result["reason"],
                    })
                label = "fork" if result["classification"] == "fork" else "own"
                print(f"    ✓ {name} → {label}")

    # --- Reconcile CHANGED skills ---
    if changed:
        print(f"\n--- Reconcile {len(changed)} changed skill(s) ---")

        for name in changed:
            show_drift_detail(repo_skills[name], project_skills[name], name)
            choice = classify_changed_skill(name)

            if choice == "C":
                skills_assigned.append(name)
                print(f"    ✓ {name} → keeping central version")
            elif choice == "P":
                src = project_skills[name]
                dst = repo_skills[name]
                shutil.rmtree(dst)
                shutil.copytree(src, dst)
                skills_assigned.append(name)
                imported_changed += 1
                print(f"    ✓ {name} → updated from project")
            elif choice == "S":
                print(f"    Skipped {name}")

    # Write origins.json
    origins_path.write_text(
        json.dumps(origins, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Add to destinations.json
    destinations_path = repo_root / "manifests" / "destinations.json"
    destinations = json.loads(destinations_path.read_text(encoding="utf-8"))

    new_dest = {
        "id": args.destination_id,
        "environment": args.destination_id.replace("_", "-"),
        "type": "skill-folder",
        "method": "skill-folder-copy",
        "target_dir": args.target_dir,
        "skills_assigned": sorted(skills_assigned),
        "enabled": False,
    }
    destinations["destinations"].append(new_dest)
    destinations_path.write_text(
        json.dumps(destinations, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Summary
    print(f"\n{'='*70}")
    print("✓ PHASE 1 Complete")
    print(f"{'='*70}")
    print(f"Imported: {imported_new} new + {imported_changed} changed")
    print(f"Assigned: {len(skills_assigned)} skills to {args.destination_id}")
    print(f"Destination: {args.destination_id} (DISABLED — enable when ready)")
    print(f"\nNext steps:")
    print(f"  1. Review origins.json and destinations.json")
    print(f"  2. Enable {args.destination_id} in destinations.json (set enabled: true)")
    print(f"  3. py scripts/generate-destinations-csv.py")
    print(f"  4. Edit destinations-matrix.csv (assign skills to destinations)")
    print(f"  5. py scripts/update-destinations-from-csv.py")
    print(f"  6. Run sync_orchestrator.ipynb to distribute")


if __name__ == "__main__":
    main()
