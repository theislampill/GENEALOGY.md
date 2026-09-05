#!/usr/bin/env python3
"""Build the anonymous note in a temporary directory, without shell escape."""
from __future__ import annotations
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
STEM = 'the-cost-of-a-decisive-revision'
SOURCE = ROOT / 'docs' / 'research' / (STEM + '.tex')
TARGET = SOURCE.with_suffix('.pdf')


def build() -> bytes:
    engine = shutil.which('pdflatex')
    if engine is None:
        raise ValueError('pdflatex is required; no PDF was produced')
    with tempfile.TemporaryDirectory(prefix='methodology-build-') as directory:
        work = Path(directory)
        shutil.copyfile(SOURCE, work / SOURCE.name)
        env = dict(os.environ, SOURCE_DATE_EPOCH='1788523570', FORCE_SOURCE_DATE='1',
                   TZ='UTC')
        for _ in range(2):
            result = subprocess.run(
                [engine, '-no-shell-escape', '-interaction=nonstopmode',
                 '-halt-on-error', '-file-line-error', SOURCE.name],
                cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, timeout=90,
            )
            if result.returncode:
                raise ValueError('pdfLaTeX failed:\n' + result.stdout[-12000:])
        log = (work / (STEM + '.log')).read_text(errors='replace')
        if 'undefined references' in log or 'undefined citations' in log or 'Overfull \\hbox' in log:
            raise ValueError('unresolved references/citations or overfull box; inspect the build')
        return (work / (STEM + '.pdf')).read_bytes()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='compare with the checked-in PDF')
    mode.add_argument('--output', type=Path, help='write a rebuilt PDF here')
    args = parser.parse_args()
    try:
        data = build()
        if args.check:
            if TARGET.read_bytes() != data:
                raise ValueError('rebuilt PDF differs; check the documented TeX toolchain, '
                                 'rather than silently replacing the reviewed PDF')
        else:
            destination = args.output or TARGET
            if destination.resolve() == SOURCE.resolve():
                raise ValueError('PDF output must not overwrite the source')
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        print('PDF_BUILD=PASS')
        print('PDF_SHA256=' + hashlib.sha256(data).hexdigest())
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print('BUILD_ERROR=' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
