# Controlled Marketplace and Analyst Assistant

Product design and engineering examples by Jeffrey Sidebottom: a working controlled-marketplace prototype, two product requirements documents, and conceptual analyst-assistant mockups. All demo organizations and listing content are fictional.

## Run the marketplace

Python 3.9+; no application dependencies or external accounts required.

```sh
python3 marketplace/app.py
```

Open http://127.0.0.1:8766. The app creates a local SQLite database on first launch. Existing edits and grants survive refresh and restart. Use the account switcher to explore buyer and seller views. New items start private; the server enforces the selected account's access. The switcher demonstrates authorization, not production authentication.

See [local setup](local-demo.md) and the [walkthrough](marketplace/README.md). Reset is destructive to demo edits; use a separate disposable database for QA.

## Explore the work

- [Marketplace PRD](PRD_Controlled_Marketplace.md)
- [Marketplace technical specification](TECH_SPEC_Marketplace.md)
- [Analyst Assistant PRD](PRD_Cyber_Analyst_Assistant.md) and [model integration notes](review/analyst-model-integration.md)
- [Standalone documents and screenshots](docs/README.md)
- [Analyst mockup gallery](mockups/index.html)
- [Implementation audit](review/marketplace-audit.md)
- [Project status](roadmap.md)

The analyst interface is conceptual. The marketplace is implemented with Python, SQLite and plain HTML/CSS/JavaScript. Hypotheses and proposed metrics are not presented as validated customer research.

## Verify

```sh
python3 -B -m unittest discover -s marketplace/tests -v
node --check marketplace/static/app.js
node --test marketplace/tests/test_ui.cjs
python3 scripts/audit-secrets.py .
```

The suite includes 18 service/HTTP-handler tests and five mocked UI regression checks. The separate browser runner uses disposable data; see [browser evidence and limitations](review/browser-qa-2026-11-14.md). Manual accessibility and user validation remain incomplete.

## Hosting boundary

[Deployment examples](deploy/README.md) illustrate a private gateway and persistent single-host application. They require operator-provided configuration and contain no live addresses, account details or credentials. Running locally requires none of that infrastructure.
