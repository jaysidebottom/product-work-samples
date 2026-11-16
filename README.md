# Product Management Work Samples

Product decisions, technical design, and working examples by Jeffrey Sidebottom.

These personal work samples show how I frame a problem, translate it into requirements, and examine implementation trade-offs. Each distinguishes working behavior from concepts and proposed outcomes.

## Selected work

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

## Scope and evidence

The marketplace runs locally with Python, SQLite, and plain HTML/CSS/JavaScript. Its account switcher demonstrates authorization, not production authentication. All demo organizations and listing content are fictional. The analyst assistant is a concept, not a working analyst application. Proposed metrics are not validated customer outcomes.

[All project artifacts](projects/README.md) · [Verification and maintenance](roadmap.md) · [Reference deployment examples](deploy/README.md)
