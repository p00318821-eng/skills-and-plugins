# Plan — skills-and-plugins

> Active/current state. Capped at 150 lines — archive older entries to `.ai/archive/`.

## Active Goals

- **Round 5 — Central `agents/` + dispatch discipline, 2026-07-15 —
  IN PROGRESS.** Repo folder renamed `skills-plugins-hooks-agents` to reflect
  broadened scope: a **library of tools** (skills, plugins, agents, and — future
  round — hooks), consumed by `project-memory-template` as a component rather than
  a memory-scaffolding replacement. Added `agents/Explore.md` (override of the
  built-in Explore, pinned to `model: haiku` — Claude Code v2.1.198+ has built-in
  Explore inherit the parent session's model, so on Opus/Fable sessions every
  dispatch ran at premium cost until pinned) and `agents/scout.md` (bounded
  doc/web researcher, `maxTurns: 15`, the gap Explore doesn't cover). **Verdict on
  Superpowers/ECC integration: borrow, don't install** — both largely duplicate
  machinery this repo's memory architecture already provides (plan mode +
  `grill-me`, `.ai/PLAN.md` ring buffer + `memory-architect`, branch-lifecycle
  hooks); installing either would contend for control of every session. Borrowed
  patterns instead: fresh-subagent-per-task with two-stage review (Superpowers),
  model routing + iterative retrieval + MCP-context frugality (ECC). Deploy target
  `~/.claude/agents/` doesn't exist yet — first file requires a session restart to
  be picked up (watcher limitation, verified against docs). GitHub repo itself is
  still named `skills-and-plugins`; renaming it is a separate, explicitly-confirmed
  step (shared-resource action), not bundled into this round.
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

- **Round 4 — Hook/agent extraction (`memory-architect` + `rayfin-companion`),
  2026-07-10 — shipped in this repo, held (not pushed).** Split both skills
  into skill + hook + agent pieces (see `.ai/rules/000-agent-operating-mandates.md`
  peer note in `project-memory-template`'s
  `.ai/rules/200-hook-authoring-conventions.md` for the authoring conventions
  this round produced), tested against real installs — global
  `~/.claude/settings.json` for `memory-architect`'s validation gate, both real
  Rayfin App projects (`fabric-apps/fabric-app-campus-profile`,
  `fabric-apps/fabric-app-student-profile`) for `rayfin-companion`'s hard-rules
  hooks. Branch `feat/memory-architecture/hook-agent-extraction-round`: 3
  commits — `049d9b6` (the split itself), `9672a63` (merged
  `fix/github-mastery-protected-branch-guardrail`, protected-branch guardrail
  + `~/.claude/hooks/protect-branches.js`), `8014428` (merged
  `feat/deprecate-prepforai-global-hooks`, one hand-resolved `CHANGELOG.md`
  conflict). Working tree clean. **Deliberately not pushed** — too much still
  "in the air" to PR (see task 6 below).

### Round 4 task queue (full detail lives in `project-memory-template`'s
`.ai/PLAN.md` — this is the resume pointer for a session starting cold here
instead of there). **Build order:** `0 → 5 → 2 → 1 → 3 → 7 → 8 → 4 → 6`
(task 5 standardizes the hook/agent scaffold shape before tasks 3/7/8 each
produce another one-off instance of it; task 4 needs task 5's rule shape for
its versioning scheme). Task 0 (this file) is done as of this edit.

1. **Resync the global `memory-architect` copy — SHIPPED 2026-07-10.** Added
   `memory-architect` + `domain-modeling` to `destinations.json`'s
   `skills_assigned` (claude-code-user + cloud-agents — neither was
   registered). Used `sync_engine.copy_skill_folder` directly, not the full
   destination sync, since `~/.claude/skills/` also holds an unrelated
   `memory-architect-workspace/` eval directory the cleanup-inclusive sync
   would have deleted. Verified byte-identical against repo source.
2. **Register `memory-architect` in `origins.json` — SHIPPED 2026-07-10** as
   an "own skill" `excluded` entry, matching `github-mastery`'s pattern.
