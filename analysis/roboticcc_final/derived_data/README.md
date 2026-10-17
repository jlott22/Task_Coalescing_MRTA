# Derived-data definitions

All differences are policy minus Eager. All continuous AGX comparisons pair on `algorithm`, `arrival_load`, and `trace_id`, verify the shared scenario/release identity upstream, and use rows for which both policies completed. Incomplete missions remain in the source and completion files but do not contribute partial continuous endpoints.

The manuscript percentage is the ratio of paired-cohort means:

```text
100 * (mean(policy on common completed traces) / mean(Eager on those traces) - 1)
```

It is not the mean of within-trace percentages. `mean_difference` is the mean of paired absolute differences. `median_paired_pct` is the median of per-trace percentages. AGX intervals are pointwise 95% percentile intervals from 10,000 shared trace-bootstrap draws, seed 20260912. The validated interval rows are copied from the final corrected handoff; the package rebuild checks and reshapes them but does not substitute a new estimator.

| File | Source and filter | Pairing/formula and incomplete-trial treatment |
| --- | --- | --- |
| `agx_policy_pairs.csv` | `source_data/agx_causal_trial_level.csv`; each non-Eager policy | Eager joined on allocator/load/trace. Contains all 2,400 planned pairs and raw status columns. Differences and trace percentages are blank where an endpoint is unavailable. |
| `all_policy_effects.csv` | `source_data/agx_effects_validated.csv`; all rows | Final 528 endpoint records (48 comparisons x 11 endpoints). Continuous values use common completers; planned/completed denominators are explicit. |
| `all_policy_effects_summary.csv` | `all_policy_effects.csv` | One row per allocator/load/treatment (48 rows), with endpoint fields widened for plotting and filtering. |
| `anchor_examples.csv` | `all_policy_effects.csv`; HIPC/high/Bounded and CBAA/high/Count-b4 | Final complete 50-pair anchor endpoints used in Table II and Results. |
| `anchor_rounds.csv` | final handoff round summary | Round 1 uses traces 0000-0024; Round 2 uses 0025-0049. The rounds partition the evidence and are not an independent holdout. |
| `low_load_count4.csv` | final handoff low-load table | Four allocator comparisons, 50 complete pairs each. Includes online latency, admission wait, post-admission time, first-40 checks, and arithmetic wait shares. |
| `mechanism_decomposition.csv` | `source_data/mechanism_decomposition_pairs.csv`; two anchors | For each trace, `W=N*c`. The symmetric identity is `delta W = delta N*(cP+cE)/2 + delta c*(NP+NE)/2`. Contributions are averaged, with the shared trace bootstrap. This is accounting, not causal mediation. |
| `hipc_medium_cross_platform.csv` | `source_data/platform_policy_pairs.csv`; HIPC/medium, providers AGX and RP2040, both policies complete | Eight rows: four traces on each platform. Pairs are same-platform Eager/Count-b4; platform-to-platform ratios are not computed. |
| `hardware_platform_summary.csv` | final handoff hardware summary | Descriptive paired-cohort means and direction counts. No confidence interval is inferred from the four-trace census. |
| `completion_summary.csv` | `source_data/completion_records.csv` | Provider totals and provider/allocator/load/policy breakdown. Scopes are labeled and must not be summed together. |
| `zero_compute_anchor_checks.csv` | `source_data/agx_zero_compute_trial_level.csv`; the two high-load anchors | Eager and treatment are joined by trace; all 50 pairs complete. Reports call-count means and paired mean difference. |
| `generality_anchor_metrics.csv` | final architecture generality audit | Descriptive normalizations, first-40 task checks, zero-compute checks, and scope diagnostics. These are sensitivity evidence, not replacement production results. |

Work is summed measured duration of valid allocator transactions, including whole dispatched transactions whose virtual completion can extend beyond final task completion. Work/call is calculated within each mission before averaging. Latency is release-to-completion; the all-task mean uses 50 tasks and the online mean uses 42. Per-mission p95 uses nearest rank (48th of 50).

