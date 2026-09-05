#!/usr/bin/env python3
"""Rebuild the frozen experimental distribution; never register or invoke a skill."""
from __future__ import annotations
import argparse
import hashlib
import io
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills' / 'make-genealogy'
EXPECTED = 'b6cade520188c2b2505704a14e0227f2818b79e8bf88bc7f9ad68251b2c45078'
MEMBERS = {
    'CHECKSUMS.sha256', 'MANIFEST.json', 'SKILL.md', 'canonical/LICENSE', 'canonical/README.md',
    'canonical/docs/specification.md', 'canonical/schema/genealogy.schema.json',
    'canonical/templates/GENEALOGY.md', 'references/operator.md',
    'requirements.txt', 'scripts/check_package.py', 'scripts/validate_public.py',
}


def read_member(name: str) -> bytes:
    path = SOURCE / name
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError('symlink source is not supported: ' + name)
    return path.read_bytes()


def build() -> bytes:
    # Only the explicitly versioned distribution members are packaged.
    # The navigation note is included without altering the pinned specification.
    declared = {}
    for line in read_member('CHECKSUMS.sha256').decode('utf-8').splitlines():
        digest, name = line.split(maxsplit=1)
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or '\\' in name or name in declared:
            raise ValueError('unsafe or duplicate checksum member')
        if len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('invalid SHA-256')
        declared[name] = digest
    if set(declared) != MEMBERS - {'CHECKSUMS.sha256'}:
        raise ValueError('distribution member set differs from the frozen candidate')
    payload = {name: read_member(name) for name in sorted(MEMBERS)}
    for name, digest in declared.items():
        if hashlib.sha256(payload[name]).hexdigest() != digest:
            raise ValueError('source checksum mismatch: ' + name)
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=6) as archive:
        for name, data in payload.items():
            info = zipfile.ZipInfo('make-genealogy/' + name, (2026, 9, 5, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compresslevel=6)
    result = output.getvalue()
    if hashlib.sha256(result).hexdigest() != EXPECTED:
        raise ValueError('archive bytes differ; do not overwrite the pinned artifact. '
                         'Check source bytes and Python/zlib build compatibility.')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='compare with the checked-in distribution')
    mode.add_argument('--output', type=Path, help='write the verified archive to this path')
    args = parser.parse_args()
    try:
        data = build()
        if args.output is not None:
            destination = args.output.resolve()
            if destination == SOURCE or SOURCE in destination.parents:
                raise ValueError('output must be outside the frozen skill source')
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        elif (ROOT/'dist/make-genealogy.skill').read_bytes() != data:
            raise ValueError('checked-in distribution differs from its source')
        print('PACKAGE_SOURCE_MATCH=YES')
        print('PACKAGE_SHA256=' + EXPECTED)
        print('NATIVE_INSTALLATION_TESTED=NO')
        return 0
    except (OSError, ValueError, UnicodeError, zipfile.BadZipFile) as exc:
        print('BUILD_ERROR=' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
