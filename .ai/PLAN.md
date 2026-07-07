# Plan — skills-and-plugins

> Active/current state. Capped at 150 lines — archive older entries to `.ai/archive/`.

## Active Goals

- **Round 2 — Notebook consolidation + memory-architecture tooling, 2026-07-07 —
  SHIPPED.** Merged three notebooks (`ingest-project.ipynb`, `update-sourced-skills.ipynb`,
  `sync_orchestrator.ipynb`) into a single `skills-workflow.ipynb` with a phase-selector
  widget over four independent phases; extracted `scripts/ingest_engine.py` and
  `scripts/update_engine.py` to de-duplicate logic that previously existed in two parallel
  implementations each; renamed the CSV scripts to importable underscore modules; retired
  `scripts/ingest-destination.py` (confirmed no external callers). Built
  `scripts/compile_claude_md.py` and `scripts/check_doc_links.py` (Python ports of the
  Standard's compile step + sync-check, since this repo has no Node toolchain) — closes
  the gap where `.claude/CLAUDE.md` claimed to be a "GENERATED FILE" with no script that
  generated it. Ran a `memory-architect` AUDIT that caught and fixed: a stray empty
  `docs/` directory, two stale README license links pre-dating the `skills/` flattening,
  a duplicated nav table between README and `.claude/CLAUDE.md` (now cross-referenced
  instead of silently duplicated), and centralized the Constraints section (license +
  update-exclusion rules) into `ARCHITECTURE.md`. Also generalized the `memory-architect`
  skill itself (SCAFFOLD step 10 made language-agnostic; new AUDIT dimension 15 for
  migration cleanliness) since both gaps are reusable lessons, not one-off fixes. Round 1
  (Hub-and-Spoke adoption) shipped 2026-07-02 — see `.ai/archive/2026-07-shipped.md`.

## Open Blockers / Decisions

- **Open architectural decision (not actioned):** `plugins/*` packages (e.g.
  `plugins/azure-skills/skills/*`) and their corresponding top-level `skills/*` folders
  duplicate content byte-for-byte — plugin skill folders were copied into `skills/` so
  the repo can treat them as individually vendored skills (see
  [ARCHITECTURE.md](../ARCHITECTURE.md)). Whether to de-duplicate (symlink, single
  source + generated copy, or accept the duplication as intentional for distribution-
  method flexibility) is a content/product decision, out of scope for this
  memory-architecture migration — flagged here for a future round.

## Resume Pointer

Round 2 is shipped and this repo is current as of 2026-07-07. Nothing mid-flight — next
session should either resolve the plugin/skills byte-duplication decision above, or start
a fresh round when new work comes up.
