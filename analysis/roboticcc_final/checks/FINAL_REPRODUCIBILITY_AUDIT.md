# Final reproducibility audit

This audit treats `analysis/roboticcc_final/` as a reviewer-facing publication package and was performed independently from the package-construction pass. Authoritative experiment data were read but not changed. Reproduction was tested in disposable copies of the package.

The numerical and statistical layer is correct. Every audited manuscript number, table entry, and plotted value agrees with an independent calculation. Release is nevertheless blocked by manuscript/figure synchronization and provenance defects described below.

## Audit scope and reference state

- Repository HEAD: `80c565dfaed53b1bf17e7624bc404fa744211d6d`.
- Current manuscript: `C:/Users/lottj/Downloads/RoboticCC_Overleaf_Package/RoboticCC_Overleaf/main.tex`.
- Current manuscript SHA-256: `652edf9ac3867851961362739dab4702b6c1d850a703e8a951daabd4d83f5549`.
- The current manuscript is byte-identical to `provenance/final_manuscript.tex` and agrees with the manuscript record in `MANIFEST.json`.
- MATLAB used for the reproduction test: 25.2.0.3123386 (R2025b) Update 3.
- The pre-audit package manifest verified all 73 listed files.

## 1. Traceability

### Quantitative chains verified

The following chains were checked independently:

1. Manuscript claim to `CLAIM_SOURCE_MAP.csv` and the publication-specific CSV named there.
2. Publication CSV to the selection, pairing, or reshaping implemented by `provenance/build_package.py`.
3. AGX point estimates and Figure 2 intervals to `source_data/agx_causal_trial_level.csv`.
4. Hardware values to `source_data/platform_policy_pairs.csv`, `source_data/rp2040_trial_level.csv`, and the matching AGX trace records.
5. Completion totals to all 6,096 records in `source_data/completion_records.csv`.
6. Package source copies to their recorded upstream inputs by SHA-256.

All 50 rows in `CLAIM_SOURCE_MAP.csv` name an existing package source and derivation script. All 528 AGX condition/endpoint rows were independently recalculated from the 3,000 causal trial records. Table I, all 18 numeric rows of Table II, all 48 Figure 2 treatment points, every plotted interval bound, and all eight Figure 3 platform/trace rows traced successfully.

The package-local data and claim builders were also run in a disposable copy. They reproduced every non-figure package file byte-for-byte without accessing the full campaign tree.

### Broken or incomplete chains

1. **The authoritative-input ledger falsely contains two `main.tex` records.**

   `provenance/authoritative_input_hashes.csv` records both a 21,474-byte object with SHA-256 `95df1dc5...` and the actual 36,842-byte manuscript with SHA-256 `652edf9a...` under the same Overleaf path. The first object is `RoboticCC_Phase1_Writing_Packet.zip`, not a stale manuscript. The cause is the catch-all external-path label in `provenance/build_package.py` lines 160-170.

2. **Two supporting claims cannot be reconstructed at trace level from package-local trial rows.**

   `first40_online_wait_mean_s`, used for the observed 19.51-s first-40 waiting result, and `recovery_attempt_count`, used for the no-recovery statement, are absent from `source_data/agx_causal_trial_level.csv`. Their validated aggregates are present and their values were independently confirmed from the hashed upstream compact input, but a reviewer cannot repeat those two trace-level calculations using only the package.

3. **The AGX bootstrap is documented but not implemented in the package builder.**

   `build_package.py` reshapes the already validated interval rows. It does not regenerate the 10,000-draw trace bootstrap. Independent reimplementation reproduced the intervals, so this is a packaging gap rather than a numerical error.

4. **The manuscript audit is manually coupled.**

   `provenance/build_claim_audit.py` hard-codes the manuscript's reported strings and audit statuses; it does not parse or assert the contents of `final_manuscript.tex`. Table II display expectations are also hard-coded in `build_package.py`. A later manuscript edit could therefore leave the package checks green.

5. **The cited repository commit does not contain the package.**

   `git ls-files analysis/roboticcc_final` returns no files, and the directory is untracked. Commit `80c565d...` is the base repository state, not a commit that contains this reviewer package. The package is still identifiable by `MANIFEST.json`, but the README label “repository package commit” is misleading until the package is committed or archived as a versioned artifact.

## 2. Statistical correctness

The statistical implementation is correct for the stated estimands.

