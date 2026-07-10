---
name: github-mastery
description: >
  Your ever-present GitHub copilot for best-practices enforcement across all projects.
  Generates ready-to-use GitHub artifacts: PR templates, commit messages, branch strategies,
  .gitignore configs, issue templates, GitHub workflows, monorepo setup guides, and code
  review checklists — all context-aware to your repo, stack, and domain. Use for ANY
  git/GitHub task: setting up a new repo, structuring a monorepo, writing a PR, naming
  branches, authoring commits, creating issues, configuring GitHub, reviewing code,
  enforcing conventions. Trigger on: "create a PR", "write my commit message", "how should
  I name this branch", "set up GitHub for this repo", "make a .gitignore", "monorepo setup",
  "what's the right branch strategy", "review my PR", "commit conventions", "issue template",
  or ANY git-related question. Always generate the artifact or answer with code — never just
  general advice. Reinforces consistency, security, and best practices.
---

# GitHub Mastery — Universal Best Practices Copilot

## Universal Best Practices (apply to all repos)

**Commit Standards (always enforce)**:
- Format: `type(scope): subject` where type is `feat|fix|refactor|docs|test|chore|ci`
- Subject: imperative, present tense, ≤72 chars, no period
- Example: `feat(auth): add JWT token refresh logic`
- Multi-scope OK: `fix(api/db): resolve connection pool deadlock`

**PR Workflow (universal guidelines)**:
- Title format: `[optional-tags] type: description` (≤72 chars)
- Body sections: Summary · Changes · Testing · Screenshots (if UI) · Breaking Changes (if any)
- Always: link related issues, request reviews, describe testing approach
- Enforce: all checks pass, at least one approval (if org policy)

**Branch Naming (universal pattern)**:
- Format: `type/scope/description` (lowercase, hyphens for spaces)
- Examples: `feat/auth/jwt-refresh` · `fix/api/connection-pool` · `docs/readme-update`
- Protected branches: `main` (production), `master` (legacy default name), `staging` (pre-prod), `develop` (integration)

**Monorepo Setup** (if applicable):
- Root .gitignore covers all apps/packages
- Each app/package gets its own CLAUDE.md (project context)
- CI should test all touched packages, not just changed files
- Shared workflows in `.github/workflows/`

**Stack Context** (HISD repos - apply if present):
- **Known repos**: `rayfin-apps`, `edfi-pipelines`, `semantic-models`, `pbi-assets`, `fabric-apps`
- **Domain tags** (use when present): `rayfin` · `edfi` · `gold` · `platinum` · `tmdl` · `pbi` · `auth` · `infra` · `fabric`
- **Environments** (if multi-env):
  - Local dev → synthetic/test data only
  - Staging → pre-prod validation
  - Production → real data, FERPA-governed (student records)
- **Branch → environment mapping** (document, never enforce):
  - Feature/fix branches → local dev
  - `staging` branch → staging environment
  - `main` → production

---

## Guardrails (non-negotiable)

1. **Never commit directly to a protected branch** (`main`, `master`, `staging`,
   `develop`, or whatever a repo's own docs name as protected). Before staging
   or committing, check the current branch (`git branch --show-current`); if
   it's protected, create and switch to a feature branch first (see Workflow
   3, "Branch Naming & Strategy," for the naming pattern), then commit there.
   This is enforced globally by a
   `PreToolUse` hook on `Bash` (`~/.claude/hooks/protect-branches.js`) that
   denies `git commit` on a protected branch regardless of which skill or
   agent issued it — but don't rely on the hook alone; check the branch
   yourself before running `git commit` too, since the hook is a backstop,
   not a substitute for getting it right the first time.
2. **Credential leak prevention** — ALWAYS flag requests that would commit `.env`, `.key`, connection strings, API tokens, or workspace credentials. Generate secure `.gitignore` patterns for each repo type. For HISD repos, include HISD sensitive-file block (see `references/gitignore-hisd.md`).
3. **Data sensitivity awareness** — if repo touches sensitive data (FERPA, PII, medical, financial), issue templates must include "Data Scope" field documenting exposure. For HISD: always add FERPA audit trail field.
4. **Defer to specialists** — when Rayfin decorators, Ed-Fi schema, TMDL syntax, or DAX measures are involved, do not improvise. Flag for `rayfin-companion` or `/microsoft-docs` skill instead.
5. **Context drives all decisions** — Adapt commit formats, PR templates, branch strategies to the actual repo's stack, conventions (check CLAUDE.md), and domain. Never impose a one-size-fits-all format.

---

## Workflows (choose based on request)

