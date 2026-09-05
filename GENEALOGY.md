---
genealogy-version: "0.1.0-draft.2"
project:
  id: "https://github.com/theislampill/GENEALOGY.md"
  name: "GENEALOGY.md"
self-citation:
  - id: "feature-provenance-convention"
    subject: "The two-block GENEALOGY.md convention: project-authored, feature-scoped citation guidance plus optional, non-exhaustive affirmative lineage entries."
    cite-when:
      - "Adopting this two-block convention, or a substantially equivalent feature-provenance file, as a repository interface."
      - "Translating this convention into another serialisation or tooling interface while preserving its self-citation and non-exhaustive-lineage semantics."
    do-not-cite-when:
      - "Using YAML front matter, JSON Schema, SPDX relationships, or ordinary licence notices independently."
      - "Maintaining generic dependency, SBOM, copyright, licence, contributor, or academic-citation metadata."
  - id: "bounded-genealogy-authoring"
    subject: "The experimental make-genealogy authoring discipline: preserve existing public content, separate supported claims from unresolved candidates, and apply target-bounded semantic adequacy before minimising meaning-equivalent output."
    cite-when:
      - "Substantially adopting or translating this particular ordered authoring procedure for repository genealogy work."
    do-not-cite-when:
      - "Using the GENEALOGY.md convention without adopting this experimental authoring procedure."
      - "Using generic validation, evidence review, caution, minimality or skill packaging independently."
      - "Merely invoking the supplied skill to author a file, without adopting its procedure as part of a descendant implementation."
lineage:
  - source: "https://x.com/francedot/article/2095052001667408295"
    subject: "The problem framing that coding agents can translate, reconstruct, or behaviourally reproduce distinctive open-source implementations while losing usable records of origin."
    relationship: "inspired"
    seen: "2026-09-02"
    applies-to:
      - "README.md"
      - "docs/specification.md"
    uncertainty: "This source motivated the provenance problem. It did not specify the GENEALOGY.md data model."
  - source: "https://firstmonday.org/ojs/index.php/fm/article/view/1151"
    subject: "The non-completeness rule and the caution against treating an incomplete credits record as legal proof of copying or infringement."
    relationship: "inspired"
    seen: "2026-09-02"
    applies-to:
      - "docs/specification.md"
    uncertainty: "The paper studies Linux CREDITS as a historical dataset; it is not itself a feature-provenance specification."
  - source: "https://spdx.github.io/spdx-spec/v3.0.1/"
    subject: "Versioned and directional comparison with established artifact-level relationship vocabularies, including explicit no-assertion semantics."
    relationship: "inspired"
    seen: "2026-09-02"
    applies-to:
      - "schema/genealogy.schema.json"
      - "docs/specification.md"
    uncertainty: "GENEALOGY.md is not an SPDX profile and does not claim SPDX conformance."
  - source: "https://citation-file-format.github.io/"
    subject: "The practical pattern of a repository-root format that remains human-readable while exposing structured metadata for tools."
    relationship: "inspired"
    seen: "2026-09-02"
    applies-to:
      - "GENEALOGY.md"
      - "templates/GENEALOGY.md"
    uncertainty: "CITATION.cff addresses software citation metadata, not conditional feature-scoped provenance."
---

# Genealogy of `GENEALOGY.md`

This repository dogfoods the draft convention it proposes. The front matter publishes two narrowly scoped self-citation subjects and records four specific intellectual antecedents. Each lineage entry states what the source influenced and what it did **not** supply.

The list is intentionally non-exhaustive. An omitted source has no negative meaning: it does not assert independent invention, deny a relationship, or imply that every possible antecedent was investigated.

The self-citation subjects distinguish the convention from the separately optional experimental authoring discipline. Neither asserts general efficacy or adds a conformance requirement.

## Suggested descendant entry

A downstream repository that adopts the convention itself may start from this entry and adjust `subject`, `relationship`, and `seen` to match what actually happened:

```yaml
lineage:
  - source: "https://github.com/theislampill/GENEALOGY.md"
    source-subject: "feature-provenance-convention"
    subject: "Feature-level provenance documentation in this repository."
    relationship: "inspired"
    seen: "2026-09-02"
```

Do not copy that entry merely because a project uses YAML, JSON Schema, SPDX, a licence file, an SBOM, or ordinary credits. The `cite-when` and `do-not-cite-when` boundaries in the front matter are part of the subject being published.

Read the [draft specification](docs/specification.md), use the [copyable template](templates/GENEALOGY.md), and validate against the [JSON Schema](schema/genealogy.schema.json).
