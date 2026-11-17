# Product Management Work Samples & Personal AI Projects

Product decisions, technical design, and working examples by Jeffrey Sidebottom.

This portfolio contains two kinds of work: product management samples that demonstrate problem framing, requirements, interaction design, and implementation trade-offs; and independently initiated personal AI projects that explore agent coordination, memory, and evaluation. Gemma and Crucible are personal projects, separate from employer work. Each sample distinguishes implemented behavior from concepts, historical observations, and proposed outcomes.

## Personal AI Projects

### [Gemma: Building and Evaluating an Agent Team](projects/gemma/README.md)
**Historical implementation · Agent architecture · Offline examples**

How can a developer coordinate specialist agents, retain useful context, and inspect their work? Explore task routing, memory layers, progression, and the distinction between activity and demonstrated capability.

[Read the case study](projects/gemma/README.md) · [Explore the architecture](projects/gemma/architecture.md) · [Inspect the evidence](projects/gemma/verification.md)

### [Crucible: Experiments in Evolving AI-Agent Prompts](projects/crucible/README.md)
**Gemma spin-off · Experimental methodology · Historical evidence**

Can systematic instruction changes produce repeatable improvements worth their evaluation cost? Explore competing mutation hypotheses, promotion criteria, and a preserved experiment with explicit limitations.

[Read the case study](projects/crucible/README.md) · [Explore the method](projects/crucible/methodology.md) · [Inspect the experiment](projects/crucible/experiment.md)

## Product Management Work Samples

### [Controlled Marketplace](projects/marketplace/README.md)
**Working local prototype · Product requirements · Access-control design**

How can buyers and sellers share useful information while retaining control over who sees sensitive details? Explore private-by-default listings, tiered access, recipient previews, and revocation.

[Read the case overview](projects/marketplace/README.md) · [See the screens](projects/marketplace/docs/screenshots/) · [Try the prototype](projects/marketplace/local-demo.md)

### [Analyst Assistant](projects/analyst-assistant/README.md)
**Product concept · Requirements · Four annotated interface mockups**

How could an AI-assisted analysis workflow make investigation plans, evidence, and uncertainty easier to review? Explore the proposed experience and the boundaries between the interface concept and model integration.

[Read the case overview](projects/analyst-assistant/README.md) · [Explore the mockups](projects/analyst-assistant/mockups/README.md) · [Read the PRD](projects/analyst-assistant/prd.md)

## Choose a reading path

| Interest | Start here | Go deeper |
|---|---|---|
| Product thinking | Project overviews above | Problem framing, requirements, and proposed success criteria in each PRD |
| Technical design | [Marketplace architecture](projects/marketplace/technical-spec.md) | [Implementation audit](projects/marketplace/review/marketplace-audit.md) and [analyst model integration](projects/analyst-assistant/model-integration.md) |
| Interaction design | [Marketplace screens](projects/marketplace/docs/screenshots/) | [Analyst mockups](projects/analyst-assistant/mockups/README.md) |
| Hands-on review | [Local marketplace setup](projects/marketplace/local-demo.md) | [Walkthrough and verification](projects/marketplace/walkthrough.md) |

For agent-system design, follow [Gemma’s task and memory architecture](projects/gemma/architecture.md), then [Crucible’s evaluation methodology](projects/crucible/methodology.md) and [recorded experiment](projects/crucible/experiment.md).

## Scope and evidence

The marketplace runs locally with Python, SQLite, and plain HTML/CSS/JavaScript. Its account switcher demonstrates authorization, not production authentication. All demo organizations and listing content are fictional. The analyst assistant is a concept, not a working analyst application. Proposed metrics are not validated customer outcomes.

Gemma and Crucible were conceived, designed, and directed by the author, with LLM-assisted code implementation. Their offline examples and historical observations do not establish validated capability gains.

[All project artifacts](projects/README.md) · [Verification and maintenance](roadmap.md) · [Reference deployment examples](deploy/README.md)
