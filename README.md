# Task Admission Coalescing in Decentralized Multi-Robot Systems

Research code and publication data for **“Embedded Evaluation of Task Admission Coalescing in Decentralized Multi-Robot Systems”** by James Lott and Vahraz Honary (submitted manuscript).

This repository lets a reader inspect the corrected experiment, regenerate the paper's numerical tables and figures, and trace reported numbers to retained outcomes. It is a research artifact; it does not promise a stable software API.

## Study at a glance

Four decentralized allocators (CBAA, ACBBA, PI, and HIPC) are compared under immediate task admission, count thresholds of 2/4/8, and a four-task threshold with a 10-second wait bound. Four robots visit 50 cells on a 19 × 19 grid. The same 50 scenario blocks are paired across three online arrival rates, allocators, policies, and two AGX timing arms. RP2040 boards measure allocator execution in a separate hardware-in-the-loop subset; routing, communication, and robot movement remain simulated.

| Campaign | Planned missions | Complete | Retained other outcomes |
| --- | ---: | ---: | ---: |
| AGX with measured computation delay | 3,000 | 2,940 | 60 algorithmic noncompletions |
| AGX with zero virtual computation delay | 3,000 | 3,000 | 0 |
| RP2040 allocator hardware-in-the-loop | 96 | 82 | 14 technical failures |

The failed and incomplete missions stay in the campaign denominator. Continuous paired effects use the common completed trace cohort, with its size shown in the data.

## Where to start

| Need | Location |
| --- | --- |
| Final manuscript data and reproduction guide | [`analysis/roboticcc_final/README.md`](analysis/roboticcc_final/README.md) |
| Paper Table I and II source tables | [`analysis/roboticcc_final/tables/`](analysis/roboticcc_final/tables/) |
| Figures 1–3, plotted CSVs, and MATLAB sources | [`analysis/roboticcc_final/figures/`](analysis/roboticcc_final/figures/) and [`analysis/roboticcc_final/matlab/`](analysis/roboticcc_final/matlab/) |
| Publication data dictionary and field definitions | [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) |
| Trace-level publication inputs | [`analysis/roboticcc_final/source_data/README.md`](analysis/roboticcc_final/source_data/README.md) |
| Derived tables and pairing rules | [`analysis/roboticcc_final/derived_data/README.md`](analysis/roboticcc_final/derived_data/README.md) |
| Claim-to-source map and manuscript checks | [`analysis/roboticcc_final/CLAIM_SOURCE_MAP.csv`](analysis/roboticcc_final/CLAIM_SOURCE_MAP.csv) and [`checks/`](analysis/roboticcc_final/checks/) |
| Corrected compact AGX and HIL exports | [`corrected_agx_v7_results/`](corrected_agx_v7_results/) and [`corrected_hardware_v9_v10_progress/`](corrected_hardware_v9_v10_progress/) |
| Simulator, admission policies, and campaign code | [`known_visit_sim/`](known_visit_sim/), [`study/`](study/), and [`Simulation/Architecture/allocator_replay/`](Simulation/Architecture/allocator_replay/) |

The older [`CURRENT_EXPERIMENT_STATUS.md`](CURRENT_EXPERIMENT_STATUS.md) is a September 8 execution snapshot. For final manuscript numbers and figure inputs, use `analysis/roboticcc_final/`.

## Reproduce the publication package

Use Python 3.12 or newer with NumPy and pandas. From the repository root:

```bash
python -m pip install -r requirements-paper.txt
python scripts/verify_current_data.py
python analysis/roboticcc_final/provenance/build_package.py
python analysis/roboticcc_final/provenance/build_claim_audit.py
```

The first command checks the corrected tracked exports. The next two regenerate compact manuscript tables and audit claims from the packaged inputs; they do not start simulations or contact hardware. They write generated files inside `analysis/roboticcc_final/`, so run them in a separate checkout if you want to preserve the released file hashes. The package's [`MANIFEST.json`](analysis/roboticcc_final/MANIFEST.json) identifies the source snapshot and input/output hashes.

The final paper figures were built in MATLAB R2025b Update 3. From `analysis/roboticcc_final/matlab/`, run `make_all_figures`. The released vector PDFs, review PNGs, and underlying plot CSVs are in `analysis/roboticcc_final/figures/`. MATLAB is only needed to regenerate the artwork; the numerical CSVs are readable without it.

For the more detailed numerical handoff and hardware analysis, see the private companion repository, `Task_Coalescing_MRTA_Research`, if you have access. Original raw campaign logs and device traces remain in the author's local archive; this public release contains corrected compact exports and publication inputs.

## Interpretation and provenance

- “Allocator work” is summed measured allocator transaction time. It is not total processor use, wall-clock mission delay, or energy.
- Hardware results are descriptive for the tested four-trace subset. They measure RP2040 allocation, not physical robot motion.
- Intervals are pointwise 95% trace-bootstrap intervals. An interval spanning zero does not establish equivalence.
- The final package audits 50 manuscript claims. Its [`checks/README.md`](analysis/roboticcc_final/checks/README.md) records zero unresolved numerical discrepancies; see the audit CSVs for the exact checks and rounding.
- The producing repository snapshot was commit `80c565dfaed53b1bf17e7624bc404fa744211d6d`; other producing commits and per-file hashes are in the package manifest.

## Citation and license

Please cite: James Lott and Vahraz Honary, **“Embedded Evaluation of Task Admission Coalescing in Decentralized Multi-Robot Systems,”** submitted manuscript, 2026. Use the paper's published bibliographic record when available.

Author-owned code, original data, and original figures in this release are available under the [MIT License](LICENSE). Citations and third-party works referenced by the study remain subject to their own terms.
