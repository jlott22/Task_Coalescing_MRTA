# Final quantitative data handoff

The corrected data support temporal admission coalescing as an allocator- and operating-regime-dependent compute control. The main AGX example saves work primarily through fewer calls; the counterexample increases both calls and cost per call despite fewer admissions. Sparse arrivals expose the waiting cost. The four tested medium-load HIPC hardware traces show a large observed responsiveness benefit that differs from the same AGX traces.

Use [all_policy_paired_effects.csv](all_policy_paired_effects.csv) as the authoritative 48-row AGX comparison table. [all_policy_effects_long.csv](all_policy_effects_long.csv) presents the same 528 endpoint records for filtering. All 11 requested continuous endpoints are included. This package contains data and short interpretation notes, not a manuscript.

## Estimators and scope

Every difference is policy minus Eager. In the tables below, percentages are **100 × (paired-cohort policy mean / paired-cohort Eager mean − 1)**. They are not averages or medians of individual percentages. CSVs separately contain mean paired differences, median paired differences, and median within-trace percentage effects with their own intervals. Work/call is calculated within each mission before averaging.

AGX intervals are pointwise 95% percentile intervals from 10,000 shared trace-bootstrap draws (seed 20260912). The trace is the replicate; tasks and calls are not replicates. Continuous effects use common completed pairs. An interval spanning zero does not establish equivalent responsiveness. Hardware summaries are descriptive for the explicitly tested traces. Lower/equal/higher counts describe the endpoint, not overall policy utility.

Manuscript terminology: **Count-b2/b4/b8** and **Bounded-b4/W10**, with admission threshold **b**, deadline **W=10 s**, and retained allocator state. Reserve uppercase **B** for the predecessor's internal planning depth.

## A. HIPC / high / Bounded-b4/W10

All 50 planned policy/Eager pairs completed. The work saving is clear; the all-task mean, p95, mission-time, and motion intervals span zero. The online-only mean penalty is positive with a pointwise interval narrowly above zero. This is a useful compute/responsiveness tradeoff candidate, without an established latency-equivalence claim.

Source: [anchor_examples.csv](anchor_examples.csv), `anchor=A`. E/P are paired-cohort means; L/E/H counts sum to 50. All displayed absolute values retain six decimals; CSVs retain greater numerical precision.

| Outcome | Eager → policy | Mean paired Δ [95% CI] | Mean-ratio % [95% CI] | L/E/H |
| --- | --- | --- | --- | --- |
| Admission epochs | 43.000000 → 12.120000 | -30.880000 [-30.960000, -30.780000] | -71.814 [-72.000, -71.581] | 50/0/0 |
| Allocator calls | 1009.900000 → 835.500000 | -174.400000 [-245.881000, -103.039500] | -17.269 [-23.446, -10.518] | 39/0/11 |
| Allocator work (processor-s) | 1.677608 → 1.352999 | -0.324609 [-0.485704, -0.152337] | -19.350 [-27.658, -9.402] | 38/0/12 |
| Mean work/call (ms) | 1.630922 → 1.565144 | -0.065778 [-0.162559, +0.036422] | -4.033 [-9.775, +2.309] | 33/0/17 |
| All-task mean latency (s) | 32.366856 → 33.771726 | +1.404870 [-0.214905, +3.146594] | +4.340 [-0.643, +9.893] | 20/0/30 |
| All-task p95 latency (s) | 88.876866 → 89.183116 | +0.306250 [-5.540858, +6.456243] | +0.345 [-6.087, +7.484] | 26/0/24 |
| Online mean latency (s) | 30.854474 → 32.420928 | +1.566454 [+0.004788, +3.217786] | +5.077 [+0.015, +10.620] | 20/0/30 |
| Mission time (s) | 140.423949 → 138.876789 | -1.547159 [-8.884128, +5.613689] | -1.102 [-6.164, +4.105] | 29/0/21 |
| Team steps | 214.200000 → 215.120000 | +0.920000 [-5.720000, +7.440500] | +0.430 [-2.608, +3.553] | 23/0/27 |
| Maximum robot steps | 73.960000 → 73.920000 | -0.040000 [-5.240000, +5.080000] | -0.054 [-6.800, +7.115] | 25/0/25 |
| Logical allocation payload (bytes) | 182494.820000 → 139182.940000 | -43311.880000 [-58713.438500, -28297.837500] | -23.733 [-30.433, -16.110] | 40/0/10 |

