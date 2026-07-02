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

## Skill Update Mechanism

`manifests/origins.json` is the source-of-truth manifest; `update-sourced-skills.ipynb`
is the tool. The notebook shallow-clones each upstream repo, diffs its `subpath`
against the local folder, prints a per-skill change-list (with diffs), and lets
you apply or disregard each update.

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
2. **Temp clones aren't cleaned up.** `clone_upstream` creates one shallow clone
   per upstream repo in the OS temp dir per session and does not remove it. The
   OS eventually clears temp; delete manually if disk pressure matters.

Both are intentional trade-offs (never-delete protects local additions), not
bugs — recorded here so they're not rediscovered later.

## Distribution System

The repo includes a _distribute_ capability alongside the _pull_ mechanism above. The
distribution side pushes skill prompts into target files (e.g. CLAUDE.md,
copilot-instructions.md) for multiple AI tool environments. (`.claude/CLAUDE.md`'s
"Distribution Methods" section links here rather than restating this.)

### How it works

1. `manifests/destinations.json` defines where skills go — each entry has a
   `target_file` (with `{HOME}` expansion), a list of `skills_assigned`, and an
   `enabled` toggle.
2. `scripts/sync_engine.py` is the shared Python library. Its `inject_markdown()`
   function uses HTML-comment boundary markers (`<!-- MANAGED-SKILLS:START -->` /
   `<!-- MANAGED-SKILLS:END -->`) to idempotently replace only the managed
   section, preserving any manual content outside the markers.
3. `sync_orchestrator.ipynb` is the interactive tool: Init → Build Cache →
   Distribute → Report.

### Cache directory

Skill prompts are cached in `.cache/prompts/` (gitignored) as flat `.md` files.
This avoids mixing build artifacts with the vendored `skills/` folders.

### Relationship to the update notebook

`update-sourced-skills.ipynb` handles _pulling_ from upstream repos.
`sync_orchestrator.ipynb` handles _distributing_ to local AI tool configs.
They share `manifests/origins.json` but do different jobs.
