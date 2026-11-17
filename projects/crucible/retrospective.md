# Crucible Retrospective

[Case study](README.md) · [Featured experiment](experiment.md)

The strongest part of Crucible was making prompt changes into explicit experiments. Exploit and contrast candidates gave competing explanations for the same weakness. Crossover explored combinations, while deletion and knockout mechanisms asked whether additional instructions were helping at all.

## Why the work stalled

The practical constraints were unsustainable usage and costs for breeding cycles, and the time needed to continue refining benchmark and baseline formulas. Those constraints explain the pause in the work. The technical findings below identify what remained to investigate; they do not establish that the approach had reached a proof-point dead end.

## Productive directions

**Hypotheses attached to changes.** A mutation brief stated the failure, target section, mechanism, and expected effect. That makes a candidate easier to criticize and learn from than a plausible-looking rewrite.

**Functional evidence before attractive scores.** The implementation distinguished valid task failures from runner failures, added acceptance thresholds, and checked regressions. These choices acknowledged that a persuasive output or strong composite score could still hide a functional problem.

**Preserved artifacts.** Prompt files, metadata, and evaluation records enable retrospective scrutiny. In the featured experiment, byte-level comparison exposed a crossover artifact that did not match its description.

## Wrong paths and unresolved assumptions

**More specificity could fit the test.** The exploit candidate addressed a known weakness with several new rules. A higher mean on that task does not show transfer to unfamiliar work, and the multi-part edit makes causal attribution difficult.

**Crossover intent did not guarantee crossover output.** The stored crossover prompt equals baseline. This calls for checks on the final assembled prompt, not just parent metadata or individually validated mutations.

**Composite fitness could conceal the product outcome.** Acceptance, judged quality, and efficiency are different signals. A single weighted score makes ranking convenient, but can make it harder to explain whether the system actually completed more useful work.

**A statistical gate was not enough.** The archived gate combined a one-sided Welch test with a minimum difference. Later project notes identified a mismatch with the small, binary, single-run SWE-bench regime. Repeated adaptive search and incomplete held-out validation also limited the strength of improvement claims. The intended holdout promotion guard was not implemented.

**Evaluation economy introduced interpretation costs.** Adaptive depth and early stopping reduced unnecessary runs in principle. Unequal coverage, confirmation selection, and incomplete run identifiers made retrospective comparisons harder. No cost-saving percentage is claimed here.

## Proposed evaluation redesign

This is an explanation of what the findings imply, not new implemented work.

1. **Define the outcome before the search.** Choose functional task success as the primary outcome; report latency, resource use, and other quality signals separately. Set the required practical improvement and budget in advance.
2. **Freeze the comparison.** Record the model/execution configuration, full effective prompt hash, benchmark and checker versions, memory policy, and run budget. Check the final assembled prompt for unintended changes or no-op candidates.
3. **Separate discovery from confirmation.** Use one task set to guide mutations. Evaluate a selected candidate on tasks withheld from mutation generation and scheduling. Keep memory and XP conditions fixed.
4. **Repeat matched comparisons.** Run baseline and candidate under comparable conditions on the same confirmation tasks. Preserve individual results, invalid attempts, retries, and intervention. Select an analysis suitable for the actual outcome and sampling design rather than reusing a gate unchanged.
5. **Keep a complete decision record.** Store why a candidate was rejected or promoted, which checks ran, and what evidence was missing. Treat missing evaluation coverage as missing evidence.

The project demonstrated the machinery for generating and examining competing instruction strategies. The available record supports that engineering and experimental work; it does not establish a generally superior evolved agent.