The separate median within-trace work effect is -23.612 [-30.228, -14.925]%.

## B. CBAA / high / Count-b4

All 50 planned pairs completed. Reducing admissions increases computation and also increases latency, mission duration, and movement. Source: `anchor_examples.csv`, `anchor=B`; each L/E/H denominator is 50.

| Outcome | Eager → policy | Mean paired Δ [95% CI] | Mean-ratio % [95% CI] | L/E/H |
| --- | --- | --- | --- | --- |
| Admission epochs | 43.000000 → 12.000000 | -31.000000 [-31.000000, -31.000000] | -72.093 [-72.093, -72.093] | 50/0/0 |
| Allocator calls | 461.080000 → 495.360000 | +34.280000 [+11.138500, +58.620500] | +7.435 [+2.378, +12.888] | 18/0/32 |
| Allocator work (processor-s) | 0.140533 → 0.172609 | +0.032076 [+0.021711, +0.042713] | +22.825 [+15.133, +30.913] | 8/0/42 |
| Mean work/call (ms) | 0.304298 → 0.347514 | +0.043217 [+0.034674, +0.051185] | +14.202 [+11.275, +16.988] | 2/0/48 |
| All-task mean latency (s) | 27.015948 → 31.223440 | +4.207492 [+3.302033, +5.153427] | +15.574 [+12.017, +19.407] | 3/0/47 |
| All-task p95 latency (s) | 65.895054 → 73.134018 | +7.238964 [+3.136892, +11.385406] | +10.986 [+4.539, +17.855] | 13/0/37 |
| Online mean latency (s) | 27.015438 → 32.202117 | +5.186680 [+4.196216, +6.236192] | +19.199 [+15.349, +23.402] | 3/0/47 |
| Mission time (s) | 117.784653 → 142.175134 | +24.390481 [+20.014041, +28.710581] | +20.708 [+16.785, +24.688] | 2/0/48 |
| Team steps | 258.600000 → 287.660000 | +29.060000 [+20.959500, +37.160000] | +11.237 [+8.039, +14.471] | 5/1/44 |
| Maximum robot steps | 68.620000 → 79.740000 | +11.120000 [+8.400000, +13.840000] | +16.205 [+12.091, +20.350] | 4/3/43 |
| Logical allocation payload (bytes) | 41381.660000 → 42969.740000 | +1588.080000 [+512.689000, +2712.884000] | +3.838 [+1.225, +6.618] | 20/0/30 |

The separate median within-trace work effect is +19.962 [+8.374, +28.730]%.

## Mechanism and execution-round consistency

Within each trace, `W=N*c`. The exact symmetric decomposition is `ΔW = ΔN*(cP+cE)/2 + Δc*(NP+NE)/2`. Averaging these terms preserves the identity; these are arithmetic contributions, not causal mediation. Source: [mechanism_decomposition.csv](mechanism_decomposition.csv), 50 pairs per row.

| Anchor | Total Δ work (s) | Calls term (s) [95% CI] | Per-call term (s) [95% CI] | Calls / per-call share (%) |
| --- | --- | --- | --- | --- |
| HIPC | -0.324609458 | -0.274289271 [-0.398868572, -0.149694121] | -0.050320187 [-0.148011534, +0.053694258] | 84.498 / 15.502 |
| CBAA | +0.032076317 | +0.011462162 [+0.003641124, +0.019687578] | +0.020614155 [+0.016334681, +0.024672287] | 35.734 / 64.266 |

