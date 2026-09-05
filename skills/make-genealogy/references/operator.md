# `make-genealogy` inner authoring operator

**Procedure ID:** `make-genealogy-inner-authoring-v3`  
**Status:** frozen candidate treatment; not a standard extension, installed skill, or publication authority  
**Supersedes:** `make-genealogy-inner-authoring-v2`

## Purpose and inputs

Help a maintainer create or update the smallest **task-adequate, truthful** canonical `GENEALOGY.md` supported by evidence they possess or expressly authorise.

Identify before work:

- target repository and exact revision or working state;
- pinned specification, schema, and template;
- any existing root `GENEALOGY.md`;
- authorised evidence sources and tool boundaries;
- what may be inspected, asked, drafted, modified, or published; and
- the bounded authoring target implied by the request.

The target is normally validation, preservation/update, self-citation, a named source or subject, or a bounded review of authorised project evidence. For a broad create/update request, propose materially distinct, adequately supported feature-provenance statements encountered within that evidence. This is neither a completeness claim nor permission for broad external search.

This procedure does not adjudicate plagiarism, determine licence compliance, certify historical truth, or guarantee a file.

## Procedure

### 1. Preserve the current public state

Use an existing conforming `GENEALOGY.md` as the starting public candidate. Do not regenerate it from an empty template merely to demonstrate work.

If an existing file declares another version or incompatible semantics, preserve it and return `MIGRATION_REVIEW_REQUIRED`. If no file exists, begin with project identity and no self-citation or lineage claim.

### 2. Inspect authorised evidence first

Read the relevant in-scope genealogy, README, design material, acknowledgements, notices, licence records, code, comments, history, issues, pull requests, dependencies, vendoring records, maintainer testimony, and any expressly authorised named-upstream snapshot.

Record what each source can establish. Several documents may repeat one originating statement; surface count is not route independence. Do not begin ordinary authoring with a broad search for similar projects.

### 3. Take the cheap path

- Existing conforming file with no supported target-relevant change: return unchanged and stop.
- No evidence of external reception: do not manufacture lineage. Draft narrow self-citation when supported; otherwise return `NO_RESPONSIBLE_FILE`.
- Syntax-only task: validate deterministically and stop.

The cheap path creates no speculative candidates, external searches, persistent private ledgers, or external-source approval ceremony.

### 4. Form a small evidence-grounded neighbourhood

Create a candidate only when the inspected record gives a concrete reason. Start with the most informative statement the record may support and compare only a nearby honest alternative when needed, such as:

- narrower subject;
- different relationship actually supported by the evidence;
- coarser supported `seen` precision, without inventing components or qualification;
- body-only acknowledgement for an established relationship lacking a responsibly known first-seen year;
- private unresolved state; or
- omission.

Do not enumerate every combination. Relationship values are not a universal strength ladder.

### 5. Apply hard constraints before usefulness

Reject or withhold any candidate requiring:

- invented or sentinel-filled date, revision, licence, URI, encounter, or relationship;
- resemblance or chronological priority treated as reception;
- `relationship: unknown` when source participation itself is unproven;
- qualification or cautious prose used to create support;
- repeated text from one origin counted as independent corroboration;
- unauthorised evidence, search, mutation, or publication;
- unresolved external material transmitted as public lineage;
- claims of completeness, independent invention, legal derivation, licence compliance, or historical verification beyond the standard; or
- violation of the pinned schema/specification.

An informative-looking result cannot outweigh a failed hard constraint.

### 6. Preserve target-bounded semantic adequacy

Do the bounded job requested. For a broad bounded review, propose each materially distinct, adequately supported statement whose inclusion materially changes understanding of how the reviewed work came about.

Repeated source identity or an additional row is not redundant when it preserves a materially different subject, relationship, reception route, or temporal claim. Omission is not denial, but an arbitrary omission may still fail the task. Do not expand beyond a named feature or source merely because other facts are known.

### 7. Use supported specificity, then minimise equivalents

For each retained proposition, use the most informative evidence-supported subject, relationship, source, revision when known, and temporal precision.

Only when two public states preserve equivalent target-relevant meaning should you prefer less redundancy, unnecessary breadth, public claim surface, maintenance cost, and avoidable burden.

Do not merge distinct known relationships into one broad `relationship: unknown` entry to save a row. When admissible non-equivalent states present a material trade-off the request does not resolve, use `ASK` rather than silently preferring fewer or more claims.

### 8. Keep publication states distinct

**Structured public claim** — Source connection, material influence, relationship, required date at supported precision, and other asserted fields have a reasonable basis. Qualification narrows an admitted statement; it does not create support. External-source entries require maintainer review before publication.

**Body-only acknowledgement** — The relationship is established, but the current structured model cannot admit it, such as when no first-seen year can responsibly be supplied. State that representational limit; do not infer structured fields from the prose.

**Private unresolved working state** — Reception, influence, relationship, chronology, or another necessary proposition is unproven, contradictory, or awaiting a discriminating answer. Keep it out of the public file. It is session-only unless a separately authorised consumer justifies persistence.

Do not print private candidates in the Markdown body merely to appear transparent, or use public `uncertainty` for a proposition that has not earned admission.

### 9. Ask only decision-changing questions

Ask only when the answer could change a public field, target, publication state, or terminal. Batch related questions and do not ask for facts already in the record. An unanswered necessary question keeps only the affected candidate private or omitted.

Use:

```text
KEEP
DROP
NARROW
KEEP_PRIVATE
ASK
STOP
```

### 10. Re-read, validate, and return

Before emission, review the whole public candidate for:

- target-relevant supported propositions omitted without a scope reason;
- meaning-equivalent duplication or materially distinct claims improperly merged;
- contradiction, excessive subject breadth, or relationship overstatement;
- unsupported source, revision, licence, or date precision;
- private/public/body-only leakage;
- stale version/schema identity; and
- completeness, legal-status, or historical-verification overclaims.

Perform one whole-file reread, not an artificial multi-round loop. Then validate front matter against the pinned schema with format checking enabled and reject duplicate local self-citation IDs. Preserve actual validation errors; never repair facts merely to pass.

Return separately:

1. proposed public `GENEALOGY.md`, or `null` with `NO_RESPONSIBLE_FILE` or `MIGRATION_REVIEW_REQUIRED`;
2. brief non-public rationale, including material candidates kept private or dropped;
3. only questions capable of changing the public result; and
4. structural validation status and limits.

Only item 1 is publication-eligible. Always state:

```text
HISTORICAL_TRUTH_VERIFIED=NO
LICENCE_COMPLIANCE_VERIFIED=NO
LINEAGE_COMPLETENESS_ASSERTED=NO
```

## Stop rule

Stop when no admissible nearby change would improve target-bounded semantic adequacy, supported specificity, or meaning-equivalent minimality, and no unanswered necessary question could change a public field, target, or terminal state.

Valid terminals are: unchanged conforming file; self-citation only; sparse structured lineage; structured lineage plus bounded body-only acknowledgement; body-only acknowledgement; `MIGRATION_REVIEW_REQUIRED`; or `NO_RESPONSIBLE_FILE`.

## Six invariants

1. Resemblance is not reception.
2. An unresolved relationship is not an unproven source.
3. Qualification does not create support.
4. Many surfaces may still be one route; route independence still does not prove truth.
5. Private candidates are not public lineage.
6. A correct-looking file does not prove an adequate authoring pathway.
