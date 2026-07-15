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
