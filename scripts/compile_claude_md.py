#!/usr/bin/env python3
"""
Regenerate .claude/CLAUDE.md's compiled "Agent Operating Mandates & Gotchas"
section from .ai/rules/*.md, closing the gap where the file claimed to be a
"GENERATED FILE" with no script that actually generated it.

This repo is Rung 1 (Compiled-only, see .ai/LINEAGE.md) — there's no PreToolUse
hook to hold Tier 2 (alwaysApply: false) content back, so every rule file
compiles in regardless of alwaysApply, in numeric-prefix filename order.

Usage:
  py scripts/compile_claude_md.py           # regenerate and write
  py scripts/compile_claude_md.py --check   # report drift only, exit 1 if stale
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

COMPILED_MARKER = "<!-- COMPILED"
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", re.DOTALL)


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for p in [start, *start.parents]:
        if (p / "manifests" / "origins.json").is_file():
            return p
    raise FileNotFoundError("manifests/origins.json not found in CWD or any parent.")


@dataclass
class RuleFile:
    path: Path
    name: str
    frontmatter: dict
    body: str


def _parse_frontmatter_field(raw: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.*)$", raw, re.MULTILINE)
    return m.group(1).strip() if m else None


def parse_rule_file(path: Path) -> RuleFile:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"{path}: missing YAML frontmatter block (expected '---' ... '---')")

    raw_frontmatter, body = m.group(1), m.group(2)
    always_apply_raw = _parse_frontmatter_field(raw_frontmatter, "alwaysApply")
    globs_raw = _parse_frontmatter_field(raw_frontmatter, "globs")
    description_raw = _parse_frontmatter_field(raw_frontmatter, "description")

    frontmatter = {
        "description": (description_raw or "").strip('"'),
        "alwaysApply": (always_apply_raw or "false").strip().lower() == "true",
        "globs": [] if not globs_raw or globs_raw.strip() == "[]" else [
            g.strip().strip('"\'') for g in globs_raw.strip("[]").split(",") if g.strip()
        ],
    }
    return RuleFile(path=path, name=path.name, frontmatter=frontmatter, body=body.strip("\n"))


def load_all_rules(rules_dir: Path) -> list[RuleFile]:
    if not rules_dir.is_dir():
        return []
    return [parse_rule_file(p) for p in sorted(rules_dir.glob("*.md"))]


def demote_headings(markdown_body: str) -> str:
    """Shift every heading down one level (# -> ##, ## -> ###, ...)."""
    lines = markdown_body.splitlines()
    out = []
    for line in lines:
        m = re.match(r"^(#{1,5})(\s.*)$", line)
        out.append(f"#{m.group(1)}{m.group(2)}" if m else line)
    return "\n".join(out)


def render_compiled_section(rules: list[RuleFile]) -> str:
    """Concatenate every rule body (heading-demoted), skipping each file's own
    top-level H1 (e.g. '# Agent Operating Mandates') since the compiled
    section already lives under the pointer file's own '## Agent Operating
    Mandates & Gotchas' heading."""
    parts = []
    for rule in rules:
        body_lines = rule.body.splitlines()
        # Drop a leading H1 line (the rule file's own title) if present.
        if body_lines and body_lines[0].startswith("# "):
            body_lines = body_lines[1:]
        body = "\n".join(body_lines).strip("\n")
        parts.append(demote_headings(body))
    return "\n\n".join(parts)


def compile_claude_md(repo_root: Path, *, check_only: bool = False) -> bool:
    """Returns True if the file was (or would be) changed."""
    claude_md_path = repo_root / ".claude" / "CLAUDE.md"
    rules_dir = repo_root / ".ai" / "rules"

    content = claude_md_path.read_text(encoding="utf-8")
    marker_idx = content.find(COMPILED_MARKER)
    if marker_idx == -1:
        raise ValueError(f"{claude_md_path}: no '{COMPILED_MARKER}' marker found")

    # The marker is an HTML comment that may span multiple lines — keep the
    # whole comment (through '-->') as part of the hand-authored prefix.
    comment_end = content.index("-->", marker_idx) + len("-->")
    marker_line_end = content.index("\n", comment_end) + 1
    before = content[:marker_line_end]

    rules = load_all_rules(rules_dir)
    new_section = render_compiled_section(rules) + "\n"
    new_content = before + "\n" + new_section

    changed = new_content != content
    print(f"Compiled {len(rules)} rule file(s) from {rules_dir}")
    print("Drift detected" if changed else "No drift - compiled section is in sync")

    if changed and not check_only:
        claude_md_path.write_text(new_content, encoding="utf-8")
        print(f"Wrote {claude_md_path}")

    return changed


def main() -> None:
    check_only = "--check" in sys.argv
    repo_root = find_repo_root()
    changed = compile_claude_md(repo_root, check_only=check_only)
    if check_only and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
