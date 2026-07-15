# Shipped — 2026-07

## Round 4 — Hook/agent extraction (`memory-architect` + `rayfin-companion`, 2026-07-10, CLOSED 2026-07-15)

Split both skills into skill + hook + agent pieces (see
`.ai/rules/000-agent-operating-mandates.md` peer note in `project-memory-template`'s
`.ai/rules/200-hook-authoring-conventions.md` for the authoring conventions this round
produced), tested against real installs — global `~/.claude/settings.json` for
`memory-architect`'s validation gate, both real Rayfin App projects
(`fabric-apps/fabric-app-campus-profile`, `fabric-apps/fabric-app-student-profile`) for
`rayfin-companion`'s hard-rules hooks. Branch
`feat/memory-architecture/hook-agent-extraction-round`: 3 commits — `049d9b6` (the split
itself), `9672a63` (merged `fix/github-mastery-protected-branch-guardrail`,
protected-branch guardrail + `~/.claude/hooks/protect-branches.js`), `8014428` (merged
`feat/deprecate-prepforai-global-hooks`, one hand-resolved `CHANGELOG.md` conflict).

**Task queue (build order `0 → 5 → 2 → 1 → 3 → 7 → 8 → 4 → 6`), all now done:**
1. Resync the global `memory-architect` copy — SHIPPED 2026-07-10. Added
   `memory-architect` + `domain-modeling` to `destinations.json`'s `skills_assigned`;
   verified byte-identical against repo source.
2. Register `memory-architect` in `origins.json` — SHIPPED 2026-07-10, as an "own skill"
   `excluded` entry, matching `github-mastery`'s pattern.
3. Review `github-mastery` for remaining hook/agent opportunities — CLOSED 2026-07-15,
   no action needed. `SKILL.md` already documents `protect-branches.js` as a
   `PreToolUse` backstop and credential-leak prevention as a guardrail; both hooks
   already exist in `~/.claude/hooks/`.
5. Full consolidation phase — SHIPPED 2026-07-10. Added hook/agent scaffold templates to
   `memory-architect/references/templates.md`; vendored `skills/domain-modeling/` from
   upstream (forked to target `.ai/CONTEXT.md`/`.ai/adr/`, tracked in `origins.json`'s
   `excluded` list like `caveman`); thinned `grill-with-docs/SKILL.md` to a delegator
   matching upstream's real shape; `memory-architect` SCAFFOLD now offers
   `.ai/CONTEXT.md`/`.ai/adr/` as an optional sibling tier. Flagged, not actioned:
   `memory-architect`'s own templates scaffold `.ai/project/`+`.ai/memory/`, but this
   repo (and `project-memory-template`) actually use `PLAN.md`+`rules/`+`archive/` —
   real inconsistency, separate future task.
7. Planning-phase skill fan-in hook design — `grill-me` unconditional, `grill-with-docs`
   stage-gated (not repo-state-gated), `caveman` dropped, `ponytail` kept as a `grill-me`
   peer. Formalizes a Plan Mode cycle: rough plan → verify → branch (trivial inline /
   hard → record + loop back) → crystallize → execute.
8. Skill-edit sync-check — global `PostToolUse` hook on `Edit|Write` warning
   (non-blocking) when `file_path` falls under a hardcoded downstream root instead of
   this repo.
4. Pre-checkin environmental-sync gate — local hook stays fast/non-blocking; real
   enforcement in a pre-push hook (decided); template owns rule *shape* one-way,
   versioned; "traveling" = conformance manifest + thin comparison script, not live
   hook code.
6. Push/PR decision, deferred until tasks 1-2 landed — pushed held branches together.
9. Vendor-fork tracking via SHA-based three-way diff — queued 2026-07-10, full detail in
   `project-memory-template/.ai/PLAN.md`.
10. Context-budget-aware planning — SHIPPED 2026-07-14 in `project-memory-template`
    (new Tier 1 rule `.ai/rules/300-context-budget-planning.md`).

## Round 5 — Central `agents/` + dispatch discipline (2026-07-15, CLOSED)

