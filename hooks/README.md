# Hooks

Tracked centrally here the same way `skills/`, `plugins/`, and `agents/` are.
`~/.claude/hooks/` is the deployed copy Claude Code actually reads; deploying is a
straight file copy (no build step). Edit here, then re-copy — same "central source of
truth, repo is a destination" pattern `agents/README.md` documents.

**Registration is not centralized.** The event/matcher wiring (which hook fires on
which `PreToolUse`/`PostToolUse`/`SessionStart`/`Stop` event) lives in
`~/.claude/settings.json`'s `hooks: {...}` block, outside this repo — that file is a
global, user-specific config with unrelated permissions/model settings mixed in. Adding
a new hook script here doesn't register it; that's still a manual edit to
`settings.json`.

## Current hooks

| Hook | Event / matcher | Behavior | Purpose |
|------|------------------|----------|---------|
| `protect-branches.js` | `PreToolUse` (Bash) | **Blocks** `git commit` while checked out on `main`/`master`/`staging`/`develop` | Systemic guardrail so branch discipline doesn't depend on an agent remembering to self-enforce it |
| `guard-credential-leak.js` | `PreToolUse` (Bash) | **Blocks** `git commit` when a staged file matches a sensitive pattern (`.env`, `.key`, `.pem`, credentials JSON, etc.) | Checks the actual staged file list, not just the command text, so it catches `git add -A`/`git add .` too |
| `enforce-commit-conventions.js` | `PreToolUse` (Bash) | **Warns only** (`additionalContext`) when a `git commit -m` message doesn't match `type(scope): subject` | Style guardrail backing `github-mastery`'s commit conventions; deliberately non-blocking — legitimate exceptions (merges, reverts, WIP branches) are common. Validates only the first line of a multi-line message, so a well-formed subject with a body no longer false-positives |
| `gate-push-rule-manifest.js` | `PreToolUse` (Bash, `git push` only) | **Blocks** the push when a repo has a `.ai/` directory but no `.ai/rule-manifest.json`; **warns only** (`additionalContext`) when the manifest is present but its `shapeVersion` is behind the template's | Enforces `project-memory-template-hisd`'s rule-shape versioning at the moment "pre-checkin" actually names; resolves repo root via a `.git`-ancestor walk-up so a push from a subdirectory still resolves correctly. Blocking here is a deliberate, documented exception to the blocking bar below — see `project-memory-template-hisd/.ai/rules/502-rule-shape-manifest.md` |
| `hisd-session-start.js` | `SessionStart` | Injects a pointer to `~/.claude/skills/semantic-modeling-prepforai/references/hisd-power-bi-context.md` | HISD-specific Power BI/Fabric naming/synonym conventions reach any semantic-model work regardless of which skill drives it |
| `hisd-tmdl-reminder.js` | `PostToolUse` (`Edit\|Write`) | Injects the same HISD context after edits to `.tmdl` files | Same goal as above, fired at edit time instead of session start |
| `memory-architect-validation-gate.js` | `Stop` | Validates `.ai/` scaffolding conventions at session end | Backs the `memory-architect` skill's structural rules |
| `suggest-planning-skills.js` | `PreToolUse` (`EnterPlanMode`) | **Warns only** (`additionalContext`) with relevant planning skills based on cheap file/dir presence checks (`.ai/`, `.pbip`/`.tmdl`, `.bicep`/`.tf`) | Lightweight fan-in nudge so planning-phase skills (`grill-me`, `memory-architect`, `fabric-skills`, etc.) aren't missed just because the agent didn't think to look |
| `check-upstream-sync.js` | `PostToolUse` (`Edit\|Write`) | **Warns only** (`additionalContext`) when an edit lands in a downstream install copy (`~/.claude/skills`, `~/.claude/hooks`, `~/.claude/agents`, `~/.agents/skills`, `~/.copilot/skills`, `~/.github/copilot-instructions.md`) without a matching change here | Catches exactly the mistake that motivated it: a fix patched into a downstream copy that never makes it back to this repo, so it's lost on the next resync |

## Design pattern

- **Fail open, always.** Every hook above treats its own internal errors (parsing
  input, reading repo state) as non-blocking — a bug in a hook must never itself
  block an unrelated `Bash` call.
- **Blocking is reserved for security-shaped guardrails** (branch protection,
  credential leaks) where a violation is unambiguous and cheap to check. Everything
  softer (style, staleness, conventions) stays advisory via `additionalContext`,
  never a hard deny — see `enforce-commit-conventions.js` for the rationale.
- **Systemic over per-skill.** These fire regardless of which skill or agent issued
  the triggering tool call, rather than relying on each skill to remember to
  self-enforce the same rule.
