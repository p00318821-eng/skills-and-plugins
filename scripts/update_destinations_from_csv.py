#!/usr/bin/env python3
"""
Convert destinations-matrix.csv back to manifests/destinations.json.

Usage:
  py scripts/update_destinations_from_csv.py

Reads:
  destinations-matrix.csv — edited version with new assignments

Writes:
  manifests/destinations.json — updated manifest
"""

import json
import csv
from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for p in [start, *start.parents]:
        if (p / "manifests" / "origins.json").is_file():
            return p
    raise FileNotFoundError("manifests/origins.json not found in CWD or any parent.")


def update_destinations_from_csv(repo_root: Path) -> dict:
    """Reads destinations-matrix.csv, rewrites manifests/destinations.json.
    Returns the new destinations manifest dict. Callable from the consolidated
    notebook's Phase 3 (re-import step)."""
    csv_path = repo_root / "destinations-matrix.csv"
    destinations_path = repo_root / "manifests" / "destinations.json"

    if not csv_path.is_file():
        raise FileNotFoundError(
            f"{csv_path} not found. Run: py scripts/generate_destinations_csv.py"
        )

    # Load current destinations for metadata
    current_dests = json.loads(destinations_path.read_text(encoding="utf-8"))
    dest_metadata = {d["id"]: d for d in current_dests.get("destinations", [])}

    # Read CSV
    assignments = {}  # {dest_id: [skill_names]}
    dest_ids = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        # Header format: Type, Name, Source Category, Source Detail, dest_id1, dest_id2, ...
        if len(header) < 4:
            print("Error: CSV header too short (expected at least 4 columns)")
            return

        dest_ids = header[4:]  # Skip "Type", "Name", "Source Category", "Source Detail"
        for dest_id in dest_ids:
            assignments[dest_id] = []

        # Read rows
        for row in reader:
            if len(row) < 4:
                continue
            item_type = row[0].strip().lower()
            item_name = row[1].strip()
            source_category = row[2].strip()

            if not item_name:
                continue

            # Check assignments for this item (starting from column 4)
            for i, dest_id in enumerate(dest_ids):
                col_idx = 4 + i
                if col_idx < len(row) and row[col_idx].strip().lower() in ("x", "check", "yes", "1", "true"):
                    assignments[dest_id].append(item_name)

    # Build new destinations manifest
    new_destinations = []

    for dest_id in dest_ids:
        # Use existing metadata if available, otherwise create new entry
        if dest_id in dest_metadata:
            dest = dest_metadata[dest_id].copy()
        else:
            # Default values for new destination
            dest = {
                "id": dest_id,
                "environment": dest_id.replace("_", "-"),
                "type": "skill-folder",
                "method": "skill-folder-copy",
                "target_dir": "{HOME}/.claude/skills",  # User must edit this
                "enabled": True,
            }

        # Update skills_assigned from CSV
        dest["skills_assigned"] = assignments[dest_id]
        new_destinations.append(dest)

    # Build manifest
    manifest = {
        "format_version": 1,
        "_comment": "Where skills get distributed. Paths use {HOME} and {REPO_ROOT} for portability.",
        "destinations": new_destinations,
    }

    # Write updated manifest
    destinations_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    print(f"Updated {destinations_path}")
    print(f"  {len(new_destinations)} destinations")
    for dest in new_destinations:
        print(f"    {dest['id']}: {len(dest['skills_assigned'])} skills assigned, enabled={dest.get('enabled', True)}")

    # Check for new destinations that need configuration
    new_dests = set(dest_ids) - set(dest_metadata.keys())
    if new_dests:
        print(f"\n⚠ New destinations added (configure these in destinations.json):")
        for dest_id in sorted(new_dests):
            print(f"    {dest_id} — set target_dir and method")

    return manifest


def main():
    update_destinations_from_csv(find_repo_root())


if __name__ == "__main__":
    main()
