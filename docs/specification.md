# `GENEALOGY.md` draft specification

**Convention version:** `0.1.0-draft.1`  
**Status:** Draft for trial use and external review. This document does not claim that `GENEALOGY.md` is an adopted industry standard.

## 1. Purpose

`GENEALOGY.md` is a repository-root convention for two independently adoptable functions:

1. **Self-citation guidance:** a project publishes precise, feature-scoped guidance describing when descendants should consider acknowledging it and what does not fall within that request.
2. **Lineage statements:** a project records affirmative statements about antecedents that materially informed a feature, method, behaviour, structure, implementation, or research result.

The format reduces the representation and preservation cost of known provenance. It does not compel disclosure, verify a statement, determine legal derivation, or solve the incentive problem that may discourage disclosure.

## 2. Normative language

`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` identify requirements or recommendations in this draft.

A document conforms to this version when its extracted front matter validates against [`schema/genealogy.schema.json`](../schema/genealogy.schema.json) and follows the semantic rules in this specification. Schema validity is necessary but not sufficient: JSON Schema cannot encode every rule about omission, identifiers, legal caution, or external-reference integrity.

## 3. File location and encoding

A conforming project:

- MUST place the file at repository root as `GENEALOGY.md`;
- MUST encode it as UTF-8;
- MUST include one structured YAML front-matter document followed by a Markdown body;
- MAY use the Markdown body for explanation, qualifications, and human-readable context; and
- SHOULD keep the front matter concise enough to review in ordinary code review.

## 4. Front-matter extraction

A conforming parser MUST apply this rule:

1. The first line MUST be exactly `---`, with no leading or trailing characters.
2. The front matter is the text after that opening line and before the **first subsequent standalone `---` line that is immediately followed by a blank line**.
3. The closing delimiter and its required following blank line are not part of the YAML document or the Markdown body.
4. Parsing stops after that first qualifying closing delimiter. A later standalone `---` in the Markdown body is ordinary Markdown, including when used as a horizontal rule, and MUST NOT cause truncation or a second front-matter parse.

Authors working with simplistic front-matter tools MAY use `***` or `___` for Markdown horizontal rules, but conforming tools cannot depend on that convention.

The extracted YAML MUST decode to a mapping compatible with the JSON data model. It MUST contain only one YAML document. Dates such as `seen` SHOULD be quoted so parsers such as PyYAML do not coerce them into implementation-specific date objects before JSON Schema validation.

## 5. Top-level document model

The front matter has these top-level fields:

| Field | Required | Meaning |
|---|---:|---|
| `genealogy-version` | Yes | Exact convention version. For this draft it MUST be `0.1.0-draft.1`. |
| `project` | Yes | Identity of the project publishing the file. |
| `self-citation` | Conditional | Non-empty list of citation subjects maintained by this project. |
| `lineage` | Conditional | Non-empty list of affirmative, non-exhaustive lineage statements. |

At least one of `self-citation` or `lineage` MUST be present. They MAY appear independently or together. An explicitly empty block is invalid; omit a block that has no entries.

Unknown fields are invalid in this draft. This keeps misspellings visible and prevents tools from silently inventing semantics.

## 6. `project`

`project.id` MUST be a URI that stably identifies the publishing project. For a GitHub repository, use its canonical HTTPS repository URL. `project.name` is optional human-readable text.

The project identifier is not a claim of copyright ownership or legal authorship.

## 7. `self-citation`

Self-citation guidance is the more stable core of version `0.1.0-draft.1`. It gives a maintainer an affirmative reason to adopt the format: the project can state its own narrow citation boundary instead of leaving descendants to invent one.

Each entry MUST contain:

- `subject`: a specific feature, method, behaviour, structure, implementation, or research result;
- `cite-when`: one or more conditions under which a descendant should consider recording the subject; and
- `do-not-cite-when`: one or more boundaries that prevent the request from expanding to generic APIs, common techniques, or unrelated metadata.

An entry MAY contain `id`, a repository-local stable identifier. IDs are optional but strongly encouraged when a project expects descendants to point back to the subject.

A self-citation entry is guidance, not a unilateral declaration that every similar project descends from it. A downstream maintainer remains responsible for characterising the actual relationship and may answer with a different antecedent, dated independent origin, or a determination that the technique is generic.

## 8. `lineage`

`lineage` is optional and experimental in this draft. Each entry is an affirmative statement that the publishing project has a reasonable basis to make. It MUST contain:

- `source`: a URI for the antecedent source;
- `subject`: the particular feature, method, behaviour, structure, implementation, or research result in the publishing project;
- `relationship`: one value from the draft vocabulary;
- `seen`: the date the source was first seen for the work being recorded.

It MAY also contain:

