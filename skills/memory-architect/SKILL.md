---
name: memory-architect
description: >
  Audit, scaffold, and consolidate standardized `.ai/` project memory
  architecture across repositories. Scores documentation completeness,
  creates missing structure files, and crystallizes ephemeral Claude
  session state into permanent repo files. Git is the system of record —
  no external databases or vendor lock-in. Use when starting a new repo,
  onboarding to an existing one, after multiple work rounds to consolidate
  learnings, or when the user mentions "memory architecture", "doc
  structure", "project memory", "knowledge consolidation", or "session
  cleanup". Also trigger on "audit docs", "scaffold docs", "consolidate",
  or any request to organize project documentation for AI agent
  consumption.
---

# Memory Architect

Standardize project memory so that a fresh checkout — by any agent or human — orients
fast, finds facts in one home, and never loses hard-won learnings to context wipes.

## Core Principles

1. **Git = system of record.** Every fact lives in a committed file. No external databases,
   vector stores, or vendor-specific state. If the tool disappears, the knowledge survives.
2. **One fact, one home.** Never duplicate content across files. Each piece of knowledge has
   exactly one canonical location.
3. **Vendor-agnostic.** The `.ai/` directory works with any AI agent, IDE, or workflow tool.
   `.claude/CLAUDE.md` is the only Claude-specific file and serves as a navigator into `.ai/`.
4. **Lazy scaffolding.** Create files only when content warrants them. Empty files are noise.

## The Standard

```
README.md                           # root — orientation, quickstart, canonical doc table
.claude/CLAUDE.md                   # Claude navigator + SOPs + critical inline gotchas

.ai/
  project/                          # stable, charter-level docs (change infrequently)
    constraints.md                  # hard constraints (compliance, API limits, platform rules)
    architecture.md                 # system narrative, conventions, reusable patterns
    operations.md                   # build/run/auth/deploy/validate/troubleshoot
    agents.md                       # template workflows, sub-agent delegation (optional)
  memory/                           # evolving state (changes with each round of work)
    decisions.md                    # shipped decisions with rationale + reversal cost
    pitfalls.md                     # failures, lessons learned, non-critical gotchas
    current-state.md                # active goals, resume pointer, open blockers
```

### Fixed-location files (never move)

| File | Location | Why fixed |
|------|----------|-----------|
| `README.md` | repo root | GitHub/human convention |
| `.claude/CLAUDE.md` | `.claude/` | Claude Code auto-discovery |
| Template files (SECURITY.md, LICENSE, CODE_OF_CONDUCT.md) | repo root | Upstream-owned; detect via markers |

### Boundary rules — where content lives

| Content type | Home | NOT here |
|---|---|---|
| Agent-critical gotchas (silent data corruption) | `.claude/CLAUDE.md` inline | `.ai/memory/pitfalls.md` |
| Broader lessons / post-mortems | `.ai/memory/pitfalls.md` | CLAUDE.md |
| Hard constraints (compliance, platform rules) | `.ai/project/constraints.md` | Scattered across files |
| System narrative, conventions, patterns | `.ai/project/architecture.md` | Separate patterns.md |
| Build/run/deploy procedures | `.ai/project/operations.md` | README (keep README lean) |
| Active sprint / goals / resume pointer | `.ai/memory/current-state.md` | README.md |
| Shipped decisions with rationale | `.ai/memory/decisions.md` | current-state.md |
| Navigation map + agent SOPs | `.claude/CLAUDE.md` | Duplicated in README |

### When migrating from root-level docs

Repos with existing root-level PLAN.md, OPERATIONS.md, etc. map as follows:

| Old location | New location |
|---|---|
| `PLAN.md` | `.ai/memory/current-state.md` |
| `PLAN-history.md` | `.ai/memory/decisions.md` |
| `OPERATIONS.md` | `.ai/project/operations.md` |
| `docs/ARCHITECTURE.md` | `.ai/project/architecture.md` |
| `AGENTS.md` | `.ai/project/agents.md` |
| `CONSTRAINTS.md` | `.ai/project/constraints.md` |

