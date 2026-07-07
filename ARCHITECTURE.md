# Architecture

Context and decisions for this skills library that aren't obvious from the file tree.
Kept here so they survive beyond any single working session.

> Environment/agent-tooling gotchas (Windows `py`, blocked `curl`, IDE auto-push, etc.)
> live in [.ai/rules/000-agent-operating-mandates.md](.ai/rules/000-agent-operating-mandates.md),
> compiled into [.claude/CLAUDE.md](.claude/CLAUDE.md) — not here.

## Repository conventions

- **One folder = one skill.** Every top-level directory contains a `SKILL.md` at
  its root, plus any reference files that skill needs. No grouping/wrapper
  folders.
- **No submodules.** The repo previously organized skills as Git submodules
  (`mattpocock/skills`, `changyuanyu/mbti-persona-skill`, plus a
  `my-custom-skills/` grouping). These were flattened into plain vendored
  folders. `.gitmodules` was removed. See [.ai/archive/](.ai/archive/) for the
  full decision record.
- **Attribution lives in `README.md`.** Each externally-sourced skill folder also
  retains its upstream license file (MIT/CC-BY) for license compliance; the
  human-readable credit is consolidated in the README's Attribution section —
  not restated here or in `plugins/README.md`.

## Constraints

Facts about this repo's license/update obligations — centralized here since they were
previously only inferable from scattered README prose.

- **License compliance is per-skill, not per-repo.** Each externally-sourced skill folder
  retains its own upstream license file (MIT/CC-BY) alongside its `SKILL.md`; the
  human-readable credit is consolidated in README's Attribution section. Deleting a
  vendored skill's license file is a compliance regression, not just a tidy-up.
- **`manifests/origins.json`'s `excluded` list is the authoritative source for which
  skills never auto-update, and why** — three categories:
  - **Locally modified** (e.g. `caveman`): diverged from upstream on purpose; an
    auto-update would silently overwrite intentional local changes.
  - **Own skills** (no upstream source): nothing to sync against.
  - **Plugin-extracted** (e.g. every `azure-skills`/`deep-wiki`/`fabric-skills`/`powerbi`/
    `reports` skill copied into `skills/`): these update via their parent plugin package's
    entry in `origins.json`, not individually — don't add them to Phase 2's per-skill
    update flow separately, that would be redundant with the plugin-level sync.
- **Tracked skills carry an upstream repo + subpath** and are the only ones Phase 2
  (`skills-workflow.ipynb`) offers to diff/update — everything in `excluded` is
  intentionally invisible to that flow.

## Skill Update Mechanism

`manifests/origins.json` is the source-of-truth manifest; `skills-workflow.ipynb`'s
Phase 2 (backed by `scripts/update_engine.py`) is the tool. It shallow-clones each
upstream repo, diffs its `subpath` against the local folder, prints a per-skill
change-list (with diffs), and lets you apply or disregard each update.

Design rules baked into the tool:

- **Excluded from updates:** `caveman` (locally modified to suit personal use),
  and the two own skills. These are listed under `excluded` in the manifest.
- **Never deletes.** Applying an update only *adds/overwrites* upstream files.
  Local-only files (e.g. the vendored `LICENSE` copies, README attribution) are
  always preserved and reported as "local-only (kept)".
- **`last_synced_sha` is informational.** Update detection is content-based
  (byte comparison), not SHA-based, so it stays correct even if the baseline SHA
  is unknown. The SHA is stamped back into the manifest on apply for reference.

### Known Limitations (from code review)

1. **Upstream deletions/renames don't propagate.** Because apply never deletes,
   an upstream *rename* leaves both the old and new file locally; an upstream
   *deletion* leaves the old file in place. These show up in the change-list as
   "local-only (kept)", so they're user-recoverable — review that list and
   remove stale files by hand when needed.
2. **Temp clones aren't cleaned up.** `update_engine.clone_upstream` creates one
   shallow clone per upstream repo in the OS temp dir per session and does not
   remove it. The OS eventually clears temp; delete manually if disk pressure
   matters.

Both are intentional trade-offs (never-delete protects local additions), not
bugs — recorded here so they're not rediscovered later.

## Distribution System

The repo includes a _distribute_ capability alongside the _pull_ mechanism above. The
distribution side pushes skill prompts into target files (e.g. CLAUDE.md,
copilot-instructions.md) for multiple AI tool environments. (`.claude/CLAUDE.md`'s
"Distribution Methods" section links here rather than restating this.)

### How it works

1. `manifests/destinations.json` defines where skills go — each entry has a
   `target_file` or `target_dir` (with `{HOME}`/`{REPO_ROOT}` expansion), a list
   of `skills_assigned`, and an `enabled` toggle. Assignments are edited via a
   `destinations-matrix.csv` spreadsheet round-trip (`scripts/generate_destinations_csv.py`
   / `scripts/update_destinations_from_csv.py`), wired into `skills-workflow.ipynb`'s
   Phase 3.
2. `scripts/sync_engine.py` is the shared Python library. Its `inject_markdown()`
   function uses HTML-comment boundary markers (`<!-- MANAGED-SKILLS:START -->` /
   `<!-- MANAGED-SKILLS:END -->`) to idempotently replace only the managed
   section, preserving any manual content outside the markers.
3. `skills-workflow.ipynb`'s Phase 4 is the interactive distribute step: Build
   Cache → Distribute → Report.

### Cache directory

Skill prompts are cached in `.cache/prompts/` (gitignored) as flat `.md` files.
This avoids mixing build artifacts with the vendored `skills/` folders.

### Relationship to the other phases

`skills-workflow.ipynb`'s Phase 2 (`scripts/update_engine.py`) handles _pulling_
from upstream repos. Phase 4 (`scripts/sync_engine.py`) handles _distributing_ to
local AI tool configs. They share `manifests/origins.json` but do different jobs —
kept as separate modules rather than folded into one, since "upstream → local"
and "origins/destinations → targets" are genuinely distinct data-flow directions.