- `source-subject`: a stable local subject ID published by the source;
- `source-revision`: a commit, tag, release, edition, or dated document;
- `source-license`: an SPDX expression or other licence identifier when relevant;
- `applies-to`: destination paths or components; and
- `uncertainty`: a plain-language qualification.

### 8.1 Non-completeness is normative

A `GENEALOGY.md` lineage list is **not exhaustive**. The `lineage` block is optional, individual relationships may be omitted, and absence has no negative meaning. **Absence does not** assert independent invention, deny that a relationship exists, indicate that a search for antecedents was performed, or imply that every known source was recorded.

Version `0.1.0-draft.1` provides no field for claiming completeness. Tools MUST NOT infer completeness from the presence of a file, the presence of some lineage entries, or an omitted source. An empty `lineage` list is invalid because it can be misread as an affirmative statement that no antecedents exist.

This follows the useful distinction made by SPDX between no assertion and an affirmative assertion of none, while remaining a separate convention. SPDX 2.3 likewise states that omitted relationships do not imply that no additional relationships exist.

### 8.2 What an entry does and does not say

An entry records a maintainer's engineering or historical characterisation. It does not independently establish copying, copyright derivation, infringement, ownership, priority, entitlement to credit, or licence compliance.

Conversely, cautious wording does not make the statement legally neutral. Renaming a field cannot remove the exposure created by publishing a dated provenance assertion.

## 9. Relationship vocabulary

The relationship value describes the publishing project's best current characterisation. It is not a legal conclusion.

| Value | Draft meaning |
|---|---|
| `copied` | Source material was incorporated verbatim or with only non-substantive changes. |
| `adapted` | A source artifact or implementation was modified to fit a new context while retaining identifiable lineage. |
| `vendored` | An external artifact was copied into the repository or distribution and is maintained or shipped as an embedded copy. |
| `translated` | A source implementation or expression was converted to another language, stack, or representation while retaining substantial structure or logic. |
| `reimplemented` | New expression was written after consulting the source while preserving a distinctive method, structure, or implementation approach; no copied expression is asserted by the term alone. |
| `behaviorally-reproduced` | Observable behaviour was intentionally reproduced from a source without asserting shared expression or internal architecture. |
| `inspired` | The source materially influenced a specific subject, but the stronger relations above would overstate what occurred. |
| `unknown` | The source is known, but the exact relationship cannot presently be characterised. Authors SHOULD explain the uncertainty. |

Broad ecosystem acknowledgements and cultural influences that cannot be tied to a specific subject belong in the Markdown body, not in structured lineage entries.

## 10. Stable subject identifiers and reference integrity

An `id` or `source-subject` MUST use lowercase ASCII letters and digits separated by single hyphens. It is local to the source project; no global registry is required.

Once published, a subject ID MUST NOT be reused for a materially different subject. Wording may evolve while the identity remains stable. If a subject is retired or removed, its ID remains reserved and SHOULD remain discoverable in version history or explanatory documentation.

A downstream `source-subject` can become unresolvable because the source renamed, removed, or moved its entry. An **unresolvable `source-subject` is an integrity warning**, not a semantic conclusion. It does not retract the downstream statement, deny the relationship, or mean the source disowned the subject. Tooling SHOULD report the broken pointer while preserving the lineage entry's independent `source`, `subject`, `relationship`, and `seen` fields.

## 11. Legal and licensing caution

Publishing a lineage entry creates a durable statement about a project's exposure to, use of, or relationship with another source. This format does not make that statement legally neutral and does not replace licence compliance.

Before publishing `copied`, `vendored`, `adapted`, or `translated` against a restrictively licensed or otherwise sensitive upstream, verify the applicable licence and any notice, source-availability, attribution, patent, confidentiality, or distribution obligations. Where ownership, permission, licence compatibility, or the character of reuse is unclear or disputed, obtain qualified legal advice before publication rather than treating the entry as a routine documentation exercise.

`GENEALOGY.md` is not legal advice. Maintainers remain responsible for preserving required notices and satisfying the licences that govern copied or distributed material.

## 12. SPDX relationship

`GENEALOGY.md` is not an SPDX profile and does not claim SPDX conformance. It has partial overlap with SPDX artifact relationships, but the mapping is versioned, directional, and often lossy.

The table below maps a `GENEALOGY.md` entry where the current project is the descendant and `source` identifies the antecedent.