CBAA contributions are both positive: 35.734% [16.205, 47.814] from calls and 64.266% [52.186, 83.795] from per-call work. HIPC saving is mainly fewer calls; its per-call contribution interval spans zero.

The main directions persist in both 25-trace rounds. These rounds partition the 50-trace evidence and are not an independent holdout. Full endpoint values and trace-direction counts are in [anchor_rounds.csv](anchor_rounds.csv).

| Anchor | Outcome | Round 1 mean-ratio % (n=25) | Round 2 mean-ratio % (n=25) |
| --- | --- | --- | --- |
| A | Allocator calls | -17.153 | -17.384 |
| A | Allocator work (processor-s) | -18.715 | -19.964 |
| A | Mean work/call (ms) | -5.517 | -2.570 |
| A | All-task mean latency (s) | +6.134 | +2.602 |
| B | Allocator calls | +8.214 | +6.660 |
| B | Allocator work (processor-s) | +26.244 | +19.467 |
| B | Mean work/call (ms) | +16.250 | +12.180 |
| B | All-task mean latency (s) | +12.613 | +18.580 |

## C. Low load / Count-b4

All four contrasts have 50 complete pairs; all-task and online mean latency increase on **50/50 traces for each allocator**. At 0.075 tasks/s, expected full-batch admission waiting is `(b−1)/(2λ)=20 s`. The measured first-40 online wait is 19.508893 s for every allocator. The remaining two online tasks follow the terminal residual rule.

Source: [low_load_count4.csv](low_load_count4.csv). Online means use 42 tasks per completed mission; every row has 50 trace pairs.

| Allocator | Online penalty s [95% CI] | Admission wait s | Post-admission Δ s [95% CI] | Wait share % | Calls % | Work % |
| --- | --- | --- | --- | --- | --- | --- |
| CBAA | +20.429 [+19.413, +21.479] | 19.339 | +1.090 [+0.526, +1.635] | 94.66 | -24.669 | -29.393 |
| ACBBA | +22.358 [+21.074, +23.666] | 19.756 | +2.602 [+1.741, +3.475] | 88.36 | -15.703 | -7.811 |
| PI | +23.574 [+22.337, +24.831] | 19.644 | +3.930 [+2.882, +5.066] | 83.33 | -10.212 | +0.214 |
| HIPC | +20.081 [+19.087, +21.085] | 19.412 | +0.669 [+0.144, +1.195] | 96.67 | -16.171 | -10.215 |

Admission waiting accounts for 83.33–96.67% of the arithmetic online latency difference, with positive post-admission penalties remaining for all four allocators. Those residuals include computation, communication, travel and contention; they are not pure travel. PI reduces calls but does not show a mean work saving. Expected batching wait establishes the cost side of the tradeoff; it is not a novelty claim.

## Regime map and figure sources

[regime_map.csv](regime_map.csv) has all 48 comparisons with Eager as the reference; draw Eager at (0,0). It records observed direction and interval direction separately. Across these correlated cells, 11 reduce admissions while increasing both mean calls and work; 30 reduce both calls and work while increasing mean latency. Only PI/high/Count-b2 lowers both mean work (−5.413190%) and mean latency (−1.161722%), and both intervals span zero.

Bounded lowers mean work in 10/12 allocator/load cells (work interval below zero in 6/12), while mean latency rises in 12/12 (interval above zero in 9/12). PI/medium is adverse: work +11.373051%, latency +22.348740%, both intervals above zero. One work-lowering Bounded cell is ACBBA/high with 30 common completers; the other nine have 50. These counts do not establish a universally best policy.

HIPC/medium/Count-b2 is another complete-cohort candidate: work −11.007287%, mean latency +3.465906% with its interval spanning zero. HIPC/high/Count-b8 saves more work (−25.324836%) than Bounded, with larger latency (+20.934979%) and mission-time (+14.584265%) increases. Explicit 10% motion/mission display flags in the map are descriptive thresholds; scientific importance depends on the application.

