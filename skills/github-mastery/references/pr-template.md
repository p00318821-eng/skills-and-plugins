# PR Template — HISD Data Platform

## Blank Template

```markdown
## Description
<!-- What changed and why. 2–4 sentences max. -->

## Domain Tags
<!-- Check all that apply -->
- [ ] rayfin
- [ ] edfi
- [ ] gold
- [ ] platinum
- [ ] tmdl
- [ ] pbi
- [ ] auth
- [ ] infra

## Commits in this PR
<!-- Commits are subunits — list key ones if >5 commits -->

## Environment Checklist
- [ ] Tested locally with synthetic data (no real student records)
- [ ] Validated in staging before targeting main
- [ ] No credentials, tokens, or connection strings in diff

## Testing Notes
<!-- What was run, what passed. "N/A" only for docs-only PRs. -->

## FERPA Data Scope
<!-- Does this change touch, transform, or expose student records? -->
- Scope: [ ] None  [ ] Indirect  [ ] Direct
- If Direct or Indirect: describe briefly
```

## Filled Example — Rayfin Auth Fix

```markdown
## Description
Fixes SSO popup appearing on cold session start when Fabric workspace token
has expired. Root cause was missing token refresh check in auth middleware.
Linked to issue #42.

## Domain Tags
- [x] rayfin
- [x] auth

## Environment Checklist
- [x] Tested locally with synthetic data
- [ ] Validated in staging before targeting main
- [x] No credentials in diff

## Testing Notes
Ran `npx rayfin dev` with expired token simulation. Popup no longer fires.
Manual test: cold start → silent refresh → app loads.

## FERPA Data Scope
- Scope: [x] Indirect
- Auth layer gates access to student-record endpoints; fix improves security posture.
```
