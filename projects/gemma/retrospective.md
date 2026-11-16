# Gemma Retrospective

[Case study](README.md)

Gemma made agent coordination, memory, and progression concrete enough to inspect. Its central unresolved question is whether accumulated experience translates into better outcomes on new work.

## Why the work stalled

The practical constraints were unsustainable usage and costs for breeding cycles, and the time needed to continue refining benchmark and baseline formulas. Those constraints explain the pause in the work. The technical findings below identify what remained to investigate; they do not establish that the approach had reached a proof-point dead end.

## What the implementation supports

Explicit task and result records make a coordinated workflow inspectable. Separating capability matching, availability, and routing policy makes individual decisions testable. Persistent memory creates a mechanism for carrying information across tasks. These are implementation properties; they are not measurements of productivity or learning.

Separating breeding, memory, and XP was an important experimental decision. A changed prompt, a useful recalled lesson, and a different routing decision can each affect results. Combining them in one before/after comparison would obscure the cause.

## Where the assumptions were too strong

**Experience was treated too much like expertise.** The progression code grants a medium, good-quality practice task three XP. Failure can still earn one XP. Full escalation also receives one XP because the minimum reward overrides a zero help multiplier. Those behaviors can represent participation, but should not independently establish mastery.

**Quality proxies could reward activity.** The historical chat-award path uses response length and recognized error strings as quality signals. A long response can therefore earn an excellent rating without external verification. Quest acceptance checks provide a more direct signal, but their coverage still determines what a score means.

**Levels changed behavior before their meaning was validated.** Higher tiers encouraged confidence; scores also influenced routing and quest eligibility. This creates a risk that additional activity earns both a stronger label and more responsibility without a corresponding capability check.

**Progression arithmetic needed stronger lifecycle tests.** The included historical decay function can charge the same elapsed period twice when called on already-decayed XP. In a fixed 90-day-idle example, a level-50 skill becomes 47 and then 45 at the same evaluation timestamp. The inspected daily integration records a decay timestamp but does not use it in that calculation. The sample preserves this limitation so the finding remains reproducible.

## How I would evaluate the design differently

This is a retrospective proposal, not implemented or scheduled development.

1. Separate an activity ledger from a mastery assessment. Attempts can earn experience; mastery should require independently checked outcomes.
2. Keep capability assessments specific to a skill and model/configuration. Distinguish missing evidence from a middling score.
3. Retain lessons with their originating task, verification result, and applicable context. Test whether retrieval helps on new tasks.
4. Compare a fixed baseline against memory alone, then memory plus a progression/routing policy. Freeze breeding during that comparison.
5. Measure unseen-task success, intervention required, regressions, latency, and total evaluation cost. Define the decision rule before observing results.

The useful product question is whether the system makes an operator's work more reliable and easier to supervise. A higher level is only useful if it helps answer that question.

The [Crucible experiment](../crucible/experiment.md) explores a related issue: a promising score change can coexist with incomplete evidence and an unexpected prompt artifact.
