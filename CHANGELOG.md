# Changelog

## Unreleased

### Added
- `skill-plugin-sources.json` manifest and `update-sourced-skills.ipynb` notebook to
  check externally-sourced skills for upstream updates, show a per-skill
  change-list with diffs, and apply or disregard each one.
- Vendored MIT `LICENSE` into each Matt Pocock skill folder (`caveman`,
  `grill-me`, `grill-with-docs`, `handoff`, `improve-codebase-architecture`).
- `docs/PROJECT-NOTES.md` capturing repository conventions, the update workflow,
  known updater limitations, and local-environment notes.
- This changelog.

### Changed
- Migrated from Git submodules to plain, self-contained per-skill folders
  (one `SKILL.md` per folder). Removed `.gitmodules` and the `mattpocock/`,
  `changyuanyu/`, and `my-custom-skills/` wrappers.
- Promoted `pbi-visual-rendering` and `semantic-modeling-prepforai` to top-level
  folders.
- Flattened `mbti-persona` out of its wrapper, keeping its upstream `LICENSE`.
- Rewrote `README.md` with a skills table, per-skill attribution, and update
  instructions; retitled the project `skills` to match the repository rename
  from `ben-skills`.

### Notes
- `caveman` is intentionally excluded from automated updates because it has been
  locally modified.
