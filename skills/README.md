# Experimental authoring skill

`make-genealogy` packages a frozen plain-language authoring procedure for creating,
preserving, updating or validating a repository-root `GENEALOGY.md`.

**The skill is optional and non-normative.** Using it is not part of
`0.1.0-draft.2` conformance. A file is not invalid merely because it was written
without the skill. The [specification](../docs/specification.md) and
[schema](../schema/genealogy.schema.json) remain the standard's authorities.

```text
STATUS=EXPERIMENTAL
BOUNDED_CORRECT_EXECUTION_DEMONSTRATED=YES
GENERAL_EFFICACY_ESTABLISHED=NO
INCREMENTAL_CAUSAL_BENEFIT_DEMONSTRATED=NO
NATIVE_INSTALLATION_INVOCATION_COMPARISON_COMPLETE=NO
```

Bounded correct execution was observed across twelve constructed pilot items,
including responsible null results. That pilot used serial, accumulating context;
authoring and judging independence were not certified. It does not establish a
clean causal treatment advantage, general efficacy or universal safety. Local
fidelity, integrity, co-delivery and filesystem-relocation checks are separate
from native host installation, activation, discovery, resupply and context value.
The latter comparison remains incomplete. This candidate is not normative or
required, and the available evidence does not establish that it generally
outperforms manual or minimally instructed authoring.

## Inspect and test

The editable source is [make-genealogy/](make-genealogy/), beginning with
[SKILL.md](make-genealogy/SKILL.md). The
[operator](make-genealogy/references/operator.md) is preserved without rewriting.
The [manifest](make-genealogy/MANIFEST.json) identifies the procedure,
package revision, standard version and canonical commit.

The generated [make-genealogy.skill](../dist/make-genealogy.skill) is available for
host-compatibility testing. A filename or successful local check does not prove
that a host has registered or invoked a skill. Use a host's supported import or
skill-directory mechanism; this repository does not claim native activation has
been tested. Inspect [distribution identity and build instructions](../dist/README.md)
before supplying the archive to a runtime.

```text
PROCEDURE_ID=make-genealogy-inner-authoring-v3
PROCEDURE_SHA256=4fe0de4c08c0d56ac73cd54e71b624a211fe6be433dfd65d04b6fea7358c7771
PACKAGE_VERSION=0.1.0-f2.2
STANDARD_VERSION=0.1.0-draft.2
CANONICAL_COMMIT=98446b44721cde375473dd72d41a1ba30214d8e6
```

From the repository root, the read-only delivery checks are:

```bash
python skills/make-genealogy/scripts/check_package.py
python scripts/build_skill.py --check
```

Structural validation additionally needs the dependencies declared in
[requirements.txt](make-genealogy/requirements.txt). Install them only in an
authorised environment, then run:

```bash
python skills/make-genealogy/scripts/validate_public.py GENEALOGY.md skills/make-genealogy/canonical/schema/genealogy.schema.json
```

This checks structure, not historical truth or licence compliance. It neither
changes the target file nor authorises publication. The bundled canonical licence
notice is retained unchanged.

### Validation correction and dependencies

The original experimental `0.1.0-f2.1` package is the predecessor of this revision.
Independent review identified B1: bare `jsonschema` can lack optional URI checking
and accept an invalid URI. `0.1.0-f2.2` declares
`jsonschema[format-nongpl]==4.26.0` and independently requires a registered URI
checker that accepts valid controls and rejects an invalid control before document
validation. The same checked instance performs the document validation. Installing
the dependency extra alone is not treated as proof of runtime capability.

The helper distinguishes these command-line terminals:

| Exit | Structure | Validation status |
|---:|---|---|
| 0 | `VALID` | `VALID_DOCUMENT` |
| 1 | `INVALID` | `INVALID_DOCUMENT` |
| 2 | `UNAVAILABLE` | `VALIDATION_CAPABILITY_UNAVAILABLE` |

Missing, inert or broken URI checking cannot report a structural pass. An
unavailable check is not a finding that the document is invalid. URI syntax
checking does not retrieve a URL or establish that its resource exists.

The correction also includes archive-local canonical navigation (N1), without
changing the pinned specification. Operator semantics remain byte-identical;
the package bytes and version do not. Earlier F2 results are not retrospectively
attributed to this corrected distribution.

For deterministic regressions, install the declared requirements in a fresh
virtual environment without system site packages, then run from the repository:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

These tests cover source/archive identity and URI provisioning/fail-closed
behaviour; they are not another operator-efficacy or native-host experiment.

## Design ownership

Ordinary invocation loads the plain-language operator, not mathematical jargon.
The [authoring and project-evolution models](../docs/design/authoring-model.md)
remain active, inspectable design/test semantics outside that invocation path.
Their separation is intentional, not abandonment. The
[methodology note](../docs/research/README.md) is non-normative research, not
independent validation of the skill or of this project.