- The mission trace is the replicate. Tasks and allocator calls are not treated as independent replicates.
- Each treatment is joined to Eager on allocator, arrival load, and trace ID.
- All 2,400 planned AGX treatment/Eager pairs have matching scenario hash, release hash, and runtime seed.
- Continuous effects use only common completed pairs. Planned counts and reduced common-completer counts remain visible.
- The percentage estimator is `100 * (mean(policy) / mean(Eager) - 1)` on the paired cohort. It is not the mean or median of within-trace percentages.
- Absolute effects are paired mean differences.
- Pointwise intervals resample the shared 50-trace frame with 10,000 draws and seed 20260912. Incomplete pairs remain masked.
- AGX and RP2040 observations are never pooled. Figure 3 computes each platform annotation after filtering to four same-platform pairs.
- Hardware results are descriptive. The four HIPC/medium hardware traces are shown individually and no inferential interval is claimed.

Independent reconstruction found:

- 42 AGX comparisons with 50 common pairs and six reduced cohorts: ACBBA/high at 33, 32, 27, and 30 pairs; ACBBA/medium Count-b8 at 48; and HIPC/low Count-b8 at 49.
- Maximum AGX point-estimate discrepancy below `4e-12` relative to stored values.
- Maximum ratio-CI endpoint discrepancy `5.83e-8`, attributable to decimal serialization.
- Table II decomposition closure within `4.44e-16` processor-s per trace.

Headline recalculations include:

| Result | Independent value |
| --- | ---: |
| HIPC/high/Bounded work | -19.349536% |
| HIPC/high/Bounded mean-latency difference | +1.404870 s |
| CBAA/high/Count-b4 work | +22.824813% |
| RP2040 HIPC/medium work | -59.851765% |
| RP2040 HIPC/medium mean latency | -39.472269% |
| RP2040 HIPC/medium mission duration | -15.462368% |
| Same-four AGX HIPC/medium mean latency | +27.691495% |

Completion accounting also reconciles exactly: 3,000/2,940/60 causal AGX planned/completed/noncompleted missions; 3,000/3,000/0 zero-compute missions; and 96/82/14 hardware planned/successful/terminal-failure missions.

## 3. Figure reproducibility

### Standalone MATLAB reproduction

The entire package was copied to a disposable directory outside the repository. From its `matlab/` directory, MATLAB was started with the default path and `make_all_figures` was run twice. Both runs completed without accessing a repository file outside the copied package.

- Figure-source CSVs remained byte-identical.
- Regenerated PNG pixel matrices were exactly identical to the packaged PNGs.
- All PDFs remained one-page vector files with embedded fonts and zero raster images; Figures 2 and 3 now use Times New Roman while Figure 1 retains its original styling.
- PDF page sizes, drawing counts, extracted text, axes, signs, units, policy labels, trace IDs, interval bars, panel order, and captions agreed with the packaged outputs.
- Figure 2 now uses work change on x and latency change on y; right/up means more work/delay.
- Figure 3 retains adverse RP2040 trace 0001 and keeps the work scales platform-specific while sharing the latency scale.
- No experimental effect, confidence limit, or sample size is hard-coded in the Figure 2 or Figure 3 scripts. Hard-coded values are limited to design/category order, load labels, and layout. Figure 1 is an intentionally static schematic.

### Figure defects and handoff failures

1. **The current Overleaf bundle has not yet received the revised package PDFs.**

   The revised package adopts the Overleaf Figure 2 axis orientation (work on x and latency on y) and closely follows its compact visual treatment. The package PDFs still need to be copied into the Overleaf bundle after approval; Figure 1 was intentionally left unchanged.

2. **The Figure 3 annotation collision was corrected after the audit.**

   The overlapping `Mean:` labels were removed in the revised compact layout. All four individual trace pairs remain visible.

3. **Raw figure hashes are not reproducibility-stable.**

   MATLAB adds creation-time metadata to PDFs and PNGs, and repeated PDF exports can introduce sub-point glyph/clip differences. The PNG image data were pixel-identical and the PDFs were visually/vector equivalent, but rerunning the figures changes all six raw file hashes and therefore makes `verify_package.py` fail. Raw hashes are valid package-integrity checks, not proof of deterministic figure rendering. The package should document this or normalize export metadata and add semantic/pixel checks.

## 4. Reviewer readability

The top-level README clearly identifies the corrected experiment, four allocators, three loads, five AGX policies, pairing, completion accounting, source-versus-derived roles, hardware scope, and MATLAB entry point. Table and figure mappings are easy to locate.

