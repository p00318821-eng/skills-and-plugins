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

<!-- TODO: Planning rules, consolidation triggers, standing conventions. -->

## Critical Gotchas

<!-- TODO: Silent-failure traps that MUST be in agent context every session.
     Test: "would a fresh agent break something important if it didn't see this?"
     If yes → here. If no → .ai/memory/pitfalls.md. -->
```