After migration, update all cross-references in CLAUDE.md and README.md. Leave redirects
or git-move so blame history is preserved.

## Mode 1: AUDIT

Invocation: user asks to "audit docs", "audit memory", "check doc structure", or
"how's my project memory?"

### Procedure

1. **Scan for `.ai/` structure.** Check for `project/` and `memory/` subdirectories
   and each expected file.

2. **Scan for legacy root-level equivalents.** If `.ai/` files are missing but root-level
   equivalents exist (PLAN.md, OPERATIONS.md, etc.), score the *content* as present but
   flag the *location* as non-standard. Do NOT penalize to F — the content exists, it just
   needs migration.

3. **Detect template-owned files.** Read first 5 lines of SECURITY.md, LICENSE,
   CODE_OF_CONDUCT.md. If they contain template markers ("BEGIN MICROSOFT SECURITY.MD",
   "Copyright (c) Microsoft", "Microsoft Open Source Code of Conduct"), flag as
   template-owned and skip — do NOT recommend moving or modifying.

4. **Score 9 dimensions on content quality** (0 = missing, 1 = partial, 2 = complete).
   Score based on whether the content exists and is comprehensive — NOT on whether it
   lives in `.ai/`. A comprehensive OPERATIONS.md at root scores 2, not 1.

   See [references/scoring-rubric.md](references/scoring-rubric.md) for detailed criteria.

   | # | Dimension | What to check |
   |---|-----------|---------------|
   | 1 | Navigator | CLAUDE.md has navigation table linking documentation files |
   | 2 | Orientation | README explains what/why/quickstart with doc table |
   | 3 | Operations | Build/run/deploy documented in a dedicated file |
   | 4 | Architecture | System narrative with conventions exists |
   | 5 | Active state | Current goals + resume pointer documented |
   | 6 | Decision history | Shipped decisions preserved with rationale |
   | 7 | Constraints | Hard constraints explicitly documented and centralized |
   | 8 | Gotchas | Silent-failure traps inline in CLAUDE.md |
   | 9 | No duplication | "One fact, one home" — no content repeated across files |

5. **Apply location modifier.** After scoring content, deduct 1–2 points if docs are at
   root instead of `.ai/` (1 if most files are at root; 2 if also no clear navigation map).
   This ensures excellent content at root scores B+, not C.

6. **Compute grade:**
   - A (16–18): Comprehensive, current, properly located in `.ai/`
   - B+ (14–15): Excellent content, non-standard locations (migration recommended)
   - B (12–13): Good content, minor gaps or non-standard locations
   - C (8–11): Basic coverage, significant gaps
   - D (4–7): Sparse, mostly missing
   - F (0–3): No documentation structure

7. **Output scorecard** as a markdown table showing content scores, location modifier,
   and final grade + prioritized action items. Separate "Content Gaps" (missing or
   incomplete content) from "Migration Recommendations" (move to `.ai/`). Action items
   should be concrete ("move PLAN.md to .ai/memory/current-state.md") not vague.

## Mode 2: SCAFFOLD

Invocation: user asks to "scaffold docs", "set up project memory", "create .ai structure",
or is starting a new repo.

### Procedure

1. **Run silent audit** to identify what already exists.

2. **Detect repo type** by scanning for markers:
   - Fabric App: `rayfin.yml` present
   - Node/TS: `package.json` present
   - Power BI: `.pbip` or `.tmdl` files present
   - Python: `pyproject.toml` or `requirements.txt` present
   - Generic: none of the above

3. **Detect template-sourced files** — scan for upstream markers in SECURITY.md, LICENSE,
   CODE_OF_CONDUCT.md. Flag as template-owned, do not touch.

4. **Create directories:** `.ai/project/` and `.ai/memory/`.

