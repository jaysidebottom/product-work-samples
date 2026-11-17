# Experiment: Domain Rules, Workflow Order, and Crossover

[Case study](README.md) · [Evidence files](evidence/README.md)

**Historical observations from March 29–30, 2026.** This example tests two ways to address a backend agent's weak middleware performance. The domain-rules candidate recorded a higher target-benchmark mean, but the available evidence does not establish a transferable improvement or a successful promotion. Inspection also found that the stored crossover prompt is identical to baseline.

## Baseline and hypothesis

The preserved baseline belongs to the `anthropic/claude-haiku-4-5-cli` lineage and records subscription-backed CLI execution. It was calibrated on March 29. Its complete [instruction file](evidence/baseline-prompt.md) hashes to the recorded short prompt identity `b581adae5dfa`.

The original `Your Role` section provided general responsibilities: write backend services, design APIs, build middleware and authentication, debug, and review code. The target middleware task concerned a composable pipeline with request IDs, logging, rate limiting, authentication, and error boundaries. The baseline's two recorded evaluations averaged 0.3125 acceptance and 0.2375 fitness.

The exploit hypothesis was to replace general responsibilities with domain-specific rules. The contrast hypothesis was to change workflow sequencing instead. Both targeted the same observed low-fitness area.

## The three artifacts

| Label and ID | Recorded intent | Actual instruction change |
|---|---|---|
| Exploit: `mut-783b94e5-01` | Add domain-specific rules | Replaces `Your Role` with explicit middleware ordering, error isolation, timeouts, contract enforcement, and resource-cleanup guidance |
| Contrast: `mut-a6e43e4f-02` | Reorder workflow steps | Replaces `Primary Languages & Frameworks` with language-specific instructions to specify execution sequences before implementation |
| Crossover: `cross-b581adae-03` | Combine the two parents at section level | **None: the stored full prompt is byte-identical to baseline** |

Read the [exploit prompt](evidence/exploit-prompt.md) and [exact diff](evidence/exploit.diff), the [contrast prompt](evidence/contrast-prompt.md) and [exact diff](evidence/contrast.diff), and the [crossover prompt](evidence/crossover-prompt.md).

The exploit change was substantial: it changed several instructions at once. Its outcomes cannot isolate whether ordering, timeouts, error handling, or another added rule helped. Some rules also prescribe fixed values or language-specific terminology, which could constrain otherwise reasonable solutions.

The crossover metadata identifies the two parents and swap indices `[5, 1]`. That metadata does not match the stored outcome. The evidence establishes the artifact discrepancy; it does not conclusively locate the historical cause in section indexing, assembly, or archival behavior.

## Recorded outcomes

Acceptance is a fraction of checks passed, not a fraction of complete tasks successfully solved. Fitness is the historical composite score; it is not a calibrated success probability. Means below are calculated from the included records. Candidate counts are audit-event counts, not verified counts of independent trials.

| Prompt | Benchmark | Records | Mean acceptance | Mean fitness |
|---|---|---:|---:|---:|
| Baseline | Middleware pipeline | 2 | 0.31250 | 0.23750 |
| Exploit | Middleware pipeline | 4 | 0.50000 | 0.53750 |
| Contrast | Middleware pipeline | 4 | 0.37500 | 0.29250 |
| Crossover label, baseline text | Middleware pipeline | 4 | 0.43750 | 0.41750 |
| Baseline | Event-sourced ledger | 2 | 0.38885 | 0.27780 |
| Exploit | Event-sourced ledger | 4 | 0.44440 | 0.38390 |
| Contrast | Event-sourced ledger | 0 in preserved events | Not available | Not available |
| Crossover label, baseline text | Event-sourced ledger | 4 | 0.44440 | 0.37515 |

The table includes every `breeding_run_completed` event found for these three candidate IDs in the preserved audit file, plus the baseline records for both represented benchmarks. It does not imply that these were the only tasks attempted or that every attempt emitted an event.

The contrast candidate's middleware acceptance alternated between 0.25 and 0.5. The crossover-labeled observations also varied despite using the baseline text. These observations weaken a simple interpretation that the exploit's higher mean must have been caused by its new rules.

## Selection outcome

A cycle-completed record immediately after the final included evaluation reports three tested variants and no winner. Its association with this group is inferred from timing and sequence: the cycle record lacks model and variant identifiers. The reported `fitness_delta: 0` is a cycle field, not evidence that every candidate's measured difference was zero.

The broader archived implementation required statistical significance and a minimum mean-fitness difference, with regression controls around selection. The preserved cycle record does not identify which condition prevented promotion here. Recomputing a test from this partial extract would not establish the historical decision.

## Limits on interpretation

- **Lineage:** model attribution comes from the archive directory and baseline metadata. Candidate evaluation events do not independently record the model, prompt hash, run index, or retry status.
- **Coverage:** the baseline had a broader suite. The extract contains only baseline tasks represented in the selected candidates' available events; it cannot support a suite-wide comparison.
- **Selection:** candidates targeted known weaknesses and were evaluated adaptively. This is exploratory evidence, not a preregistered or held-out confirmation.
- **Measurement:** acceptance depends on the checks' coverage. Composite fitness also depends on other recorded scoring inputs. Full judge inputs and run workspaces are not included, and fitness is not recomputed.
- **Prompt context:** full prompt files are preserved, but they reference generic container resources and memory tools. The original surrounding context is not reproduced here, so experimental isolation cannot be certified from prompt text alone.
- **Artifact integrity:** the crossover is an unchanged baseline prompt, not evidence that combining the proposed mutations helped.

## What this experiment contributes

It makes the mutation reasoning inspectable, preserves an alternative that performed less favorably, and exposes a discrepancy between metadata and actual instructions. The next methodological step would be a fresh, tightly controlled comparison with verified final prompt identity and independent evaluation tasks. That is a proposed redesign, not a claim that it was performed.

Run the [offline inspector](src/inspect_experiment.py) to verify hashes, diffs, and descriptive summaries. Continue to the [retrospective](retrospective.md) for how these findings affect the experimental design.