| Relation | SPDX 3.0.1 | SPDX 2.3 | Fit and direction |
|---|---|---|---|
| `copied` | Source `copiedTo` current element; current may also be `descendantOf` source | Current `COPY_OF` source when exact | Strong only for an exact artifact copy; non-substantive changes may require ancestry or variant semantics instead. |
| `adapted` | Current `descendantOf` source, or source `hasVariant` current | Current `DESCENDANT_OF` or `VARIANT_OF` source | Lossy: SPDX does not preserve the nature or extent of adaptation. |
| `vendored` | Project `contains` embedded artifact plus source `copiedTo` embedded artifact | Project `CONTAINS` embedded artifact plus embedded artifact `COPY_OF` source | Composite mapping; “vendored” also describes repository and maintenance posture. |
| `translated` | Current may be `descendantOf` source | Current may be `DESCENDANT_OF` source | Lossy: ancestry can be preserved, but the semantic fact of language or stack translation is lost. |
| `reimplemented` | No safe core equivalent; `other` plus comment is possible | `OTHER` plus comment is possible | A normal ancestry relation may imply a stronger artifact link than intended. |
| `behaviorally-reproduced` | No core equivalent | No core equivalent | The relation concerns reproduced behaviour without necessarily sharing artifact expression or architecture. |
| `inspired` | No core equivalent | No core equivalent | Historical influence is not an ordinary bill-of-materials relationship. |
| `unknown` | `NoAssertionElement` is only partial; `other` plus comment may retain the known source | `NOASSERTION` is only partial; `OTHER` plus comment may retain the known source | The source is known while the exact relation is unresolved, so a bare no-assertion value loses information. |

Relevant official references:

- [SPDX 3.0.1 relationship vocabulary](https://spdx.github.io/spdx-spec/v3.0.1/model/Core/Vocabularies/RelationshipType/)
- [SPDX 3.0.1 `NoAssertionElement`](https://spdx.github.io/spdx-spec/v3.0.1/model/Core/Individuals/NoAssertionElement/)
- [SPDX 3.0.1 `attributionText`](https://spdx.github.io/spdx-spec/v3.0.1/model/Software/Properties/attributionText/)
- [SPDX 3.0.1 Extension Profile](https://spdx.github.io/spdx-spec/v3.0.1/model/Extension/Classes/Extension/)
- [SPDX 2.3 relationships](https://spdx.github.io/spdx-spec/v2.3/relationships-between-SPDX-elements/)

SPDX `attributionText` is adjacent to self-citation because it can carry acknowledgement text and contextual reproduction guidance, but it does not provide structured feature-level `cite-when` and `do-not-cite-when` boundaries. An SPDX Extension could model additional concepts in the future; requiring that machinery for a small repository-root authoring convention would impose disproportionate adoption friction in this draft.

## 13. Relationship to `CITATION.cff`, REUSE, licences, and SBOMs

`GENEALOGY.md` complements rather than replaces established mechanisms:

- [`CITATION.cff`](https://citation-file-format.github.io/) provides human- and machine-readable software citation metadata. It does not define conditional, feature-scoped provenance guidance.
- [REUSE](https://reuse.software/spec/) standardises per-file copyright and licensing information. `GENEALOGY.md` does not satisfy REUSE or preserve notices on its behalf.
- SPDX documents and SBOMs describe artifacts, components, licences, and relationships at supply-chain scale. `GENEALOGY.md` is a lightweight authoring convention for feature-level statements, including conceptual and behavioural relations that may lack an artifact-level copy.
- `LICENSE`, `NOTICE`, copyright headers, package manifests, and Git history retain their own roles.

A project SHOULD use the established mechanism appropriate to each obligation. Adding `GENEALOGY.md` never relaxes another requirement.

## 14. Validation

The normative schema uses [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12). A schema validator MUST:

1. extract the YAML document using section 4;
2. parse the YAML safely; and
3. validate the resulting mapping against the schema with URI and date format checking enabled.

A full conformance checker MUST additionally reject duplicate local `self-citation.id` values, because JSON Schema cannot express uniqueness by one object property. It SHOULD report an unresolvable external `source-subject` separately as an integrity warning rather than a schema error or semantic retraction.

Network access is not required for ordinary schema validation or local-ID checking when the schema is available locally. Cross-repository `source-subject` resolution is optional and cannot change the meaning of an otherwise well-formed lineage entry.

The repository [README](../README.md) supplies disposable Bash and PowerShell commands using PyYAML and `jsonschema`. They perform schema validation and the local duplicate-ID check. They do not resolve external subject references and are adoption aids, not a committed validator implementation.

## 15. Versioning and evolution

The exact `genealogy-version` value prevents a validator from silently applying incompatible semantics. During the draft period:

- backwards-compatible clarifications MAY retain the same draft version;
- a schema or semantic change that can invalidate or reinterpret an existing conforming file MUST use a new version; and
- no draft version should be described as stable until at least one external repository has trialled it and an independent reviewer has assessed the result.

A future version may add redirects or explicit retirement metadata for subject IDs, richer source identities, or SPDX export. Version `0.1.0-draft.1` deliberately omits those features until adoption demonstrates a need.
