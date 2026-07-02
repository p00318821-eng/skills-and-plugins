# Plan — skills-and-plugins

> Active/current state. Capped at 150 lines — archive older entries to `.ai/archive/`.

## Active Goals

- **Round 1 — Hub-and-Spoke adoption (Compiled-only rung), 2026-07-02 — IN PROGRESS.**
  Migrated `.ai/` structure onto this repo (previously zero `.ai/` presence): moved
  `CLAUDE.md` → `.claude/CLAUDE.md` (now a compiled pointer file), renamed
  `docs/PROJECT-NOTES.md` → `ARCHITECTURE.md` (root, deduplicated), consolidated
  attribution onto `README.md` (regenerated the 93-row skill table), added
  `.ai/rules/000-agent-operating-mandates.md`, deleted the orphaned
  `skill-plugin-sources.json` stub. Also absorbed a large pending expansion
  (~1,645 untracked files: Azure/Foundry skills, azure-skills/deep-wiki plugins, the
  distribution-tooling subsystem) into clean, reviewable commits as part of the same
  pass. See `.ai/archive/2026-07-shipped.md` once this round closes.

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

If interrupted mid-migration: check whether `.claude/CLAUDE.md` exists and is compiled
(not the old root `CLAUDE.md`), whether `ARCHITECTURE.md` exists at root (not
`docs/PROJECT-NOTES.md`), and whether `README.md`'s skill table has 93 rows — those are
the three largest, most interruptible steps. `.ai/LINEAGE.md` should name the
**Compiled-only** rung explicitly once present; if it's missing, the migration hasn't
reached that step yet.
