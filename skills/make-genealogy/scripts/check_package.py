#!/usr/bin/env python3
"""Read-only local delivery check, not skill registration or history verification."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

OP = "4fe0de4c08c0d56ac73cd54e71b624a211fe6be433dfd65d04b6fea7358c7771"
VERSION = "0.1.0-draft.2"
COMMIT = "98446b44721cde375473dd72d41a1ba30214d8e6"
SCHEMA = "76c7c8cde4bd3f77331045a40dc95ecc34398f318f27ad98933717d5f4d3333d"
ID = "https://raw.githubusercontent.com/theislampill/GENEALOGY.md/v0.1.0-draft.2/schema/genealogy.schema.json"


def verify(root: Path) -> dict:
    root = root.resolve()
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    if manifest["name"] != "make-genealogy" or manifest["package_version"] != "0.1.0-f2.2":
        raise ValueError("package identity mismatch")
    if manifest["status"] != "EXPERIMENTAL_CANDIDATE":
        raise ValueError("unexpected package status")
    if manifest["procedure"] != {"id": "make-genealogy-inner-authoring-v3", "sha256": OP}:
        raise ValueError("operator binding mismatch")
    if manifest["standard"] != {"version": VERSION, "commit": COMMIT, "schema_id": ID, "schema_sha256": SCHEMA}:
        raise ValueError("standard binding mismatch")
    required = {"references/operator.md", "canonical/docs/specification.md",
                "canonical/schema/genealogy.schema.json", "canonical/templates/GENEALOGY.md",
                "canonical/LICENSE", "canonical/README.md", "scripts/validate_public.py", "scripts/check_package.py", "requirements.txt"}
    if set(manifest["files"]) != required:
        raise ValueError("unexpected or missing semantic resource")
    for rel, expected in manifest["files"].items():
        parts = PurePosixPath(rel)
        if parts.is_absolute() or ".." in parts.parts:
            raise ValueError("unsafe resource path")
        path = root / rel
        if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
            raise ValueError("symlink resource is not supported")
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError("missing/outside resource: " + rel)
        data = path.read_bytes()
        if len(data) != expected["bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError("resource identity mismatch: " + rel)
    op = (root / "references/operator.md").read_bytes()
    schema_bytes = (root / "canonical/schema/genealogy.schema.json").read_bytes()
    if hashlib.sha256(op).hexdigest() != OP or hashlib.sha256(schema_bytes).hexdigest() != SCHEMA:
        raise ValueError("pinned semantic bytes mismatch")
    schema = json.loads(schema_bytes)
    if schema["$id"] != ID or schema["properties"]["genealogy-version"]["const"] != VERSION:
        raise ValueError("schema identity mismatch")
    return {"status": "IDENTITY_VERIFIED", "handle": "make-genealogy",
            "package_version": manifest["package_version"], "procedure_sha256": OP,
            "standard_version": VERSION, "canonical_commit": COMMIT,
            "semantic_files_verified": len(required), "native_installation_verified": False}


def main() -> int:
    try:
        result = verify(Path(__file__).resolve().parents[1])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "PACKAGE_LOAD_ERROR", "detail": str(exc)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