3. **Review `github-mastery` for remaining hook/agent opportunities**:
   credential-leak prevention (`.env`/`.key`/token commits, same shape as
   `guard-rayfin-secrets.cjs`) and commit-message/branch-naming enforcement.
   Own plan-mode pass before building.
5. **Full consolidation phase — SHIPPED 2026-07-10.** Added hook/agent
   scaffold templates to `memory-architect/references/templates.md`; vendored
   `skills/domain-modeling/` from upstream (forked to target `.ai/CONTEXT.md`/
   `.ai/adr/`, tracked in `origins.json`'s `excluded` list like `caveman`);
   thinned `grill-with-docs/SKILL.md` to a delegator matching upstream's real
   shape; `memory-architect` SCAFFOLD now offers `.ai/CONTEXT.md`/`.ai/adr/`
   as an optional sibling tier. **Flagged, not actioned:** `memory-architect`'s
   own templates scaffold `.ai/project/`+`.ai/memory/`, but this repo (and
   `project-memory-template`) actually use `PLAN.md`+`rules/`+`archive/` —
   `memory-architect`'s own host repo doesn't follow its own scaffolded
   structure. Real inconsistency, separate future task.
7. **Planning-phase skill fan-in hook design** — `grill-me` unconditional,
   `grill-with-docs` stage-gated (not repo-state-gated), `caveman` dropped,
   `ponytail` kept as a `grill-me` peer. Formalizes a Plan Mode cycle: rough
   plan → verify → branch (trivial inline / hard → record + loop back) →
   crystallize → execute. Complementary to task 10 below (7 = *which skills*
   fire during planning; 10 = *context-cost shape* of the resulting plan).
8. **Skill-edit sync-check** — global `PostToolUse` hook on `Edit|Write`
   warning (non-blocking) when `file_path` falls under a hardcoded downstream
   root instead of this repo.
4. **Pre-checkin environmental-sync gate** — local hook stays
   fast/non-blocking; real enforcement in a pre-push hook (decided); template
   owns rule *shape* one-way, versioned; "traveling" = conformance manifest +
   thin comparison script, not live hook code.
6. **Push/PR decision**, deferred until tasks 1-2 (or more) land — push all
   three held branches (`skills-and-plugins`, `fabric-apps`,
   `project-memory-template`) together, not piecemeal.
9. **Vendor-fork tracking via SHA-based three-way diff** — queued 2026-07-10:
   `domain-modeling`'s fork otherwise shows permanent false-positive diffs in
   `update_engine.py` forever. Fix: reuse `last_synced_sha` (already tracked)
   to also fetch upstream at that historical SHA, not just HEAD — no new
   storage needed. Generalizes to `caveman` too. Full detail in
   `project-memory-template/.ai/PLAN.md`.
10. **Context-budget-aware planning — SHIPPED 2026-07-14** in
    `project-memory-template` (new Tier 1 rule
    `.ai/rules/300-context-budget-planning.md`): classify plan phases by
    context cost, decide inline vs. delegate (`Agent` tool) vs. gate
    (human/`/compact` boundary) explicitly in the plan text. Full detail in
    `project-memory-template/.ai/PLAN.md`.

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

**Active round is Round 5** (central `agents/` + dispatch discipline) — `agents/`
folder created and populated, docs updated. Remaining: deploy to
`~/.claude/agents/`, append dispatch protocol to global `~/.claude/CLAUDE.md`,
update project memory, PR. Round 4 (hook/agent extraction) — tasks 0, 5, 2, 1, 10 done
(10 shipped in `project-memory-template`, unordered/low-urgency). Next: task 3
(review `github-mastery` for remaining hook/agent opportunities), per the
build order above. Round 3 remains open in parallel and
unblocked by Round 4: re-run Phase 4 distribution for
`semantic-modeling-prepforai` and one sibling skill (plan items 9-11), plus
the trigger-avoidance smoke test (plan item 11). The plugin/skills
byte-duplication decision from Round 2 is still open and unrelated to either
round.
