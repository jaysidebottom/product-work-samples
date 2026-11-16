# Crucible: Experiments in Evolving AI-Agent Prompts

**Jeffrey Sidebottom · Personal experimental project · Historical evidence and offline inspection tools**

Crucible explored whether systematic changes to agent instructions could produce repeatable improvements worth the cost of generating and evaluating them. It grew out of [Gemma](../gemma/README.md), where agent coordination, memory, practice, and breeding ideas were already being developed.

The project treated prompts as experimental artifacts: generate a change, state its hypothesis, evaluate it, compare it with the baseline, and decide whether to keep it. The work produced mutation and crossover machinery, benchmark evaluation, selection controls, and preserved experiment records. It did not establish generalizable capability gains.

## My contribution

I originated the idea and owned the mutation plan, promotion formula and criteria, experimental direction, and interpretation of results. I also owned the broader product and system decisions. The code was implemented with LLM assistance under my direction. Models used to generate candidates or perform benchmark tasks were experimental components, separate from that coding assistance.

## Problem and scope

The intended user was someone configuring specialist agents who wanted a more systematic alternative to ad hoc prompt editing. A better instruction might improve a recurring task, but a convincing change also had to survive regression checks and justify its evaluation cost.

The experiment changed agent instructions, not underlying model weights. The selected example focuses on a backend agent and two evaluated task areas. Memory and XP were separate mechanisms whose effects should not be folded into a breeding claim.

## From random variation to explicit hypotheses

| Mechanism | Experimental question |
|---|---|
| Exploit mutation | Will a targeted change address the failure already observed? |
| Contrast mutation | Would a different mechanism solve the same weakness better? |
| Section-level crossover | Can changes in different instruction sections be combined usefully? |
| Deletion or knockout | Is an instruction contributing value, or adding burden and noise? |
| Operator history and section tracking | Which changes are worth testing next, given the recorded results? |

The selected cycle contains exploit, contrast, and crossover artifacts. Deletion/knockout and operator tracking belong to the broader implementation; this example does not supply outcomes for every operator.

## How mutations earned promotion

I designed the evaluation policy around both the size of an improvement and the evidence behind it. The archived promotion gate required a one-sided Welch p-value below 0.05 and an absolute mean-fitness increase greater than 0.02 for specialists or 0.05 for the director, alongside applicable regression controls. Fitness combined functional acceptance, judged quality, completion, and resource efficiency, with different scoring branches for failing and more successful runs.

The experimental architecture linked failure diagnosis to mutation briefs, baseline calibration, artifact checks, benchmark execution, and a recorded selection decision. Exploit and contrast candidates tested competing mechanisms; deletion questioned whether accumulated instructions helped; crossover tested combinations. Adaptive scheduling and confirmation runs attempted to control evaluation expense.

Regression controls and prompt-size management were explicit parts of that design. Gemma's cycle runner re-evaluated the baseline alongside candidates; the later Crucible archive reused calibration to reduce evaluation work. Repetition checks, section-growth limits, and scheduled deletion/knockout candidates challenged instruction bloat instead of allowing mutations only to add more text.

The [experimental-method deep dive](methodology.md) details the mutation logic, exact scoring weights and promotion equations, actual benchmark checks, calibration behavior, and cost trade-offs. It distinguishes the later archived evaluator from the earlier featured experiment.

## A concrete experiment

The [featured experiment](experiment.md) compares a generic backend prompt with domain-specific instructions and a workflow-ordering alternative. It includes the complete preserved prompts, exact diffs, and all 20 available evaluation events for the three selected candidate IDs.

The exploit candidate had higher recorded mean acceptance on the targeted middleware benchmark: 50% versus the baseline's 31.25%. That observation is exploratory, not a validated improvement claim. The candidate labeled crossover was actually byte-identical to the baseline. Its different recorded scores illustrate why labels and score summaries alone are insufficient evidence.

## Product and evaluation trade-offs

- Targeted instructions made the mutation hypothesis concrete, but increased the risk of fitting a known benchmark.
- Composite fitness represented several concerns, but could obscure the distinction between passing functional checks and looking efficient or well-written.
- Adaptive evaluation and early stopping aimed to control expense, but complicated interpretation of unequal run coverage.
- Promotion gates expressed a desire for repeatable improvement. They could not compensate for weak checks, missing provenance, or absent held-out validation.

## Why the work stalled

Breeding usage and costs became unsustainable for continued personal experimentation. Continuing also required substantial time to refine the benchmarks and baseline formulas. Those resource constraints stalled the work. The evaluation findings describe questions still being investigated; they were not a finding that the underlying approach could not work.

## Inspect the work

1. [Mutation science, scoring formulas, and benchmark design](methodology.md)
2. [Architecture and experimental controls](architecture.md)
3. [The experiment, prompts, and recorded outcomes](experiment.md)
4. [Retrospective and proposed evaluation redesign](retrospective.md)
5. [Selected implementation](src/README.md) and [verification](verification.md)

From the repository root, using Python 3.9+:

```sh
python3 -B projects/crucible/src/inspect_experiment.py
python3 -B -m unittest discover -s projects/crucible/tests -v
```

The inspector verifies prompt hashes and diffs, then summarizes recorded values. It does not launch models or rerun benchmarks.

[Gemma case study](../gemma/README.md) · [Portfolio index](../../README.md)