5. **Generate starters for missing files** using templates from
   [references/templates.md](references/templates.md). Rules:
   - Only create files that the repo type warrants (e.g., skip `operations.md` for a
     simple library with no deploy process).
   - Templates contain section headings + TODO comments only. Never generate fake content.
   - Always create: `current-state.md`, `constraints.md` (even if minimal).
   - Create on demand: `architecture.md` (when repo has complex internals),
     `operations.md` (when repo has non-trivial ops), `agents.md` (when `.agents/` exists),
     `decisions.md` (when prior decisions exist to record), `pitfalls.md` (when lessons
     have accumulated).

6. **Wire `.claude/CLAUDE.md`** — create or update the navigation table to point to all
   `.ai/` docs. If CLAUDE.md doesn't exist, create a minimal one with the navigation table
   and a placeholder for agent SOPs.

7. **Migration checklist** — if root-level equivalents exist, output a numbered checklist:
   ```
   Migration checklist:
   1. [ ] Move PLAN.md → .ai/memory/current-state.md
   2. [ ] Move OPERATIONS.md → .ai/project/operations.md
   3. [ ] Update CLAUDE.md navigation table
   4. [ ] Update README.md doc table links
   5. [ ] Verify: npm run check:docs (if available)
   ```
   Do NOT auto-move files — the user decides when to migrate.

## Mode 3: CONSOLIDATE

Invocation: user asks to "consolidate", "crystallize session", "clean up memory",
"promote learnings", or after 3+ rounds of work have shipped.

### Procedure

1. **Scan ephemeral state:**
   - `~/.claude/projects/.../memory/*.md` for the current project
   - `~/.claude/plans/*.md` for active/completed plans
   - Read each file and extract content not already in repo `.ai/` files.

2. **Classify each piece** against the boundary-rules table above. For each unique finding,
   identify the target `.ai/` file and the specific section where it belongs.

3. **Propose insertions** — show each piece with its target file and insertion point.
   Format as diffs or quoted blocks. Let the user approve before writing.

4. **Archive shipped work:**
   - Move completed goals/phases from `current-state.md` to `decisions.md`.
   - Each archived decision should include: what was decided, why, what alternatives
     were rejected, and the **reversal cost** (how hard it would be to undo).

5. **Purge stale references:**
   - Grep the repo for ephemeral paths: `~/.claude/plans/`, `~/.claude/projects/`,
     bare `memory/` references.
   - Flag any matches for cleanup.

6. **Validation gate** (if available):
   - Run `npm run build` + `npm run lint` (if `package.json` exists)
   - Run `npm run check:docs` (if the script exists)
   - Report pass/fail.

7. **Summary** — output a table: what was promoted (and where), what was archived,
   what was discarded (already present or derivable from code), what stale references
   were found.

## Cross-Cutting Rules

- **Never generate fake content.** Starters have headings and TODOs. The user or agent
  fills them in during actual work.
- **Respect template provenance.** Files with upstream markers (Microsoft, Rayfin, etc.)
  are never touched. Detect by reading the first 5 lines for known headers.
- **Decisions include reversal cost.** Every entry in `decisions.md` should note how
  hard it would be to reverse the decision (trivial / moderate / expensive / irreversible).
  This is the single most valuable metadata most teams don't track.
- **"Why" over "what."** Memory entries should explain WHY a decision was made, not just
  WHAT was done. "Implemented Managed Identity" is useless; "Selected Managed Identity
  because it eliminates secret rotation and satisfies enterprise security review" survives
  five years.
- **Current-state decays fast.** `current-state.md` should be refreshed at least weekly.
  Stale goals mislead more than missing goals.
- **Critical gotchas stay in CLAUDE.md.** If a gotcha causes silent data corruption or
  invisible breakage when missed for one session, it belongs inline in CLAUDE.md, not
  in `.ai/memory/pitfalls.md`. The test: "would a fresh agent break something important
  if it didn't see this?" If yes → CLAUDE.md. If no → pitfalls.md.
