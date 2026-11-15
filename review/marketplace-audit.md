# Marketplace implementation audit

This maps product requirements to the implemented local application and verification limits. It is source traceability, not customer research or infrastructure certification.

## Requirement reconciliation

| PRD | Implemented evidence | Verification and limits |
|---|---|---|
| M1 roles/ownership | Fixed ORGS; Store.request resolves actor; own() gates edit/access/preview; project() denies same-role before grants | Both-role service matrix, invalid grants, corrupted same-role grant, HTTP identity checks pass. Identity selectable, never authenticated. |
| M2 private create/edit | UUID creation without grants; validated content; edit updates content only | Creation, invalid fields, edit/grant retention and restart tests pass. Native required/email/url validation; server errors appear in modal, not inline at each field. |
| M3 explicit sharing | Composite item/recipient primary key; validated whole-map replacement transaction; unsaved form and proposed preview | Atomic invalid-grant tests and nonmutating preview pass. Recorded browser trace covers Save/Cancel. Last successful save wins across concurrent owner tabs; no conflict detection. |
| M4 authorized discovery | project() allowlists fields before search/count; direct detail uses same projection; missing/denied return same 404 | Both-role summary/full exact key sets; search canaries; HTTP omission/no-store checks pass. Search is title/category/summary only, including for full recipients. No pagination. |
| M5 preview/change handling | Saved and proposed preview use project(); generation/request/dialog counters discard stale results; focus revalidates detail and refreshes list | Five mocked UI checks cover downgrade/revoke, close-during-refresh, unsaved forms and escaping. No polling/push: an already visible view can remain until retrieval/focus/refresh. Focus with a form deliberately skips reload. Browser scroll/focus behavior pending. |
| M6 persistence/context | SQLite file outside source assets; browser localStorage account; server fixed role; initialize clears dialog/list | Store restart and immutable role tests pass. Same-browser tabs share account changes through storage events; isolated browser contexts needed for concurrent different-role testing. |
| M8 rich content | Seller highlights/visual/company fields; buyer rejects nonempty marketing fields; role-specific forms; SVG drawn from authorized enum | Marketing projection, validation and fixture-upgrade preservation pass. Company website is rendered text, not an active link. Diagrams are illustrations, not screenshots. |
| M7 deferred scope | No groups, expiry, defaults, or individual accounts within organizations | Intentionally absent; no production identity, payments, procurement, notifications or uploads. |

## Boundaries and additional implemented behavior

- API has context, mine, discover, detail and preview reads; create, edit, access and reset mutations. No item-delete action. IDs/kind/access accompany content; these are response metadata, not undisclosed content groups.
- Directory contains fixed ID/name/role only. No catalog counts or listing-specific company information leaks through it.
- Summary fields: title/category/summary, plus seller highlights/visual/companyBio/companyExpertise/companyWebsite/companyLocation. Full adds description/specifications/timing/contactName/contactEmail/useCases/deployment/successCriteria. Only owner receives grants.
- All text fields have a 5,000-character server limit; title/category/summary required. Email validated; website HTTPS without credentials; highlights at most three lines, 100 characters each; diagram enum constrained. All owner text is escaped before HTML insertion.
- Reset is global and available to every demo account, explicitly confirmed in UI. It is a demo convenience, not owner-only administration. Never run reset-based QA against presentation data.
- Existing fixture upgrade uses exact original-content equality before enriching; changed fixtures and grants survive. This is one data upgrade marker, not a general migration framework.
- Static paths are allowlisted to three assets. Responses use no-store, Vary, CSP, and nosniff. No public database/media path, CORS, attachment or external-image pipeline.
- Direct link is displayed as text. Reloading a direct URL rechecks the currently selected identity. Refresh closes detail; focus revalidates in place. Unsaved forms survive focus, not explicit cancel/close/reload/account switch; there is no unsaved-change confirmation.
- No product event telemetry is implemented; PRD metrics/instrumentation are proposed. Content-free HTTP failure events include method/status; routine request logging is suppressed. Operational alert delivery and external monitoring are outside this local application.

## Verification limits

The service/HTTP-handler and mocked UI suites support the policy claims above. Historical disposable browser evidence is recorded in [the browser report](browser-qa-2026-11-14.md). Manual keyboard/focus/scrolled-mobile checks, customer validation and production identity remain incomplete. Tests must use isolated data; do not reset a presentation database.