Recommended four layouts, with no styling fixed:

1. [01_regime_scatter.csv](figure_sources/01_regime_scatter.csv): work-change x latency-change scatter, load columns and allocator rows, four policy symbols plus Eager, pointwise x/y intervals and incomplete-cohort n labels.
2. [02_mechanism.csv](figure_sources/02_mechanism.csv): two anchor columns with epochs → calls → work/call → total work → latency rows. Add the exact additive decomposition as a small table.
3. [03_hardware_pairs.csv](figure_sources/03_hardware_pairs.csv): four labeled HIPC/medium traces, paired Eager/Count values for work, latency and mission, with adjacent matching AGX panels. Retain failures when displaying other conditions.
4. [04_completion.csv](figure_sources/04_completion.csv): optional compact completion table; filter one `scope` at a time to avoid summing totals with their constituent rows.

## RP2040 evidence and corresponding AGX traces

[rp2040_pairs.csv](rp2040_pairs.csv) retains all 48 planned paired blocks, including failures: **38 complete pairs, six one-sided blocks, four blocks with neither policy completed**. All 38 usable pairs share board and runtime lineage. [rp2040_summary.csv](rp2040_summary.csv) covers all 12 allocator/load conditions.

HIPC/medium retains all four tested traces (0000–0003), with three improving work, mean latency and mission duration together; trace 0001 worsens all three. The aggregate effect differs sharply from the same four AGX traces. PI/high supplies secondary evidence on three of four planned blocks: all three save work; two improve latency and mission duration. Its fourth Count job is a retained terminal failure.

The following values are descriptive paired-cohort means and their percentage ratios. Source: [hardware_platform_summary.csv](hardware_platform_summary.csv), `algorithm/arrival_load/provider` as shown.

| Condition | Platform | Pairs | Outcome | Eager → Count-b4 | Change % | L/E/H |
| --- | --- | --- | --- | --- | --- | --- |
| HIPC/medium | rp2040 | 4 | Allocator work (processor-s) | 353.312354 → 141.848676 | -59.851765 | 3/0/1 |
| HIPC/medium | rp2040 | 4 | All-task mean latency (s) | 62.387960 → 37.762016 | -39.472269 | 3/0/1 |
| HIPC/medium | rp2040 | 4 | Mission time (s) | 238.469452 → 201.596429 | -15.462368 | 3/0/1 |
| HIPC/medium | agx | 4 | Allocator work (processor-s) | 1.100963 → 1.015202 | -7.789690 | 3/0/1 |
| HIPC/medium | agx | 4 | All-task mean latency (s) | 23.724405 → 30.294047 | +27.691495 | 0/0/4 |
| HIPC/medium | agx | 4 | Mission time (s) | 168.725580 → 192.717822 | +14.219683 | 1/0/3 |
| PI/high | rp2040 | 3 | Allocator work (processor-s) | 771.537086 → 627.522564 | -18.665923 | 3/0/0 |
| PI/high | rp2040 | 3 | All-task mean latency (s) | 215.178238 → 188.618215 | -12.343266 | 2/0/1 |
| PI/high | rp2040 | 3 | Mission time (s) | 386.414374 → 375.274534 | -2.882874 | 2/0/1 |
| PI/high | agx | 3 | Allocator work (processor-s) | 1.721000 → 2.005073 | +16.506273 | 1/0/2 |
| PI/high | agx | 3 | All-task mean latency (s) | 37.263974 → 47.887046 | +28.507619 | 0/0/3 |
| PI/high | agx | 3 | Mission time (s) | 145.277065 → 195.064574 | +34.270729 | 0/0/3 |

Individual board/lineage values, all four HIPC traces, call counts, p95 latency and per-call work are in [hardware_notes.md](hardware_notes.md) and the hardware figure CSV. These are observed platform-dependent policy effects; the comparison does not isolate processor speed.

