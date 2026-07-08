---
description: "Agent tooling behavior for this repo — not project/domain constraints"
globs: []
alwaysApply: true
---

# Agent Operating Mandates

## No MCP for local file operations

Local file reads/writes use Claude Code's native Read/Grep/Edit tools, never a local-
filesystem MCP wrapper. This repo has no domain MCP server dependency to carve out —
the mandate applies without exception here.

## Structural output binding

Use the Read and Grep tools for file inspection — they already return line-numbered,
structured output and are the documented preference over raw Bash `cat`/`grep` in this
environment. Don't shell out to `cat -n`/`grep -Hn` here; that guidance is for
raw-terminal agents without an equivalent structured tool.

## Ring-buffer discipline

`.ai/PLAN.md` stays under 150 lines. At each milestone, slice the oldest entries
into `.ai/archive/` (committed to git, excluded only from default agent context) via a
`tail`/`head`/`>>` sequence.

## Windows Python: use `py`, not `python`

The bare `python` command resolves to the Windows Store stub, not a real interpreter —
it produces confusing "app not found" or no-op behavior instead of a clear error. Use the
`py` launcher (Python 3.12.x) to run notebooks and scripts (`py scripts/sync_engine.py`,
etc.).

## `curl` is blocked; use `git`/`gh` for network operations

Corporate Schannel policy blocks `curl`/HTTPS API calls with
`CRYPT_E_NO_REVOCATION_CHECK`. Anything that needs network access uses `git`
(clone / ls-remote) or the `gh` CLI (PRs, issues, repo API calls) instead — both are
installed and authenticated (verify with `gh auth status` if unsure). Don't assume `curl`
works even for something trivial; it doesn't.

## VS Code / Synapse Git integration auto-pushes to `origin/main`

Local commits are not private — the IDE's Git integration can push to `origin/main`
automatically without an explicit `git push`. Treat every local commit as already public;
this has already happened once (the initial flat-structure commit landed on remote `main`
without an explicit push).
