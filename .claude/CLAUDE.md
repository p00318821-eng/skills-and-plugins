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

## Agent SOPs

Infrastructure changes to `.ai/rules/` route through the `memory-architect` skill (AUDIT
before changing anything, SCAFFOLD for new pieces, CONSOLIDATE periodically or after an ad
hoc request produces new learnings) — not ad hoc edits to this file. See
[.ai/LINEAGE.md](../.ai/LINEAGE.md).

- **Pull updates:** Run `update-sourced-skills.ipynb` in VS Code. Review diffs, apply/skip per skill.
- **Distribute skills:** Run `sync_orchestrator.ipynb`. Copies skill folders to discovery directories and injects markdown blocks into target files.
- **Add a new upstream skill:** Add entry to `manifests/origins.json`, run update notebook.
- **Manage destinations (recommended):**
  1. Run `py scripts/generate-destinations-csv.py` → exports `destinations-matrix.csv` with source categories (tracked, own, fork, plugin-extracted)
  2. Edit the CSV: add `x` to assign skills, add columns for new destinations, remove rows for unneeded skills
  3. Run `py scripts/update-destinations-from-csv.py` → updates `manifests/destinations.json`
  4. Run `sync_orchestrator.ipynb` to apply changes
- **Ingest a new project (two-phase workflow):**
  - **Phase 1 (one-time initial intake):**
    1. Dry-run: `py scripts/ingest-destination.py --source {project-path} --destination-id {id}`
    2. Review reconciliation report: new skills, changed skills (with diffs), skills not in project
    3. Apply: `py scripts/ingest-destination.py --source {project-path} --destination-id {id} --apply --target-dir {target}`
    4. Classify each new skill interactively: **[T]racked** (provide upstream repo), **[F]ork** (modified from upstream), **[O]wn** (no upstream), **[S]kip**
    5. Reconcile each changed skill: **[C]entral** (keep central version), **[P]roject** (take project edits), **[S]kip**
    6. Central imports skills, project becomes a destination (starts disabled)
  - **Phase 2 (ongoing distribution):**
    1. Central is now source of truth
    2. Generate CSV: `py scripts/generate-destinations-csv.py` (reflects newly imported skills)
    3. Edit CSV: assign skills to destinations, enable the new project destination
    4. Convert: `py scripts/update-destinations-from-csv.py`
    5. Distribute: run `sync_orchestrator.ipynb`
    6. No more scanning/importing; central controls what goes to project
- **Add your own skill:** Create `skills/{name}/SKILL.md`, add to `excluded` in origins.json.
- **Add a destination manually:** Edit `manifests/destinations.json` directly, add entry with `enabled: true`, `method` (skill-folder-copy or markdown-boundary), and `target_dir`/`target_file`.

## File Map

| Path | Purpose |
|------|---------|
| `skills/` | Vendored skill folders (each: SKILL.md + references) |
| `plugins/` | Plugin packages (azure-skills, deep-wiki, fabric, fabric-skills, powerbi, reports) |
| `manifests/origins.json` | Tracks where each skill is sourced from (v2 format) |
| `manifests/destinations.json` | Tracks where skills get distributed to |
| `scripts/sync_engine.py` | Distribution engine: folder-copy + markdown-boundary methods |
| `scripts/generate-destinations-csv.py` | Export destinations as editable spreadsheet |
| `scripts/update-destinations-from-csv.py` | Convert spreadsheet back to destinations.json |
| `update-sourced-skills.ipynb` | Fetch upstream skill updates (interactive) |
| `sync_orchestrator.ipynb` | Distribute skills to configured destinations |
| `ingest-project.ipynb` | Two-phase workflow to ingest an external project's skills |
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