## Device timing context

[compute_gap_summary.csv](compute_gap_summary.csv) uses 81 successful same-condition/trace AGX–RP2040 mission matches, covering four distinct scenario identities. One additional successful hardware mission has a noncomplete AGX counterpart and is excluded from timing ratios. The overall mean-work ratio is 323.855146×; the median within-matched-mission work ratio is 54.163456×, showing strong skew.

| Allocator | Matched missions | Work ratio, RP/AGX cohort means | Mean-call ratio, RP/AGX cohort means | Median mission-mean call ms, AGX / RP |
| --- | --- | --- | --- | --- |
| ALL | 81 | 323.855 | 341.041 | 0.628883 / 34.527801 |
| ACBBA | 12 | 544.005 | 229.198 | 0.707069 / 32.286378 |
| CBAA | 23 | 41.697 | 29.336 | 0.332978 / 9.365752 |
| HIPC | 24 | 307.391 | 471.373 | 0.964733 / 237.986206 |
| PI | 22 | 286.524 | 362.382 | 0.940935 / 276.716192 |

Ratios compare retained measured allocator transactions under each execution setting. They are not universal speed multipliers or critical-path delays. Call counts and call workloads can differ. The CSV provides min/p25/median/p75/p95/max across mission totals and mission-average call work. These are not pooled individual-call quantiles; raw call samples are unavailable.

## Completion and terminal-work scope

[completion_accounting.csv](completion_accounting.csv), `scope=provider_total`: AGX causal **2,940/3,000 complete, 60 noncomplete**; zero-compute **3,000/3,000 complete**; RP2040 **82/96 successful, 14 terminal failures**. The 59 ACBBA causal noncompletions comprise 57 high-load jobs and two medium/Count-b8 jobs; one further causal noncompletion is HIPC/low/Count-b8. These are finite stopping-rule outcomes, not evidence of permanent liveness failure.

**42/48 AGX comparisons have 50 common completers**, including both main anchors and every low-load Count-b4 contrast. The six incomplete contrasts are ACBBA/high Count-b2/b4/b8/Bounded with n=33/32/27/30, ACBBA/medium Count-b8 n=48, and HIPC/low Count-b8 n=49. Their continuous effects are conditional on common completion. Planned/completion counts remain in every primary table row.

End-of-mission work cannot be separated from current retained summaries: per-call simulated dispatch/finish timestamps aligned with final task completion are unavailable. Headline work therefore retains whole valid measured transactions; whether terminal overhang materially changes the contrasts is unknown. See [end_of_mission_work.md](end_of_mission_work.md). No production experiments or hardware reconstruction were performed.

## Methods, predecessors and reproducibility

[paper_methods_fact_sheet.md](paper_methods_fact_sheet.md) contains the exact grid, starts, releases, timing boundaries, admission rules, virtual processors, HIL structure and inference procedure. [predecessor_overlap.md](predecessor_overlap.md) compares only the two specified public predecessor papers. The shared static CV architecture is background; online releases, causal computation and temporal admission interventions define the extension. Internal retained planning depth B is distinct from admission threshold b. Prior publication of this group's AGX/RP2040 evaluation is not assumed.

[DATA_DICTIONARY.md](DATA_DICTIONARY.md) defines fields and units. [REPRODUCE.md](REPRODUCE.md) gives portable commands; [manifest.json](manifest.json) records producing commits, original input hashes and packaged file identities. Source rows, scripts and figure CSVs are included in the ZIP, so the folder does not need to be handed over separately.

## Numbers safe to quote verbatim in the manuscript

Every percentage below is a ratio of paired-cohort means unless explicitly labeled otherwise.

