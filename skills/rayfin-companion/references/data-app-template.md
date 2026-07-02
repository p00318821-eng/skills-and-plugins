# Data App Template Reference

Official template for apps that analyze/visualize Fabric semantic model data.
Built-in: Fabric auth + semantic model connectivity, DAX generation, chart/grid
primitives, theming, Playwright validation. Encodes the Execute DAX Queries
(Arrow) flow internally — do not hand-roll Arrow/DAX plumbing when this
template applies.

## Prerequisites

- Fabric Apps workload enabled by tenant admin (Admin Portal → Tenant
  settings → "Fabric Apps (preview)" → Enabled).
- **Dataset Execute Queries REST API** tenant setting enabled (Admin Portal →
  Integration settings) — required, template uses Execute DAX Queries API.
- Build + Read permissions on target semantic model.
- Semantic model hosted on Fabric or Power BI capacity.

## Scaffold

```bash
npm create @microsoft/rayfin@latest -- "<appitemname>" --template dataapp --workspace <workspacename>
```

Only the Rayfin CLI currently supports this template (not manual `rayfin init`).

## Connect to a Semantic Model

After scaffold, open GitHub Copilot (VS Code Copilot pane or terminal `copilot`)
and prompt with a Power BI share link:

```
Use my sales model at https://app.powerbi.com/groups/<workspace-id>/modeling/<model-id>/modelView
to generate an invoicing application.
```

Share link encodes workspace ID + model ID — Copilot extracts both. No manual
auth wiring needed; authenticated users with existing Build/Read permissions
get live data automatically, no separate sign-in screen.

## Built-In Visual Primitives

Preconfigured chart types (ask Copilot by name, fewer iterations than custom):

- Bar (vertical/horizontal, grouped, stacked)
- Line (with optional markers)
- Area
- Scatter
- Pie / donut
- Heatmap
- Bubble
- Waterfall
- Single-value card (KPI callout)
- Layered/composite (bars + data labels, dual-axis line)

Cross-highlighting between visuals is built in.

## Data Grid Primitive

Preconfigured features:
- Column headers auto-derived from semantic model metadata
- Number/date formatting per column via format strings
- Sorting, scrollable overflow rows
- Light/dark theme support
- Custom cell renderers: data bars, boolean check/cross, clickable URLs,
  image cells with lightbox, multi-field cells

## Theming

Single central style file drives all components (cards, buttons, charts,
grids, tooltips). Prompt Copilot with branding intent ("dark blue, rounded
corners, modern sans-serif") — propagates everywhere. Don't restyle
components individually; edit the central style file.

## Format Strings

Define number/currency/percent formatting once per column — applies
automatically across chart axes, tooltips, data labels, and grid cells.
Avoids inconsistent formatting (e.g. `$1,500.50` in one chart vs `1500.5` in
another).

## Playwright Validation (Pre-Publish)

Agent opens app in real browser before publish, checks:
- Visuals render correctly
- Charts not cut off/squished
- Text readable
- No console errors

Run before `npx rayfin up` for data-app-template projects.

## Deploy

Same as standard flow:

```bash
npx rayfin up
```

## Known Limitation

> **CRITICAL**: Apps connected to a semantic model **cannot run standalone
> outside the Fabric portal**. Opening via direct "Open" URL causes visual
> queries to error. This is a current platform limitation (temporary) — data
> app template apps are portal-embedded only until resolved.

## When NOT to Use This Template

- Pure operational CRUD apps (Todo, Notes, etc.) — use standard `react-vite`
  or other CRUD templates from `references/data-models.md` /
  `references/client-api.md`. Data app template is for semantic-model
  analytics/visualization specifically.
- If standalone (non-portal) access is a hard requirement — current
  limitation blocks this for semantic-model-connected apps.

## Relationship to Architectural Grounding Rules

This template is the **officially supported implementation** of the
Data App layer described in SKILL.md's dual-template architecture. It
internally implements one-shot DAX grounding (pre-fetch metrics before
invoking Copilot) and uses the GA Execute DAX Queries (Arrow) API — you don't
write this DAX/Arrow code by hand when using this template.
