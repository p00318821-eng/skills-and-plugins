# Plan — skills-plugins-hooks-agents

> Active/current state. Capped at 150 lines — archive older entries to `.ai/archive/`.

## Active Goals

- **Round 7 — Deterministic plan-mode skill-invocation gate — SHIPPED
  2026-07-21** (PR #19 merged `5241994`). New `PreToolUse`/`ExitPlanMode`
  hook (`hooks/gate-plan-mode-skill-invocation.js`) hard-blocks exiting plan
  mode unless an allow-listed planning skill (`grill-me`, `grill-with-docs`,
  `ponytail`, `microsoft-docs`, `memory-architect`) was invoked via the Skill
  tool this session — replaces relying on the model to notice
  `suggest-planning-skills.js`'s advisory nudge with a real enforcement
  point. Second documented exception to `hooks/README.md`'s blocking bar,
  alongside `gate-push-rule-manifest.js`. Allow path attaches a compact-prep
  `additionalContext` reminder (don't jump into code before durably
  recording plan-round state, since `/compact` may follow `ExitPlanMode`).
  Handoff doc landed in `project-memory-template-hisd` (PR #14 merged
  `9acb48a`) for its `memory-architect` CONSOLIDATE pass to fold into
  `.ai/rules/500-planning-skill-fan-in.md`. **Open residual gap (accepted,
  not solved):** the gate is coarse — any allow-listed skill satisfies it,
  not necessarily the *right* one for the task (e.g. doesn't guarantee
  `/microsoft-docs` ran when platform-behavior uncertainty was the actual
  issue). **Also open:** live confirmation that `ExitPlanMode` actually
  fires as a `PreToolUse` matcher in Claude Code wasn't forced this round
  (would have required overwriting the approved plan file to test) — hook
  logic itself (deny/allow/fail-open/non-match) was verified directly via
  crafted stdin payloads; the matcher-firing question resolves itself the
  next time any session completes a plan-mode cycle.
- **Round 6 — Hooks migration — SHIPPED 2026-07-15** (PR #13 merged `a8e61f2`,
  `hooks/` is now the source of truth for all 6 hook scripts, `~/.claude/hooks/`
  is the deployed copy). Full detail in `.ai/archive/2026-07-shipped.md`.
- **Round 5 — Central `agents/` + dispatch discipline — SHIPPED 2026-07-15**
  (PR #12 merged `8c36a25`, GitHub repo renamed `skills-plugins-hooks-agents`,
  deployed agents verified working). Full detail in
  `.ai/archive/2026-07-shipped.md`.
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
- **Round 2 — Notebook consolidation + memory-architecture tooling — SHIPPED
  2026-07-07.** Round 1 (Hub-and-Spoke adoption) shipped 2026-07-02. Both — see
  `.ai/archive/2026-07-shipped.md`.

- **Round 4 — Hook/agent extraction (`memory-architect` + `rayfin-companion`) —
  CLOSED 2026-07-15, all 10 tasks done** (build order `0→5→2→1→3→7→8→4→6`; task
  3 was the last one open, closed same day as Round 5, no action needed — see
  above). Full detail (commits, per-task notes) in
  `.ai/archive/2026-07-shipped.md`.

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

**Rounds 4, 5, 6, and 7 all CLOSED** (7 on 2026-07-21) — see Active Goals
above and `.ai/archive/2026-07-shipped.md` for full detail. No round is
currently active; next round not yet chosen. Round 3 remains open in parallel and
unblocked by Round 4: re-run Phase 4 distribution for
`semantic-modeling-prepforai` and one sibling skill (plan items 9-11), plus
the trigger-avoidance smoke test (plan item 11). The plugin/skills
byte-duplication decision from Round 2 is still open and unrelated to either
round.
