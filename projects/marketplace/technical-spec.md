# Marketplace technical specification

This document describes the implemented local application and generic single-host deployment examples. The application is a Python standard-library HTTP server, SQLite database and plain browser interface. All data is fictional. Production authentication, membership, availability guarantees and user validation are outside the demonstrated scope.

## 1. Application contract and authorization


`projects/marketplace/app.py` serves only the homepage, app.js, style.css and `/api/marketplace`. GET views are context, mine, discover, detail and owner preview; POST actions are create, edit, access and demo reset. There is no item deletion, upload, messaging or payment API.

`project()` applies owner → same-role prohibition → explicit opposite-role grant → deny. The same allowlisted projection serves discovery, detail and preview. Unauthorized/missing items return the same 404. Only owners receive the grant roster. Search/count operate on authorized projections, and search covers title/category/summary even with Full details access. The context directory exposes fixed ID/name/role, not item existence or company content.

Summary fields are title/category/summary plus seller highlights, visual selection and company bio/expertise/HTTPS website/location. Full details add description, specifications, timing, contact name/email, use cases, deployment and success criteria. Buyer records reject nonempty seller marketing fields. Server limits include 5,000 characters per field, required title/category/summary, validated email/HTTPS website, three highlight lines of at most 100 characters and an allowlisted diagram enum. Owner text is escaped before HTML insertion; the diagrams are local illustrations, not uploaded media.

Grant replacement validates the entire map before one transaction replaces it. Same-role and invalid recipients are rejected. Preview of a proposed grant does not persist it. No optimistic concurrency exists: the last successful owner save wins. No pagination, general schema migration ledger or production membership management is implemented.

The browser clears account-specific content and rejects stale async responses. Returning focus revalidates an open detail and preserves scroll; downgrade/revoke removes inaccessible content on retrieval. Unsaved forms skip focus reload. There is no polling/push, so already displayed content can remain until the next request/focus/refresh. Closing, reloading or switching accounts discards unsaved edits without a confirmation prompt. Tabs in one browser share demo account changes via localStorage/storage events; use isolated contexts for concurrent different identities. Revocation cannot retract copied information.

## 2. Persistence and database choice

SQLite is implemented; PostgreSQL is not. The current schema is:

| Table | Stored data and constraints |
|---|---|
| items | ID primary key, owner ID, JSON content text |
| grants | Item foreign key with cascading delete, recipient, summary/full CHECK, composite item/recipient primary key |
| settings | Primary-key seed and fixture-upgrade markers |

Organizations are server-defined. Each connection enables foreign keys and a ten-second lock timeout. The default rollback journal is retained. SQLite serializes writers; the recorded five-worker read/two-writer smoke test is not a capacity benchmark or a multi-host guarantee.

In the reference deployment, code releases and persistent data use separate directories. Local and hosted databases are independent. Existing edits and grants must survive release changes.

The rich-listings upgrade only enriches exactly unchanged original fixtures, preserving edited content and grants. Future schema changes need an ordered migration ledger, backups, unknown-version failure handling and old/edited-data upgrade tests. Code rollback must not automatically restore an old database over later edits.

Retaining SQLite minimizes changes to the tested authorization policy and suits this bounded single-host demo. Reconsider PostgreSQL for multiple app hosts or sustained write contention, and reassess the serving layer, identity and operations for real-data use. Migration must preserve IDs, composite grant uniqueness, foreign keys and projection tests. A database change does not replace authorization or create a recovery SLA.


## 3. Reference hosting boundary

The deployment examples place a private HTTPS gateway and restricted reverse proxy before a loopback app. Service isolation, resource limits, no-store/CSP/nosniff headers, explicit Origin validation and separate persistent storage are defense-in-depth measures. They do not turn the selectable demo identity into authenticated customer access.

`MARKETPLACE_PUBLIC_ORIGIN` or `--public-origin` specifies an exact allowed HTTPS origin. Forwarded headers cannot override the comparison. Local loopback behavior remains available without a proxy. The reference scripts require private operator configuration and are not a tested migration of any existing installation.

## 4. Operations and verification limits

SQLite backup and integrity checks are illustrated in [deployment examples](../../deploy/README.md). Backups on the same host are not independent disaster recovery. Restore verification, retained off-host generations, alert delivery, release rollback drills, monitoring and capacity planning must be established for a specific deployment; no SLA is claimed here.

The application emits content-free HTTP failure method/status events. Product analytics and a complete security audit trail are not implemented. There is no dedicated readiness endpoint.

Eighteen service/HTTP-handler tests and five mocked UI checks exercise access control, projection, persistence and frontend regressions. Historical disposable browser evidence is recorded separately. Physical focus changes, comprehensive keyboard/scrolled-mobile accessibility, customer research and production security acceptance are not complete. See [implementation audit](review/marketplace-audit.md) and [browser evidence](review/browser-qa-2026-11-14.md).
