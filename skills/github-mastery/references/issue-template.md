# Issue Template — HISD Data Platform

## Blank Template

```markdown
## What
<!-- One sentence: what needs to happen. -->

## Why
<!-- One sentence: why it matters. Business or compliance reason. -->

## Data Scope
<!-- Does this issue involve student records? -->
- [ ] None — no student data touched
- [ ] Indirect — affects systems that access student data
- [ ] Direct — creates, transforms, or exposes student records

## Linked PR
<!-- Fill in when PR is opened. -->
```

## Filled Example — Ed-Fi Pipeline Bug

```markdown
## What
Chronic absence pipeline incorrectly counts excused absences toward the
chronic threshold, inflating flags in the Gold layer.

## Why
Incorrect flags trigger intervention workflows and misrepresent student
attendance records — FERPA-relevant data quality issue.

## Data Scope
- [x] Direct — transforms StudentSchoolAssociation attendance data into Gold fact table

## Linked PR
#87
```

## Filled Example — Rayfin Feature

```markdown
## What
Add pagination support to the student caseload endpoint in the Rayfin app.

## Why
Current endpoint returns all records unbounded; causes timeout on large campuses.

## Data Scope
- [x] Indirect — endpoint serves student records but change is structural, not data-transforming

## Linked PR
<!-- pending -->
```
