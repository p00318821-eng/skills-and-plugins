# Templates

Starter templates for `.ai/` files. Each template contains section headings and TODO
placeholders only — never generate fake content. Select the repo-type variant when
available; fall back to Generic.

---

## `.ai/memory/current-state.md`

```markdown
# Current State

> Last updated: YYYY-MM-DD

## Active Goals

<!-- TODO: List current sprint/round goals. Keep this short — 3-5 items max. -->

## Open Blockers

<!-- TODO: List anything blocking progress. Remove when resolved. -->

## Resume Pointer

<!-- TODO: Where should the next session pick up? One sentence. -->
```

---

## `.ai/memory/decisions.md`

```markdown
# Decisions

Shipped decisions with rationale. Most recent first.

<!-- Each entry should include:
  - **Decision:** What was decided
  - **Why:** The reasoning and constraints that drove the decision
  - **Alternatives rejected:** What else was considered and why it lost
  - **Reversal cost:** trivial / moderate / expensive / irreversible
  - **Date:** When the decision was made
-->

<!-- TODO: Add first decision entry when a significant choice is made. -->
```

---

## `.ai/memory/pitfalls.md`

```markdown
# Pitfalls & Lessons Learned

Non-critical gotchas and lessons from past work. For agent-critical gotchas that cause
silent data corruption, put those in `.claude/CLAUDE.md` instead.

<!-- Each entry should include:
  - **What happened:** Brief description of the failure or surprise
  - **Root cause:** Why it happened
  - **Fix/workaround:** What solved it
  - **How to avoid:** What to check in the future
-->

<!-- TODO: Add first entry after encountering a non-obvious failure. -->
```

---

## `.ai/project/constraints.md`

```markdown
# Constraints

Hard constraints that apply regardless of current goals or plan phase. These are the
most valuable memory — they rarely change and explain WHY most architectural decisions
were made.

## Platform / Infrastructure

<!-- TODO: e.g., "Must deploy to Azure", "Embed-only (runs inside Fabric portal)" -->

## Compliance / Security

<!-- TODO: e.g., "FERPA: all queries must aggregate to campus grain", "No student PII in logs" -->

## Team / Budget

<!-- TODO: e.g., "Solo developer", "No dedicated DevOps" -->

## API / Integration

<!-- TODO: e.g., "One EVALUATE per DAX query (SDK limit)", "Rate-limited to N concurrent" -->
```

---

## `.ai/project/architecture.md`

### Generic variant

```markdown
# Architecture

System narrative — how the pieces fit together and why.

## Overview

<!-- TODO: 2-3 paragraph narrative of the system architecture. -->

## Key Components

<!-- TODO: List major components/modules and their responsibilities. -->

## Conventions

<!-- TODO: Coding patterns, naming conventions, file organization rules. -->

## Data Flow

<!-- TODO: How data moves through the system. -->
```

### Fabric App variant

```markdown
# Architecture

System narrative for this Fabric App — how the pieces fit together and why.

## Overview

<!-- TODO: App type (operational vs analytical), data source, embedding model. -->

## Data Layer

<!-- TODO: Semantic model name, connection alias, query pattern (one EVALUATE per .dax file). -->

## Query Conventions

<!-- TODO: DAX file naming, factory pattern, column metadata format. -->

## Visualization Conventions

<!-- TODO: Chart library, known gotchas, print considerations. -->

## Print Pipeline

<!-- TODO: If the app prints, document the pipeline (print-window.ts, CSS, chart sizing). -->
```

### Power BI variant

```markdown
# Architecture

Architecture for this Power BI project.

## Semantic Model

<!-- TODO: Model name, data source, refresh schedule. -->

## Measures & Calculations

<!-- TODO: Key measure groups, calculation patterns, formatting conventions. -->

## Report Structure

<!-- TODO: Page layout, visual types, interaction patterns. -->
```

---

## `.ai/project/operations.md`

### Generic variant

```markdown
# Operations

Build, run, deploy, and troubleshoot.

## Prerequisites

<!-- TODO: Required tools, versions, accounts. -->

## Build & Dev

<!-- TODO: Commands table: install, dev, build, lint, test. -->

## Deploy

<!-- TODO: Deployment steps and environment details. -->

## Troubleshoot

<!-- TODO: Common symptoms and fixes table. -->
```

