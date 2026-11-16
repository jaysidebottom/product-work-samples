# Controlled Marketplace

**Personal work sample · Working local prototype**

Buyers and sellers need to discover relevant opportunities without exposing every detail to every participant. This sample explores explicit sharing: items begin private, owners choose recipients, and each grant exposes either a summary or full details.

## The key product decision

Visibility is an owner-controlled relationship between an item and a recipient organization. Preview uses the same field projection as recipient reads; changing or revoking a grant affects the next retrieval. The design makes disclosure choices inspectable while acknowledging that already copied information cannot be recalled.

## Read the work

1. [Product requirements](prd.md): problem framing, user flows, scope, and acceptance criteria.
2. [Screenshots](docs/screenshots/): a fictional-data walkthrough of private listings, preview, sharing, and buyer access.
3. [Technical specification](technical-spec.md): authorization, storage, and implementation boundaries.
4. [Implementation audit](review/marketplace-audit.md) and [browser evidence](review/browser-qa-2026-11-14.md): checks performed and remaining gaps.

The [standalone PRD](docs/marketplace.html) includes screenshots and can be downloaded and opened in a browser. GitHub displays HTML source rather than hosting an interactive page.

## Try it locally

From the repository root:

```sh
python3 projects/marketplace/app.py
```

Open http://127.0.0.1:8766. Python 3.9+ is sufficient; no external account or application dependency is required. Follow [setup and data-preservation guidance](local-demo.md), then the [interactive walkthrough](walkthrough.md).

## Evidence boundary

The prototype implements access rules for a simulated identity. It does not establish production authentication, customer adoption, or complete accessibility. Requirements and proposed product metrics are separate from observed outcomes. The walkthrough documents offline checks and optional isolated browser verification.

[Portfolio](../../README.md) · [All artifacts](../README.md)
