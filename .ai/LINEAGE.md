# Architecture Lineage

This repo's Hub-and-Spoke memory architecture (`.ai/rules/`, compiled pointer file)
follows the Standard published at:

- Source: https://github.com/p00318821-eng/project-memory-template
- Version/commit: `3af6758`
- Adopted: 2026-07-02
- Last reviewed for drift: 2026-07-02

**This repo deliberately adopted the Compiled-only Hub-and-Spoke rung** (see
`memory-architect` SKILL.md § "The Three Rungs") — `.ai/rules/*.md` remains the source of
truth, but ALL rule files compile into `.claude/CLAUDE.md` regardless of
`alwaysApply`/`globs`, and there is intentionally no `PreToolUse` hook, no sync-check
script, and no `.cursor/rules/*.mdc` mirror. This is because this repo is Python-only (no
`package.json`) and its rule candidates are few and universal (Windows/environment
gotchas — `py` vs `python`, blocked `curl`, no `gh`, IDE auto-push), not
narrow-and-numerous — introducing a Node hook runtime would be overhead disproportionate
to the benefit. A future AUDIT should not flag the absent hook as a gap unless the
repo's rule surface grows to genuinely narrow, numerous Tier 2 candidates, at which
point re-evaluate for the Full rung.

There is no automated sync between this repo and the source template — re-run
`memory-architect` AUDIT periodically, or manually diff
`.ai/rules/000-agent-operating-mandates.md` against the source when it's been a while.
