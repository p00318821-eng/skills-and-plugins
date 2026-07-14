# Backlog Writer Templates

These templates govern the structure of all work items produced by the Backlog Writer Agent. Every section heading is required. Populate sections from the input; leave sections explicitly marked [Not confirmed] rather than omitting or fabricating.

---

## Epic Template

```markdown
# Epic: [Title]

## Strategic Objective
<!-- 1-3 sentences: the business capability this epic delivers. -->

## Scope & Boundaries
- **In scope:** [what this epic covers]
- **Out of scope:** [what is explicitly excluded]

## Source Systems & Data Lineage
<!-- One bullet per confirmed source with origin → target path. -->

## Target Architecture
<!-- Semantic model type, lakehouse/warehouse targets, key pipeline stages. -->

## Security & Governance
<!-- RLS/OLS summary, PII/PHI considerations, governance tier. -->

## Features
<!-- Numbered list of child Features with one-line descriptions. -->
1. [Feature title] — [one-line scope]

## Success Criteria
<!-- Measurable outcomes that define "done" for the epic. -->

## Open Items / Risks
<!-- Unresolved items from discovery. Never fabricate resolutions. -->
```

---

## Feature Template

```markdown
# Feature: [Title]
**Parent Epic:** [Epic Title]

## Purpose
<!-- 1-2 sentences: what this feature delivers within the epic. -->

## Functional Scope
<!-- Specific pipeline stages, semantic model objects, or report components. -->

## Data Sources (Feature-Scoped)
<!-- Subset of epic-level sources relevant to this feature. -->

## Business Rules & Calculation Logic
<!-- Rules, metric definitions, time-intelligence patterns, missing-data handling scoped to this feature. -->

## Pipeline & Refresh Requirements
<!-- Latency targets, triggers, volume estimates for this feature's data path. -->

## Acceptance Criteria
<!-- Testable conditions defining "done." Each traces to a confirmed input requirement. -->
- [ ] [Criterion — Given/When/Then for behavioral; declarative for structural]
- [ ] [Criterion]

## User Stories
<!-- Numbered list of child User Stories with one-line descriptions. -->
1. [Story title] — [one-line scope]
```

---

## User Story Template

```markdown
# User Story: [Title]
**Parent Feature:** [Feature Title]

## Story
As a [persona from input],
I need [specific capability],
so that [measurable business outcome].

## Acceptance Criteria
<!-- Every criterion: EXPLICIT, TESTABLE, traceable to a confirmed input requirement. -->
<!-- Behavioral: Given [precondition] → When [action] → Then [observable result]. -->
<!-- Structural: Declarative statement of configuration or design requirement. -->
- [ ] **AC-1:** [criterion]
- [ ] **AC-2:** [criterion]

## Technical Notes
<!-- Implementation guidance: target tables, DAX patterns, PySpark transforms, relationship cardinalities, RLS filters, pipeline config. Only include what is confirmed. -->

## Validation Anchors
<!-- Baseline numbers, source-of-truth queries, or legacy report references for verification. -->

## Dependencies
<!-- Other stories, features, or external systems this story depends on. -->
```

---

## Decomposition Guidance

When generating from a Discovery Summary, apply this mapping:

| Discovery Summary Section | Maps To |
|---|---|
| Business Objective & Audience | Epic: Strategic Objective, Story: persona |
| Data Sources & Lineage | Epic: Source Systems; Feature: Data Sources |
| Business Rules & Logic Location | Feature: Business Rules; Story: Technical Notes |
| Dimensional Model | Epic: Target Architecture; Feature: Functional Scope |
| Metrics & Calculations | Feature: Business Rules; Story: AC + Technical Notes |
| Security & Governance | Epic: Security & Governance; Story: AC (RLS/OLS criteria) |
| Pipeline & Refresh | Feature: Pipeline & Refresh; Story: AC (refresh criteria) |
| Validation Anchors | Story: Validation Anchors |
| Unresolved Items | Epic: Open Items / Risks |
