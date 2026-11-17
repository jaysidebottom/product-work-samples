# Experiment Evidence

[Experiment narrative](../experiment.md)

These files are a reviewed extract from the historical Crucible experiment, not synthetic results. No raw operating logs, workspaces, or archive bundles are distributed.

| Files | Contents |
|---|---|
| [experiment.json](experiment.json) | Baseline metadata and selected run values; three candidate metadata objects; all 20 preserved completion events for those IDs; nearby cycle record; explicit lineage limitations |
| [baseline-prompt.md](baseline-prompt.md) | Complete archived baseline instruction file |
| [exploit-prompt.md](exploit-prompt.md) and [exploit.diff](exploit.diff) | Complete domain-rules candidate and exact change from baseline |
| [contrast-prompt.md](contrast-prompt.md) and [contrast.diff](contrast.diff) | Complete workflow-ordering candidate and exact change from baseline |
| [crossover-prompt.md](crossover-prompt.md) | Complete crossover-labeled artifact, byte-identical to baseline |

The four prompt files are unmodified artifact text. Their references to generic `/shared`, `/workspace`, and `/ipc` container paths are historical instructions, not personal machine paths or usable setup instructions. Statements such as “expert” and “production-quality” are prompt wording, not verified claims about the agents.

Baseline values come from a March 30 archive of a March 29 calibration. Candidate metadata and prompts come from the corresponding preserved variant archives. Evaluation values come from matching variant IDs in the audit record. Numeric values and timestamps are retained; unrelated records, runtime paths, verbose outputs, and personal environment data are omitted. This selection is not a complete original experiment environment.

Full SHA-256 values in `experiment.json` identify the distributed prompts. The baseline's first 12 hash characters match its recorded calibration identity. The offline inspector verifies these hashes and the two diffs. There is no crossover diff because its contents equal baseline.

No benchmark was rerun to prepare this sample. Candidate events lack some configuration and trial identifiers; therefore the inspector calculates descriptive means only. It does not infer independent trials, statistical confidence, or a historical promotion decision.
