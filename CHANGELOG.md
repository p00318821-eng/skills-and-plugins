# Changelog

Dated by the day the work actually shipped (per git history), not by release
tag — this repo doesn't version by release.

## 2026-07-14

### Added
- `skills/sdi-backlog-writer/`: own skill (Benjamin Hanna / Houston ISD),
  hand-authored during the Discipline 2.1 SDI Follow-Up session. Converts a
  9-section HISD SDI Discovery Summary into Azure DevOps Epic/Feature/User
  Story markdown, mirroring the SDI Azure DevOps Backlog Writer Agent
  (Copilot Studio). Ingested into this repo via Phase 1 (`ingest_engine.py`)
  as an "own" classification, registered in `manifests/origins.json`'s
  `excluded` list, added to `claude-code-user`'s `skills_assigned`.

### Fixed
- `scripts/ingest_engine.py`'s `apply_ingest`: re-running Phase 1 ingest
  against an already-onboarded destination (e.g. `claude-code-user`, which
  is `enabled: true` with 14 skills already assigned) silently reset
  `enabled` to `false` and replaced `skills_assigned` wholesale instead of
  merging — discovered while ingesting `sdi-backlog-writer` above. Now
  merges `skills_assigned` (union) and leaves an existing destination's
  `enabled` flag untouched; only brand-new destinations get the
  starts-disabled default.

## 2026-07-10

### Added (Round 4 — consolidation phase)
- `skills/domain-modeling/`: vendored from `github.com/mattpocock/skills`
  (`skills/engineering/domain-modeling`), forked to target `.ai/CONTEXT.md` /
  `.ai/adr/` instead of upstream's root-level `CONTEXT.md` / `docs/adr/`, plus
  one added rule (check for an existing HISD-glossary owner before adding a
  term). Tracked in `manifests/origins.json`'s `excluded` list (locally
  modified, same treatment as `caveman`).
- `skills/memory-architect/references/templates.md`: hook/agent scaffold
  templates (courtesy-copy reference-doc template, `.cjs` hook skeleton,
  agent-definition skeleton) generalized from this round's two real, tested
  examples (`memory-architect`'s own validation gate, `rayfin-companion`'s
  hard-rules hooks); `.ai/CONTEXT.md` starter as an optional sibling tier to
  `current-state.md`/`decisions.md`/`pitfalls.md`.
- `manifests/origins.json`: registered `memory-architect` as an "own skill"
  entry (`excluded` list), matching `github-mastery`'s existing pattern — its
  repo footprint (`agents/`, `hooks/`, `scripts/`, four `references/*.md`
  files) now warrants the same tracking.
- `manifests/destinations.json`: added `memory-architect` and
  `domain-modeling` to `claude-code-user`/`cloud-agents`' `skills_assigned`
  (neither was registered anywhere, despite a stale hand-placed
  `memory-architect` copy already existing at `~/.claude/skills/`). Resynced
  both to `~/.claude/skills/` and `~/.agents/skills/` via
  `sync_engine.copy_skill_folder`, verified byte-identical to repo source.

