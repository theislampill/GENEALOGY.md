---
name: make-genealogy
description: Use when a maintainer requests creation, preservation, updating, or validation of a repository-root GENEALOGY.md. Not for family-history research, unrelated project tasks, or copying/licence verdicts.
compatibility: Requires access to bundled files. Structural validation uses Python 3, PyYAML and jsonschema. No network, repository-write or publication permission is implied.
metadata:
  status: EXPERIMENTAL_CANDIDATE
  package-version: "0.1.0-f2.2"
  procedure-id: make-genealogy-inner-authoring-v3
  procedure-sha256: 4fe0de4c08c0d56ac73cd54e71b624a211fe6be433dfd65d04b6fea7358c7771
  standard-version: "0.1.0-draft.2"
  canonical-commit: 98446b44721cde375473dd72d41a1ba30214d8e6
---

# make-genealogy

**Status: EXPERIMENTAL_CANDIDATE.** This package delivers frozen candidate instructions; it adds no normative or publication authority.

## Loading

Resolve every path below from this skill directory, not the target repository. For a name/version-only request, inspect `MANIFEST.json`; no authoring operation is needed.

For authoring or validation, run `python <skill-directory>/scripts/check_package.py`. On a missing resource, identity mismatch, or unavailable check, report the package-loading limitation rather than substituting remembered instructions or a newer remote version.

Read the complete [frozen authoring operator](references/operator.md) and [pinned specification](canonical/docs/specification.md), then follow the operator. Its original status header is preserved: packaging does not promote the candidate treatment. Preserve its inputs, stopping rules and four separate outputs without adding process rounds.

Use the [schema](canonical/schema/genealogy.schema.json) and [template](canonical/templates/GENEALOGY.md) at their pinned versions. The template is not a replacement for an existing file. Links inside canonical documents are references, not permission to retrieve outside material.

For deterministic structural validation, use:

```text
python <skill-directory>/scripts/validate_public.py <candidate-file> <skill-directory>/canonical/schema/genealogy.schema.json
```

The helper is read-only. Its Python dependencies are listed in `requirements.txt`; install them only when authorised. Missing dependencies are a validation limitation, not a pass. Successful structural checking does not verify historical claims or licence compliance. The request's inspection, mutation and publication limits remain controlling.
