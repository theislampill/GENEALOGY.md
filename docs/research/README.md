# Non-normative research note

**The Cost of a Decisive Revision: Evidence, Reuse, and Self-Application**

[Read the four-page PDF](the-cost-of-a-decisive-revision.pdf) or
[inspect its LaTeX source](the-cost-of-a-decisive-revision.tex).

The anonymous, purpose-agnostic note concerns decision cost, authorised evidence,
reuse of retained records and predecessor-governed self-application. Its claims
are relative to the specified finite observation model. It is neither the
normative specification nor independent validation of a project or procedure.
The [draft standard](../specification.md) remains separate. The
[project-specific design model](../design/authoring-model.md) has a different,
explicitly non-normative responsibility.

## Build

From the repository root:

```bash
python scripts/build_methodology.py --check
python scripts/build_methodology.py --output /tmp/the-cost-of-a-decisive-revision.pdf
```

The builder runs pdfLaTeX twice in an isolated temporary directory with shell
escape disabled. The source suppresses date/trailer metadata; the build fixes
the source-date epoch. It does not fetch dependencies or contact external sites.
The required TeX packages are declared in the source.

The checked-in PDF was rebuilt identically in separate temporary directories with
pdfTeX 1.40.26 (TeX Live 2025/dev/Debian), using the installed Latin Modern fonts
and declared LaTeX packages. Byte reproducibility is qualified to that toolchain;
other TeX/font versions may produce a different PDF. `--check` reports a mismatch
instead of replacing the reviewed artifact. The source's mathematical body and
bibliography are unchanged from the supplied manuscript; publication editing is
limited to title, title layout and reproducible anonymous metadata.
