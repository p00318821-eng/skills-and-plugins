# Scoring Rubric

Detailed criteria for each audit dimension. Score each 0–2.

| Score | Meaning |
|-------|---------|
| 0 — Missing | No content exists for this dimension |
| 1 — Partial | Content exists but is incomplete, outdated, or fragmented across files |
| 2 — Complete | Content is comprehensive and current |

Location is scored separately — see Location Modifier below.

---

## 1. Navigator

**What:** `.claude/CLAUDE.md` has a navigation table linking to documentation files.

| Score | Criteria |
|-------|----------|
| 0 | No CLAUDE.md or no navigation table |
| 1 | CLAUDE.md exists but navigation table is incomplete (missing links, broken anchors) |
| 2 | Navigation table links every documentation file; all links resolve; no orphaned references |

---

## 2. Orientation

**What:** `README.md` explains what the project is, who it's for, quickstart, and links to docs.

| Score | Criteria |
|-------|----------|
| 0 | No README or only a title/stub |
| 1 | README exists but missing quickstart, doc table, or purpose statement |
| 2 | README has purpose, audience, quickstart commands, and a doc-index table |

---

## 3. Operations

**What:** Build/run/deploy procedures documented.

| Score | Criteria |
|-------|----------|
| 0 | No operations documentation anywhere |
| 1 | Operations info exists but is scattered or missing key sections (auth, deploy, troubleshoot) |
| 2 | Dedicated operations doc covers prerequisites, build/dev commands, auth, deploy, and troubleshoot |

**Note:** Simple libraries with no deploy process score 2 if ops are adequately covered
in README (a dedicated operations file is optional for them).

---

## 4. Architecture

**What:** System narrative with conventions documented.

| Score | Criteria |
|-------|----------|
| 0 | No architecture documentation |
| 1 | Architecture info exists but is scattered or lacks narrative (just a list of files) |
| 2 | Dedicated architecture doc has a coherent system narrative, key components, conventions, and data flow |

---

## 5. Active State

**What:** Current goals and a resume pointer documented.

| Score | Criteria |
|-------|----------|
| 0 | No active-state documentation |
| 1 | Goals exist but are stale (>2 weeks without update) or missing resume pointer |
| 2 | Active-state doc has dated goals, open blockers (if any), and a resume pointer |

---

## 6. Decision History

**What:** Shipped decisions preserved with rationale.

| Score | Criteria |
|-------|----------|
| 0 | No decision history |
| 1 | Decisions are recorded but missing rationale, alternatives, or reversal cost |
| 2 | Decision history has entries with decision, why, alternatives rejected, reversal cost, and date |

---

## 7. Constraints

**What:** Hard constraints explicitly documented.

| Score | Criteria |
|-------|----------|
| 0 | No explicit constraints documentation |
| 1 | Constraints are mentioned but scattered across multiple files, not centralized |
| 2 | Constraints are centralized in one file listing platform, compliance, team, and API constraints with context |

---

## 8. Gotchas

**What:** Silent-failure traps documented inline in `.claude/CLAUDE.md`.

| Score | Criteria |
|-------|----------|
| 0 | No gotchas documented anywhere |
| 1 | Gotchas exist but are incomplete or buried where agents won't see them |
| 2 | Critical gotchas (those causing silent data corruption) are inline in CLAUDE.md; broader lessons are separated |

**Distinction:** A gotcha is "critical" if a fresh agent missing it would produce silently
incorrect output. The `"(Blank)"` sentinel in fabric-visuals or `withSchoolCode()` regex
no-op are examples — they cause silent data corruption, not visible errors.

---

## 9. No Duplication

**What:** "One fact, one home" enforced across all documentation files.

| Score | Criteria |
|-------|----------|
| 0 | Significant content duplicated across multiple files (e.g., build commands in both README and CLAUDE.md) |
| 1 | Minor duplication (e.g., constraint restated in 2-3 files with slight variation) |
| 2 | Each fact appears in exactly one file; cross-references use links, not copies |

**How to check:** Search for key phrases (command names, constraint statements, pattern
descriptions) across all doc files. If the same content appears in two places with
different wording, that's duplication.

---

## Location Modifier

After scoring all 9 dimensions on content quality, apply a location modifier:

| Structure | Modifier | Meaning |
|-----------|----------|---------|
| `.ai/` standard | +0 | Already using the standard structure |
| Root-level equivalents | -1 to -2 | Content is in root-level files (PLAN.md, OPERATIONS.md, etc.) instead of `.ai/`. Deduct 1 point from total if most files are at root; deduct 2 if there's also no clear navigation map. |
| No structure | -0 | Already reflected in per-dimension 0 scores |

The modifier ensures that a repo with comprehensive content at root scores B (not C or D),
while still flagging that migration to `.ai/` would improve discoverability.

---

## Grading Scale

| Grade | Score Range | Meaning |
|-------|------------|---------|
| A | 16–18 | Comprehensive, current, properly located in `.ai/` |
| B+ | 14–15 | Excellent content, non-standard locations (migration recommended) |
| B | 12–13 | Good content, minor gaps or non-standard locations |
| C | 8–11 | Basic coverage, significant gaps |
| D | 4–7 | Sparse, mostly missing |
| F | 0–3 | No documentation structure |

The audit output should always include:
1. The raw content score (before location modifier)
2. The location modifier applied
3. The final grade
4. A "Migration Recommendations" section separate from the grade
