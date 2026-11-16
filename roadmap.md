# Project status and maintenance

Updated November 15, 2026.

## Start here

This repository contains a controlled-marketplace prototype and an analyst-assistant product concept. The requested product work is complete. Address concrete review findings without reopening completed scope.

Read the PRDs for product decisions, the technical specification for implementation boundaries, and the implementation audit for verification limits. Assumptions and proposed metrics remain distinct from validated research.

## Current handoff

- Marketplace product scope, implementation and PRD structure are complete. Buyer/seller ownership, private-by-default items, summary/full grants, preview and revocation remain the accepted baseline.
- The analyst concept includes four annotated mockups. It is not a working analyst application.
- This portfolio copy contains portable Markdown/HTML documents, images, source and reference deployment files. Private operating records, document-session links and personal reusable templates are not publication inputs.
- Preserve authoritative native documents and their edits outside the repository. Never reimport an older generated document over them.
- Preserve local and hosted presentation data. Use disposable databases for tests, captures and walkthrough resets.
- Reference deployment examples use generic names. They have not been applied to any existing host. Publishing this repository does not deploy code or migrate infrastructure.
- Product metrics, customer validation, physical focus/keyboard behavior and complete scrolled-mobile accessibility remain unverified. Do not convert these gaps into claims of completion.

## Publication checks

Review the tracked file set, run the secret audit and relevant tests, and inspect generated HTML before publishing. Keep credentials, local databases, backups, connection manifests and private records out of Git. Use this sanitized repository as the publication source; do not synchronize a private operating workspace wholesale.

The repository history begins with a sanitized portfolio snapshot. Source operating history is not a publication input. Organizing these samples does not change repository visibility or deploy an application.

## Portfolio organization

Samples are grouped under `projects/`, each with an overview and paths to requirements, visuals, and evidence. Shared audit/build tools remain in `scripts/`; reference deployment examples remain in `deploy/`. All existing samples and assets are preserved.

Checks from the repository root:

```sh
python3 -B -m unittest discover -s projects/marketplace/tests -v
node --test projects/marketplace/tests/test_ui.cjs
python3 scripts/audit-secrets.py .
```