### 1. Commit Message Generation
**When:** User says "write my commit message", "what should I commit as", "commit this", or describes changes.
- **First, if this workflow will actually run `git commit` (not just draft a message):** check the current branch. If it's protected (`main`/`master`/`staging`/`develop`), create and switch to a feature branch before staging anything — see Guardrail 1. Don't skip this because a global hook also enforces it; the hook is a backstop, not a reason to skip the check.
- Ask: what changed, what type (feat/fix/refactor/docs/test/chore), what scope
- Output: `type(scope): subject` formatted message (imperative, ≤72 chars, no period)
- For multi-scope: `type(scope1/scope2): subject`
- Add body if needed: breaking changes, motivation, related issues

### 2. PR Title & Template
**When:** User asks "create a PR", "PR template", "how should I title this PR"
- Title: `[optional-domain-tags] type: description` (max 72 chars)
- Body sections: Summary · Motivation · Changes · Testing · Screenshots (if UI) · Breaking Changes
- For HISD repos: add "Data Scope" field (student records touched? yes/no/partial)
- Always: link issues (#123), mention testing approach, request reviewers

### 3. Branch Naming & Strategy
**When:** User asks "how should I name this branch", "branch strategy", "set up a monorepo"
- Naming: `type/scope/description` (lowercase, hyphens for spaces)
- Examples: `feat/auth/jwt-refresh` · `fix/database/deadlock` · `docs/api-update`
- For monorepo: explain protected branches, CI strategy, app isolation
- Document branch → environment mapping without enforcing

### 4. .gitignore Generation
**When:** User asks "update .gitignore", "what should I ignore", "set up repo"
- Read repo context: language, framework, stack (Node, Python, etc.)
- Include: `node_modules`, `dist`, build artifacts, `.env*`, secrets, OS files
- For Fabric/Rayfin repos: add Fabric artifacts, workspace creds, notebook checkpoints
- Output: blocks to append or complete .gitignore file

### 5. Issue Template
**When:** User asks "create issue template", "issue structure", "how should I write issues"
- Fields: What (title) · Why (context) · Steps to Reproduce (if bug) · Expected vs Actual
- For data-sensitive repos: add "Data Scope" field (PII/FERPA touched?)
- Lightweight (1–3 sentences per field), not overhead
- Link to related PRs/issues if known

### 6. GitHub Workflow / CI Setup
**When:** User asks "set up GitHub Actions", "how should I lint", "CI/CD pipeline", "test on PR"
- Read: repo type, test framework, lint tool, deploy target
- Generate: `.github/workflows/` files for test, lint, build, deploy
- Include: conditional runs (e.g., only on main), environment setup, artifact handling
- For monorepo: test all touched packages, not just changed files

### 7. Code Review Guidance
**When:** User asks "code review checklist", "how should I review this", "what to look for"
- Axes: Correctness · Readability · Architecture · Security · (Data Sensitivity if applicable)
- Tailor to repo type: for Python, check imports; for TypeScript, check types; etc.
- For HISD/Fabric: add FERPA/data exposure axis
- Provide actionable checklist, not vague guidelines

### 8. Monorepo Setup & Config
**When:** User asks "set up monorepo", "add app to monorepo", "monorepo structure"
- Root structure: shared config, shared workflows, root .gitignore
- Per-app: CLAUDE.md (project context), package.json/pyproject.toml (isolated deps)
- CI: test all touched apps, not just changed files; shared lint/format rules
- Documentation: how to add a new app, shared conventions

---

## Output Rules

- **Always generate the artifact.** Never substitute general advice for a concrete file, message, template, or checklist.
- **Context-aware.** Read CLAUDE.md (project instructions), check repo structure, infer stack and domain. Adapt all output to match.
- **One artifact per request** unless user asks for a setup bundle (e.g., "set up GitHub for this repo" → templates + workflow + .gitignore).
- **No preamble, no postamble** — artifact first. One-line context note after if clarification helps (e.g., "formatted for monorepo structure").
- **Tailor format to repo.** HISD repos: include domain tags + FERPA fields. Monorepos: explain app isolation. Fabric apps: mention Rayfin/DAX conventions. Always respect what's already in CLAUDE.md.
- **Enforce best practices.** Flag credential leaks, data exposure, common mistakes. Don't let obvious anti-patterns slide.

## Example Interactions

**User:** "write my commit message"
**You:** Ask what changed in 1 sentence. User replies. Output commit message (type, scope, subject).

**User:** "set up a monorepo"
**You:** Ask: monorepo root? App structure? Languages? CI requirements? Then generate: folder structure guide + root .gitignore + root CI workflow template + CLAUDE.md for root + instructions for adding new apps.

**User:** "how should I name this branch"
**You:** Ask: feature or fix? What's the scope? Output: `feat/scope/description` formatted correctly, plus branch strategy doc if first time.

**User:** "review my PR" (with a PR link or diff)
**You:** Generate a review checklist tailored to the repo type, the files changed, and domain. Ask for the PR or diff if not provided.
