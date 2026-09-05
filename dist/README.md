# Generated experimental distribution

[make-genealogy.skill](make-genealogy.skill) is a generated ZIP-format experimental
candidate, not the editable source or a GitHub Release. The canonical source is
[skills/make-genealogy/](../skills/make-genealogy/); read the
[status and limitations](../skills/README.md) before testing.

This is the corrected experimental distribution:

```text
PACKAGE_VERSION=0.1.0-f2.2
ARCHIVE_BYTES=22938
ARCHIVE_SHA256=b6cade520188c2b2505704a14e0227f2818b79e8bf88bc7f9ad68251b2c45078
```

Its predecessor is `0.1.0-f2.1`, archive SHA-256
`fb8ee0a3b59a5c5ee31e235f9480206a02c282622ff8ac2cb8c74bf91d3898a0`.
Independent review discovered the URI-dependency fail-open defect B1. This
revision closes that contract and fixes archive navigation N1. The frozen operator
and pinned specification, schema, template and licence bytes are unchanged; the
helper, requirements, navigation note and package identities are not. Original
F2 evidence remains evidence about the predecessor, not these corrected bytes.

The source-to-artifact relationship is explicit in
[SOURCE-IDENTITY.json](SOURCE-IDENTITY.json). The archive contains the eleven paths
in the source's `CHECKSUMS.sha256`, plus that checksum file itself, under
`make-genealogy/`. The included `canonical/README.md` uses archive-local links, so
the pinned specification's `../README.md` reference resolves after extraction.
No tests, private evidence or mathematical companion is injected into ordinary
invocation.

Build or verify from the repository root:

```bash
python scripts/build_skill.py --check
python scripts/build_skill.py --output /tmp/make-genealogy.skill
```

The builder uses Python's standard library: sorted paths, fixed ZIP timestamps,
regular-file mode 0644, no archive comments or extras, and DEFLATE level 6. It
checks every input hash and the final revision-specific archive hash before
writing. Compression-library changes can alter archive bytes; a mismatch is
reported, not silently blessed as the same artifact. The checked-in checksum
records accepted bytes, not a signature or proof of native installation.

The skill's package version and the convention version are independent. These
corrections do not revise the `0.1.0-draft.2` standard. The convention-focused
[changelog](../CHANGELOG.md) is intentionally unchanged. Native installation and
invocation value remain untested.
