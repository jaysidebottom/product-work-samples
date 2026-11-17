# Project artifacts

Start with the [portfolio](../README.md) for an overview and reading paths.

| Sample | Overview | Product and design | Implementation and evidence |
|---|---|---|---|
| Gemma | [Case study](gemma/README.md) | [Architecture and diagrams](gemma/architecture.md), [retrospective](gemma/retrospective.md) | [Selected code](gemma/src/README.md), [verification](gemma/verification.md) |
| Crucible | [Case study](crucible/README.md) | [Methodology and diagrams](crucible/methodology.md), [architecture](crucible/architecture.md) | [Experiment](crucible/experiment.md), [verification](crucible/verification.md) |
| Controlled Marketplace | [Overview](marketplace/README.md) | [PRD](marketplace/prd.md), [screens](marketplace/docs/screenshots/), [standalone document](marketplace/docs/marketplace.html) | [Technical specification](marketplace/technical-spec.md), [walkthrough](marketplace/walkthrough.md), [audit](marketplace/review/marketplace-audit.md) |
| Analyst Assistant | [Overview](analyst-assistant/README.md) | [PRD](analyst-assistant/prd.md), [mockups](analyst-assistant/mockups/README.md), [standalone document](analyst-assistant/docs/analyst-assistant.html) | [Model integration concept](analyst-assistant/model-integration.md); no working application |

Markdown PRDs are the publication sources. Standalone HTML documents are downloadable artifacts, not hosted demos. Rebuild them from the repository root with `node scripts/build-docs.cjs` after installing `marked` externally or setting `MARKED_MODULE` to its installed location. The prototype itself has no Node dependency.
