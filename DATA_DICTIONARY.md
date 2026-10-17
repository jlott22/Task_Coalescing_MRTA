# Publication data dictionary

The paper's authoritative tables, figure inputs and compact source rows are under [`analysis/roboticcc_final/`](analysis/roboticcc_final/README.md). CSVs use comma delimiters and headers. A blank numeric field means unavailable, undefined or inapplicable, never zero. This page defines the paper-facing fields; the [source-data guide](analysis/roboticcc_final/source_data/README.md) and [derived-data guide](analysis/roboticcc_final/derived_data/README.md) give file-specific filters and formulas.

## Keys and cohorts

| Field | Meaning |
| --- | --- |
| `algorithm` | Allocator: CBAA, ACBBA, PI or HIPC. |
| `arrival_load` | Online arrival rate: low = 0.075, medium = 0.30, high = 0.60 tasks/s. |
| `trace_id` | Scenario block. AGX uses 0000–0049; RP2040 uses 0000–0003. Repeated IDs across conditions identify paired scenarios, not independent replicates. |
| `policy_id` | `eager_b1`, `count_b2`, `count_b4`, `count_b8`, or `bounded_b4_w10`. Every policy admits the initial eight tasks at time zero. |
| `provider` / `timing_arm` | AGX with measured compute delay, AGX zero-compute, or RP2040 hardware allocator timing. |
| `scenario_sha256`, `release_sha256`, `runtime_seed` | Identities used to verify a paired spatial layout, task-release stream and runtime randomness. |
| `completed`, `all_tasks_completed`, `failure_category`, `technical_failure` | Outcome and failure classification. Planned failures remain in completion records; continuous paired metrics use only common completers. |

Admission threshold `b` is separate from predecessor allocator planning depth `B`. `bounded_b4_w10` admits four pending tasks or releases the pending remainder after the oldest task waits 10 seconds, subject to the documented terminal rule.

## Paper endpoints

| Field | Unit | Definition |
| --- | --- | --- |
| `allocation_epoch_count` | epochs | Environmental admission batches, including the initial eight-task batch. |
| `allocator_call_count` | calls | Valid allocator transactions summed across four robots. |
| `work_s` | processor-seconds | Sum of measured allocator transaction durations; it is not total onboard computation or mission delay. |
| `work_per_call_s` | seconds/call | `work_s / allocator_call_count` within each mission, then averaged across missions. |
| `mean_release_to_completion_latency_s` | simulated seconds | Per-mission mean release-to-first-completion latency over all 50 tasks. |
| `p95_release_to_completion_latency_s` | simulated seconds | Per-mission nearest-rank p95, the 48th ordered latency among 50 tasks. |
| `online_mean_s` | simulated seconds | Per-mission mean latency over the 42 online tasks. |
| `online_wait_mean_s` | simulated seconds | Online release-to-environmental-admission wait, excluding later announcement or allocation delays. |
| `online_post_admission_mean_s` | simulated seconds | Online admission-to-completion time, including subsequent computation, communication, travel and contention. |
| `mission_elapsed_time_s` | simulated seconds | Time to the final required task completion. |
| `total_team_steps`, `max_robot_steps` | grid traversals | Sum across robots and maximum for one robot, respectively; not physical distance or energy. |
| `logical_allocation_payload_bytes_sent_total` | bytes | Logical allocator-message payload before network fan-out; excludes transport overhead. |

AGX work uses the AGX allocator timer; RP2040 work uses the board allocator timer. Hardware HIL includes no physical robot movement. Whole dispatched transactions can finish after the final task completion and still count toward work.

## Main files and comparison fields

| File | One row represents |
| --- | --- |
| [`source_data/agx_causal_trial_level.csv`](analysis/roboticcc_final/source_data/agx_causal_trial_level.csv) and [`agx_zero_compute_trial_level.csv`](analysis/roboticcc_final/source_data/agx_zero_compute_trial_level.csv) | One planned AGX mission, including incomplete outcomes (3,000 rows each). |
| [`source_data/completion_records.csv`](analysis/roboticcc_final/source_data/completion_records.csv) | One planned AGX or RP2040 job (6,096 rows), including all noncompletions/failures. |
| [`derived_data/agx_policy_pairs.csv`](analysis/roboticcc_final/derived_data/agx_policy_pairs.csv) | One planned Eager/treatment trace pair (2,400 rows). `*_eager`, `*_policy` and `*_difference` are endpoint values; `both_completed` identifies valid continuous pairs. |
| [`derived_data/all_policy_effects.csv`](analysis/roboticcc_final/derived_data/all_policy_effects.csv) | One of 11 endpoints for each of 48 treatment comparisons (528 rows). `common_completed_pairs` and `n` give the included pair count. |
| [`tables/`](analysis/roboticcc_final/tables/) and [`figures/source/`](analysis/roboticcc_final/figures/source/) | Display selections for manuscript Tables I–II and Figures 1–3. |

In `all_policy_effects.csv`, `mean_difference` is the mean of within-trace treatment minus Eager values. `ratio_of_paired_means_pct` is `100 × (mean(treatment on common traces) / mean(Eager on those traces) − 1)`; it is not the mean within-trace percentage. `median_paired_pct` is a separate median of trace percentages. `*_ci_low` and `*_ci_high` are pointwise 95% trace-bootstrap bounds. `n_lower`, `n_equal`, and `n_higher` count paired directions for that endpoint. Intervals spanning zero do not establish equivalence.

The full RP2040 compact trial export retains extensive device/runtime provenance columns beyond the paper endpoints. Its field names and source code provide the detailed schema; the paper's tested hardware subset and failures are summarized in the package guide and completion records. The [claim map](analysis/roboticcc_final/CLAIM_SOURCE_MAP.csv) gives the exact source/filter for each manuscript number.