### Added
- `memory-architect`: `scripts/detect-structure.js` (mechanical AUDIT/SCAFFOLD
  detection — file presence, legacy paths, template markers, repo type, on
  demand, not a hook — there's no tool-use event that means "run an audit"),
  `hooks/validation-gate.js` (global `Stop` hook: blocks ending a turn if `.ai/`
  is dirty and `build`/`lint`/`check:docs` fail; installed live in
  `~/.claude/settings.json` + `~/.claude/hooks/`), `agents/memory-consolidator.md`
  (dispatchable agent for CONSOLIDATE mode's scan/classify/propose loop),
  `references/global-hooks.md`, `references/agents.md`.
- `rayfin-companion`: `hooks/check-rayfin-rules.cjs` (`PostToolUse` backstop for
  hard rules 2/3/5/7/9) and `hooks/guard-rayfin-secrets.cjs` (`PreToolUse` guard
  blocking `git add`/`commit` of `rayfin/.env`/`rayfin/.temp/`, rule 10),
  `references/repo-hooks.md`. Installed live into both real Rayfin App projects
  (`fabric-apps/fabric-app-campus-profile`,
  `fabric-apps/fabric-app-student-profile`).
- `.ai/rules/200-hook-authoring-conventions.md` equivalent promoted upstream to
  `project-memory-template` (this repo's canonical reference) — see that repo's
  changelog/PLAN for the consolidation pass.
- Two global Claude Code hooks (`~/.claude/settings.json` + `~/.claude/hooks/`,
  outside this repo): `SessionStart` points Claude at HISD Power BI/Fabric
  context once per session; `PostToolUse` (scoped to `.tmdl` edits/writes)
  reminds Claude of HISD conventions after any `.tmdl` change — regardless of
  which skill (vendored or first-party) drove the edit. Reference copy at
  `skills/semantic-modeling-prepforai/references/global-hooks.md`.
- `skills/semantic-modeling-prepforai/references/hisd-power-bi-context.md`:
  consolidated HISD-specific content (synonym glossary, AI Instructions
  template, dual synonym-annotation mechanics, AI-consumer compatibility
  matrix, phantom-annotations list, relationship naming pattern) delivered by
  the hooks above.
- Fixed a pre-existing defect in the global `memory-architect` skill (outside
  this repo, `~/.claude/skills/memory-architect/`): its JIT-delivery design
  claimed a `PreToolUse` hook could inject `additionalContext` — verified
  false against official docs and a closed GitHub issue. Corrected to
  `PostToolUse` with `hookSpecificOutput.additionalContext` (not
  `updatedToolOutput`, which replaces rather than appends).
- `skills/github-mastery/SKILL.md`: promoted "never commit to a protected
  branch" to an explicit Guardrail with a pre-commit branch check, backed by a
  new global `PreToolUse` hook (`~/.claude/hooks/protect-branches.js`) that
  denies `git commit` on `main`/`master`/`staging`/`develop`.

### Changed
- `skills/grill-with-docs/SKILL.md`: thinned from an 89-line inlined copy of
  `domain-modeling`'s interview/CONTEXT-maintenance logic down to a short
  delegator matching upstream's real ~245-byte version — corrects a real
  architectural divergence (our copy had inlined logic that upstream keeps in
  a separate `domain-modeling` skill). `CONTEXT-FORMAT.md`/`ADR-FORMAT.md`
  moved from `grill-with-docs/` to the new `domain-modeling/` folder.
- `skills/memory-architect/SKILL.md`: SCAFFOLD mode's step 3 now lists
  hook/agent scaffolding and `.ai/CONTEXT.md`/`.ai/adr/` as offer-don't-auto-
  create options, alongside the existing on-demand file list.
- `memory-architect/SKILL.md`: AUDIT and SCAFFOLD modes now call
  `scripts/detect-structure.js` instead of re-deriving file-presence/legacy/
  template-marker facts by hand; CONSOLIDATE mode now dispatches
  `memory-consolidator` instead of running the scan/classify/propose loop inline.
- `rayfin-companion/SKILL.md`: Hard Rules section now points at the hook
  backstop for rules 2/3/5/7/9/10.
- Hook reference-doc naming standardized: `global-hooks.md` (installs once,
  applies to every repo) vs `repo-hooks.md` (installs per target project) —
  `memory-architect` and `rayfin-companion` renamed to match; `hooks/*.js`
  renamed to `hooks/*.cjs` for `rayfin-companion` after both real installs threw
  `ReferenceError: require is not defined` in the target projects' ESM
  (`"type": "module"`) `package.json`.
- `skills/semantic-modeling-prepforai/`: deprecated as an actively-invoked
  skill. `SKILL.md` reduced to a deprecation notice; the manual copy/paste
  TMDL workflow and its Truncation Prevention protocol are obsolete now that
  editing happens via MCP-first tools. Folder retained only because it's
  still `scripts/sync_engine.py`'s distribution vehicle to `~/.claude/skills/`
  and `~/.agents/skills/`, which the new global hooks read from.
- `manifests/origins.json`: updated the `semantic-modeling-prepforai` excluded
  entry's `reason` to explain the deprecation and why the folder still exists.

### Removed
- `skills/rayfin-companion/rayfin-companion/` — stale nested duplicate (byte-
  identical reference files, missing only `data-app-template.md` versus the
  root copy).
- `skills/semantic-modeling-prepforai/references/ai-compatibility-matrix.md`,
  `references/naming-conventions.yml`: content absorbed into
  `references/hisd-power-bi-context.md`.

## 2026-07-07

### Added
- `skills-workflow.ipynb`: single consolidated notebook (phase-selector widget
  over four independent phases — Ingest, Update from source, Assign
  destinations, Distribute), superseding the three notebooks below.
- `scripts/ingest_engine.py`, `scripts/update_engine.py`: pure-logic modules
  extracted from the retired notebooks/scripts, de-duplicating scan/classify/
  reconcile/apply and upstream-clone/diff/apply logic that previously existed
  in two parallel implementations each.
- `scripts/compile_claude_md.py`, `scripts/check_doc_links.py`: Python ports of
  the `project-memory-template` Hub-and-Spoke compile step and doc-link/sync
  checker, closing the gap where `.claude/CLAUDE.md` claimed to be a
  "GENERATED FILE" with no script that actually generated it.

### Changed
- `scripts/generate-destinations-csv.py` / `scripts/update-destinations-from-csv.py`
  renamed to underscore filenames and refactored into importable functions
  (`generate_csv`, `update_destinations_from_csv`), wired into the new
  notebook's Phase 3 instead of requiring a separate terminal step.
- `scripts/sync_engine.py`: removed `clone_upstream`/`extract_skill_content`/
  `fetch_skill` (unused — superseded by `scripts/update_engine.py`, which is
  now the single implementation of upstream fetch/diff logic).

### Removed
- `ingest-project.ipynb`, `update-sourced-skills.ipynb`, `sync_orchestrator.ipynb`:
  superseded by `skills-workflow.ipynb`.
- `scripts/ingest-destination.py`: retired CLI duplicate of the ingest
  notebook's logic (confirmed no external callers before removal).

## 2026-07-02

### Added
- Distribution system: `scripts/sync_engine.py` engine with idempotent
  boundary-marker injection, `sync_orchestrator.ipynb` notebook, and
  `manifests/destinations.json` manifest for routing skills to AI tool
  environments.
- `CLAUDE.md` with file map, SOPs, and environment gotchas.
- `.env.example` and `requirements.txt` (python-dotenv).
- `.cache/` directory (gitignored) for intermediate prompt cache.
- `ingest-project.ipynb`: two-phase workflow (dry-run + apply) to onboard an
  external project's skills into this repo and register the project as a
  distribution destination.
- 27 Azure/Entra/Foundry skills and the `plugins/azure-skills` package
  (Microsoft, `github.com/microsoft/skills`).
- 10 `wiki-*` documentation-generation skills and the `plugins/deep-wiki`
  package (same source).
- `skill-creator`, `mcp-builder` (Anthropic, `github.com/anthropics/skills`);
  `ponytail` (Dietrich Gebert); `microsoft-docs`, `continual-learning`,
  `github-issue-creator` (Microsoft, individually tracked); own skills
  `github-mastery`, `k12-dashboard-mockup`, `rayfin-companion`.

### Changed
- Migrated `skill-plugin-sources.json` to `manifests/origins.json` (format v2)
  with `type` and `format` fields. Old path is a one-line redirect stub.
- Fixed stale `local` paths in origins manifest to reflect the `skills/` move
  (e.g. `"grill-me"` → `"skills/grill-me"`).
- Updated `update-sourced-skills.ipynb` to read from `manifests/origins.json`.
- Expanded `.gitignore` to cover `.cache/`, `.env`, and `__pycache__/`.
- Adopted the Hub-and-Spoke memory architecture (Compiled-only rung — see
  `.ai/LINEAGE.md`): `CLAUDE.md` moved to `.claude/CLAUDE.md` and rewritten as a
  compiled pointer file; `docs/PROJECT-NOTES.md` renamed to root `ARCHITECTURE.md`
  with environment-gotchas and historical-narrative content relocated to
  `.ai/rules/000-agent-operating-mandates.md` and `.ai/archive/` respectively;
  attribution consolidated onto `README.md` (regenerated the skill table to cover
  all 93 skills, up from 44); `skill-plugin-sources.json` deleted (superseded by
  `manifests/origins.json`).

### Removed
- `skill-plugin-sources.json` orphaned stub — fully superseded by
  `manifests/origins.json`, no remaining references.

## 2026-06-02

### Added
- `skill-plugin-sources.json` manifest and `update-sourced-skills.ipynb` notebook to
  check externally-sourced skills for upstream updates, show a per-skill
  change-list with diffs, and apply or disregard each one.
- Vendored MIT `LICENSE` into each Matt Pocock skill folder (`caveman`,
  `grill-me`, `grill-with-docs`, `handoff`, `improve-codebase-architecture`).
- `docs/PROJECT-NOTES.md` capturing repository conventions, the update workflow,
  known updater limitations, and local-environment notes.
- This changelog.

### Changed
- Migrated from Git submodules to plain, self-contained per-skill folders
  (one `SKILL.md` per folder). Removed `.gitmodules` and the `mattpocock/`,
  `changyuanyu/`, and `my-custom-skills/` wrappers.
- Promoted `pbi-visual-rendering` and `semantic-modeling-prepforai` to top-level
  folders.
- Flattened `mbti-persona` out of its wrapper, keeping its upstream `LICENSE`.
- Rewrote `README.md` with a skills table, per-skill attribution, and update
  instructions; retitled the project `skills` to match the repository rename
  from `ben-skills`.

### Notes
- `caveman` is intentionally excluded from automated updates because it has been
  locally modified.
