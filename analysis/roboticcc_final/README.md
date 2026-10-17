# RoboticCC final analysis package

This folder is the reviewer-facing reproduction package for the final RoboticCC manuscript, **Embedded Evaluation of Task Admission Coalescing in Decentralized Multi-Robot Systems**. It contains the compact publication data, trace-level pairing records, manuscript claim map, paper tables, and native MATLAB sources for Figures 1-3. It does not contain the full raw campaign tree.

## Experiment represented here

The corrected experiment evaluates four decentralized allocators:

- Consensus-Based Auction Algorithm (CBAA)
- Asynchronous Consensus-Based Bundle Algorithm (ACBBA)
- Performance Impact (PI)
- Hybrid Information and Plan Consensus (HIPC)

Each AGX timing arm crosses three online arrival loads (low 0.075, medium 0.30, and high 0.60 tasks/s), five admission policies (Eager, Count b=2, Count b=4, Count b=8, and Bounded b=4/W=10 s), and 50 paired scenario traces per condition. The measured-compute, causal arm has 3,000 planned missions: 2,940 complete and 60 retained algorithmic noncompletions. The paired zero-compute arm has 3,000/3,000 complete missions. Zero-compute reruns the allocator but inserts zero duration into each robot's virtual processor; it is not a replay of causal decisions.

The RP2040 allocator hardware-in-the-loop subset crosses the same four allocators and three loads with Eager and Count b=4 on traces 0000-0003. It has 96 planned missions, 82 successful missions, 14 retained terminal technical failures, and 38 complete Eager-Count paired blocks. Each board measures native allocator transactions for an entire simulated four-robot mission. World state, communication, routing, and physical motion remain simulated. Hardware summaries are descriptive because only four traces were planned per condition.

## Exact data and manuscript versions

- Repository package commit: `80c565dfaed53b1bf17e7624bc404fa744211d6d`
- Corrected AGX producing commit: `598485103ee270a27d8b684c0082e46e2ad53802`
- RP2040 v9 producing commit: `3fe1f578987088fc8f044741bd046ca4e5488267`
- RP2040 v10 producing commit: `a3490a7748d852af5b05f1df3caa1f86a44dda17`
- Final compact data handoff: `roboticcc_final_data`, created 2026-09-12 UTC
- Final manuscript copy: `provenance/final_manuscript.tex`, SHA-256 `652edf9ac3867851961362739dab4702b6c1d850a703e8a951daabd4d83f5549`

`MANIFEST.json` records all authoritative input and package-output hashes. `provenance/authoritative_input_hashes.csv` provides a flat reviewer-readable version of the upstream input list. The current Overleaf `main.tex` is the manuscript source of truth. No Phase 5 claim ledger was present; the final Phase 1 ledger is retained in `provenance/phase1_claim_ledger.csv` and was augmented from the final manuscript in `CLAIM_SOURCE_MAP.csv`.

## Reproducing figures and tables

From the repository root, refresh the compact data products and checks with:

```text
python analysis/roboticcc_final/provenance/build_package.py
python analysis/roboticcc_final/provenance/build_claim_audit.py
```

The first command operates entirely from package-local `source_data/` after initialization. It does not rerun a mission or modify an authoritative result file.

Generate every final paper figure in MATLAB:

```matlab
cd analysis/roboticcc_final/matlab
make_all_figures
```

The figures were verified with MATLAB 25.2.0.3123386 (R2025b) Update 3. MATLAB writes vector PDFs to `figures/pdf/` and 400-dpi review PNGs to `figures/png/`.

| Manuscript item | Reproduction source | Final output |
| --- | --- | --- |
| Figure 1, admission architecture | `matlab/fig1_admission_architecture.m` | `figures/pdf/fig1_admission_architecture.pdf` |
| Figure 2, AGX coalescing regimes | `matlab/fig2_coalescing_regimes.m`; `figures/source/fig2_coalescing_regimes.csv` | `figures/pdf/fig2_coalescing_regimes.pdf` |
| Figure 3, HIPC medium AGX/RP2040 pairs | `matlab/fig3_hipc_medium_hardware.m`; `figures/source/fig3_hipc_medium_hardware.csv` | `figures/pdf/fig3_hipc_medium_hardware.pdf` |
| Table I, experiment coverage | `provenance/build_package.py` | `tables/table1_experiment_design.csv` |
| Table II, anchor mechanisms | `provenance/build_package.py` | `tables/table2_anchor_mechanisms.csv` |

Figure 2 follows the publication layout: **x is allocator-work change and y is task-latency change**, both relative to Eager. Right means more processor work; up means more delay; lower-left is favorable. The four treatment policies are never pooled across allocators. Eager is a reference cross at the origin rather than a fifth treatment point.

## Source data and derived values

`source_data/` contains compact publication inputs and validated final-handoff statistical rows. The main trace-level files are:

- `agx_causal_trial_level.csv`: all 3,000 corrected causal AGX missions, including incomplete outcomes;
- `agx_zero_compute_trial_level.csv`: all 3,000 zero-compute missions;
- `rp2040_trial_level.csv`: all 82 successful HIL missions with board/runtime lineage;
- `completion_records.csv`: all 6,096 planned AGX and HIL outcome records, including the 14 hardware failures;
- `platform_policy_pairs.csv`: all 48 planned hardware blocks plus the matching AGX pairs;
- `agx_effects_validated.csv`: the final 528 endpoint-level AGX effect records and pointwise intervals.

`derived_data/` contains reproducible manuscript-specific selections, pair tables, completion summaries, mechanism decomposition, and cross-platform summaries. Trace identifiers are preserved. See `derived_data/README.md` for every source, filter, pairing rule, formula, and incomplete-trial treatment.

Every policy effect is policy minus Eager. The manuscript percentage convention is:

```text
100 * (paired-cohort policy mean / paired-cohort Eager mean - 1)
```

This ratio of paired-cohort means is distinct from the mean paired absolute difference and from the median within-trace percentage change. The CSVs label all three estimands separately. Continuous AGX effects use only common completed Eager/policy pairs; planned and completed counts remain explicit. Forty-two of 48 comparisons retain all 50 pairs. Hardware means use the exact complete matched traces and have no inferential interval.

## Audits

- `CLAIM_SOURCE_MAP.csv` maps all important final-manuscript numbers to package data and filters.
- `checks/manuscript_number_audit.csv` verifies the Abstract, Results and Discussion, Conclusion, tables, and numerical figure captions/annotations.
- `checks/figure_data_audit.csv` verifies plotted row counts, interval completeness, incomplete-cohort annotations, and retention of adverse hardware trace 0001.
- `checks/table_data_audit.csv` verifies Table I coverage and Table II endpoint coverage.
- `checks/README.md` summarizes results and interpretation cautions.

The package intentionally retains algorithmic noncompletions and terminal technical failures as outcomes. Diagnostic replays were not substituted for production measurements. Original raw logs, task-level campaign trees, attempt-failure archives, and superseded pre-correction August products are outside this reviewer package.
