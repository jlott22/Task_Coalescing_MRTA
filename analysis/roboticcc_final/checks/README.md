# Final consistency audit

The final manuscript audit contains 50 claim rows covering the Abstract, Results and Discussion, Conclusion, both tables, and numerical figure captions/annotations.

- 13 rows match exact integer, direction, coverage, or formula results.
- 37 rows match the final data with display rounding only.
- 0 genuine numerical discrepancies were found.
- 0 numerical derivations were unresolved or ambiguous.

`figure_data_audit.csv` and `table_data_audit.csv` contain only passing checks. Figure 2 contains all 48 treatment points and all pointwise x/y intervals, with six incomplete common-completer cohorts labeled. Figure 3 contains the exact eight HIPC/medium platform-trace rows and retains adverse RP2040 trace 0001.

Interpretation and wording cautions:

- The Abstract's 3,000 causal AGX missions is the planned/retained design count; 2,940 completed and 60 are retained algorithmic noncompletions.
- Hardware comparisons are descriptive tested-platform effects. Runtime, communication timing, and lineage differ, so the package does not claim an isolated processor-speed effect.
- The manuscript phrase "team travel" refers to `total_team_steps`, not measured physical distance or energy.
- The statement that high-load RP2040 HIPC does not preserve the medium-load benefit means the joint work/latency/mission benefit is absent: work is +7.39% and mission duration +4.61%, although mean latency is -6.18%.
- The source manuscript still contains author-input placeholders for detailed AGX/RP2040 hardware configuration and the public archive URL/version. They are not numerical data discrepancies.
- Figure 2 uses the publication axes (work on x, latency on y). The manuscript caption is axis-neutral.

Re-run the audits from the package root with:

```text
python provenance/build_package.py
python provenance/build_claim_audit.py
```

Audit statuses mean `MATCH` for exact agreement and `ROUNDING_ONLY` when the manuscript is a correctly rounded display of the stored value.