The following issues materially reduce reviewer readability:

- The four copied upstream provenance documents contain 44 broken relative links: 22 in `FINAL_DATA_HANDOFF.md`, 14 in `GENERALITY_AUDIT.md`, and four each in `upstream_methods_and_metrics.md` and `upstream_provenance.md`. Some text also describes the layout of the original handoff rather than this package.
- `source_data/` contains 18 data files, but no package data dictionary defines all keys, units, blank/status conventions, or canonical provider-specific fields. The 182-column RP2040 trial file contains legacy aliases that are difficult to interpret without the upstream dictionary.
- `derived_data/hipc_medium_cross_platform.csv` and `figures/source/fig3_hipc_medium_hardware.csv` are intentionally identical, but the frozen plotting-copy relationship is not documented.
- `figures/source/fig1_admission_architecture.csv` is documentation only; Figure 1 does not load it. This should be stated explicitly if it is retained.
- Python and library versions are not documented, and the README reproduction sequence omits the final `verify_package.py` command.
- The TeX snapshot is provenance, not a compile-ready paper copy: its relative figure paths do not resolve from `provenance/`, and `reference.bib` is absent. Labeling it as a non-buildable snapshot would prevent confusion.

## 5. Manuscript consistency

### Checks with no defect

- The packaged manuscript snapshot is the current newest `main.tex`.
- No stale `W=5`, `bounded_b4_w5`, obsolete arrival rate, superseded completion count, or superseded experiment version appears in the manuscript or active package documentation.
- Current arrival rates are consistently 0.075, 0.30, and 0.60 tasks/s.
- Current policy identifiers and labels consistently use Eager, Count b=2/4/8, and Bounded b=4, W=10 s.
- Both manuscript tables agree with their source CSVs.
- All 50 audited quantitative manuscript rows agree exactly or after stated display rounding.
- Figure captions agree with the final package's axes, samples, units, and panel structure.

### Manuscript issues

1. `main.tex` line 138 still contains author-input placeholders for AGX and RP2040 configuration. Some requested clock, power/governor, thermal, firmware, and timer-resolution facts are explicitly unavailable in the packaged provenance and must not be filled from datasheet defaults.
2. `main.tex` line 270 still contains the public archive URL/version placeholder. `reference.bib` also retains a TODO for the exact `lott2026benchmark` arXiv identifier/version.
3. The manuscript reports 38 complete hardware pairs of 48 planned blocks but does not show the uneven 12-cell coverage. For example, ACBBA/high has 0/4 complete pairs and seven failed jobs. A compact coverage supplement would make the selected descriptive hardware cells easier to assess.
4. “Platform-dependent” and “demonstrates” are stronger than the four-trace, non-isolated cross-platform comparison supports. The body correctly states that runtime and message timing also differ. Abstract and conclusion wording should likewise describe observed responses in two tested execution settings rather than imply an isolated processor/platform effect.

## Exact fixes required before release

1. Replace all three Overleaf `figures/*.pdf` files with the audited package PDFs, compile the paper, and inspect pagination; the final Figure 1 is substantially taller than the current placeholder.
2. Resolve the hardware-configuration and archive placeholders using verified records, explicitly preserve unknown settings where records do not exist, and finish the `lott2026benchmark` bibliography entry.
3. Correct the external-input naming bug so the Phase 1 ZIP and current manuscript have distinct ledger records. Remove the false duplicate `main.tex` entry and regenerate the manifest.
4. Commit/version the reviewer package or label `80c565d...` unambiguously as the base-code commit and provide a separate immutable package release identifier.
5. Repair the 44 provenance-document links or move the copied documents under an `upstream_snapshots/` area with a banner explaining that their links describe the original handoff layout.
6. Add a package-local statistical verifier that regenerates AGX point estimates and trace-bootstrap intervals, add the omitted first-40-wait and recovery-count trace fields, and make the manuscript audit assert or parse the actual TeX snapshot.
7. Completed after this audit: remove the Figure 3 mean labels, regenerate the figure, and visually inspect the compact layout.
8. Document MATLAB figure hash nondeterminism and add a data dictionary, Python environment requirements, and the final manifest-verification command.
9. Add compact hardware-cell coverage to the paper or supplement and qualify cross-platform claims as descriptive tested-setting effects.

FAIL — current manuscript/figure integration and reviewer-package provenance contain publication-blocking defects
