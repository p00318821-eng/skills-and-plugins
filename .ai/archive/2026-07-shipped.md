# Shipped — 2026-07

## Submodule-to-flat-folders migration

**Decision:** Replaced Git submodules (`mattpocock/skills` at `6da833d`,
`ChangyuanYU/mbti-persona-skill` at `8181d7b`, plus a `my-custom-skills/`-style
grouping) with plain vendored folders under `skills/`. `.gitmodules` was removed;
`d395fb7` ("Flatten skills to top-level folders; add update tooling and attribution")
is the commit where this landed.

**Why:** Submodules add clone/update friction that's inconsistent with this repo's
"dotfiles for AI" distribution use case — a fresh clone shouldn't need
`git submodule update --init` before the skills are usable, and distributing skills to
other environments (the whole point of `sync_orchestrator.ipynb`) is simpler against
plain folders than against submodule pointers.

**Alternatives rejected:** Keeping submodules (rejected — the friction described above).
Git subtree merges (not attempted — flat vendored copies plus the
`update-sourced-skills.ipynb` pull-tool achieved the same "stay in sync with upstream"
goal with less git-internals complexity).

**Reversal cost:** Moderate — would require re-establishing submodule pointers and
losing the flattened attribution/license-file layout built on top of the flat structure
since this migration (each vendored skill's own `LICENSE` copy, the README attribution
table).

## Recent plugin sync work (pre-dates this repo's `.ai/` adoption)

**Decision:** Added three external plugin packages (`plugins/fabric-skills` from
`microsoft/skills-for-fabric`, `plugins/powerbi` and `plugins/fabric` from
`RuiRomano/powerbi-agentic-plugins`, `plugins/reports` from
`data-goblin/power-bi-agentic-development`), then copied each plugin's skill folders
into the top-level `skills/` directory so the repo could treat them as individually
vendored skills (via `ddc7bab` "Expand repository to add plugins" and
`8092a66`/`5ae0fef` "Move skill files into skills/ directory"). `manifests/origins.json`
was extended to track the new plugin directories.

**Why:** Enable both plugin-native distribution (a plugin package installs as a unit in
tools that support the Claude Code plugin format) and per-skill vendoring (this repo's
own `sync_orchestrator.ipynb` distribution mechanism, which operates on individual skill
folders) simultaneously, without picking one delivery mechanism over the other.

**Alternatives rejected:** None recorded at the time this work shipped.

**Reversal cost:** Moderate — would require deleting the duplicated `skills/` copies and
updating any destination manifest entries that reference skills by name rather than by
parent plugin. **Cross-reference:** this is exactly the byte-duplication now flagged as
an open, unresolved decision in [`.ai/PLAN.md`](../PLAN.md) — the same pattern was
repeated for the `azure-skills` and `deep-wiki` plugins added in the 2026-07-02
Hub-and-Spoke migration round, so the duplication has grown rather than shrunk since
this entry was first true.
