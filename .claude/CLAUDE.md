<!-- GENERATED FILE — compiled from ALL .ai/rules/*.md files (Compiled-only Hub-and-Spoke
     rung — no JIT hook exists to hold Tier 2 content back, see .ai/LINEAGE.md). Do not
     hand-edit the "Agent Operating Mandates & Gotchas" section below; edit the source
     rule files and recompile. The Navigation Map, Agent SOPs, File Map, and Distribution
     Methods sections are hand-authored boilerplate and may be edited directly. -->

# Agent Operating Instructions — skills-and-plugins

## Navigation Map

| You need… | Read |
|-----------|------|
| What this repo is / quickstart | [README.md](../README.md) |
| Conventions, skill-update mechanism, distribution system narrative | [ARCHITECTURE.md](../ARCHITECTURE.md) |
| Current goals + open decisions | [.ai/PLAN.md](../.ai/PLAN.md) |
| Historical decisions, rationale | [.ai/archive/](../.ai/archive/) |
| Rule sources (edit here, not below — this file is compiled) | [.ai/rules/](../.ai/rules/) |
| Why this repo's memory is structured this way | [.ai/LINEAGE.md](../.ai/LINEAGE.md) |
| What changed, by release | [CHANGELOG.md](../CHANGELOG.md) |

This table mirrors README.md's "Documentation" table (kept separately since this file is
auto-loaded by agents at session start, while README.md is the human-facing GitHub entry
point) — update both if the doc set changes.

## Agent SOPs

Infrastructure changes to `.ai/rules/` route through the `memory-architect` skill (AUDIT
before changing anything, SCAFFOLD for new pieces, CONSOLIDATE periodically or after an ad
hoc request produces new learnings) — not ad hoc edits to this file. See
[.ai/LINEAGE.md](../.ai/LINEAGE.md).

All four lifecycle steps below live in one notebook, **`skills-workflow.ipynb`** —
a phase-selector widget at the top lets you run just the phase(s) you need this
session; each phase reads its own state fresh from disk, so they don't have to
run in order. Phase logic lives in `scripts/`, the notebook is a thin UI shell.

- **Phase 1 — Ingest a new project's skills:** scan a project's skill directory
  vs. central, classify each new skill (**[T]racked**/**[F]ork**/**[O]wn**/**[S]kip**),
  reconcile each changed one (**[C]entral**/**[P]roject**/**[S]kip**), apply, then
  verify the manifest ledger. Backed by `scripts/ingest_engine.py`. Central
  becomes source of truth; the project becomes a destination (starts disabled).
- **Phase 2 — Pull updates from upstream:** shallow-clones each tracked skill's
  upstream repo, diffs vs. local, shows added/modified files (with diffs), lets
  you apply or skip per skill. Backed by `scripts/update_engine.py`.
- **Phase 3 — Assign destinations:** a deliberate spreadsheet handoff, not an
  in-notebook grid editor. Export `destinations-matrix.csv`
  (`scripts/generate_destinations_csv.py`), edit it in Excel (add `x` to assign
  a skill to a destination, add columns for new destinations), then re-import
  (`scripts/update_destinations_from_csv.py`) to rewrite `manifests/destinations.json`.
- **Phase 4 — Distribute:** fully automatable, no human decision points. Builds
  the prompt cache and pushes to every enabled destination via
  `scripts/sync_engine.py` (folder-copy or markdown-boundary injection).
- **Add a new upstream skill:** add entry to `manifests/origins.json`, run Phase 2.
- **Add your own skill:** Create `skills/{name}/SKILL.md`, add to `excluded` in origins.json.
- **Add a destination manually:** Edit `manifests/destinations.json` directly, add entry with `enabled: true`, `method` (skill-folder-copy or markdown-boundary), and `target_dir`/`target_file`.

## File Map