- HIPC/high/Bounded-b4/W10: allocator work **1.677608488 → 1.352999030 processor-s; −19.349536%**, 95% CI **[−27.658327%, −9.402127%]**; lower on **38/50** traces. Source: `anchor_examples.csv`, `anchor=A, metric=work_s`; **50/50 common pairs**.
- Same anchor: calls **1009.900000 → 835.500000; −17.269037%**; admission epochs **43 → 12.12; −71.813953%**. Source: `anchor_examples.csv`, `anchor=A, metric=allocator_call_count/allocation_epoch_count`; **50/50 common pairs**.
- Same anchor: all-task mean latency **+1.404870 s**, 95% CI **[−0.214905, +3.146594] s**, or **+4.340458%**; online mean latency **+1.566454 s**, 95% CI **[+0.004788, +3.217786] s**. Source: `anchor_examples.csv`, `anchor=A, metric=mean_release_to_completion_latency_s/online_mean_s`; **50/50 pairs**, 50 all tasks or 42 online tasks per mission.
- CBAA/high/Count-b4: epochs **43 → 12; −72.093023%**, calls **+7.434718%**, per-call work **+14.202072%**, and total work **+22.824813%**. Source: `anchor_examples.csv`, `anchor=B`, corresponding four metric rows; **50/50 common pairs**.
- Same counterexample: work increases on **42/50** traces; all-task mean latency increases on **47/50** and mission time on **48/50**. Source: `anchor_examples.csv`, `anchor=B, metric=work_s/mean_release_to_completion_latency_s/mission_elapsed_time_s`, `n_higher`; **50 pairs**.
- CBAA work increase **+0.032076317 processor-s** decomposes into **+0.011462162** from call count and **+0.020614155** from per-call cost, **35.734% / 64.266%** of the increase. Source: `mechanism_decomposition.csv`, `algorithm=CBAA`; **50 common pairs**, exact symmetric arithmetic decomposition.
- Low-load Count-b4 increases online mean latency by **20.429294 / 22.358108 / 23.573571 / 20.080903 s** for **CBAA / ACBBA / PI / HIPC**; every allocator has **50/50** traces with increased latency. Source: `low_load_count4.csv`, all four rows, `online_mean_s__mean_difference/n_higher`; **50 pairs per allocator**, 42 online tasks per mission.
- Bounded reduces mean work in **10/12** allocator/load cells while increasing mean all-task latency in **12/12**. Source: `regime_map.csv`, `policy_id=bounded_b4_w10`, signed mean effects; **12 correlated cells**, 11 with 50 pairs and ACBBA/high with 30.
- RP2040 HIPC/medium: work **353.312353750 → 141.848675750 processor-s (−59.851765%)**, mean latency **62.387959586 → 37.762016439 s (−39.472269%)**, mission **238.469451678 → 201.596428594 s (−15.462368%)**; **3/4** traces improve all three. Source: `hardware_platform_summary.csv`, `provider=rp2040, algorithm=HIPC, arrival_load=medium`; **4/4 common pairs, eight successful planned jobs**.
- Matching AGX HIPC/medium traces: work **−7.789690%**, mean latency **+27.691495%**, mission **+14.219683%**. Source: `hardware_platform_summary.csv`, `provider=agx, algorithm=HIPC, arrival_load=medium`; **the same four trace IDs, 4/4 common pairs**.
- RP2040 PI/high: work **−18.665923%**, mean latency **−12.343266%**, mission **−2.882874%**. Source: `hardware_platform_summary.csv`, `provider=rp2040, algorithm=PI, arrival_load=high`; **3/4 planned blocks usable, seven successful jobs and one terminal failure out of eight**.
- Completion totals: **AGX causal 2940/3000; AGX zero-compute 3000/3000; RP2040 82/96**; **42/48** AGX contrasts have complete 50-pair data. Source: `completion_accounting.csv`, `scope=provider_total`, and `all_policy_paired_effects.csv`, `complete_50_pairs`; denominators are **planned missions** and **policy-versus-Eager contrasts**, respectively.