### Fabric App variant

```markdown
# Operations

Build, run, authenticate, deploy, validate, and troubleshoot.

## Prerequisites

<!-- TODO: Node version, Azure CLI, other tools. -->

## Build & Dev

| Task | Command | Notes |
|------|---------|-------|
| Install | `npm install` | |
| Build | `npm run build` | <!-- TODO: what it runs --> |
| Lint | `npm run lint` | |
| Test | `npm run test` | |

## Authentication

<!-- TODO: az login command, tenant ID, SSO details. -->

## Local Dev Inside the Fabric Embed

<!-- TODO: Deploy-to-preview workflow (standard) and devUri (advanced). -->

## Deploy

<!-- TODO: rayfin up commands, rollback procedure. -->

## Troubleshoot

| Symptom | Cause / Fix |
|---------|-------------|
| <!-- TODO --> | <!-- TODO --> |
```

---

## `.ai/project/agents.md` (optional)

```markdown
# Agent Workflows

Template and sub-agent delegation patterns for this project.

<!-- Only create this file if the repo has .agents/skills/ or complex agent workflows. -->

## Available Skills

<!-- TODO: List skills in .agents/skills/ with one-line descriptions. -->

## Delegation Patterns

<!-- TODO: When to spawn sub-agents vs handle inline. -->
```

---

## Hook & agent scaffolding (optional — offer, don't auto-create)

