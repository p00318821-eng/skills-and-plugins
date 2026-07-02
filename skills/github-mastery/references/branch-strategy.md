# Branch Strategy — HISD Data Platform

## Convention (document, not enforced by tooling)

### Branch → Environment Mapping

| Branch pattern | Deploys to | Data allowed |
|---|---|---|
| `feature/*`, `fix/*`, `refactor/*`, `docs/*` | Local dev | Synthetic only |
| `staging` | Staging | Synthetic only |
| `main` | Production | Real student records |

**Rule of thumb:** If you wouldn't deploy it to prod today, it doesn't merge to `main`.

---

### Naming Convention

Format: `type/[domain-]short-desc` or `type/issue-number-short-desc`

**Types:** `feature` · `fix` · `refactor` · `docs` · `chore`

**Domain prefix** (use when branch touches a single domain clearly):

```
feature/rayfin-pagination-caseload
fix/edfi-chronic-absence-threshold
refactor/gold-attendance-fact-grain
docs/tmdl-synonyms-enrollment
chore/gitignore-fabric-artifacts
fix/42-sso-cold-session-popup
```

Multi-domain branches (common for solo dev owning cross-layer work):
```
feature/attendance-pipeline-gold-rayfin
fix/edfi-gold-chronic-absence-grain
```

---

### Lifecycle

```
main (production)
  └── staging (pre-prod validation)
        └── feature/fix/refactor branches (local dev)
```

1. Branch off `main` (or `staging` if building on staged work)
2. Develop locally — synthetic data only
3. PR → `staging` for validation
4. PR → `main` after staging sign-off
5. Delete branch after merge

---

### Branch Protection Recommendations (configure in GitHub Settings)

**`main`:**
- Require PR before merging
- Require at least 1 approval
- Dismiss stale reviews on new commits
- Restrict direct pushes (all contributors including admins)

**`staging`:**
- Require PR before merging
- No approval required (small team, move fast)
- Allow direct push for repo owner only

---

### Long-lived Branch Warning

Branches open >2 weeks without a PR are stale. Options:
- Rebase on latest `main` and open a draft PR
- Close and reopen fresh from current `main`

Solo dev reality: commits within a branch are subunits of the PR's story — commit freely, keep the PR the unit of review.
