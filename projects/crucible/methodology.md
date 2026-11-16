# Mutation Design, Fitness, and Promotion

[Case study](README.md) · [Architecture](architecture.md) · [Recorded experiment](experiment.md)

I designed the mutation plan and promotion formula to turn prompt editing into a repeatable experimental process: diagnose a weakness, propose competing mechanisms, measure their effects, and require evidence before replacing the baseline. Code implementation was LLM-assisted under my direction.

This page describes the inspected archived breeding implementation. It evolved over time; its final scoring and scheduling code is not a version-pinned reconstruction of the March 29–30 experiment. That experiment's recorded scores remain historical observations and are not recalculated using later formulas.

## 1. Diagnose a failure before generating a change

The failure-ranking helper examined baseline evidence along three axes: whether the agent produced usable artifacts, whether those artifacts passed acceptance checks, and their composite fitness. It flagged first-pass materialization below 0.8, acceptance below 0.7, and fitness below 0.6, ranking each by one minus the corresponding score. Failed check names supplied more concrete context than the score alone.

A mutation brief recorded the target benchmark, failure evidence, instruction section, mechanism, role, and expected effect. The aim was to make each change answer a question that could be examined afterward.

| Strategy | Hypothesis being tested | Implementation approach |
|---|---|---|
| Exploit | A rule aimed at the observed failure will improve that behavior | Select a mechanism appropriate to the failure and modify a relevant section |
| Contrast | A different mechanism may address the same failure better | Choose a different mechanism category, retaining the same underlying problem |
| Injection or substitution | Missing guidance or an ineffective rule is limiting performance | Add or replace instructions inside a section |
| Deletion / knockout | Accumulated instructions may add noise or constrain useful behavior | Remove material; periodically consider large sections with weak improvement history |
| Crossover | Useful changes in different sections may work together | Assemble selected sections from two parent prompts |
| Cross-pollination | A useful pattern from another agent may transfer | Rank source sections for mechanism relevance, failure relevance, and recorded performance |

Operator history influenced subsequent choices, including avoiding repeated unproductive mechanisms. Section tracking estimated where another edit might help. These were adaptive search heuristics; their scores did not establish causal contributions of individual sections.

For the featured experiment, the competing hypotheses were concrete: add domain rules for middleware behavior, or make execution order explicit before implementation. The first changed several instructions at once. It therefore tested a bundle of guidance, not the isolated effect of a single rule. The crossover-labeled artifact turned out to equal baseline, so that record cannot demonstrate the intended combination.

## 2. Validate the experimental artifact

The inspected validator rejected empty or unchanged mutations, changed section headings, extra headings, repeated four-word sequences appearing at least three times, and extreme growth beyond 15 times the original length. Prompt hashes and stored variants supported identity checks and retrospective comparison.

Those controls operated at particular stages. A valid section mutation does not guarantee that the final assembled prompt contains it. The crossover discrepancy illustrates the need to verify final prompt bytes as well as generation metadata. Neither mutation validity nor a plausible hypothesis establishes a performance improvement.

### Prompt bloat was an experimental variable

Managing the instruction Markdown was part of the search design. Repeatedly adding rules could make every subsequent execution more expensive and introduce contradictory or distracting guidance. The system therefore supported subtraction as well as addition:

- **Structural validation:** preserve section headings, reject repeated four-word sequences, and cap extreme section growth. The inspected archive's cap is 15× the original section length; older documentation records tighter caps, so there was no single unchanged limit throughout development.
- **Scheduled knockout pressure:** when mutable content has at least 30 lines, consider a deletion candidate every fourth cycle or after a recent concentration of additive operators. The actual growth trigger counts at least three injection/benchmark-directed entries among the last nine history entries after filtering for exploit/contrast roles; it does not measure a literal 20-line increase, despite a declared growth-threshold constant.
- **Choose where to subtract:** rank sections by `line count × (1 − historical improvement rate)`, favoring large sections with weak recorded benefit. The third candidate slot can become a deletion experiment instead of a crossover.
- **Evaluate the shorter candidate:** deletion produces a candidate that must compete on the benchmark and promotion policy. Shorter text is a hypothesis about efficiency and clarity, not an automatic improvement.

