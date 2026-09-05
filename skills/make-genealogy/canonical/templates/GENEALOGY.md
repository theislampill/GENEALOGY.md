---
genealogy-version: "0.1.0-draft.2"
project:
  id: "https://github.com/OWNER/REPOSITORY"
  name: "Project name"
self-citation:
  - id: "distinctive-feature"
    subject: "A precise description of the distinctive feature, method, behaviour, or structure maintained here."
    cite-when:
      - "Substantially reimplementing, translating, or otherwise adopting this specific subject."
    do-not-cite-when:
      - "Using the same generic public API or common technique without adopting this subject."
# `lineage` is optional and non-exhaustive. Uncomment only for an affirmative
# statement that the project has a reasonable basis to publish.
# lineage:
#   - source: "https://github.com/UPSTREAM/PROJECT"
#     source-subject: "optional-upstream-subject-id"
#     source-revision: "optional commit, tag, release, or dated document"
#     subject: "The particular feature, method, behaviour, or structure in this project."
#     relationship: "reimplemented"
# `seen` accepts a quoted year, month, or full date: "2023", "2023-05",
# or "2023-05-14". Missing components are not defaults.
# Optional: seen-qualifier: "approximate" | "uncertain" |
#           "approximate-and-uncertain"
# If no first-seen year is responsibly known, do not invent one; explain the
# relationship in Markdown prose instead of structured lineage in this draft.
#     seen: "2026-09-02"
#     source-license: "optional SPDX expression or other licence identifier"
#     applies-to:
#       - "optional/path/or/component"
#     uncertainty: "Optional plain-language qualification."
---

# Genealogy

This file publishes feature-scoped citation guidance for possible descendants. It may also record affirmative, non-exhaustive lineage statements about antecedents.

Replace every placeholder in the YAML front matter. Keep the opening delimiter on line 1 and leave one blank line immediately after the closing delimiter. See the [draft specification](https://github.com/theislampill/GENEALOGY.md/blob/main/docs/specification.md) for field meanings, relationship definitions, identifier stability, legal cautions, and SPDX mappings.

An omitted lineage entry carries no negative meaning. It does not claim independent invention, deny a relationship, or state that a search for antecedents was performed.