Generalized from this round's two real, tested examples (`memory-architect`'s
own `hooks/validation-gate.js` + `references/global-hooks.md`, and
`rayfin-companion`'s `hooks/*.cjs` + `references/repo-hooks.md`). Offer these
when a repo already has documented Hard Rules/constraints
(`.ai/project/constraints.md` or equivalent) but no enforcement hook yet —
never as part of the default `current-state.md`/`constraints.md` always-create
set. Before writing either skeleton, read
[`project-memory-template`'s `.ai/rules/200-hook-authoring-conventions.md`](../../../../project-memory-template/.ai/rules/200-hook-authoring-conventions.md)
for the naming (`global-hooks.md` vs `repo-hooks.md`) and blocking-schema rules
— don't re-derive them here.

### `references/<scope>-hooks.md` (courtesy-copy reference doc)

```markdown
# {Rule name} enforcement hook (reference copy)

**Status:** {installed at <path> | not yet installed}.

{One paragraph: what Hard Rule(s) this backstops, and why a hook rather than
relying on the skill alone (generation-time guidance can be missed under
pressure or skipped entirely if the skill isn't loaded).}

{global-hooks.md: state this hook is global — installs once in
~/.claude/settings.json / ~/.claude/hooks/, self-scopes per-repo. |
repo-hooks.md: state this hook is repo-scoped — only meaningful inside this
project type, must be copied into the target project's own
.claude/settings.json.}

**Known limitation:** <!-- TODO: what this hook can't catch, e.g. relies on
npm scripts only, or can't see .gitignore state from a command string alone. -->

## `.claude/settings.json` (hooks section)

​```jsonc
{
  "hooks": {
    "<PreToolUse|PostToolUse|Stop>": [
      {
        "matcher": "<tool name or omit for Stop>",
        "hooks": [
          { "type": "command", "command": "node \"<path to hook script>\"" }
        ]
      }
    ]
  }
}
​```

## `<hook-script-name>.cjs`

<!-- TODO: One paragraph describing the mechanism (self-filter condition,
deny vs warn, fail-open posture). Full source: [`../hooks/<name>.cjs`](../hooks/<name>.cjs). -->
```

### `hooks/<name>.cjs` (script skeleton)

```javascript
#!/usr/bin/env node
// <PreToolUse|PostToolUse|Stop> hook — <global|repo-scoped>, <one-line trigger description>.
//
// <!-- TODO: which Hard Rule(s) this backstops and why a hook, not just the skill. -->
//
// IMPORTANT — the two blocking schemas are NOT interchangeable, don't guess:
//   PreToolUse deny:  exit 0, JSON stdout with
//     hookSpecificOutput.permissionDecision: "deny" + permissionDecisionReason
//   Stop block:       exit 0, JSON stdout with top-level decision: "block" + reason
//     (NOT nested under hookSpecificOutput) — also check incoming
//     stop_hook_active and allow silently if already true, or this loops.
//
// Fails open on every unexpected condition (parse errors, missing files,
// thrown errors) — never let this hook itself become the failure.

function readStdin() {
  try {
    return require("fs").readFileSync(0, "utf-8");
  } catch {
    return "";
  }
}

let input;
try {
  input = JSON.parse(readStdin());
} catch {
  process.exit(0); // fail open
}

// <!-- TODO: self-filter — e.g. `if (input.tool_name !== "Bash") process.exit(0);`
// or `if (!/\.tmdl$/.test(input.tool_input?.file_path || "")) process.exit(0);` -->

try {
  // <!-- TODO: the actual check. -->
} catch {
  // fail open
}

process.exit(0);
```

### `agents/<name>.md` (agent skeleton)

Only scaffold an agent when the task is genuinely agent-shaped — bounded,
multi-source, requires independent judgment across content not yet seen (the
`memory-consolidator` test, see [references/agents.md](agents.md)). A
single-pass lookup or fixed-rubric check stays inline in the skill; it doesn't
need an agent.

```markdown
---
name: <agent-name>
description: >
  <!-- TODO: what it scans, what it proposes, when to dispatch it (trigger
  phrases or conditions). Be specific — this is what makes the Agent tool
  select it correctly. -->
tools: <deliberately restricted list — no broader than the task needs>
model: sonnet
---

<!-- TODO: procedure. End with a proposal/summary handed back for user
approval — don't grant unilateral write authority unless the calling skill
explicitly does. -->
```

---

## `.ai/CONTEXT.md` (optional sibling tier — via `domain-modeling`)

Not a replacement for `current-state.md`/`decisions.md`/`pitfalls.md` — a
narrow terminology glossary + ADR log, a different job than this Standard's
broader operating-memory. Offer only when the repo also wants
`domain-modeling`/`grill-with-docs` planning sessions. Don't hand-write
content — `domain-modeling` creates this lazily on the first resolved term;
scaffold only the empty shell if the user wants the file to exist before that:

```markdown
# {Context Name}

<!-- TODO: one or two sentences — what this context is and why it exists. -->

## Language

<!-- TODO: terms get added here as domain-modeling resolves them. See
domain-modeling/CONTEXT-FORMAT.md for the format. -->
```

`.ai/adr/` needs no starter — `domain-modeling` creates it on the first
qualifying ADR, same as `.ai/CONTEXT.md`.

---

## `.claude/CLAUDE.md` (navigator template)

```markdown
# Agent Operating Instructions

## Navigation Map

| You need… | Read |
|-----------|------|
| What the app is / quickstart | [README.md](../README.md) |
| Hard constraints | [.ai/project/constraints.md](../.ai/project/constraints.md) |
| Architecture & conventions | [.ai/project/architecture.md](../.ai/project/architecture.md) |
| Build/run/deploy | [.ai/project/operations.md](../.ai/project/operations.md) |
| Current goals | [.ai/memory/current-state.md](../.ai/memory/current-state.md) |
| Past decisions | [.ai/memory/decisions.md](../.ai/memory/decisions.md) |
| Lessons learned | [.ai/memory/pitfalls.md](../.ai/memory/pitfalls.md) |

## Agent SOPs

<!-- TODO: standing planning/consolidation conventions for this repo. Starter
pattern (generalize, don't copy verbatim) — split any named skill by whether the
agent can actually invoke it:
- Agent-invocable (via the `Skill` tool, proactively): skills without
  `disable-model-invocation` in their SKILL.md frontmatter.
- User-triggered only (agent should suggest, not silently assume it ran): skills
  with `disable-model-invocation: true` — only a typed `/command` fires these.
State explicitly that the SOP applies to ad hoc research/debugging, not only formal
planning-mode sessions — a hook tied to `EnterPlanMode` alone won't cover inline
diagnostic work. See project-memory-template-hisd's `.ai/PLAN.md` task 12 for the
real incident this pattern comes from. -->

## Critical Gotchas

<!-- TODO: Silent-failure traps that MUST be in agent context every session.
     Test: "would a fresh agent break something important if it didn't see this?"
     If yes → here. If no → .ai/memory/pitfalls.md. -->
```
