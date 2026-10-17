# Producing provenance and corrections

**VERIFIED, local read-only audit.** Current checkout was `80c565dfaed53b1bf17e7624bc404fa744211d6d` when analysis began. Its corrected data reconcile to 3,000 AGX causal missions (2,940 complete/60 finite noncompletions), 3,000 zero-compute complete missions, and 96 planned RP2040 jobs (82 successful/14 terminal technical failures). No subsequent verified completed campaign is present. AGX execution ended 2026-08-16; latest successful hardware completion is 2026-08-28; September dates describe corrected export/archive snapshots, not new experimental runs.

## Source and configuration identities

| Producing scope | Commit | Attested source-tree SHA-256 | Result population |
|---|---|---|---|
| Four AGX v7 campaigns | `598485103ee270a27d8b684c0082e46e2ad53802` | `49b978dd91f3e30388d913f090454ec645459f246d8daa4e7e754127a13bfc7c` | Round1 trace 0–24, Round2 trace 25–49; causal and zero each 1,500/round |
| RP2040 v9 | `3fe1f578987088fc8f044741bd046ca4e5488267` | `4dc06c3d1edcae1722ad3295e412fa863ced136415528bb840cd0b0c421724fe` | 26 preserved successes / 13 complete Eager–Count blocks |
| RP2040 v10 continuation | `a3490a7748d852af5b05f1df3caa1f86a44dda17` | `895b1584cf51aa2adf31aa5c197f1e24514af08667b507b055c39955e85d77d6` | 70 scheduled remaining jobs, 56 successful; final 14 failures retained |

The AGX campaign-start manifests attest 86 individual source file hashes. **All 86 match the actual Git blobs at 5984851.** The aggregate tree identity is preserved as campaign-attested metadata, not misrepresented as a complete filesystem hash. Hardware schedules preserve aggregate source identity rather than the same 86-file list.

**All six frozen campaign configurations reconcile.** AGX raw producing config bytes match recorded hashes. Hardware hashes are of canonical **effective configuration** after adding the recorded boards, core affinities, and binding-file hash; raw hardware config file hashes are different by design (`study/causal/model.py`). [frozen_configs](frozen_configs) includes original Git-blob configs and reconstructed effective hardware configs, with exact hashes in [campaign_provenance.json](campaign_provenance.json).

The manifest index SHA-256 is `c837091d8f78be01f270e6f2bfc71856afdbddc664f68a4bdb6ee96f023f09e2` in all six campaigns and matches the producing Git object. It describes 50 scenario files and 150 load-specific release files with 50 shared independent trace blocks. Full manifest index and one compact example scenario are included. Windows checkout CRLF conversion is not mistaken for changed scientific source: the audit hashes Git blob bytes.

## Lineage comparison, rather than trusting current prose

`git diff 5984851 80c565d -- known_visit_sim` changes only a test's fixture path; simulator/desktop allocator production code is identical. Therefore present simulator line references in the methods dossier genuinely describe v7 and hardware authoritative host semantics. This conclusion does **not** extend to all native code or documentation.

Between AGX v7 source and the actual v9 hardware source, native checkpoint support changed materially: mature state synchronization, restored admission/epoch handling, ACBBA processing omitted peer claims before inactive-target validation, PI path repair on every valid callback (including unchanged ties), and HIPC tuple-shaped peer signature retention. V9 was explicitly restarted without pooling aborted earlier hardware lineages. This is why using the native runtime at 5984851 to reproduce archived v9/v10 calls would be wrong.

Between v9 and v10, only two device source files changed: `device/common/replay_worker.py` and `device/native/collaborative/runtime.py` (91 insertions, 22 deletions). V10 lazy-loads the active allocator, collects after integrity checks and before timed entry, and preallocates exact-length transfer buffers while retaining chunk sequencing. Desktop allocator semantics and native algorithm files are unchanged across this cutover. Timing may nevertheless differ through heap/automatic-GC effects. Source diff summary is included in [verification.json](verification.json); implementation explanation is supported by `docs/provenance/RP2040_HEAP_FIX_20260817.md`, which is a historical engineering report, not newly repeated hardware verification.

| Runtime lineage | Build ID | Module-set SHA-256 |
|---|---|---|
| v9 | `micropython_1_24_o0_coalescing_collaborative_b6c6d632d015` | `b49e0857162bf1359651eb2699491dddee2a20e995b5f44760b24536fd70abe4` |
| v10 | `micropython_1_24_o0_coalescing_collaborative_eb924f353fdd` | `4422cab60818ed3721ee228e6a62a4c5aee71d4ea1dc2653d9f99c24068406c2` |

