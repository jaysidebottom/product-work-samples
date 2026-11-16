# Gemma: Building and Evaluating an Agent Team

**Jeffrey Sidebottom · Personal experimental project · Historical implementation with selected offline examples**

Gemma explored how a developer could coordinate specialist AI agents, preserve useful context between tasks, and inspect what the agents were doing. The project connected task routing, persistent memory, practice tasks, and skill progression into one system. Its most important evaluation question was whether those mechanisms produced more reliable work, rather than simply more activity.

This case study presents the system design and selected implementation. It does not claim validated productivity gains or customer adoption. The related [Crucible case study](../crucible/README.md) examines the prompt-evolution experiments that grew out of Gemma.

## Problem and hypothesis

The intended user was a developer directing AI-assisted work across specialties. A standalone conversation can produce an answer, but coordinating several agents raises additional questions: who should take the task, what context should they receive, how should dependencies and failures be handled, and what should persist afterward?

The hypothesis was that explicit roles, inspectable task state, and reusable experience could make this work easier to coordinate. A second hypothesis was that practice and skill records could help select work and adapt agent behavior. These were product hypotheses, not findings from customer research.

## My contribution

I originated the project and owned its concept, system design, scope, experiment direction, and evaluation decisions. I developed the mutation plan and promotion criteria that informed the breeding work carried into Crucible. The code was implemented with LLM assistance under my direction. AI coding assistance supported implementation; the product and experimental decisions were mine.

Models also performed tasks and generated experimental prompt variants inside the system. Those roles are distinct from the coding assistance used to implement it.

## A task through the system

1. The user gives the director a task. The director can break it into specialist assignments with dependencies.
2. Routing considers declared capabilities, skill records, availability, and existing work.
3. A worker receives its role instructions and relevant context, executes the task, and records a result or failure.
4. The director reviews the result and coordinates subsequent work. The quality of this review still depends on the checks and evidence supplied.
5. Memory can retain lessons for future retrieval. Skill records and audit events make progression and activity visible.

Practice quests extend this loop during idle time. They provide tasks, acceptance checks, and XP rewards. Breeding changes instructions; memory retains experience; XP summarizes activity through a progression formula. They require separate evaluation to identify which mechanism contributes value.

## The technical design behind the agent team

I connected four feedback loops: executing and reviewing tasks, retaining useful knowledge, choosing practice through skill progression, and evaluating changes to agent instructions. Memory used separate agent and shared banks, L0/L1/L2 context levels, namespace-based retrieval, selective deduplication, and extraction of reusable lessons. The purpose was to control both what an agent remembered and how much context it loaded.

Evaluation extended to the director itself. Ten scenario definitions exercised decomposition, routing, dependencies, recovery, budgets, review, and memory curation. For example, a decomposition benchmark checked task assignments and dependency graphs; a curation benchmark required identifying a contradiction in existing knowledge and deciding which lessons should become shared memory.

Regression protection was part of the breeding architecture: Gemma ran the incumbent baseline alongside candidates each cycle and used fresh trusted-core results for the comparison, with additional regression coverage and a director promotion veto. The memory wrapper adapted OpenViking-inspired context-management ideas; separate deletion and knockout experiments controlled growth in the instruction Markdown.

The [architecture deep dive](architecture.md) explains these memory layers, the execution lifecycle, actual benchmark examples, and the XP formula. [Crucible's experimental method](../crucible/methodology.md) explains the mutation and prompt-promotion logic that developed from this work.

## Decisions and trade-offs

| Decision | Intended benefit | Trade-off or limitation |
|---|---|---|
| Specialist agents coordinated by a director | Explicit ownership and task boundaries | Decomposition and coordination add work; multiple agents do not automatically outperform one |
| File-based tasks, results, heartbeats, and audit records | Inspectable state and straightforward debugging | Concurrent updates and recovery require care |
| Capability and skill-aware routing | Match work to a suitable available agent | Routing quality depends on the meaning and completeness of skill scores |
| Persistent memory with retrieval and lesson extraction | Reuse context rather than repeatedly rediscover it | An inaccurate lesson can persist; memory usefulness needs evaluation |
| XP, levels, and practice quests | Make experience visible and guide practice | Accumulated XP is not an independent test of competence |
| Separate breeding from memory and leveling | Make improvement claims more interpretable | Requires controlled conditions and more evaluation effort |

The broader implementation also included a dashboard and credential-proxy architecture. Those components are described at the [architecture level](architecture.md); this sample does not reproduce a deployed environment or assert a verified security boundary.

## What the sample demonstrates

The included code demonstrates routing and progression behavior without model accounts or services. The [retrospective](retrospective.md) explains where the design outpaced the evidence, including reward quality and decay behavior. These findings are part of the design assessment, not hidden behind the progression interface.

Run the synthetic walkthrough from the repository root with Python 3.9+:

```sh
python3 -B projects/gemma/src/walkthrough.py
python3 -B -m unittest discover -s projects/gemma/tests -v
```

It selects between fictional agents, shows how a busy-agent penalty changes routing, and calculates a practice reward. It creates and removes only its own temporary directory.

## Why the work stalled

The linked Gemma and Crucible work stalled under the usage and cost of breeding cycles and the time needed to keep refining benchmarks and baseline formulas. The remaining technical questions were unfinished experimental work, not a conclusion that the approach could not succeed.

## Explore

- [Architecture and task lifecycle](architecture.md)
- [Selected implementation and its boundaries](src/README.md)
- [Retrospective: experience versus demonstrated capability](retrospective.md)
- [Verification and limitations](verification.md)
- [Crucible: the linked prompt-evolution experiment](../crucible/README.md)
- [Portfolio index](../../README.md)
