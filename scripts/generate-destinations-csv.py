#!/usr/bin/env python3
"""
Generate a spreadsheet (CSV) showing all skills/plugins and their destination assignments.

Usage:
  py scripts/generate-destinations-csv.py

Output:
  destinations-matrix.csv — edit this file in Excel/Sheets to assign items to destinations
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


def categorize_source(skill_name: str, skill_entry: dict, is_tracked: bool) -> str:
    """Categorize skill source into 4 categories. Details in Source Detail column."""
    if is_tracked:
        return "skill-tracked"

    reason = skill_entry.get("reason", "")

    if "own skill" in reason.lower():
        return "skill-excluded-own"
    elif "locally modified" in reason.lower() or "fork" in reason.lower():
        return "skill-excluded-fork"
    elif "extracted from" in reason.lower():
        return "skill-plugin-extracted"
    else:
        return "skill-excluded-own"


def main():
    repo_root = find_repo_root()
    origins_path = repo_root / "manifests" / "origins.json"
    destinations_path = repo_root / "manifests" / "destinations.json"
    output_path = repo_root / "destinations-matrix.csv"

    # Load manifests
    origins = json.loads(origins_path.read_text(encoding="utf-8"))
    destinations = json.loads(destinations_path.read_text(encoding="utf-8"))

    # Collect all items
    items = []

    # Add all skills from origins.skills (tracked)
    for skill in origins.get("skills", []):
        items.append({
            "type": "skill",
            "name": skill["name"],
            "source": "skill-tracked",
            "source_detail": skill.get("repo", "").split("/")[-1].replace(".git", ""),
        })

    # Add all skills from origins.excluded
    for skill in origins.get("excluded", []):
        category = categorize_source(skill["name"], skill, False)
        items.append({
            "type": "skill",
            "name": skill["name"],
            "source": category,
            "source_detail": skill.get("reason", ""),
        })

    # Sort by source category, then name
    category_order = [
        "skill-tracked",
        "skill-excluded-own",
        "skill-excluded-fork",
        "skill-plugin-extracted",
    ]
    def sort_key(item):
        source = item["source"]
        cat_idx = category_order.index(source) if source in category_order else len(category_order)
        return (cat_idx, item["name"])

    items.sort(key=sort_key)

    # Get destination IDs (headers)
    dest_ids = [d["id"] for d in destinations.get("destinations", [])]

    # Build assignment map: {destination_id: {item_name}}
    assignments = {dest_id: set() for dest_id in dest_ids}
    for dest in destinations.get("destinations", []):
        dest_id = dest["id"]
        for skill in dest.get("skills_assigned", []):
            assignments[dest_id].add(skill)

    # Write CSV
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        header = ["Type", "Name", "Source Category", "Source Detail"] + dest_ids
        writer.writerow(header)

        # Rows
        for item in items:
            row = [
                item["type"],
                item["name"],
                item["source"],
                item["source_detail"],
            ]
            for dest_id in dest_ids:
                row.append("x" if item["name"] in assignments[dest_id] else "")
            writer.writerow(row)

    print(f"Generated {output_path}")
    print(f"  {len(items)} items")
    print(f"  {len(dest_ids)} destinations")
    print(f"\nEdit the file to assign items to destinations:")
    print(f"  - Add 'x' in a cell to assign that item to that destination")
    print(f"  - Add new columns for new destinations")
    print(f"  - Remove rows for items you don't want to distribute")
    print(f"\nThen run: py scripts/update-destinations-from-csv.py")


if __name__ == "__main__":
    main()
