---
name: sdi-backlog-writer
description: Convert a Discovery Summary (the 9-section HISD SDI intake handoff artifact) into Azure DevOps Epic/Feature/User Story markdown, ready to paste into ADO by hand. Use when the user has a Discovery Summary — or enough confirmed findings to assemble one — for a Power BI/Fabric data request and wants a formal backlog written from it.
---

# SDI Backlog Writer

Turns a Discovery Summary into an Epic → Feature → User Story backlog, following the canonical HISD SDI contract and templates. This mirrors the SDI Azure DevOps Backlog Writer Agent (Copilot Studio) so the same input/output discipline applies here.

## Canonical source files

Read these in full before writing anything — they are the actual contract, not paraphrased below:

- `references/discovery-summary-contract.md` — defines the 9 required Discovery Summary sections, their exact headings, and what each maps to in the backlog.
- `references/backlog-writer-templates.md` — the literal Epic/Feature/User Story markdown templates and the section-mapping table.

If a newer copy of either file exists in the HISD `copilot-agents/SDI Request Intake Bot` repo, prefer that one and update the local reference copy — the repo root copy is contract-canonical per the contract file itself.

## Process

1. **Get or assemble a Discovery Summary.** All 9 sections, exact headings, in order. If the user hasn't written one, build it from whatever confirmed findings they give you (meeting transcripts, diffs, existing docs). Any section with no confirmed content gets the literal line `Unresolved — see Section 9.` — never fabricate to fill a gap.
2. **Decompose per the mapping table** in `backlog-writer-templates.md`. One Epic per Discovery Summary. One Feature per major capability area. One or more User Stories per Feature, scoped to a single testable unit of work.
3. **Populate every template section.** Use `[Not confirmed]` for anything not established by the Discovery Summary — never invent acceptance criteria, table names, DAX, or owners.
4. **Unresolved Items never become acceptance criteria.** They stay in the Epic's Open Items / Risks section only.
5. **Technical strings pass through verbatim** — table/column names, DAX, file paths — exactly as given, no renaming or abbreviating.
6. **Output as markdown**, Epic first, then each Feature, then each Feature's User Stories, ready to paste into Azure DevOps work items by hand.