| Path | Purpose |
|------|---------|
| `skills/` | Vendored skill folders (each: SKILL.md + references) |
| `plugins/` | Plugin packages (azure-skills, deep-wiki, fabric, fabric-skills, powerbi, reports) |
| `manifests/origins.json` | Tracks where each skill is sourced from (v2 format) |
| `manifests/destinations.json` | Tracks where skills get distributed to |
| `skills-workflow.ipynb` | Single interactive notebook: Ingest → Update from source → Assign destinations → Distribute |
| `scripts/ingest_engine.py` | Ingest/classify/reconcile/apply logic (Phase 1) |
| `scripts/update_engine.py` | Upstream clone/diff/apply logic (Phase 2) |
| `scripts/sync_engine.py` | Distribution engine: folder-copy + markdown-boundary methods (Phase 4) |
| `scripts/generate_destinations_csv.py` | Export destinations as editable spreadsheet (Phase 3) |
| `scripts/update_destinations_from_csv.py` | Convert spreadsheet back to destinations.json (Phase 3) |
| `scripts/compile_claude_md.py` | Regenerates this file's compiled section from `.ai/rules/*.md` |
| `scripts/check_doc_links.py` | Validates doc links + Hub-and-Spoke sync (manual gate — no CI in this repo) |
| `ARCHITECTURE.md` | Conventions, decisions, skill-update/distribution mechanics |
| `.ai/rules/` | Agent gotcha/convention source of truth, compiled into this file |

## Distribution Methods

Full narrative (cache directory, relationship to the update notebook) lives in
[ARCHITECTURE.md § Distribution System](../ARCHITECTURE.md#distribution-system). Summary:
the sync engine supports **skill-folder-copy** (copies whole skill folders to discovery
directories — idempotent, unassigned skills deleted) and **markdown-boundary** (injects
concatenated skill prompts between `<!-- MANAGED-SKILLS:START/END -->` markers into a
single instruction file — never edit between markers manually).

## Agent Operating Mandates & Gotchas

<!-- COMPILED (Rung 1 — Compiled-only): every rule file in .ai/rules/ compiles here in
     full, regardless of alwaysApply/globs, because no PreToolUse hook exists to hold
     Tier 2 content back. Currently the only rule file is 000-agent-operating-mandates.md. -->

### No MCP for local file operations

Local file reads/writes use Claude Code's native Read/Grep/Edit tools, never a local-
filesystem MCP wrapper. This repo has no domain MCP server dependency to carve out —
the mandate applies without exception here.

### Structural output binding

Use the Read and Grep tools for file inspection — they already return line-numbered,
structured output and are the documented preference over raw Bash `cat`/`grep` in this
environment. Don't shell out to `cat -n`/`grep -Hn` here; that guidance is for
raw-terminal agents without an equivalent structured tool.

### Ring-buffer discipline

`.ai/PLAN.md` stays under 150 lines. At each milestone, slice the oldest entries
into `.ai/archive/` (committed to git, excluded only from default agent context) via a
`tail`/`head`/`>>` sequence.

### Windows Python: use `py`, not `python`

The bare `python` command resolves to the Windows Store stub, not a real interpreter —
it produces confusing "app not found" or no-op behavior instead of a clear error. Use the
`py` launcher (Python 3.12.x) to run notebooks and scripts (`py scripts/sync_engine.py`,
etc.).

### `curl` is blocked; use `git` for network operations

Corporate Schannel policy blocks `curl`/HTTPS API calls with
`CRYPT_E_NO_REVOCATION_CHECK`. Anything that needs network access uses `git`
(clone / ls-remote) instead. The `gh` CLI is not installed — don't assume it's available.

### VS Code / Synapse Git integration auto-pushes to `origin/main`

Local commits are not private — the IDE's Git integration can push to `origin/main`
automatically without an explicit `git push`. Treat every local commit as already public;
this has already happened once (the initial flat-structure commit landed on remote `main`
without an explicit push).
