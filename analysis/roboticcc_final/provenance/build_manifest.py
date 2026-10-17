#!/usr/bin/env python3
"""Write MANIFEST.json for the completed reviewer package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def producer(relative: str) -> str:
    if relative.startswith("figures/pdf/") or relative.startswith("figures/png/"):
        stem = Path(relative).stem
        return f"matlab/{stem}.m"
    if relative == "CLAIM_SOURCE_MAP.csv" or relative.startswith("checks/manuscript_number_audit"):
        return "provenance/build_claim_audit.py"
    if (
        relative.startswith("source_data/")
        or relative.startswith("derived_data/")
        or relative.startswith("tables/")
        or relative.startswith("figures/source/")
        or relative in {
            "checks/data_build_validation.json",
            "checks/figure_data_audit.csv",
            "checks/table_data_audit.csv",
        }
        or relative.startswith("provenance/final_")
        or relative.startswith("provenance/upstream_")
        or relative.startswith("provenance/authoritative_input_hashes")
        or relative.startswith("provenance/phase1_claim_ledger")
        or relative.startswith("provenance/handoff_proposed")
        or relative.startswith("provenance/GENERALITY_AUDIT")
        or relative.startswith("provenance/paper_methods_fact_sheet")
    ):
        if relative.endswith("README.md"):
            return "reviewer documentation (human-authored)"
        return "provenance/build_package.py"
    if relative.startswith("matlab/"):
        return "MATLAB reproduction source (human-authored)"
    if relative.endswith("README.md") or relative == "checks/matlab_version.txt":
        return "reviewer documentation (human-authored)"
    if relative.startswith("provenance/build_"):
        return "package reproduction source (human-authored)"
    return "package assembly"


head = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
).strip()

authoritative = []
with (PACKAGE / "provenance" / "authoritative_input_hashes.csv").open(
    newline="", encoding="utf-8-sig"
) as stream:
    for row in csv.DictReader(stream):
        row["bytes"] = int(row["bytes"])
        authoritative.append(row)

outputs = []
for path in sorted(PACKAGE.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(PACKAGE).as_posix()
    if relative == "MANIFEST.json":
        continue
    outputs.append(
        {
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "generated_by": producer(relative),
        }
    )

manuscript = PACKAGE / "provenance" / "final_manuscript.tex"
matlab_version = (PACKAGE / "checks" / "matlab_version.txt").read_text(
    encoding="utf-8"
).strip()

manifest = {
    "package": "analysis/roboticcc_final",
    "purpose": "Reviewer-readable final RoboticCC data, claim, table, and MATLAB figure reproduction package.",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "repository_commit_sha": head,
    "dataset_identity": {
        "corrected_agx_package": "corrected_agx_v7_results",
        "corrected_hardware_package": "corrected_hardware_v9_v10_progress",
        "final_data_handoff": "roboticcc_final_data (created 2026-09-12 UTC)",
        "agx_producing_commit": "598485103ee270a27d8b684c0082e46e2ad53802",
        "hardware_v9_producing_commit": "3fe1f578987088fc8f044741bd046ca4e5488267",
        "hardware_v10_producing_commit": "a3490a7748d852af5b05f1df3caa1f86a44dda17",
        "bootstrap_draws": 10000,
        "bootstrap_seed": 20260912,
        "interval": "pointwise percentile 95% trace bootstrap",
    },
    "matlab_version": matlab_version,
    "final_manuscript": {
        "package_path": "provenance/final_manuscript.tex",
        "sha256": sha256(manuscript),
        "bytes": manuscript.stat().st_size,
        "source_role": "Newest RoboticCC Overleaf main.tex; reporting source of truth",
    },
    "authoritative_input_files": authoritative,
    "generated_output_files": outputs,
    "manifest_hash_note": "MANIFEST.json excludes itself; rerunning this script refreshes timestamps and all file hashes.",
}

(PACKAGE / "MANIFEST.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
print(f"Wrote MANIFEST.json with {len(authoritative)} authoritative inputs and {len(outputs)} package files")