Both attest firmware SHA-256 `c64e31b161421148abdd87a4eea541048456e8e99e6db08407499b0dfa7bfb7c`. Boards A/B/C/D attest UIDs `e4621cb30b16392f` / `e4621cb30b2b352f` / `e4621cb30b43372f` / `e4621cb30b4b372f` respectively. Build identities are metadata-verified, not binaries reconstructed on this laptop.

## Hardware pairing and platform comparison

[hardware_block_lineage.csv](hardware_block_lineage.csv) shows all 48 planned allocator×load×trace blocks. Of these, 38 have both policy successes, six have one success, and four have none. **All 38 complete blocks are within the same physical board and within the same v9/v10 lineage; zero are mixed.** The 26 preserved v9 results were sealed/excluded as 13 full blocks, avoiding a successful Eager-v9/Count-v10 comparison. Workload/policy mix across lineages remains uneven, so pooled v9-v10 performance differences are not a clean runtime effect.

The schedules alternate Eager/Count order across board blocks and preserve the actual assigned board. Across-platform primary workload manifests match, but communication differs: AGX runner retains ±10 ms jitter around 40 ms; hardware runner removes it. AGX Python hash seed is paired runtime modulo 2³²; hardware uses 0. Native MicroPython representations and checkpoint architecture differ from desktop Python. Accordingly matched-scenario comparisons support **observed effects in two execution settings**, not an isolated clock-speed explanation, and whole-mission work ratios may involve different call counts/state trajectories as well as implementation execution speed.

## Statements to correct or qualify

| Prior/current shorthand | Evidence-based replacement |
|---|---|
| August timeout, destructive reset, small planning horizon | Use producing B4/W10; initial eight together, strict online batching, no piggyback/final-release flush, conditional residual; retained allocator state, uncapped full known task pool. |
| Current architecture says software never populates RP2040 fields | The archived AGX exporter actually retains legacy RP2040-named rounded host-proxy aliases. Select work by provider and use AGX-named measured work for AGX. |
| Four boards are the four simultaneous robots of a mission | Each board executes a different whole mission with four logical checkpoints, one resident native runtime. Parallelism within a mission is modeled virtually. |
| AGX/RP2040 differ only in measured allocation speed | They also differ in peer-message jitter, runtime/hash-seed setup, native representation/checkpoint path and hardware operating conditions. |
| V9/V10 policy timing is necessarily confounded | Actual complete paired blocks have the same board and lineage. Report lineage; the remaining platform/missingness limitations still apply. |
| `recovery_state_change_count` proves that many state changes | It counts truthy recovery return flags; some returns mean a valid route or claimable task already exists. |
| Completed task latency describes noncomplete mission | It covers only completed tasks and must not summarize all 50 requirements. Report noncompletion before success-conditional latency/work. |
| Source or local loopback proves physical hardware correctness | Source/hash checks validate lineage; summary metadata attest accepted parity. Missing raw transactions and unavailable boards prevent full independent physical revalidation. |

## Missing artifacts and local reproducibility

The compact exports carry hash indices for raw trial files but the original per-call transaction/state streams are not contained here. Hardware effective configs require `study/native_gates/environment/native_environment_report.json` and `study/native_gates/preflight/native_preflight_report.json`; neither corresponding producing report, deployment attestation/binaries, nor original `configs/local/agx_board_bindings.json` bytes are present. Board bindings can be reconstructed from the schedule for effective config hashing, but that does not reproduce the original external file or physical inspection. Missing gate reports would resolve recorded CPU/power/governor/firmware/timer-resolution details; raw transactions would allow precise state/timing/parity reconstruction of individual calls. No superseded `paper_v2_data_bundle` environment is substituted.

Run locally from repository root:

```powershell
python roboticcc_handoff/methods/audit_methods.py
```

It reads exports and historical Git objects, verifies 86 source hashes, six campaign config identities and the shared manifest index, checks board/lineage pairing, and regenerates compact evidence files. It writes **only** this methods directory; it neither connects to hardware nor modifies production code or historical data. Source excerpts and configs remain self-contained in the handoff even when the reader does not possess Git history. The root handoff manifest provides whole-package/export data hashes and its separate retained-outcome verifier result.
