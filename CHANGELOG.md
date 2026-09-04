# Changelog

## 0.1.0-draft.2 — 2026-09-04

### Changed

- `seen` now accepts quoted year, year-month, or full calendar-date precision.
- Added optional `seen-qualifier` for `approximate`, `uncertain`, or
  `approximate-and-uncertain` temporal reports at every supported precision.
- Clarified that missing date components are not defaults and must not be
  invented or added during normalisation.
- Clarified that a lineage relationship with a wholly unknown first-seen year
  may be described in Markdown prose but is not structurally representable in
  this draft.
- Assigned the schema a version-specific identity for the immutable
  `v0.1.0-draft.2` repository state.

Full dates valid under `0.1.0-draft.1` retain their meaning.

## 0.1.0-draft.1 — 2026-09-02

- Initial public draft.
