---
name: semantic-modeling-prepforai
description: >
  DEPRECATED as an actively-invoked skill (2026-07-10). Its HISD-specific
  content is now delivered to Claude Code automatically via two global hooks
  (SessionStart + PostToolUse on .tmdl files), so it reaches any semantic-model
  editing skill regardless of which one is invoked — not just this one. Do not
  invoke this skill directly; see references/hisd-power-bi-context.md instead.
---

# Semantic Model Enhancement & Prep for AI (Deprecated)

This skill is deprecated as something to invoke directly. It previously drove a
manual copy/paste TMDL enhancement workflow ("export from Tabular Editor, paste
into chat, Claude enhances, paste back") that is now obsolete — that workflow
existed only because early AI tooling couldn't edit live models. Editing now
happens via MCP-first tools like `fabric-skills:semantic-model-authoring`,
which also has a more rigorously engineered generic AI-readiness workflow than
this skill ever had.

## What survives

The genuinely HISD-specific and gap-filling content — the synonym glossary, the
AI Instructions template, the dual synonym-annotation mechanics, the
AI-consumer compatibility matrix, the phantom-annotations list, and the
relationship naming pattern (a real gap in every comparison skill checked) —
is consolidated into
[references/hisd-power-bi-context.md](references/hisd-power-bi-context.md).

## How it reaches Claude now

Two global Claude Code hooks (registered in `~/.claude/settings.json`, outside
any single repo) deliver this content automatically:

1. **`SessionStart`** — points Claude at
   `references/hisd-power-bi-context.md` at the start of every session.
2. **`PostToolUse`** (scoped to `.tmdl` edits/writes) — reminds Claude to check
   that file after any `.tmdl` edit, regardless of which skill drove it.

See [references/global-hooks.md](references/global-hooks.md) for the hook
implementation (a reference copy — the live config is the source of truth).

## Why this folder still exists

This folder is retained, not deleted, because it's still
`scripts/sync_engine.py`'s existing distribution vehicle to
`~/.claude/skills/semantic-modeling-prepforai/` and
`~/.agents/skills/semantic-modeling-prepforai/` — the hooks above read the
reference file from that distributed path, not from this repo directly.
