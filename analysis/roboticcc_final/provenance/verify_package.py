#!/usr/bin/env python3
"""Verify package-output hashes recorded in MANIFEST.json."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


manifest = json.loads((PACKAGE / "MANIFEST.json").read_text(encoding="utf-8"))
failures = []
for record in manifest["generated_output_files"]:
    path = PACKAGE / record["path"]
    if not path.exists():
        failures.append(f"missing: {record['path']}")
        continue
    if path.stat().st_size != record["bytes"]:
        failures.append(f"size: {record['path']}")
    if sha256(path) != record["sha256"]:
        failures.append(f"sha256: {record['path']}")

if failures:
    raise SystemExit("Manifest verification failed:\n" + "\n".join(failures))
print(f"PASS: {len(manifest['generated_output_files'])} package files match MANIFEST.json")
