# Plan — skills-and-plugins

> Active/current state. Capped at 150 lines — archive older entries to `.ai/archive/`.

## Active Goals

- **Round 3 — Deprecate `semantic-modeling-prepforai` + global HISD hooks +
  memory-architect defect fix, 2026-07-10 — SHIPPED, live-session hook
  verification CONFIRMED (2026-07-10).** A skill comparison exercise found 3 of 6 comparable
  Power BI/Fabric skills already had AI-readiness content, most notably
  `fabric-skills:semantic-model-authoring`'s own dedicated workflow — more
  rigorously engineered but missing HISD-specific content entirely. Rather
  than fork or maintain a parallel skill (fragile: relies on two skills'
  descriptions co-triggering), HISD context is now delivered via two global
  Claude Code hooks (`SessionStart` + `PostToolUse` on `.tmdl`, registered in
  `~/.claude/settings.json`, outside this repo) that fire regardless of which
  skill drives an edit. Verifying the hooks mechanism against official docs +
  GitHub issues surfaced two real corrections along the way: (1) a
  pre-existing defect in the global `memory-architect` skill claiming
  `PreToolUse` can inject `additionalContext` (it can't — fixed to
  `PostToolUse`); (2) `updatedToolOutput` *replaces* the tool result rather
  than appending to it, so the corrected hook design uses
  `hookSpecificOutput.additionalContext` instead, in both `memory-architect`
  and the new HISD hooks. `skills/semantic-modeling-prepforai/SKILL.md` is now
  a ~40-line deprecation notice; its manual copy/paste TMDL workflow and
  Truncation Prevention protocol were dropped as obsolete (MCP-first editing
  supersedes them); HISD-specific content (synonym glossary, AI Instructions
  template, relationship naming pattern, AI-consumer compatibility matrix)
  consolidated into `references/hisd-power-bi-context.md`. Folder retained —
  still `sync_engine.py`'s distribution vehicle to `~/.claude/skills/` and
  `~/.agents/skills/`, which the hooks read from. **Live-session verification
  (2026-07-10, confirmed in a fresh session):** `SessionStart`'s
  `additionalContext` pointer fired; `PostToolUse` fired correctly on both
  `Write` and `Edit` to a scratch `.tmdl` file (reminder appeared only in the
  tool-result system reminder, never written into the file); a `.txt` write
  in the same session produced no reminder (negative case holds); temporarily
  renaming `hisd-tmdl-reminder.js` and editing a `.tmdl` file still succeeded
  normally with no error surfaced (fail-open holds) — hook restored after.
  Distribution regression check (Phase 4 dry-run for this skill + one
  sibling) is still open — see plan file items 9-11.
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

Round 3's file changes are shipped as of 2026-07-10, and the live-session hook
verification (SessionStart, PostToolUse positive/negative, fail-open) is now confirmed —
see Active Goals above. Remaining open items from the Part 5 checklist: re-run Phase 4
distribution for `semantic-modeling-prepforai` and one sibling skill to confirm no
regressions (plan items 9-11), and the trigger-avoidance smoke test (plan item 11). The
plugin/skills byte-duplication decision from Round 2 is still open and unrelated to this
round.
