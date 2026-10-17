#!/usr/bin/env python3
"""Build the compact RoboticCC publication analysis package.

This script never edits authoritative experiment outputs.  On its first run inside
the research repository it copies publication-relevant rows from the corrected
final-data handoff into ``source_data``.  Every later run can operate entirely
from those compact package inputs.

Publication figures are intentionally not generated here.  MATLAB scripts in
``../matlab`` read the CSVs written to ``../figures/source``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[1]
SOURCE = PACKAGE / "source_data"
DERIVED = PACKAGE / "derived_data"
TABLES = PACKAGE / "tables"
FIGSRC = PACKAGE / "figures" / "source"
CHECKS = PACKAGE / "checks"
PROVENANCE = PACKAGE / "provenance"

MANUSCRIPT_CANDIDATES = [
    Path.home() / "Downloads" / "RoboticCC_Overleaf_Package" / "RoboticCC_Overleaf" / "main.tex",
]

FLOAT_FORMAT = "%.15g"
POLICY_ORDER = ["count_b2", "count_b4", "count_b8", "bounded_b4_w10"]
POLICY_LABELS = {
    "count_b2": "Count b=2",
    "count_b4": "Count b=4",
    "count_b8": "Count b=8",
    "bounded_b4_w10": "Bounded b=4, W=10 s",
    "eager_b1": "Eager",
}
ALGORITHM_ORDER = ["CBAA", "ACBBA", "PI", "HIPC"]
LOAD_ORDER = ["low", "medium", "high"]

METRICS = [
    "allocation_epoch_count",
    "allocator_call_count",
    "work_s",
    "work_per_call_s",
    "mean_release_to_completion_latency_s",
    "p95_release_to_completion_latency_s",
    "online_mean_s",
    "mission_elapsed_time_s",
    "total_team_steps",
    "max_robot_steps",
    "logical_allocation_payload_bytes_sent_total",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, float_format=FLOAT_FORMAT, lineterminator="\n")


def copy_file(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def initialize_sources(force: bool = False) -> None:
    """Create package-local source inputs from the corrected handoff."""

    marker = SOURCE / "agx_causal_trial_level.csv"
    if marker.exists() and not force:
        return

    compact_path = REPO / "roboticcc_handoff" / "analysis" / "trial_level_compact.csv"
    compact = pd.read_csv(compact_path, low_memory=False)
    expected = {"agx": 3000, "zero_compute": 3000, "rp2040": 82}
    observed = compact["provider"].value_counts().to_dict()
    if observed != expected:
        raise ValueError(f"Unexpected compact trial coverage: {observed}")

    final_data = REPO / "roboticcc_final_data"
    causal_input = final_data / "source_rows" / "agx_causal_trial_inputs.csv"
    hardware_input = final_data / "source_rows" / "hardware_successful_trials.csv"
    copy_file(causal_input, SOURCE / "agx_causal_trial_level.csv")
    write_csv(
        compact.loc[compact.provider.eq("zero_compute")].copy(),
        SOURCE / "agx_zero_compute_trial_level.csv",
    )
    copy_file(hardware_input, SOURCE / "rp2040_trial_level.csv")
    direct_inputs = {
        final_data / "all_policy_effects_long.csv": SOURCE / "agx_effects_validated.csv",
        final_data / "low_load_count4.csv": SOURCE / "low_load_count4_validated.csv",
        final_data / "mechanism_decomposition.csv": SOURCE / "mechanism_decomposition_validated.csv",
        final_data / "anchor_rounds.csv": SOURCE / "anchor_rounds_validated.csv",
        final_data / "hardware_platform_summary.csv": SOURCE / "hardware_platform_summary_validated.csv",
        final_data / "completion_accounting.csv": SOURCE / "completion_accounting_validated.csv",
        final_data / "figure_sources" / "03_hardware_pairs.csv": SOURCE / "platform_policy_pairs.csv",
        final_data / "source_rows" / "completion_source_rows.csv": SOURCE / "completion_records.csv",
        final_data / "source_rows" / "hardware_terminal_failed_jobs.csv": SOURCE / "rp2040_terminal_failures.csv",
        final_data / "source_rows" / "mechanism_decomposition_pairs.csv": SOURCE / "mechanism_decomposition_pairs.csv",
        final_data / "source_rows" / "mechanism_online_wait_effects.csv": SOURCE / "online_wait_effects_validated.csv",
        final_data / "source_rows" / "hardware_design_metadata.json": SOURCE / "hardware_design_metadata.json",
        REPO / "architecture_generality_audit" / "no_recovery_replay.csv": SOURCE / "recovery_disabled_replays.csv",
        REPO / "architecture_generality_audit" / "anchor_metric_comparisons.csv": SOURCE / "generality_anchor_metrics.csv",
        REPO / "roboticcc_handoff" / "methods" / "trace_seeds_and_release_horizons.csv": SOURCE / "trace_seeds_and_release_horizons.csv",
    }
    for src, dst in direct_inputs.items():
        copy_file(src, dst)

    provenance_inputs = {
        final_data / "FINAL_DATA_HANDOFF.md": PROVENANCE / "FINAL_DATA_HANDOFF.md",
        final_data / "paper_methods_fact_sheet.md": PROVENANCE / "paper_methods_fact_sheet.md",
        final_data / "manifest.json": PROVENANCE / "final_data_manifest.json",
        final_data / "package_validation.json": PROVENANCE / "final_data_validation.json",
        final_data / "table_validation.json": PROVENANCE / "final_table_validation.json",
        REPO / "architecture_generality_audit" / "GENERALITY_AUDIT.md": PROVENANCE / "GENERALITY_AUDIT.md",
        REPO / "roboticcc_handoff" / "PROPOSED_NUMERICAL_CLAIMS.csv": PROVENANCE / "handoff_proposed_numerical_claims.csv",
        REPO / "roboticcc_handoff" / "methods" / "PROVENANCE.md": PROVENANCE / "upstream_provenance.md",
        REPO / "roboticcc_handoff" / "methods" / "METHODS_AND_METRICS.md": PROVENANCE / "upstream_methods_and_metrics.md",
    }
    for src, dst in provenance_inputs.items():
        copy_file(src, dst)

    phase1_zip = Path.home() / "Downloads" / "RoboticCC_Phase1_Writing_Packet.zip"
    if phase1_zip.exists():
        with zipfile.ZipFile(phase1_zip) as archive:
            ledger_bytes = archive.read("roboticcc_phase1/CLAIM_LEDGER.csv")
        (PROVENANCE / "phase1_claim_ledger.csv").write_bytes(ledger_bytes)

    manuscript = next((path for path in MANUSCRIPT_CANDIDATES if path.exists()), None)
    if manuscript is None:
        raise FileNotFoundError("Newest RoboticCC Overleaf main.tex was not found")
    copy_file(manuscript, PROVENANCE / "final_manuscript.tex")

    upstream = [
        compact_path,
        causal_input,
        hardware_input,
        *direct_inputs.keys(),
        *provenance_inputs.keys(),
        *([phase1_zip] if phase1_zip.exists() else []),
        manuscript,
    ]
    rows = [
        {
            "role": "authoritative_or_validated_input",
            "repository_relative_path_or_source_name": (
                str(path.relative_to(REPO)).replace("\\", "/")
                if path.is_relative_to(REPO)
                else "RoboticCC_Overleaf_Package/RoboticCC_Overleaf/main.tex"
            ),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in upstream
    ]
    write_csv(pd.DataFrame(rows), PROVENANCE / "authoritative_input_hashes.csv")


def make_agx_policy_pairs(causal: pd.DataFrame) -> pd.DataFrame:
    key = ["algorithm", "arrival_load", "trace_id"]
    eager = causal.loc[causal.policy_id.eq("eager_b1")].copy()
    policy = causal.loc[causal.policy_id.ne("eager_b1")].copy()
    keep = key + [
        "campaign_id",
        "round",
        "job_id",
        "policy_id",
        "all_tasks_completed",
        "algorithmic_failure_type",
        "scenario_sha256",
        "release_sha256",
        *METRICS,
    ]
    pairs = policy[keep].merge(
        eager[keep], on=key, how="left", validate="many_to_one", suffixes=("_policy", "_eager")
    )
    pairs["both_completed"] = (
        pairs["all_tasks_completed_policy"].eq(True)
        & pairs["all_tasks_completed_eager"].eq(True)
    )
    pairs["reference_policy_id"] = "eager_b1"
    for metric in METRICS:
        policy_col, eager_col = f"{metric}_policy", f"{metric}_eager"
        pairs[f"{metric}_difference"] = pairs[policy_col] - pairs[eager_col]
        pairs[f"{metric}_pct_change"] = np.where(
            pairs[eager_col].ne(0),
            100 * (pairs[policy_col] / pairs[eager_col] - 1),
            np.nan,
        )
    ordered = [
        "algorithm",
        "arrival_load",
        "policy_id_policy",
        "reference_policy_id",
        "trace_id",
        "round_policy",
        "campaign_id_policy",
        "job_id_policy",
        "job_id_eager",
        "all_tasks_completed_policy",
        "all_tasks_completed_eager",
        "both_completed",
        "algorithmic_failure_type_policy",
        "algorithmic_failure_type_eager",
        "scenario_sha256_policy",
        "release_sha256_policy",
    ]
    value_columns: list[str] = []
    for metric in METRICS:
        value_columns.extend(
            [
                f"{metric}_eager",
                f"{metric}_policy",
                f"{metric}_difference",
                f"{metric}_pct_change",
            ]
        )
    result = pairs[ordered + value_columns].rename(
        columns={"policy_id_policy": "policy_id", "round_policy": "round"}
    )
    return result.sort_values(
        ["algorithm", "arrival_load", "policy_id", "trace_id"],
        key=lambda series: series.map(
            {**{v: i for i, v in enumerate(ALGORITHM_ORDER)},
             **{v: i for i, v in enumerate(LOAD_ORDER)},
             **{v: i for i, v in enumerate(POLICY_ORDER)}}
        ).fillna(series),
    )


def build_effect_summary(effects: pd.DataFrame) -> pd.DataFrame:
    index = [
        "algorithm",
        "arrival_load",
        "policy_id",
        "planned_trials_per_policy",
        "common_completed_pairs",
    ]
    fields = [
        "eager_mean",
        "policy_mean",
        "mean_difference",
        "mean_difference_ci_low",
        "mean_difference_ci_high",
        "ratio_of_paired_means_pct",
        "ratio_of_paired_means_pct_ci_low",
        "ratio_of_paired_means_pct_ci_high",
        "median_paired_pct",
        "median_paired_pct_ci_low",
        "median_paired_pct_ci_high",
        "n_lower",
        "n_equal",
        "n_higher",
    ]
    wanted = effects.loc[effects.metric.isin(METRICS)].copy()
    pieces = []
    for metric in METRICS:
        block = wanted.loc[wanted.metric.eq(metric), index + fields].copy()
        block = block.rename(columns={name: f"{metric}__{name}" for name in fields})
        pieces.append(block)
    wide = pieces[0]
    for piece in pieces[1:]:
        wide = wide.merge(piece, on=index, how="outer", validate="one_to_one")
    wide["reference_policy_id"] = "eager_b1"
    wide["complete_50_pairs"] = wide["common_completed_pairs"].eq(50)
    return wide.sort_values(["algorithm", "arrival_load", "policy_id"]).reset_index(drop=True)


def build_hardware_cross_platform(pairs: pd.DataFrame) -> pd.DataFrame:
    selected = pairs.loc[
        pairs.algorithm.eq("HIPC")
        & pairs.arrival_load.eq("medium")
        & pairs.provider.isin(["agx", "rp2040"])
        & pairs.both_completed.eq(True)
    ].copy()
    if len(selected) != 8 or selected.trace_id.nunique() != 4:
        raise ValueError("Expected four matched HIPC/medium pairs on each platform")
    selected["platform"] = selected.provider.map({"agx": "AGX", "rp2040": "RP2040"})
    selected["policy_id"] = "count_b4"
    selected["reference_policy_id"] = "eager_b1"
    columns = [
        "platform",
        "provider",
        "algorithm",
        "arrival_load",
        "trace_id",
        "policy_id",
        "reference_policy_id",
        "eager_board_id",
        "count4_board_id",
        "eager_runtime_lineage",
        "count4_runtime_lineage",
        "same_runtime_lineage",
        "same_board",
        "eager_work_s",
        "count4_work_s",
        "work_s_difference",
        "work_s_pct_change",
        "eager_mean_release_to_completion_latency_s",
        "count4_mean_release_to_completion_latency_s",
        "mean_release_to_completion_latency_s_difference",
        "mean_release_to_completion_latency_s_pct_change",
        "eager_mission_elapsed_time_s",
        "count4_mission_elapsed_time_s",
        "mission_elapsed_time_s_difference",
        "mission_elapsed_time_s_pct_change",
        "eager_allocator_call_count",
        "count4_allocator_call_count",
        "allocator_call_count_pct_change",
        "eager_work_per_call_s",
        "count4_work_per_call_s",
        "work_per_call_s_pct_change",
        "eager_scenario_sha256",
        "eager_release_sha256",
    ]
    selected = selected[columns]
    selected["platform_order"] = selected.platform.map({"AGX": 0, "RP2040": 1})
    return selected.sort_values(["platform_order", "trace_id"]).drop(columns="platform_order")


def build_completion_summary(records: pd.DataFrame) -> pd.DataFrame:
    records = records.copy()
    records["completed"] = records.completed.eq(True)
    records["technical_failure"] = records.technical_failure.eq(True)
    records["algorithmic_noncompletion"] = (~records.completed) & (~records.technical_failure)

    def summarize(group: pd.DataFrame, scope: str, keys: dict[str, str]) -> dict[str, object]:
        row: dict[str, object] = {
            "scope": scope,
            "provider": keys.get("provider", "ALL"),
            "algorithm": keys.get("algorithm", "ALL"),
            "arrival_load": keys.get("arrival_load", "ALL"),
            "policy_id": keys.get("policy_id", "ALL"),
            "planned": len(group),
            "completed": int(group.completed.sum()),
            "algorithmic_noncompletions": int(group.algorithmic_noncompletion.sum()),
            "terminal_technical_failures": int(group.technical_failure.sum()),
        }
        row["other_total"] = row["algorithmic_noncompletions"] + row["terminal_technical_failures"]
        return row

    rows: list[dict[str, object]] = []
    for provider, group in records.groupby("provider", sort=False):
        rows.append(summarize(group, "provider_total", {"provider": provider}))
    for key, group in records.groupby(
        ["provider", "algorithm", "arrival_load", "policy_id"], sort=True, dropna=False
    ):
        rows.append(
            summarize(
                group,
                "provider_algorithm_load_policy",
                dict(zip(["provider", "algorithm", "arrival_load", "policy_id"], key)),
            )
        )
    return pd.DataFrame(rows)


def build_table1(completion: pd.DataFrame) -> pd.DataFrame:
    totals = completion.loc[completion.scope.eq("provider_total")].set_index("provider")
    definitions = [
        ("AGX causal", "agx_causal", 5, 50, "algorithmic noncompletions"),
        ("AGX zero-compute", "agx_zero_compute", 5, 50, "none"),
        ("RP2040 HIL", "rp2040", 2, 4, "terminal technical failures"),
    ]
    rows = []
    for label, provider, policies, traces, other_definition in definitions:
        row = totals.loc[provider]
        rows.append(
            {
                "campaign": label,
                "timing_provider": provider,
                "allocators": 4,
                "arrival_loads": 3,
                "policies": policies,
                "traces_per_condition": traces,
                "planned_missions": int(row.planned),
                "complete_or_successful": int(row.completed),
                "other_outcomes": int(row.other_total),
                "other_outcome_definition": other_definition,
                "source_file": "derived_data/completion_summary.csv",
                "source_filter": f"scope=provider_total,provider={provider}",
            }
        )
    return pd.DataFrame(rows)


def build_table2(anchor: pd.DataFrame, mechanism: pd.DataFrame) -> pd.DataFrame:
    metric_rows = [
        ("allocation_epoch_count", "Admission epochs", "epochs", 2, 2, 1),
        ("allocator_call_count", "Allocator calls", "calls", 2, 2, 2),
        ("work_per_call_s", "Mean work per call", "ms", 3, 3, 3),
        ("work_s", "Total allocator work", "processor-s", 4, 4, 4),
        ("mean_release_to_completion_latency_s", "Mean task latency", "s", 2, 2, 5),
        ("p95_release_to_completion_latency_s", "Mean within-mission p95", "s", 2, 2, 6),
        ("mission_elapsed_time_s", "Mission duration", "s", 2, 2, 7),
    ]
    conditions = [
        ("HIPC", "bounded_b4_w10", "HIPC high / Bounded b=4, W=10 s"),
        ("CBAA", "count_b4", "CBAA high / Count b=4"),
    ]
    rows = []
    for algorithm, policy, label in conditions:
        subset = anchor.loc[anchor.algorithm.eq(algorithm) & anchor.policy_id.eq(policy)]
        for metric, quantity, units, eager_digits, policy_digits, order in metric_rows:
            item = subset.loc[subset.metric.eq(metric)].iloc[0]
            scale = 1000.0 if metric == "work_per_call_s" else 1.0
            if metric == "work_s" and algorithm == "HIPC":
                eager_digits = 3
                policy_digits = 3
            eager_value = float(item.eager_mean) * scale
            policy_value = float(item.policy_mean) * scale
            difference = float(item.mean_difference) * scale
            rows.append(
                {
                    "condition": label,
                    "algorithm": algorithm,
                    "arrival_load": "high",
                    "policy_id": policy,
                    "reference_policy_id": "eager_b1",
                    "row_order": order,
                    "quantity": quantity,
                    "metric": metric,
                    "units": units,
                    "n_pairs": int(item.n),
                    "eager_mean": eager_value,
                    "policy_mean": policy_value,
                    "mean_difference": difference,
                    "ratio_of_paired_means_pct": float(item.ratio_of_paired_means_pct),
                    "display_eager": f"{eager_value:.{eager_digits}f}",
                    "display_policy": f"{policy_value:.{policy_digits}f}",
                    "source_file": "derived_data/anchor_examples.csv",
                    "source_filter": f"algorithm={algorithm},arrival_load=high,policy_id={policy},metric={metric}",
                }
            )
        decomp = mechanism.loc[mechanism.algorithm.eq(algorithm)].iloc[0]
        for order, quantity, column in [
            (8, "Call-count term", "calls_contribution_s"),
            (9, "Per-call-work term", "per_call_contribution_s"),
        ]:
            value_ms = float(decomp[column]) * 1000
            rows.append(
                {
                    "condition": label,
                    "algorithm": algorithm,
                    "arrival_load": "high",
                    "policy_id": policy,
                    "reference_policy_id": "eager_b1",
                    "row_order": order,
                    "quantity": quantity,
                    "metric": column,
                    "units": "ms",
                    "n_pairs": int(decomp.common_completed_pairs),
                    "eager_mean": np.nan,
                    "policy_mean": np.nan,
                    "mean_difference": value_ms,
                    "ratio_of_paired_means_pct": np.nan,
                    "display_eager": "",
                    "display_policy": "",
                    "source_file": "derived_data/mechanism_decomposition.csv",
                    "source_filter": f"algorithm={algorithm}",
                }
            )
    return pd.DataFrame(rows).sort_values(["condition", "row_order"])


def build_outputs() -> None:
    causal = pd.read_csv(SOURCE / "agx_causal_trial_level.csv", low_memory=False)
    effects = pd.read_csv(SOURCE / "agx_effects_validated.csv", low_memory=False)
    platform_pairs = pd.read_csv(SOURCE / "platform_policy_pairs.csv", low_memory=False)
    completion_records = pd.read_csv(SOURCE / "completion_records.csv", low_memory=False)
    low_load = pd.read_csv(SOURCE / "low_load_count4_validated.csv", low_memory=False)
    mechanism = pd.read_csv(SOURCE / "mechanism_decomposition_validated.csv", low_memory=False)
    hardware_summary = pd.read_csv(SOURCE / "hardware_platform_summary_validated.csv", low_memory=False)
    anchor_rounds = pd.read_csv(SOURCE / "anchor_rounds_validated.csv", low_memory=False)
    generality = pd.read_csv(SOURCE / "generality_anchor_metrics.csv", low_memory=False)

    pairs = make_agx_policy_pairs(causal)
    write_csv(pairs, DERIVED / "agx_policy_pairs.csv")
    write_csv(effects, DERIVED / "all_policy_effects.csv")

    summary = build_effect_summary(effects)
    write_csv(summary, DERIVED / "all_policy_effects_summary.csv")

    anchors = effects.loc[
        (effects.algorithm.eq("HIPC") & effects.arrival_load.eq("high") & effects.policy_id.eq("bounded_b4_w10"))
        | (effects.algorithm.eq("CBAA") & effects.arrival_load.eq("high") & effects.policy_id.eq("count_b4"))
    ].copy()
    anchors["anchor"] = np.where(anchors.algorithm.eq("HIPC"), "A", "B")
    anchors["reference_policy_id"] = "eager_b1"
    write_csv(anchors, DERIVED / "anchor_examples.csv")
    write_csv(anchor_rounds, DERIVED / "anchor_rounds.csv")
    write_csv(low_load, DERIVED / "low_load_count4.csv")
    write_csv(mechanism, DERIVED / "mechanism_decomposition.csv")
    write_csv(hardware_summary, DERIVED / "hardware_platform_summary.csv")
    write_csv(generality, DERIVED / "generality_anchor_metrics.csv")

    cross_platform = build_hardware_cross_platform(platform_pairs)
    write_csv(cross_platform, DERIVED / "hipc_medium_cross_platform.csv")

    completion = build_completion_summary(completion_records)
    write_csv(completion, DERIVED / "completion_summary.csv")

    zero = pd.read_csv(SOURCE / "agx_zero_compute_trial_level.csv", low_memory=False)
    zero_checks = []
    for algorithm, policy in [("HIPC", "bounded_b4_w10"), ("CBAA", "count_b4")]:
        subset = zero.loc[zero.algorithm.eq(algorithm) & zero.arrival_load.eq("high")]
        eager = subset.loc[subset.policy_id.eq("eager_b1") & subset.all_tasks_completed.eq(True)]
        treatment = subset.loc[subset.policy_id.eq(policy) & subset.all_tasks_completed.eq(True)]
        merged = treatment[["trace_id", "allocator_call_count"]].merge(
            eager[["trace_id", "allocator_call_count"]],
            on="trace_id",
            suffixes=("_policy", "_eager"),
            validate="one_to_one",
        )
        zero_checks.append(
            {
                "algorithm": algorithm,
                "arrival_load": "high",
                "policy_id": policy,
                "reference_policy_id": "eager_b1",
                "n_pairs": len(merged),
                "eager_mean_allocator_calls": merged.allocator_call_count_eager.mean(),
                "policy_mean_allocator_calls": merged.allocator_call_count_policy.mean(),
                "mean_difference_allocator_calls": (
                    merged.allocator_call_count_policy - merged.allocator_call_count_eager
                ).mean(),
                "source_file": "source_data/agx_zero_compute_trial_level.csv",
                "source_filter": f"algorithm={algorithm},arrival_load=high,policy_id in (eager_b1,{policy}),completed=true",
            }
        )
    write_csv(pd.DataFrame(zero_checks), DERIVED / "zero_compute_anchor_checks.csv")

    fig2 = summary[
        [
            "algorithm",
            "arrival_load",
            "policy_id",
            "reference_policy_id",
            "planned_trials_per_policy",
            "common_completed_pairs",
            "complete_50_pairs",
            "mean_release_to_completion_latency_s__ratio_of_paired_means_pct",
            "mean_release_to_completion_latency_s__ratio_of_paired_means_pct_ci_low",
            "mean_release_to_completion_latency_s__ratio_of_paired_means_pct_ci_high",
            "mean_release_to_completion_latency_s__mean_difference",
            "mean_release_to_completion_latency_s__mean_difference_ci_low",
            "mean_release_to_completion_latency_s__mean_difference_ci_high",
            "work_s__ratio_of_paired_means_pct",
            "work_s__ratio_of_paired_means_pct_ci_low",
            "work_s__ratio_of_paired_means_pct_ci_high",
            "work_s__mean_difference",
            "work_s__mean_difference_ci_low",
            "work_s__mean_difference_ci_high",
            "work_s__n_lower",
            "work_s__n_higher",
        ]
    ].copy()
    fig2 = fig2.rename(
        columns={
            "planned_trials_per_policy": "n_planned",
            "common_completed_pairs": "n_used",
            "mean_release_to_completion_latency_s__ratio_of_paired_means_pct": "x_latency_pct",
            "mean_release_to_completion_latency_s__ratio_of_paired_means_pct_ci_low": "x_latency_pct_ci_low",
            "mean_release_to_completion_latency_s__ratio_of_paired_means_pct_ci_high": "x_latency_pct_ci_high",
            "mean_release_to_completion_latency_s__mean_difference": "latency_difference_s",
            "mean_release_to_completion_latency_s__mean_difference_ci_low": "latency_difference_s_ci_low",
            "mean_release_to_completion_latency_s__mean_difference_ci_high": "latency_difference_s_ci_high",
            "work_s__ratio_of_paired_means_pct": "y_work_pct",
            "work_s__ratio_of_paired_means_pct_ci_low": "y_work_pct_ci_low",
            "work_s__ratio_of_paired_means_pct_ci_high": "y_work_pct_ci_high",
            "work_s__mean_difference": "work_difference_s",
            "work_s__mean_difference_ci_low": "work_difference_s_ci_low",
            "work_s__mean_difference_ci_high": "work_difference_s_ci_high",
            "work_s__n_lower": "work_n_lower",
            "work_s__n_higher": "work_n_higher",
        }
    )
    fig2["policy_label"] = fig2.policy_id.map(POLICY_LABELS)
    fig2["reference_x_pct"] = 0.0
    fig2["reference_y_pct"] = 0.0
    write_csv(fig2, FIGSRC / "fig2_coalescing_regimes.csv")
    write_csv(cross_platform, FIGSRC / "fig3_hipc_medium_hardware.csv")

    architecture_rows = pd.DataFrame(
        [
            ("release", "Task release", "pending", "enters environmental queue"),
            ("pending", "Pending queue", "rule", "release and admission are distinct"),
            ("rule", "Eager / Count / Bounded rule", "announce", "threshold or deadline"),
            ("announce", "Reliable task-admission announcement", "pool", "robot-local delivery"),
            ("pool", "Robot-local known-task pool", "allocator", "retained local knowledge"),
            ("allocator", "Decentralized allocator transaction", "state", "local virtual processor only"),
            ("state", "Retained goal and path state", "execution", "no destructive reset"),
            ("execution", "Physical or simulated execution", "allocator", "completion and peer feedback"),
        ],
        columns=["from_id", "from_label", "to_id", "relationship"],
    )
    write_csv(architecture_rows, FIGSRC / "fig1_admission_architecture.csv")

    table1 = build_table1(completion)
    write_csv(table1, TABLES / "table1_experiment_design.csv")
    table2 = build_table2(anchors, mechanism)
    write_csv(table2, TABLES / "table2_anchor_mechanisms.csv")

    build_data_audits(fig2, cross_platform, table1, table2, effects, completion)


def build_data_audits(
    fig2: pd.DataFrame,
    fig3: pd.DataFrame,
    table1: pd.DataFrame,
    table2: pd.DataFrame,
    effects: pd.DataFrame,
    completion: pd.DataFrame,
) -> None:
    figure_checks = []

    def add_figure_check(figure: str, check: str, observed: object, expected: object, passed: bool, notes: str = "") -> None:
        figure_checks.append(
            {
                "figure": figure,
                "check": check,
                "observed": observed,
                "expected": expected,
                "status": "PASS" if passed else "FAIL",
                "notes": notes,
            }
        )

    add_figure_check("Figure 1", "schematic data dependency", "labels and topology only", "no numerical result data", True)
    add_figure_check("Figure 2", "plotted treatment points", len(fig2), 48, len(fig2) == 48)
    add_figure_check("Figure 2", "allocator/load/policy uniqueness", fig2[["algorithm", "arrival_load", "policy_id"]].drop_duplicates().shape[0], 48, fig2[["algorithm", "arrival_load", "policy_id"]].drop_duplicates().shape[0] == 48)
    add_figure_check("Figure 2", "incomplete paired cohorts annotated", int((fig2.n_used < 50).sum()), 6, int((fig2.n_used < 50).sum()) == 6)
    ci_cols = [column for column in fig2.columns if column.endswith("ci_low") or column.endswith("ci_high")]
    add_figure_check("Figure 2", "missing plotted intervals", int(fig2[ci_cols].isna().sum().sum()), 0, fig2[ci_cols].notna().all().all())
    work = effects.loc[effects.metric.eq("work_s"), [
        "algorithm", "arrival_load", "policy_id", "ratio_of_paired_means_pct",
        "ratio_of_paired_means_pct_ci_low", "ratio_of_paired_means_pct_ci_high",
    ]].rename(columns={
        "ratio_of_paired_means_pct": "expected_y",
        "ratio_of_paired_means_pct_ci_low": "expected_y_low",
        "ratio_of_paired_means_pct_ci_high": "expected_y_high",
    })
    latency = effects.loc[effects.metric.eq("mean_release_to_completion_latency_s"), [
        "algorithm", "arrival_load", "policy_id", "ratio_of_paired_means_pct",
        "ratio_of_paired_means_pct_ci_low", "ratio_of_paired_means_pct_ci_high",
    ]].rename(columns={
        "ratio_of_paired_means_pct": "expected_x",
        "ratio_of_paired_means_pct_ci_low": "expected_x_low",
        "ratio_of_paired_means_pct_ci_high": "expected_x_high",
    })
    comparison = fig2.merge(work, on=["algorithm", "arrival_load", "policy_id"], validate="one_to_one")
    comparison = comparison.merge(latency, on=["algorithm", "arrival_load", "policy_id"], validate="one_to_one")
    plotted = comparison[["x_latency_pct", "x_latency_pct_ci_low", "x_latency_pct_ci_high", "y_work_pct", "y_work_pct_ci_low", "y_work_pct_ci_high"]].to_numpy(float)
    expected = comparison[["expected_x", "expected_x_low", "expected_x_high", "expected_y", "expected_y_low", "expected_y_high"]].to_numpy(float)
    max_error = float(np.max(np.abs(plotted - expected)))
    add_figure_check("Figure 2", "plotted values equal validated effects", max_error, 0, max_error < 1e-12)
    add_figure_check("Figure 3", "matched trace/platform rows", len(fig3), 8, len(fig3) == 8)
    adverse = fig3.loc[
        fig3.provider.eq("rp2040")
        & fig3.trace_id.eq("trace_0001")
        & (fig3.work_s_difference > 0)
        & (fig3.mean_release_to_completion_latency_s_difference > 0)
        & (fig3.mission_elapsed_time_s_difference > 0)
    ]
    add_figure_check("Figure 3", "adverse RP2040 trace retained", len(adverse), 1, len(adverse) == 1)
    for provider, platform in [("agx", "AGX"), ("rp2040", "RP2040")]:
        block = fig3.loc[fig3.provider.eq(provider)]
        work_pct = 100 * (block.count4_work_s.mean() / block.eager_work_s.mean() - 1)
        latency_pct = 100 * (
            block.count4_mean_release_to_completion_latency_s.mean()
            / block.eager_mean_release_to_completion_latency_s.mean() - 1
        )
        source = pd.read_csv(DERIVED / "hardware_platform_summary.csv")
        source = source.loc[
            source.provider.eq(provider) & source.algorithm.eq("HIPC")
            & source.arrival_load.eq("medium")
        ].iloc[0]
        error = max(
            abs(work_pct - source.work_s_ratio_of_paired_cohort_means_pct),
            abs(latency_pct - source.mean_release_to_completion_latency_s_ratio_of_paired_cohort_means_pct),
        )
        add_figure_check("Figure 3", f"{platform} aggregate matches summary", error, 0, error < 1e-10)
    write_csv(pd.DataFrame(figure_checks), CHECKS / "figure_data_audit.csv")

    table_checks = []

    def add_table_check(table: str, check: str, observed: object, expected: object, passed: bool, notes: str = "") -> None:
        table_checks.append(
            {
                "table": table,
                "check": check,
                "observed": observed,
                "expected": expected,
                "status": "PASS" if passed else "FAIL",
                "notes": notes,
            }
        )

    expected_t1 = {
        "AGX causal": (3000, 2940, 60),
        "AGX zero-compute": (3000, 3000, 0),
        "RP2040 HIL": (96, 82, 14),
    }
    for campaign, expected in expected_t1.items():
        row = table1.loc[table1.campaign.eq(campaign)].iloc[0]
        observed = (int(row.planned_missions), int(row.complete_or_successful), int(row.other_outcomes))
        add_table_check("Table I", campaign, str(observed), str(expected), observed == expected)

    add_table_check("Table II", "condition count", table2.condition.nunique(), 2, table2.condition.nunique() == 2)
    add_table_check("Table II", "rows per condition", str(table2.groupby("condition").size().to_dict()), "9 each", (table2.groupby("condition").size() == 9).all())
    source_metrics = set(effects.metric)
    required_metrics = {
        "allocation_epoch_count",
        "allocator_call_count",
        "work_per_call_s",
        "work_s",
        "mean_release_to_completion_latency_s",
        "p95_release_to_completion_latency_s",
        "mission_elapsed_time_s",
    }
    add_table_check("Table II", "required endpoint coverage", len(required_metrics & source_metrics), len(required_metrics), required_metrics <= source_metrics)
    expected_table2 = {
        "HIPC high / Bounded b=4, W=10 s": {
            "Admission epochs": "43.00 to 12.12",
            "Allocator calls": "1009.90 to 835.50",
            "Mean work per call": "1.631 to 1.565",
            "Total allocator work": "1.678 to 1.353",
            "Mean task latency": "32.37 to 33.77",
            "Mean within-mission p95": "88.88 to 89.18",
            "Mission duration": "140.42 to 138.88",
            "Call-count term": "-274.29",
            "Per-call-work term": "-50.32",
        },
        "CBAA high / Count b=4": {
            "Admission epochs": "43.00 to 12.00",
            "Allocator calls": "461.08 to 495.36",
            "Mean work per call": "0.304 to 0.348",
            "Total allocator work": "0.1405 to 0.1726",
            "Mean task latency": "27.02 to 31.22",
            "Mean within-mission p95": "65.90 to 73.13",
            "Mission duration": "117.78 to 142.18",
            "Call-count term": "+11.46",
            "Per-call-work term": "+20.61",
        },
    }
    for condition, expected_rows in expected_table2.items():
        for quantity, expected_display in expected_rows.items():
            row = table2.loc[table2.condition.eq(condition) & table2.quantity.eq(quantity)].iloc[0]
            if pd.notna(row.eager_mean):
                observed_display = f"{row.display_eager} to {row.display_policy}"
            else:
                observed_display = f"{row.mean_difference:+.2f}"
            add_table_check(
                "Table II", f"{condition}: {quantity}", observed_display,
                expected_display, observed_display == expected_display,
                "Compared with main.tex lines 213-222",
            )
    write_csv(pd.DataFrame(table_checks), CHECKS / "table_data_audit.csv")

    validation = {
        "agx_causal_rows": int(pd.read_csv(SOURCE / "agx_causal_trial_level.csv").shape[0]),
        "agx_zero_compute_rows": int(pd.read_csv(SOURCE / "agx_zero_compute_trial_level.csv").shape[0]),
        "rp2040_successful_rows": int(pd.read_csv(SOURCE / "rp2040_trial_level.csv").shape[0]),
        "completion_record_rows": int(pd.read_csv(SOURCE / "completion_records.csv").shape[0]),
        "agx_policy_pair_rows": int(pd.read_csv(DERIVED / "agx_policy_pairs.csv").shape[0]),
        "agx_effect_rows": int(effects.shape[0]),
        "figure2_rows": int(fig2.shape[0]),
        "figure3_rows": int(fig3.shape[0]),
        "all_checks_pass": bool(
            (pd.DataFrame(figure_checks).status.eq("PASS").all())
            and (pd.DataFrame(table_checks).status.eq("PASS").all())
        ),
    }
    (CHECKS / "data_build_validation.json").write_text(
        json.dumps(validation, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refresh-source-data",
        action="store_true",
        help="Re-extract package inputs from the authoritative repository handoff.",
    )
    args = parser.parse_args()
    for directory in [SOURCE, DERIVED, TABLES, FIGSRC, CHECKS, PROVENANCE]:
        directory.mkdir(parents=True, exist_ok=True)
    initialize_sources(force=args.refresh_source_data)
    build_outputs()
    print(f"Built compact data, tables, and figure sources in {PACKAGE}")


if __name__ == "__main__":
    main()