These controls managed the evolving `SKILL.md` prompt. The [OpenViking-inspired memory work](../gemma/architecture.md#openviking-inspired-context-management) addressed a related but separate source of context growth: retrieving and maintaining accumulated knowledge.

## 3. Calibrate against actual tasks

### Fresh cycle controls and regression protection in Gemma

Gemma's inspected runner evaluated **the baseline alongside the new candidates in each cycle**. It constructed a common run plan containing core benchmarks at adaptive depth, up to four additional regression benchmarks not already covered by the core plan, and observational tasks when a refresh was due. Baseline and candidate runs followed that plan, subject to execution and budget limits. Fresh baseline results supplied the control scores against which mutations competed.

This is distinct from rerunning initial calibration. Gemma could reuse calibration metadata when the instruction hash matched, while still executing the baseline as a cycle participant. Thus “re-baselining each cycle” accurately describes the fresh control comparison, but “forcing a full recalibration of every benchmark each cycle” would overstate the inspected implementation.

Regression protection had several layers:

| Layer | Implemented protection |
|---|---|
| Baseline trust | At least two valid capability runs establish trusted calibration; breeding requires at least three trusted core benchmarks |
| Fresh comparison | Promotion uses current-cycle baseline and candidate scores from trusted core tasks, excluding provisional, observational, and invalid execution results |
| Regression coverage | Additional regression tasks enter the run plan without duplicating tasks already in core coverage |
| Director veto | A candidate is blocked if an evaluated director regression run has acceptance below 0.5 |
| Confirmation protection | The director regression gate is reapplied across original and confirmation runs, preventing the extra statistical test from bypassing it |

Provisional tasks could remain visible for regression assessment while being excluded from promotion arithmetic. These safeguards were meaningful engineering work; their protection still depended on the checked behaviors and completed coverage.

### Later Crucible calibration reuse

The later Crucible archive made a different resource trade-off: it removed the baseline from the per-cycle candidate run list and used stored calibration scores as the comparison control. The fresh-baseline Gemma path and the later calibration-reuse Crucible path should not be collapsed into one universal rule.

Baseline calibration evaluated the incumbent prompt and retained benchmark-level acceptance, fitness, resource measurements, and run details. Candidate evaluation reused that reference. The inspected runner could reuse calibration when the prompt hash was unchanged. Prompt identity is necessary but cannot by itself rule out changes in models, checkers, or surrounding execution conditions.

The featured evidence preserves two baseline runs for each of its two represented benchmarks. A later archived calibration function executes one run per benchmark despite a separately declared calibration-count setting. Run counts must therefore come from the relevant records and execution path, rather than assuming every configuration constant was honored.

| Benchmark | Requested behavior | Checks in the inspected definition |
|---|---|---|
| Middleware pipeline | Composable request-ID, logging, rate-limit, authentication, and error-boundary middleware | Python parsing, app discovery, request-ID response header, rate-limit response and retry header, missing-auth rejection, error-response inspection, test-file presence, and a test command |
| Event-sourced ledger | Account creation, immutable events, reconstructed balances, overdraft prevention, transfers, and history | Python parsing, app discovery, account/deposit/balance/overdraft/transfer/history checks, test-file presence, and a test command |

The judging rubrics also asked about properties such as middleware composability, transfer atomicity, and historical projections. A requested property and a rubric question are not equivalent to an exhaustive executable check. For example, the middleware error probe could pass for a non-500 response without demonstrating that a forced server exception was handled correctly. Benchmark and checker refinement was substantive ongoing engineering work.

The architecture later supported named suites and separate core versus observational tasks. The inspected backend-suite-v2 manifest contains eight core tasks and two observational tasks; that later frontier suite is distinct from the featured Haiku comparison. Core tasks drove promotion; observational tasks monitored breadth and drift. They were not an implemented independent held-out promotion gate.

## 4. Score functionality, quality, and resource use

The archived specialist composite used the following weights. The director placed more weight on judged quality and completion, and less on efficiency.

| Signal | Symbol | Specialist weight | Director weight |
|---|---|---:|---:|
| Fraction of acceptance checks passed | A | 0.20 | 0.20 |
| Token efficiency | E_token | 0.12 | 0.08 |
| Tool-call efficiency | E_tool | 0.08 | 0.04 |
| Turn efficiency | E_turn | 0.10 | 0.08 |
| Judged quality | Q | 0.40 | 0.45 |
| Completion credit | C | 0.10 | 0.15 |

For the full specialist composite:

```text
F = 0.20A + 0.12E_token + 0.08E_tool + 0.10E_turn + 0.40Q + 0.10C
```

The function applied three scoring branches:

1. **A = 0:** fitness is capped at 0.10 and computed from one quarter of the weighted quality contribution.
2. **0 < A < 0.5:** fitness includes only weighted acceptance and quality.
3. **A ≥ 0.5:** use the full composite and set completion credit to 1. With Q ≥ 0.8, efficiency ratios compare baseline consumption with candidate consumption, capped at 1.

For example, token efficiency is `min(1, baseline tokens / max(1, candidate tokens))`. With missing baseline token or tool data, the implementation uses 0.5; absent usable turn-reference data gives turn efficiency 1. When Q is below 0.8, token and tool terms remain at 0.5 while the turn term becomes zero. Thus the code retains neutral token/tool contributions even though its comments describe withholding efficiency credit for low quality. The `completed` argument does not control completion credit in this branch; acceptance does.

The weighting expressed a product preference: functional and judged quality should matter alongside resource consumption. It also made formula calibration important. Passing half the checks triggers a discrete branch change; judged quality carries substantial weight; and the resulting number is not a probability of task success.

## 5. Require a practical difference and a statistical gate

The preserved [selection implementation](src/evolution.py) computes a one-sided Welch comparison between candidate fitness scores and baseline fitness scores:

```text
delta = mean(candidate) − mean(baseline)
t = delta / sqrt(variance(candidate)/n_candidate + variance(baseline)/n_baseline)

promotion gate = (one-sided p < 0.05) AND (rounded delta > threshold)
```

The archived runner sets the threshold to **0.02 for specialists** and **0.05 for the director**. These are absolute differences on the fitness scale—two or five percentage points—not relative percentage improvements. The helper rounds delta to four decimal places before the strict comparison. It returns a non-promoting result when either sample has fewer than two observations or the standard error is zero.

The two requirements serve different purposes: the delta threshold encodes the minimum change the policy values; the statistical gate considers the observed difference relative to sample variability. The implementation used Welch–Satterthwaite degrees of freedom. Its p-value is not the probability that the candidate is better, and it does not correct for repeatedly searching and selecting candidates on the same tasks.

Additional controls included:

- A destructive-regression helper flags any evaluated benchmark whose candidate mean falls below 50% of its positive calibration baseline. Missing candidate results are skipped, so absence of a flag does not prove coverage.
- For director candidates, the runner additionally requires acceptance of at least 0.5 on each evaluated regression run. Unevaluated regression benchmarks are skipped.
- Among candidates that clear the main gate and applicable checks, the runner selects the greatest positive delta.
- A no-winner confirmation path considers a candidate with at least 0.05 higher mean, p ≤ 0.20, and no recorded regression-check block. It adds two candidate runs on the strongest-signal benchmark and pools them with prior candidate results, reusing calibration baseline scores. This is adaptive follow-up, not independent held-out confirmation.

These rules document the designed decision process. They do not establish which gate caused the featured cycle's no-winner record; its lineage is incomplete.

## 6. Manage the cost of the search

The evaluation planner allocated more repetitions to weaker core benchmarks and fewer to the others. Round-robin execution, early stopping, calibration reuse, and selective confirmation attempted to spend runs where they could affect a decision. The early-stop helper projected perfect remaining scores and applied the promotion test; this was an implemented heuristic, not independently verified here as a statistical impossibility bound.

These policies also affected interpretation. Pooling runs gives more influence to tasks with more repetitions, reused baselines may age, and selective confirmation favors already promising signals. Cost control and experimental rigor were coupled design problems.

The work stalled because breeding usage and costs were unsustainable for continued personal experimentation, alongside the time required to refine benchmark and baseline formulas. This is the author's account of the practical constraint. The remaining evaluation questions were unfinished work; the project did not establish that the underlying approach had reached a proof-point dead end.

## Three different meanings of “tests”

**Agent benchmarks** evaluate generated work. **Breeding checks** evaluate artifacts, fitness, and promotion eligibility. **Software regression tests** check that the evaluator and its helpers behave as intended. The portfolio's seven Crucible checks exercise the distributed evidence and logic extracts; they do not rerun historical model benchmarks or verify the entire original execution system.

The [featured experiment](experiment.md) supplies observations. This methodology page explains the machinery and decisions behind the broader investigation. The [retrospective](retrospective.md) distinguishes implemented controls from proposed follow-up work.
