# Agents

Custom subagent definitions, tracked centrally here the same way `skills/` and
`plugins/` are. `~/.claude/agents/` is the deployed copy Claude Code actually reads;
deploying is a straight file copy (no build step). Edit here, then re-copy — see
[ARCHITECTURE.md](../ARCHITECTURE.md) for the broader "central source of truth, repo
is a destination" pattern this repo uses for skills.

- **Explore.md** — pins the built-in `Explore` name to `model: haiku` so exploration
  dispatches don't inherit the parent session's (potentially premium) model.
- **scout.md** — bounded researcher for doc/web lookups Explore doesn't cover
  (read-only local tools + WebFetch/WebSearch, `maxTurns: 15`).
- **sql-pro.md**, **python-pro.md** — vendored from
  [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents),
  `categories/02-language-specialists`. Tracked via `manifests/origins.json`'s
  `language-specialist-agents` entry (`forked: true`, `local: agents`, `subpath:
  categories/02-language-specialists`) — a curated subset, not a full mirror. The
  ~30 sibling agents in that upstream category we haven't adopted always show up in
  Phase 2's `fork_delta` (that's the intended "available to mine" signal, browse the
  category for more candidates); genuine upstream edits to files we *have* adopted
  show as real drift in `added`/`modified`. Adopt a new one by copying its `.md` file
  straight into this folder.

## Vendored tool: `tools/subagent-catalog`

`tools/subagent-catalog` (also tracked in `origins.json`, plain mirror, not forked)
is VoltAgent's own on-demand lookup mechanism for the other ~160 agents in their
catalog — `/subagent-catalog:search`, `:fetch`, `:list`, `:invalidate` slash
commands with a 12h cache, installed by copying that folder to
`~/.claude/commands/`. Use it to browse/fetch a pattern ad hoc before deciding
whether it's worth adopting into `agents/` the way sql-pro/python-pro were.
