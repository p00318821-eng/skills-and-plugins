# Project notes

Context and decisions for this skills library that aren't obvious from the file
tree. Kept here so they survive beyond any single working session.

## Repository conventions

- **One folder = one skill.** Every top-level directory contains a `SKILL.md` at
  its root, plus any reference files that skill needs. No grouping/wrapper
  folders.
- **No submodules.** The repo previously organized skills as Git submodules
  (`mattpocock/skills`, `changyuanyu/mbti-persona-skill`, plus a
  `my-custom-skills/` grouping). These were flattened into plain vendored
  folders. `.gitmodules` was removed.
- **Attribution lives in `README.md`.** Each externally-sourced skill folder also
  retains its upstream license file (MIT/CC-BY) for license compliance; the
  human-readable credit is consolidated in the README's Attribution section.

## Skill origins

| Skill | Origin | License |
|---|---|---|
| caveman | Matt Pocock (locally modified) | MIT |
| grill-me, grill-with-docs, handoff, improve-codebase-architecture | Matt Pocock | MIT |
| mbti-persona | ChangyuanYU | MIT |
| task-observer (`one-skill-to-rule-them-all/`) | Eoghan Henn / rebelytics.com | CC BY 4.0 |
| pbi-visual-rendering, semantic-modeling-prepforai | Benjamin Hanna (Houston ISD) | own |

## Updating sourced skills

`skill-plugin-sources.json` is the source-of-truth manifest; `update-sourced-skills.ipynb`
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

### Known limitations (from code review)

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

## Recent plugin sync work

- Added three new external plugin packages to the repo:
  - `plugins/fabric-skills` from `microsoft/skills-for-fabric`
  - `plugins/powerbi` and `plugins/fabric` from `RuiRomano/powerbi-agentic-plugins`
  - `plugins/reports` from `data-goblin/power-bi-agentic-development`
- Copied the plugin skill folders into the top-level `skills/` directory so the
  repo can treat them as individual vendored skills.
- Updated `plugins/README.md` and `skills/README.md` with attribution for the
  new plugin sources and skill names.
- Extended `skill-plugin-sources.json` to track the new plugin directories, so
  `update-sourced-skills.ipynb` can sync them in the future.

## Local environment notes

- **Python:** the `python` command is the Windows Store stub; use the `py`
  launcher (Python 3.12.x) to run the notebook / scripts.
- **`git` works; `curl` is restricted.** Corporate Schannel policy blocks
  `curl`/HTTPS API calls with `CRYPT_E_NO_REVOCATION_CHECK`. Use `git`
  (clone / ls-remote) for anything that needs network. `gh` CLI is not installed.
- **The IDE auto-pushes.** The VS Code / Synapse Git integration can push commits
  to `origin/main` automatically. Don't assume a local commit is private — it may
  already be on GitHub. (This is why the initial flat-structure commit landed on
  remote `main` without an explicit `git push`.)
