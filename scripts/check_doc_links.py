#!/usr/bin/env python3
"""
Doc-link and Hub-and-Spoke sync checker. Two jobs:

1. Validate intra-repo markdown links/anchors (relative file links resolve,
   heading-anchor links resolve against the target's actual headings).
2. Hub-and-Spoke sync check: verify every rule body in .ai/rules/*.md appears
   verbatim in .claude/CLAUDE.md's compiled section, flag orphaned Tier 2
   rules (alwaysApply: false with no globs), and flag zero-Tier-1-coverage.

Manual gate — this repo has no CI (no .github/workflows/), so run this by hand:
  py scripts/check_doc_links.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    # Works when imported as `scripts.check_doc_links` (repo root on sys.path).
    from scripts.compile_claude_md import find_repo_root, load_all_rules, render_compiled_section
except ImportError:
    # Works when run directly: `py scripts/check_doc_links.py` (scripts/ on sys.path).
    from compile_claude_md import find_repo_root, load_all_rules, render_compiled_section

SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".cache", ".venv"}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def find_markdown(repo_root: Path) -> list[Path]:
    out = []
    for p in repo_root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.relative_to(repo_root).parts):
            continue
        out.append(p)
    return out


def _slugify(heading_text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", heading_text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def heading_slugs(content: str) -> set[str]:
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    for line in content.splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = _slugify(m.group(2))
        if base in counts:
            counts[base] += 1
            slugs.add(f"{base}-{counts[base]}")
        else:
            counts[base] = 0
            slugs.add(base)
    return slugs


def check_links(repo_root: Path, files: list[Path]) -> list[str]:
    errors: list[str] = []
    for md_file in files:
        content = md_file.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(content):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "tel:")):
                continue

            if target.startswith("#"):
                if target[1:] not in heading_slugs(content):
                    errors.append(f"{md_file}: broken same-file anchor '{target}'")
                continue

            path_part, _, anchor = target.partition("#")
            resolved = (md_file.parent / path_part).resolve()
            if not (resolved.is_file() or resolved.is_dir()):
                errors.append(f"{md_file}: broken relative link '{target}' -> {resolved}")
                continue

            if anchor and resolved.is_file() and resolved.suffix == ".md":
                target_content = resolved.read_text(encoding="utf-8")
                if anchor not in heading_slugs(target_content):
                    errors.append(f"{md_file}: broken heading anchor '#{anchor}' in '{path_part}'")

    return errors


def check_hub_and_spoke_sync(repo_root: Path) -> list[str]:
    errors: list[str] = []
    rules_dir = repo_root / ".ai" / "rules"
    claude_md_path = repo_root / ".claude" / "CLAUDE.md"

    rules = load_all_rules(rules_dir)
    if not rules:
        return errors

    if not claude_md_path.is_file():
        return [f"{rules_dir}: rule files exist but {claude_md_path} is missing"]

    claude_md_content = claude_md_path.read_text(encoding="utf-8").replace("\r\n", "\n")

    has_tier1 = any(r.frontmatter["alwaysApply"] for r in rules)
    if not has_tier1:
        errors.append(f"{rules_dir}: no alwaysApply:true rule exists (missing Tier 1 safety net)")

    for rule in rules:
        if not rule.frontmatter["alwaysApply"] and not rule.frontmatter["globs"]:
            errors.append(f"{rule.path}: alwaysApply:false with empty globs (orphaned Tier 2 rule)")

        # Use the same H1-drop + heading-demote transform compile_claude_md.py
        # applies, so what's checked here matches what actually gets compiled.
        compiled_rule = render_compiled_section([rule]).replace("\r\n", "\n")
        check_line = next((line.strip() for line in compiled_rule.splitlines() if line.strip()), "")
        if check_line and check_line not in claude_md_content:
            errors.append(
                f"{rule.path}: body not found verbatim in {claude_md_path} (drift - run compile_claude_md.py)"
            )

    return errors


def main() -> None:
    repo_root = find_repo_root()
    errors = check_links(repo_root, find_markdown(repo_root))
    errors += check_hub_and_spoke_sync(repo_root)

    if errors:
        print(f"X {len(errors)} doc issue(s):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)

    print("OK: all intra-repo doc links/anchors resolve, and .ai/rules/ <-> CLAUDE.md are in sync")


if __name__ == "__main__":
    main()
