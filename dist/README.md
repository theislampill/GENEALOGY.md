# Generated experimental distribution

[make-genealogy.skill](make-genealogy.skill) is a generated ZIP-format experimental
candidate, not the editable source or a GitHub Release. The canonical source is
[skills/make-genealogy/](../skills/make-genealogy/); read the
[status and limitations](../skills/README.md) before testing.

The archive preserves the accepted packaging candidate exactly:

```text
PACKAGE_VERSION=0.1.0-f2.1
ARCHIVE_BYTES=21281
ARCHIVE_SHA256=fb8ee0a3b59a5c5ee31e235f9480206a02c282622ff8ac2cb8c74bf91d3898a0
```

The source-to-artifact relationship is explicit in
[SOURCE-IDENTITY.json](SOURCE-IDENTITY.json). The archive contains the ten paths
in the source's unchanged `CHECKSUMS.sha256`, plus that checksum file itself,
under `make-genealogy/`. All eleven file contents are unchanged. The adjacent
repository-only `canonical/README.md` navigation note is not packaged and is not
a runtime instruction. No tests, private evidence or mathematical companion is
injected into ordinary invocation.

Build or verify from the repository root:

```bash
python scripts/build_skill.py --check
python scripts/build_skill.py --output /tmp/make-genealogy.skill
```

The builder uses Python's standard library: sorted paths, fixed ZIP timestamps,
regular-file mode 0644, no archive comments or extras, and DEFLATE level 6. It
checks every input hash and the final accepted archive hash before writing.
Compression-library changes can alter archive bytes; a mismatch is reported,
not silently blessed as the same artifact. The checked-in checksum records the
accepted bytes, not a signature or proof of native installation.

The skill's package version and the convention version are independent. These
repository-level additions do not revise the `0.1.0-draft.2` standard. The
convention-focused [changelog](../CHANGELOG.md) is intentionally unchanged.
