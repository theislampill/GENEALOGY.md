# Contributing

`GENEALOGY.md` is an early draft convention. Contributions should improve its usefulness without manufacturing the appearance of a mature standards organisation.

## Before proposing a change

Read the [draft specification](docs/specification.md), the [schema](schema/genealogy.schema.json), and the root [dogfooded example](GENEALOGY.md).

A field, relationship, or semantic change should include:

1. the concrete problem it solves;
2. a concrete example from a real or realistic repository;
3. the exact schema and prose change proposed;
4. its effect on backwards compatibility and existing `0.1.0-draft.2` files;
5. a migration path when the change is incompatible; and
6. an SPDX 3.0.1 and SPDX 2.3 comparison when the proposal overlaps artifact relationships.

A proposal affecting `seen`, temporal precision, or qualification must state which lexical forms become valid or invalid, whether existing values change meaning, and how tools preserve precision. Do not use dummy exact dates for unknown periods.

Run the disposable validation command in the [README](README.md) before submitting a pull request.

## Corrections to provenance statements

A correction to this repository's `GENEALOGY.md` should identify the affected entry, explain the factual basis for the correction, and preserve uncertainty where the record does not support a stronger statement.

Do not use an issue or pull request as a copying verdict, infringement finding, or public-pressure substitute for evidence. A missing entry is a lead for a specific question, not a conviction. A recorded entry is a maintainer's statement, not an adjudication.

## Scope discipline

The repository intentionally omits governance, support, security-reporting, release-management, and CI scaffolding until real use creates a need. Proposals to add such machinery should identify the concrete force that now makes it load-bearing.

By contributing, you agree that your contribution is licensed under the repository's [MIT License](LICENSE).