Repo folder renamed `skills-plugins-hooks-agents` to reflect broadened scope: a
**library of tools** (skills, plugins, agents, hooks-in-progress), consumed by
`project-memory-template` as a component rather than a memory-scaffolding replacement.
Added `agents/Explore.md` (override of the built-in Explore, pinned to `model: haiku` —
Claude Code v2.1.198+ has built-in Explore inherit the parent session's model, so on
Opus/Fable sessions every dispatch ran at premium cost until pinned) and
`agents/scout.md` (bounded doc/web researcher, `maxTurns: 15`, the gap Explore doesn't
cover). Verdict on Superpowers/ECC integration: borrow, don't install — both largely
duplicate machinery this repo's memory architecture already provides (plan mode +
`grill-me`, `.ai/PLAN.md` ring buffer + `memory-architect`, branch-lifecycle hooks);
installing either would contend for control of every session. Borrowed patterns
instead: fresh-subagent-per-task with two-stage review (Superpowers), model routing +
iterative retrieval + MCP-context frugality (ECC). Deployed to `~/.claude/agents/` —
first file in a previously-empty dir needed a session restart before pickup (watcher
limitation, verified against docs) — **verified working post-restart 2026-07-15**
(dispatched both `Explore` and `scout`, both returned correctly bounded results).
GitHub repo renamed `p00318821-eng/skills-and-plugins` →
`p00318821-eng/skills-plugins-hooks-agents` (user-confirmed, bundled into PR #12).
Added `hooks/README.md` — a documentation-only index of the 6 hooks currently live in
`~/.claude/hooks/` (branch protection, credential-leak guard, commit-convention
advisory, two HISD context-injection hooks, memory-architect validation gate). Not yet
centralized the way `agents/` is — the actual scripts still live outside the repo; full
centralization (source-of-truth here, deploy = copy) is Round 6.

PR #12 merged to `main` (`8c36a25`); local `main` fast-forwarded, feature branch deleted
(local + remote).

## Round 2 — Notebook consolidation + memory-architecture tooling (2026-07-07)

Merged three notebooks into `skills-workflow.ipynb` with a phase-selector widget;
extracted `scripts/ingest_engine.py`/`update_engine.py` to de-duplicate logic; built
`scripts/compile_claude_md.py` and `scripts/check_doc_links.py` (Python ports of the
Standard's compile/sync-check steps, since this repo has no Node toolchain). Ran a
`memory-architect` AUDIT that fixed several doc-hygiene gaps and generalized the skill
itself (language-agnostic SCAFFOLD step, new AUDIT dimension for migration
cleanliness).

## Hub-and-Spoke adoption (Compiled-only rung)

**Decision:** Adopted the Hub-and-Spoke Compiled-only rung from
`project-memory-template@3af6758`. Moved `CLAUDE.md` → `.claude/CLAUDE.md` (now a
compiled pointer file), renamed `docs/PROJECT-NOTES.md` → root `ARCHITECTURE.md`
(deduplicated), consolidated attribution onto `README.md` (regenerated the 93-row skill
table), added `.ai/rules/000-agent-operating-mandates.md`, deleted the orphaned
`skill-plugin-sources.json` stub. Absorbed a large pending expansion (~1,645 untracked
files: Azure/Foundry skills, azure-skills/deep-wiki plugins, the distribution-tooling
subsystem) into clean, reviewable commits as part of the same pass.

**Why:** The repo's doc/skill surface had grown well past what a single flat `CLAUDE.md`
could hold coherently, and there was no way for an agent or human to tell "this repo
follows a deliberate memory pattern" from "this `.ai/` folder happened by accident" —
adopting a published Standard (rather than inventing an ad hoc scheme) gave the repo a
name for its own structure and a way to self-identify via `.ai/LINEAGE.md`.

**Alternatives rejected:** Staying with a flat `CLAUDE.md` + `docs/PROJECT-NOTES.md`
(rejected — already past the Granularity Floor given the skill/plugin expansion
happening in the same round).

**Reversal cost:** Moderate — would require re-flattening `.ai/rules/` back into a single
hand-maintained `CLAUDE.md` and losing the `.ai/LINEAGE.md` self-identification; git
history preserves the prior flat `CLAUDE.md` content if ever needed.

**Date:** 2026-07-02

## Submodule-to-flat-folders migration

**Decision:** Replaced Git submodules (`mattpocock/skills` at `6da833d`,
`ChangyuanYU/mbti-persona-skill` at `8181d7b`, plus a `my-custom-skills/`-style
grouping) with plain vendored folders under `skills/`. `.gitmodules` was removed;
`d395fb7` ("Flatten skills to top-level folders; add update tooling and attribution")
is the commit where this landed.

**Why:** Submodules add clone/update friction that's inconsistent with this repo's
"dotfiles for AI" distribution use case — a fresh clone shouldn't need
`git submodule update --init` before the skills are usable, and distributing skills to
other environments (the whole point of `sync_orchestrator.ipynb`) is simpler against
plain folders than against submodule pointers.

**Alternatives rejected:** Keeping submodules (rejected — the friction described above).
Git subtree merges (not attempted — flat vendored copies plus the
`update-sourced-skills.ipynb` pull-tool achieved the same "stay in sync with upstream"
goal with less git-internals complexity).

**Reversal cost:** Moderate — would require re-establishing submodule pointers and
losing the flattened attribution/license-file layout built on top of the flat structure
since this migration (each vendored skill's own `LICENSE` copy, the README attribution
table).

## Recent plugin sync work (pre-dates this repo's `.ai/` adoption)

**Decision:** Added three external plugin packages (`plugins/fabric-skills` from
`microsoft/skills-for-fabric`, `plugins/powerbi` and `plugins/fabric` from
`RuiRomano/powerbi-agentic-plugins`, `plugins/reports` from
`data-goblin/power-bi-agentic-development`), then copied each plugin's skill folders
into the top-level `skills/` directory so the repo could treat them as individually
vendored skills (via `ddc7bab` "Expand repository to add plugins" and
`8092a66`/`5ae0fef` "Move skill files into skills/ directory"). `manifests/origins.json`
was extended to track the new plugin directories.

**Why:** Enable both plugin-native distribution (a plugin package installs as a unit in
tools that support the Claude Code plugin format) and per-skill vendoring (this repo's
own `sync_orchestrator.ipynb` distribution mechanism, which operates on individual skill
folders) simultaneously, without picking one delivery mechanism over the other.

**Alternatives rejected:** None recorded at the time this work shipped.

**Reversal cost:** Moderate — would require deleting the duplicated `skills/` copies and
updating any destination manifest entries that reference skills by name rather than by
parent plugin. **Cross-reference:** this is exactly the byte-duplication now flagged as
an open, unresolved decision in [`.ai/PLAN.md`](../PLAN.md) — the same pattern was
repeated for the `azure-skills` and `deep-wiki` plugins added in the 2026-07-02
Hub-and-Spoke migration round, so the duplication has grown rather than shrunk since
this entry was first true.
