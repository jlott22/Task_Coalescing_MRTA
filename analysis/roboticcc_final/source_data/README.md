# Package source data

These files are compact, publication-relevant inputs copied or filtered from the corrected final-data handoff. They are not the repository's full raw experiment tree, and the build scripts never overwrite their authoritative upstream sources.

Trial-level inputs preserve `trace_id`, completion status, campaign/round or board/runtime lineage, and the endpoints needed by the manuscript. `completion_records.csv` also retains all failed or noncompleted jobs so continuous common-completer effects can be interpreted beside the full planned denominators.

Files ending in `_validated.csv` are final-handoff statistical inputs. They retain the already verified shared-bootstrap intervals and specialized task-waiting summaries. The package-local build reshapes and filters them while independently checking row counts and point estimates against trial-level values. Upstream hashes are in `../provenance/authoritative_input_hashes.csv`; package hashes are in `../MANIFEST.json`.

`platform_policy_pairs.csv` includes both the 48 planned RP2040 blocks (successes and failures) and corresponding AGX pairs. Filter on `provider` before aggregating. `completion_accounting_validated.csv` contains overlapping scopes; use one `scope` at a time.
