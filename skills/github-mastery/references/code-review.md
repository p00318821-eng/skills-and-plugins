# Code Review Checklist — HISD Data Platform

## Five Axes

### 1. Correctness
- Does it satisfy the intent of the linked issue?
- Edge cases handled (null students, empty cohorts, missing Ed-Fi descriptors)?
- For pipelines: grain is correct, no fan-out/fan-in distortion?

### 2. Readability
- Naming matches domain language (Ed-Fi entity names, Rayfin decorator conventions)?
- Logic self-documenting or commented where non-obvious?
- No magic numbers — constants named and placed appropriately?

### 3. Architecture
- Domain boundaries respected (Gold doesn't reach into raw Silver directly)?
- Rayfin decorator rules followed — **do not review decorator syntax from memory, flag for `rayfin-companion`**
- No tight coupling between repos (e.g., `rayfin-apps` shouldn't hardcode Ed-Fi pipeline paths)?

### 4. Security
- No secrets, tokens, connection strings, or `.env` values in diff?
- No student PII hardcoded (names, IDs, SSNs, IEP data)?
- Fabric workspace credentials not exposed in logs or error messages?
- Auth checks present on any new endpoints serving student data?

### 5. FERPA
- Does this change create, transform, or expose student records?
- If yes: is access scoped appropriately (role-based, campus-scoped)?
- Synthetic data used in all test evidence — no real records in screenshots, logs, or test fixtures?
- Audit trail preserved — change traceable to an issue with documented Data Scope?

---

## Review Disposition

| Signal | Action |
|---|---|
| All 5 axes pass | Approve |
| Minor issues (naming, comments) | Approve with comments |
| Axis 4 or 5 failure | Request changes — do not approve |
| Rayfin decorator questions | Flag, defer to `rayfin-companion` |
| Correctness unclear without running it | Request testing evidence |

**Principle:** Approve if the change explicitly improves overall code health. Perfection is not the bar — FERPA compliance and credential safety are non-negotiable, everything else is continuous improvement.

---

## Per-Domain Review Notes

### `rayfin-apps`
- Decorator syntax: defer to `rayfin-companion`
- Auth popup behavior: verify SSO flow tested on cold session
- FK naming: follow established conventions (see `rayfin-companion` rules)

### `edfi-pipelines`
- Verify Ed-Fi entity names match UDM v6 exactly
- Check grain before and after transformation
- Notebook outputs cleared before commit (no embedded query results)

### `semantic-models` (TMDL)
- `///` descriptions present on tables, columns, measures?
- Synonyms added for AI/Copilot readability?
- Defer detailed review to `semantic-modeling-prepforai`

### `pbi-assets`
- Deneb/Vega specs: defer to `pbi-visual-rendering`
- DAX measures: no hardcoded campus/year filters unless intentional
- No student-level data embedded in visual spec JSON
