#!/usr/bin/env python3
"""Build the manuscript claim map and quantitative number audit.

The final Overleaf manuscript is treated as the reporting source of truth.  Each
row below corresponds to a quantitative result in the Abstract, Results and
Discussion, Conclusion, a paper table, or a numerical figure caption.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PACKAGE = Path(__file__).resolve().parents[1]
DERIVED = PACKAGE / "derived_data"
TABLES = PACKAGE / "tables"
CHECKS = PACKAGE / "checks"


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(path, index=False, float_format="%.15g", lineterminator="\n")


effects = pd.read_csv(DERIVED / "all_policy_effects.csv")
summary = pd.read_csv(DERIVED / "all_policy_effects_summary.csv")
low = pd.read_csv(DERIVED / "low_load_count4.csv")
hardware = pd.read_csv(DERIVED / "hardware_platform_summary.csv")
mechanism = pd.read_csv(DERIVED / "mechanism_decomposition.csv")
rounds = pd.read_csv(DERIVED / "anchor_rounds.csv")
completion = pd.read_csv(DERIVED / "completion_summary.csv")
zero = pd.read_csv(DERIVED / "zero_compute_anchor_checks.csv")
generality = pd.read_csv(DERIVED / "generality_anchor_metrics.csv")
table1 = pd.read_csv(TABLES / "table1_experiment_design.csv")
table2 = pd.read_csv(TABLES / "table2_anchor_mechanisms.csv")


def effect(algorithm: str, load: str, policy: str, metric: str) -> pd.Series:
    rows = effects.loc[
        effects.algorithm.eq(algorithm)
        & effects.arrival_load.eq(load)
        & effects.policy_id.eq(policy)
        & effects.metric.eq(metric)
    ]
    if len(rows) != 1:
        raise ValueError((algorithm, load, policy, metric, len(rows)))
    return rows.iloc[0]


def hw(provider: str, algorithm: str, load: str) -> pd.Series:
    rows = hardware.loc[
        hardware.provider.eq(provider)
        & hardware.algorithm.eq(algorithm)
        & hardware.arrival_load.eq(load)
    ]
    if len(rows) != 1:
        raise ValueError((provider, algorithm, load, len(rows)))
    return rows.iloc[0]


claims: list[dict[str, object]] = []


def add(
    claim_id: str,
    section: str,
    line: str,
    description: str,
    *,
    algorithm: str = "ALL",
    arrival_load: str = "ALL",
    policy: str = "ALL",
    reference: str = "",
    provider: str = "mixed",
    n_planned: object = "",
    n_used: object = "",
    metric: str,
    reported: str,
    units: str,
    scope: str,
    source_file: str,
    source_filter: str,
    source_value: str,
    status: str,
    notes: str = "",
) -> None:
    claims.append(
        {
            "claim_id": claim_id,
            "manuscript_section": section,
            "manuscript_line": line,
            "claim_text_or_short_description": description,
            "algorithm": algorithm,
            "arrival_load": arrival_load,
            "policy": policy,
            "reference_policy": reference,
            "timing_provider": provider,
            "n_planned": n_planned,
            "n_used": n_used,
            "metric": metric,
            "reported_value": reported,
            "reported_units": units,
            "uncertainty_or_scope": scope,
            "source_file": source_file,
            "source_filter_or_rows": source_filter,
            "derivation_script": "provenance/build_package.py",
            "notes": notes,
            "source_value_full_precision_or_basis": source_value,
            "audit_status": status,
        }
    )


# Abstract.
add(
    "ABS-01", "Abstract", "33", "Campaign sizes and retained hardware completions",
    metric="mission coverage", reported="3000 causal AGX; 3000 zero-compute; 96 HIL planned; 82 HIL successful",
    units="missions", scope="AGX counts are planned/retained runs; causal completion is 2940/3000",
    source_file="derived_data/completion_summary.csv", source_filter="scope=provider_total",
    source_value="agx_causal 3000/2940/60; agx_zero_compute 3000/3000/0; rp2040 96/82/14",
    status="MATCH", notes="The Abstract's 3000 causal missions is a design count, not a completion count.",
)
r_work = effect("HIPC", "high", "bounded_b4_w10", "work_s")
r_lat = effect("HIPC", "high", "bounded_b4_w10", "mean_release_to_completion_latency_s")
add(
    "ABS-02", "Abstract", "33", "HIPC high-load Bounded work and latency effect",
    algorithm="HIPC", arrival_load="high", policy="bounded_b4_w10", reference="eager_b1", provider="agx_causal",
    n_planned=50, n_used=50, metric="work_s; mean_release_to_completion_latency_s",
    reported="-19.35%; +1.40", units="%; s", scope="ratio of paired-cohort means; paired mean latency difference",
    source_file="derived_data/anchor_examples.csv", source_filter="algorithm=HIPC,arrival_load=high,policy_id=bounded_b4_w10",
    source_value=f"{r_work.ratio_of_paired_means_pct:.12g}%; {r_lat.mean_difference:.12g} s", status="ROUNDING_ONLY",
)
r_cbaa_work = effect("CBAA", "high", "count_b4", "work_s")
r_cbaa_epoch = effect("CBAA", "high", "count_b4", "allocation_epoch_count")
add(
    "ABS-03", "Abstract", "33", "CBAA high-load Count-b4 work increase despite fewer epochs",
    algorithm="CBAA", arrival_load="high", policy="count_b4", reference="eager_b1", provider="agx_causal",
    n_planned=50, n_used=50, metric="work_s; allocation_epoch_count", reported="+22.82%; 43 to 12", units="%; epochs",
    scope="ratio of paired-cohort means; paired-cohort means", source_file="derived_data/anchor_examples.csv",
    source_filter="algorithm=CBAA,arrival_load=high,policy_id=count_b4",
    source_value=f"{r_cbaa_work.ratio_of_paired_means_pct:.12g}%; {r_cbaa_epoch.eager_mean:.12g} to {r_cbaa_epoch.policy_mean:.12g}",
    status="ROUNDING_ONLY",
)
hwm = hw("rp2040", "HIPC", "medium")
add(
    "ABS-04", "Abstract", "33", "RP2040 HIPC medium-load aggregate and direction count",
    algorithm="HIPC", arrival_load="medium", policy="count_b4", reference="eager_b1", provider="rp2040",
    n_planned=4, n_used=4, metric="work_s; mean latency; mission duration; joint direction",
    reported="-59.85%; -39.47%; -15.46%; 3 of 4 improve all three", units="%; traces",
    scope="descriptive four-trace matched cohort; no inferential interval",
    source_file="derived_data/hardware_platform_summary.csv", source_filter="provider=rp2040,algorithm=HIPC,arrival_load=medium",
    source_value=(f"{hwm.work_s_ratio_of_paired_cohort_means_pct:.12g}%; "
                  f"{hwm.mean_release_to_completion_latency_s_ratio_of_paired_cohort_means_pct:.12g}%; "
                  f"{hwm.mission_elapsed_time_s_ratio_of_paired_cohort_means_pct:.12g}%; "
                  f"{int(hwm.work_and_mean_latency_both_lower_traces)} work+latency lower; mission checked tracewise"),
    status="ROUNDING_ONLY", notes="Hardware outcome is descriptive for the tested platform/runtime conditions.",
)
hagx = hw("agx", "HIPC", "medium")
add(
    "ABS-05", "Abstract", "33", "Same-four AGX HIPC medium-load latency response",
    algorithm="HIPC", arrival_load="medium", policy="count_b4", reference="eager_b1", provider="agx_causal",
    n_planned=4, n_used=4, metric="mean_release_to_completion_latency_s", reported="+27.69", units="%",
    scope="descriptive same-four-scenario paired-cohort mean ratio", source_file="derived_data/hardware_platform_summary.csv",
    source_filter="provider=agx,algorithm=HIPC,arrival_load=medium",
    source_value=f"{hagx.mean_release_to_completion_latency_s_ratio_of_paired_cohort_means_pct:.12g}%", status="ROUNDING_ONLY",
)

# Results: regime-level summaries.
call_col = "allocator_call_count__ratio_of_paired_means_pct"
work_col = "work_s__ratio_of_paired_means_pct"
lat_col = "mean_release_to_completion_latency_s__ratio_of_paired_means_pct"
epoch_col = "allocation_epoch_count__ratio_of_paired_means_pct"
count_30 = int(((summary[call_col] < 0) & (summary[work_col] < 0) & (summary[lat_col] > 0)).sum())
count_11 = int(((summary[epoch_col] < 0) & (summary[call_col] > 0) & (summary[work_col] > 0)).sum())
add(
    "RES-01", "Results and Discussion - Regimes", "190", "Matrix completion and observed direction counts",
    metric="comparison count; directional pattern", reported="48 comparisons; 42 with 50 pairs; 6 incomplete; 30 lower calls/work with higher latency; 11 higher calls/work despite fewer epochs",
    units="comparisons", scope="direction of observed paired-cohort means, not independent significance tests",
    source_file="derived_data/all_policy_effects_summary.csv", source_filter="all 48 algorithm/load/policy rows",
    source_value=f"48; {int(summary.complete_50_pairs.sum())}; {int((~summary.complete_50_pairs).sum())}; {count_30}; {count_11}", status="MATCH",
)
low_penalties = low["online_mean_s__mean_difference"]
low_shares = low["admission_wait_share_of_mean_online_latency_difference_pct"]
first40_wait = low["first40_online_wait_mean_s__policy_mean"].mean()
add(
    "RES-02", "Results and Discussion - Regimes", "192", "Low-load Count-b4 waiting penalty across allocators",
    arrival_load="low", policy="count_b4", reference="eager_b1", provider="agx_causal", n_planned=50, n_used=50,
    metric="online_mean_s; admission wait share; first40_online_wait_mean_s",
    reported="+20.08 to +23.57 s; 50/50 higher for each allocator; 83.3-96.7%; expected 20 s; observed first-40 wait 19.51 s",
    units="s; traces; %", scope="50 complete pairs per allocator; expected wait=(b-1)/(2 lambda)",
    source_file="derived_data/low_load_count4.csv", source_filter="all four rows",
    source_value=(f"{low_penalties.min():.12g} to {low_penalties.max():.12g} s; all n_higher=50; "
                  f"{low_shares.min():.12g} to {low_shares.max():.12g}%; expected 20; {first40_wait:.12g} s"),
    status="ROUNDING_ONLY",
)
low_cbaa = effect("CBAA", "low", "count_b4", "work_s")
add(
    "RES-03", "Results and Discussion - Regimes", "192", "CBAA Count-b4 work reverses between low and high load",
    algorithm="CBAA", arrival_load="low; high", policy="count_b4", reference="eager_b1", provider="agx_causal",
    n_planned=50, n_used=50, metric="work_s", reported="-29.39% at low; +22.82% at high", units="%",
    scope="ratio of paired-cohort means", source_file="derived_data/all_policy_effects.csv",
    source_filter="algorithm=CBAA,policy_id=count_b4,metric=work_s,arrival_load in (low,high)",
    source_value=f"{low_cbaa.ratio_of_paired_means_pct:.12g}%; {r_cbaa_work.ratio_of_paired_means_pct:.12g}%", status="ROUNDING_ONLY",
)
hipc_low_count = low.loc[low.algorithm.eq("HIPC")].iloc[0]
hipc_low_bounded = effect("HIPC", "low", "bounded_b4_w10", "online_mean_s")
wait_effects = pd.read_csv(PACKAGE / "source_data" / "online_wait_effects_validated.csv")
bounded_wait = wait_effects.loc[
    wait_effects.algorithm.eq("HIPC") & wait_effects.arrival_load.eq("low")
    & wait_effects.policy_id.eq("bounded_b4_w10") & wait_effects.metric.eq("online_wait_mean_s")
].iloc[0]
add(
    "RES-04", "Results and Discussion - Regimes", "194", "Low-load HIPC deadline comparison",
    algorithm="HIPC", arrival_load="low", policy="count_b4; bounded_b4_w10", reference="eager_b1", provider="agx_causal",
    n_planned=50, n_used=50, metric="online_mean_s; online_wait_mean_s",
    reported="latency 14.18 (Eager), 34.26 (Count), 21.36 (Bounded); wait 19.41 (Count) to 7.58 (Bounded)", units="s",
    scope="paired-cohort means; 42 online tasks per completed mission", source_file="derived_data/all_policy_effects.csv; source_data/online_wait_effects_validated.csv",
    source_filter="algorithm=HIPC,arrival_load=low,policies eager/count_b4/bounded_b4_w10",
    source_value=(f"{hipc_low_count['online_mean_s__eager_mean']:.12g}; {hipc_low_count['online_mean_s__policy_mean']:.12g}; "
                  f"{hipc_low_bounded.policy_mean:.12g}; {hipc_low_count['online_wait_mean_s__policy_mean']:.12g}; {bounded_wait.policy_mean:.12g}"),
    status="ROUNDING_ONLY",
)
bounded = summary.loc[summary.policy_id.eq("bounded_b4_w10")]
add(
    "RES-05", "Results and Discussion - Regimes", "196", "Bounded direction counts and incomplete ACBBA/high cohort",
    policy="bounded_b4_w10", reference="eager_b1", provider="agx_causal", n_planned=50,
    metric="work_s; mean_release_to_completion_latency_s; common pairs", reported="work lower 10/12; latency higher 12/12; ACBBA/high n=30; other nine work-lowering cells n=50",
    units="conditions; pairs", scope="observed means; incomplete comparison is common-completer conditional",
    source_file="derived_data/all_policy_effects_summary.csv", source_filter="policy_id=bounded_b4_w10",
    source_value=(f"{int((bounded[work_col] < 0).sum())}/12; {int((bounded[lat_col] > 0).sum())}/12; "
                  f"ACBBA/high n={int(bounded.loc[bounded.algorithm.eq('ACBBA') & bounded.arrival_load.eq('high'),'common_completed_pairs'].iloc[0])}"),
    status="MATCH",
)
pi_work = effect("PI", "medium", "bounded_b4_w10", "work_s")
pi_lat = effect("PI", "medium", "bounded_b4_w10", "mean_release_to_completion_latency_s")
add(
    "RES-06", "Results and Discussion - Regimes", "196", "PI medium-load Bounded adverse cell",
    algorithm="PI", arrival_load="medium", policy="bounded_b4_w10", reference="eager_b1", provider="agx_causal", n_planned=50, n_used=50,
    metric="work_s; mean_release_to_completion_latency_s", reported="+11.37%; +22.35%", units="%",
    scope="ratios of paired-cohort means", source_file="derived_data/all_policy_effects.csv",
    source_filter="algorithm=PI,arrival_load=medium,policy_id=bounded_b4_w10",
    source_value=f"{pi_work.ratio_of_paired_means_pct:.12g}%; {pi_lat.ratio_of_paired_means_pct:.12g}%", status="ROUNDING_ONLY",
)
count8_work = effect("HIPC", "high", "count_b8", "work_s")
count8_lat = effect("HIPC", "high", "count_b8", "mean_release_to_completion_latency_s")
count8_mission = effect("HIPC", "high", "count_b8", "mission_elapsed_time_s")
add(
    "RES-07", "Results and Discussion - Regimes", "196", "HIPC high-load Count-b8 versus Bounded tradeoff",
    algorithm="HIPC", arrival_load="high", policy="count_b8; bounded_b4_w10", reference="eager_b1", provider="agx_causal", n_planned=50, n_used=50,
    metric="work_s; mean latency; mission duration", reported="Count-b8 -25.32% work, +20.93% latency, +14.58% mission; Bounded -19.35% work, +4.34% latency",
    units="%", scope="ratios of paired-cohort means", source_file="derived_data/all_policy_effects.csv",
    source_filter="algorithm=HIPC,arrival_load=high,policy_id in (count_b8,bounded_b4_w10)",
    source_value=(f"{count8_work.ratio_of_paired_means_pct:.12g}; {count8_lat.ratio_of_paired_means_pct:.12g}; "
                  f"{count8_mission.ratio_of_paired_means_pct:.12g}; {r_work.ratio_of_paired_means_pct:.12g}; {r_lat.ratio_of_paired_means_pct:.12g}"),
    status="ROUNDING_ONLY",
)

# Detailed mechanism paragraphs.
decomp_h = mechanism.loc[mechanism.algorithm.eq("HIPC")].iloc[0]
round_h = rounds.loc[rounds.algorithm.eq("HIPC") & rounds.metric.eq("work_s")]
add(
    "RES-08", "Results and Discussion - Mechanism", "200", "HIPC work-saving mechanism and round consistency",
    algorithm="HIPC", arrival_load="high", policy="bounded_b4_w10", reference="eager_b1", provider="agx_causal", n_planned=50, n_used=50,
    metric="work_s; allocator_call_count; work_per_call_s; decomposition", reported="1.678 to 1.353; -19.35% [9.40,27.66] reduction; 38/50 lower; calls -17.27%; call term 84.5%; work/call -4.03% with CI spanning 0; rounds -18.72%/-19.96%",
    units="processor-s; %; traces", scope="pointwise 95% bootstrap intervals; rounds partition the same 50 traces",
    source_file="derived_data/anchor_examples.csv; derived_data/mechanism_decomposition.csv; derived_data/anchor_rounds.csv",
    source_filter="HIPC/high/Bounded anchor",
    source_value=(f"{r_work.eager_mean:.12g}->{r_work.policy_mean:.12g}; {r_work.ratio_of_paired_means_pct:.12g} "
                  f"[{r_work.ratio_of_paired_means_pct_ci_low:.12g},{r_work.ratio_of_paired_means_pct_ci_high:.12g}]; "
                  f"n_lower={int(r_work.n_lower)}; calls={effect('HIPC','high','bounded_b4_w10','allocator_call_count').ratio_of_paired_means_pct:.12g}; "
                  f"share={decomp_h.calls_share_of_mean_work_difference_pct:.12g}; rounds={';'.join(f'{x:.12g}' for x in round_h.ratio_of_paired_means_pct)}"),
    status="ROUNDING_ONLY",
)
r_online = effect("HIPC", "high", "bounded_b4_w10", "online_mean_s")
r_p95 = effect("HIPC", "high", "bounded_b4_w10", "p95_release_to_completion_latency_s")
r_mission = effect("HIPC", "high", "bounded_b4_w10", "mission_elapsed_time_s")
add(
    "RES-09", "Results and Discussion - Mechanism", "229", "HIPC latency, p95, and mission changes",
    algorithm="HIPC", arrival_load="high", policy="bounded_b4_w10", reference="eager_b1", provider="agx_causal", n_planned=50, n_used=50,
    metric="mean latency; online mean; p95 latency; mission duration", reported="+1.40 s [-0.21,+3.15]; +1.57 s online; +0.31 s p95; -1.55 s mission; p95 and mission CIs span zero",
    units="s", scope="paired mean differences; pointwise 95% intervals", source_file="derived_data/anchor_examples.csv",
    source_filter="HIPC/high/Bounded latency and mission rows",
    source_value=(f"{r_lat.mean_difference:.12g} [{r_lat.mean_difference_ci_low:.12g},{r_lat.mean_difference_ci_high:.12g}]; "
                  f"{r_online.mean_difference:.12g}; {r_p95.mean_difference:.12g}; {r_mission.mean_difference:.12g}"),
    status="ROUNDING_ONLY",
)
c_calls = effect("CBAA", "high", "count_b4", "allocator_call_count")
c_per = effect("CBAA", "high", "count_b4", "work_per_call_s")
decomp_c = mechanism.loc[mechanism.algorithm.eq("CBAA")].iloc[0]
add(
    "RES-10", "Results and Discussion - Mechanism", "231", "CBAA work increase and decomposition",
    algorithm="CBAA", arrival_load="high", policy="count_b4", reference="eager_b1", provider="agx_causal", n_planned=50, n_used=50,
    metric="allocator calls; work/call; work; decomposition", reported="+7.43%; +14.20%; +22.82% [15.13,30.91]; 42/50 higher; 35.7% calls term; 64.3% per-call term",
    units="%; traces", scope="ratio of paired-cohort means; pointwise 95% interval; exact symmetric accounting decomposition",
    source_file="derived_data/anchor_examples.csv; derived_data/mechanism_decomposition.csv", source_filter="CBAA/high/Count-b4 anchor",
    source_value=(f"{c_calls.ratio_of_paired_means_pct:.12g}; {c_per.ratio_of_paired_means_pct:.12g}; "
                  f"{r_cbaa_work.ratio_of_paired_means_pct:.12g} [{r_cbaa_work.ratio_of_paired_means_pct_ci_low:.12g},{r_cbaa_work.ratio_of_paired_means_pct_ci_high:.12g}]; "
                  f"n_higher={int(r_cbaa_work.n_higher)}; {decomp_c.calls_share_of_mean_work_difference_pct:.12g}/{decomp_c.per_call_share_of_mean_work_difference_pct:.12g}"),
    status="ROUNDING_ONLY",
)
c_mission = effect("CBAA", "high", "count_b4", "mission_elapsed_time_s")
c_latency = effect("CBAA", "high", "count_b4", "mean_release_to_completion_latency_s")
c_steps = effect("CBAA", "high", "count_b4", "total_team_steps")
intensity = generality.loc[
    generality.comparison.eq("agx_cbaa_high_b4") & generality.metric.eq("work_s_per_mission_s")
].iloc[0]
add(
    "RES-11", "Results and Discussion - Mechanism", "233", "CBAA absolute work, mission, latency, steps, and normalized intensity",
    algorithm="CBAA", arrival_load="high", policy="count_b4", reference="eager_b1", provider="agx_causal", n_planned=50, n_used=50,
    metric="work_s; mission duration; mean latency; total_team_steps; work/mission-s",
    reported="+0.0321 processor-s; +24.39 s mission; +4.21 s latency; +11.24% team steps; +1.50% work per mission second",
    units="processor-s; s; %", scope="team travel means completed grid traversals, not physical distance or energy",
    source_file="derived_data/anchor_examples.csv; derived_data/generality_anchor_metrics.csv",
    source_filter="CBAA/high/Count-b4",
    source_value=(f"{r_cbaa_work.mean_difference:.12g}; {c_mission.mean_difference:.12g}; {c_latency.mean_difference:.12g}; "
                  f"{c_steps.ratio_of_paired_means_pct:.12g}; {intensity.ratio_of_paired_means_pct:.12g}"),
    status="ROUNDING_ONLY", notes="Manuscript's 'team travel' is the total_team_steps endpoint.",
)

# Hardware results.
add(
    "RES-12", "Results and Discussion - Embedded Execution", "237", "Hardware pair coverage and primary matched subset",
    algorithm="ALL; HIPC", arrival_load="ALL; medium", policy="count_b4", reference="eager_b1", provider="rp2040",
    n_planned=48, n_used=38, metric="completed policy pairs", reported="38 complete pairs of 48 planned blocks; four HIPC/medium pairs complete on both platforms",
    units="paired blocks", scope="hardware summaries are descriptive", source_file="source_data/platform_policy_pairs.csv",
    source_filter="provider=rp2040 for 48 blocks; HIPC/medium for primary subset", source_value="38/48; HIPC/medium 4/4", status="MATCH",
)
add(
    "RES-13", "Results and Discussion - Embedded Execution", "247", "RP2040 HIPC medium-load work, calls, per-call work, latency, mission, and directions",
    algorithm="HIPC", arrival_load="medium", policy="count_b4", reference="eager_b1", provider="rp2040", n_planned=4, n_used=4,
    metric="work; calls; work/call; mean latency; mission duration", reported="work 353.31 to 141.85 (-59.85%); calls -9.93%; work/call 437.10 to 194.12 ms (-55.59%); latency 62.39 to 37.76 (-39.47%); mission 238.47 to 201.60 (-15.46%); 3/4 improve all; trace 0001 adverse",
    units="processor-s; %; ms; s; traces", scope="descriptive same-board/runtime pairs",
    source_file="derived_data/hardware_platform_summary.csv; figures/source/fig3_hipc_medium_hardware.csv",
    source_filter="provider=rp2040,algorithm=HIPC,arrival_load=medium",
    source_value=(f"{hwm.work_s_eager_mean:.12g}->{hwm.work_s_count4_mean:.12g} ({hwm.work_s_ratio_of_paired_cohort_means_pct:.12g}); "
                  f"calls {hwm.allocator_call_count_ratio_of_paired_cohort_means_pct:.12g}; "
                  f"per-call {1000*hwm.work_per_call_s_eager_mean:.12g}->{1000*hwm.work_per_call_s_count4_mean:.12g} ({hwm.work_per_call_s_ratio_of_paired_cohort_means_pct:.12g}); "
                  f"latency {hwm.mean_release_to_completion_latency_s_eager_mean:.12g}->{hwm.mean_release_to_completion_latency_s_count4_mean:.12g}; "
                  f"mission {hwm.mission_elapsed_time_s_eager_mean:.12g}->{hwm.mission_elapsed_time_s_count4_mean:.12g}"),
    status="ROUNDING_ONLY", notes="Do not interpret this as an isolated processor-speed effect.",
)
add(
    "RES-14", "Results and Discussion - Embedded Execution", "249", "Same-four AGX HIPC medium-load response",
    algorithm="HIPC", arrival_load="medium", policy="count_b4", reference="eager_b1", provider="agx_causal", n_planned=4, n_used=4,
    metric="work; mean latency; mission duration; latency direction", reported="work 1.101 to 1.015 (-7.79%); latency +27.69%; mission +14.22%; latency higher 4/4",
    units="processor-s; %; traces", scope="descriptive same four scenario identities",
    source_file="derived_data/hardware_platform_summary.csv; figures/source/fig3_hipc_medium_hardware.csv",
    source_filter="provider=agx,algorithm=HIPC,arrival_load=medium",
    source_value=(f"{hagx.work_s_eager_mean:.12g}->{hagx.work_s_count4_mean:.12g} ({hagx.work_s_ratio_of_paired_cohort_means_pct:.12g}); "
                  f"latency {hagx.mean_release_to_completion_latency_s_ratio_of_paired_cohort_means_pct:.12g}; "
                  f"mission {hagx.mission_elapsed_time_s_ratio_of_paired_cohort_means_pct:.12g}; higher={int(hagx.mean_release_to_completion_latency_s_higher_traces)}"),
    status="ROUNDING_ONLY", notes="Compared platforms also differ in runtime and message timing.",
)
hh = hw("rp2040", "HIPC", "high")
ph = hw("rp2040", "PI", "high")
add(
    "RES-15", "Results and Discussion - Embedded Execution", "251", "High-load RP2040 counterexamples",
    algorithm="HIPC; PI", arrival_load="high", policy="count_b4", reference="eager_b1", provider="rp2040",
    n_planned="4 each", n_used="HIPC 4; PI 3", metric="work; latency; mission; completion",
    reported="HIPC work +7.39%, mission +4.61%, both higher on 3 traces; PI work -18.67%, latency -12.34%, all 3 save work, 2 improve latency and mission; fourth Count trial failed",
    units="%; traces", scope="descriptive hardware subsets; PI is incomplete because of a retained technical failure",
    source_file="derived_data/hardware_platform_summary.csv; source_data/rp2040_terminal_failures.csv",
    source_filter="provider=rp2040,arrival_load=high,algorithm in (HIPC,PI)",
    source_value=(f"HIPC {hh.work_s_ratio_of_paired_cohort_means_pct:.12g}/{hh.mission_elapsed_time_s_ratio_of_paired_cohort_means_pct:.12g}; "
                  f"PI {ph.work_s_ratio_of_paired_cohort_means_pct:.12g}/{ph.mean_release_to_completion_latency_s_ratio_of_paired_cohort_means_pct:.12g}; n={int(ph.common_completed_pairs)}"),
    status="ROUNDING_ONLY",
)

# Generality/sensitivity.
z_h = zero.loc[zero.algorithm.eq("HIPC")].iloc[0]
z_c = zero.loc[zero.algorithm.eq("CBAA")].iloc[0]
add(
    "RES-16", "Results and Discussion - Generality", "255", "Zero-compute call-count directions and recovery checks",
    algorithm="HIPC; CBAA", arrival_load="high", policy="bounded_b4_w10; count_b4", reference="eager_b1", provider="agx_zero_compute",
    n_planned=50, n_used=50, metric="allocator_call_count; recovery_attempt_count; replay equality",
    reported="HIPC 992.74 to 859.78; CBAA 456.40 to 486.46; no causal recovery attempts; eight recovery-disabled replay pairs match",
    units="calls; pairs", scope="descriptive sensitivity check; local replays are not new production measurements",
    source_file="derived_data/zero_compute_anchor_checks.csv; source_data/recovery_disabled_replays.csv; derived_data/generality_anchor_metrics.csv",
    source_filter="two high-load anchors",
    source_value=(f"HIPC {z_h.eager_mean_allocator_calls:.12g}->{z_h.policy_mean_allocator_calls:.12g}; "
                  f"CBAA {z_c.eager_mean_allocator_calls:.12g}->{z_c.policy_mean_allocator_calls:.12g}; 8 paired replay rows"),
    status="MATCH",
)
first40 = generality.loc[
    generality.comparison.eq("agx_cbaa_high_b4")
    & generality.metric.eq("release_to_completion_s_first40_online")
].iloc[0]
add(
    "RES-17", "Results and Discussion - Generality", "257", "CBAA high-load first-40 online-task sensitivity",
    algorithm="CBAA", arrival_load="high", policy="count_b4", reference="eager_b1", provider="agx_causal", n_planned=50, n_used=50,
    metric="release_to_completion_s_first40_online", reported="27.23 to 30.43", units="s",
    scope="first 40 online tasks only; execution and recorded mission work unchanged",
    source_file="derived_data/generality_anchor_metrics.csv", source_filter="comparison=agx_cbaa_high_b4,metric=release_to_completion_s_first40_online",
    source_value=f"{first40.eager_mean:.12g} to {first40.policy_mean:.12g}", status="ROUNDING_ONLY",
)
add(
    "RES-18", "Results and Discussion - Generality", "261", "Incomplete AGX comparison scope and headline completeness",
    metric="completion cohort", reported="six AGX contrasts omit noncompleted pairs; principal HIPC and CBAA anchors retain all 50",
    units="comparisons; pairs", scope="continuous estimates for incomplete cells are common-completer conditional",
    source_file="derived_data/all_policy_effects_summary.csv", source_filter="complete_50_pairs=false; two anchor filters",
    source_value=f"incomplete={int((~summary.complete_50_pairs).sum())}; anchor n=50,50", status="MATCH",
)

# Table I.
for index, row in table1.iterrows():
    add(
        f"TAB1-{index+1:02d}", "Table I", "127-129", f"{row.campaign} retained coverage",
        provider=str(row.timing_provider), n_planned=int(row.planned_missions), n_used=int(row.complete_or_successful),
        metric="policies; traces; planned; complete; other",
        reported=f"{int(row.policies)} policies; {int(row.traces_per_condition)} traces; {int(row.planned_missions)} planned; {int(row.complete_or_successful)} complete; {int(row.other_outcomes)} other",
        units="counts", scope=str(row.other_outcome_definition), source_file="tables/table1_experiment_design.csv",
        source_filter=f"campaign={row.campaign}", source_value="exact table row", status="MATCH",
    )

# Table II: one row per quantitative table cell pair/term.
for index, row in table2.reset_index(drop=True).iterrows():
    if pd.notna(row.eager_mean):
        reported = f"{row.display_eager} to {row.display_policy}"
        source_value = f"{row.eager_mean:.15g} to {row.policy_mean:.15g}"
    else:
        reported = f"{row.mean_difference:+.2f}"
        source_value = f"{row.mean_difference:.15g}"
    add(
        f"TAB2-{index+1:02d}", "Table II", "213-222", f"{row.condition}: {row.quantity}",
        algorithm=str(row.algorithm), arrival_load="high", policy=str(row.policy_id), reference="eager_b1", provider="agx_causal",
        n_planned=50, n_used=int(row.n_pairs), metric=str(row.metric), reported=reported, units=str(row.units),
        scope="means over complete paired scenarios; decomposition terms are arithmetic contributions",
        source_file="tables/table2_anchor_mechanisms.csv", source_filter=f"condition={row.condition},quantity={row.quantity}",
        source_value=source_value, status="ROUNDING_ONLY",
    )

# Figure caption/annotation quantities.
add(
    "FIG1-01", "Figure 1 caption", "96", "Four logical robots and one local virtual processor per logical robot",
    metric="logical robot count", reported="4", units="robots", scope="HIL board measures allocator transactions; motion remains simulated",
    source_file="provenance/paper_methods_fact_sheet.md", source_filter="Agents / Causal clock / RP2040 HIL rows",
    source_value="4", status="MATCH",
)
incomplete_rows = summary.loc[~summary.complete_50_pairs, ["algorithm", "arrival_load", "policy_id", "common_completed_pairs"]]
add(
    "FIG2-01", "Figure 2 caption and annotations", "184", "Pointwise interval and incomplete-cohort annotations",
    metric="interval level; common completed pairs", reported="95% pointwise; n=50 except ACBBA/high 33/32/27/30, ACBBA/medium Count-b8 48, HIPC/low Count-b8 49",
    units="%; pairs", scope="legend order Count-b2, Count-b4, Count-b8, Bounded",
    source_file="figures/source/fig2_coalescing_regimes.csv", source_filter="n_used<50",
    source_value="; ".join(f"{r.algorithm}/{r.arrival_load}/{r.policy_id} n={int(r.common_completed_pairs)}" for r in incomplete_rows.itertuples()),
    status="MATCH",
)
add(
    "FIG3-01", "Figure 3 caption", "243", "Four shared HIPC/medium traces shown individually on both platforms",
    algorithm="HIPC", arrival_load="medium", policy="count_b4", reference="eager_b1", provider="agx_causal; rp2040",
    n_planned=4, n_used=4, metric="trace coverage", reported="4 shared traces (0000-0003)", units="traces",
    scope="individual measured pairs; no uncertainty interval",
    source_file="figures/source/fig3_hipc_medium_hardware.csv", source_filter="all rows",
    source_value="trace_0000; trace_0001; trace_0002; trace_0003 on AGX and RP2040", status="MATCH",
)

# Conclusion duplicates are intentionally mapped to their final-paper locations.
add(
    "CON-01", "Conclusion", "265", "Conclusion repeats HIPC and CBAA high-load anchors",
    algorithm="HIPC; CBAA", arrival_load="high", policy="bounded_b4_w10; count_b4", reference="eager_b1", provider="agx_causal",
    n_planned=50, n_used=50, metric="work_s; mean latency; epochs",
    reported="HIPC -19.35% work with +1.40 s latency; CBAA +22.82% work with epochs 43 to 12",
    units="%; s; epochs", scope="same estimators as Abstract and Results",
    source_file="derived_data/anchor_examples.csv", source_filter="two high-load anchors",
    source_value=(f"HIPC {r_work.ratio_of_paired_means_pct:.12g}%/{r_lat.mean_difference:.12g}s; "
                  f"CBAA {r_cbaa_work.ratio_of_paired_means_pct:.12g}%/{r_cbaa_epoch.eager_mean:.12g}->{r_cbaa_epoch.policy_mean:.12g}"),
    status="ROUNDING_ONLY",
)
add(
    "CON-02", "Conclusion", "267", "Conclusion repeats RP2040 HIPC medium-load aggregate",
    algorithm="HIPC", arrival_load="medium", policy="count_b4", reference="eager_b1", provider="rp2040", n_planned=4, n_used=4,
    metric="work; mean latency; mission duration; joint directions",
    reported="-59.85% work; -39.47% latency; -15.46% mission; 3 scenarios improve all three",
    units="%; scenarios", scope="descriptive tested hardware subset",
    source_file="derived_data/hardware_platform_summary.csv", source_filter="provider=rp2040,algorithm=HIPC,arrival_load=medium",
    source_value=(f"{hwm.work_s_ratio_of_paired_cohort_means_pct:.12g}; "
                  f"{hwm.mean_release_to_completion_latency_s_ratio_of_paired_cohort_means_pct:.12g}; "
                  f"{hwm.mission_elapsed_time_s_ratio_of_paired_cohort_means_pct:.12g}; 3/4"),
    status="ROUNDING_ONLY", notes="Do not infer an isolated processor-speed causal effect.",
)
add(
    "CON-03", "Conclusion", "267", "Conclusion notes different same-four AGX latency direction",
    algorithm="HIPC", arrival_load="medium", policy="count_b4", reference="eager_b1", provider="agx_causal", n_planned=4, n_used=4,
    metric="mean latency direction", reported="higher mean task latency on AGX", units="direction",
    scope="same four scenario identities", source_file="derived_data/hardware_platform_summary.csv",
    source_filter="provider=agx,algorithm=HIPC,arrival_load=medium",
    source_value=f"+{hagx.mean_release_to_completion_latency_s_ratio_of_paired_cohort_means_pct:.12g}%; 4/4 higher", status="MATCH",
)


claim_frame = pd.DataFrame(claims)
required_columns = [
    "claim_id", "manuscript_section", "manuscript_line", "claim_text_or_short_description",
    "algorithm", "arrival_load", "policy", "reference_policy", "timing_provider",
    "n_planned", "n_used", "metric", "reported_value", "reported_units",
    "uncertainty_or_scope", "source_file", "source_filter_or_rows", "derivation_script", "notes",
]
write_csv(claim_frame[required_columns], PACKAGE / "CLAIM_SOURCE_MAP.csv")

audit = claim_frame[
    [
        "claim_id", "manuscript_section", "manuscript_line", "claim_text_or_short_description",
        "reported_value", "source_value_full_precision_or_basis", "audit_status",
        "source_file", "source_filter_or_rows", "notes",
    ]
].copy()
audit["genuine_discrepancy"] = audit.audit_status.eq("DISCREPANCY")
audit["ambiguous_derivation"] = audit.audit_status.eq("AMBIGUOUS")
write_csv(audit, CHECKS / "manuscript_number_audit.csv")

summary_rows = pd.DataFrame(
    [
        {"audit_status": status, "claim_rows": int((audit.audit_status == status).sum())}
        for status in sorted(audit.audit_status.unique())
    ]
)
write_csv(summary_rows, CHECKS / "manuscript_number_audit_summary.csv")
print(f"Wrote {len(claim_frame)} claim-map and manuscript-audit rows")
