# Controlled Marketplace Discovery PRD

**Author:** Jeffrey Sidebottom
**Date / version:** November 14, 2026 / 0.9  
**Status:** Draft for review. Prototype implemented and privately deployed on AWS Lightsail with SQLite. Automated access checks and recorded hosted acceptance pass. Complete manual browser acceptance and user validation remain pending. Sections 1–7 present the product proposal, requirements, rollout, metrics, and risks. The appendices document the working prototype, verification evidence, and demonstration operations.

## 1. Proposal and problem

Build a marketplace where government buyers selectively share wishlist items with commercial sellers, and sellers selectively share catalog items with buyers. Owners can choose the recipient and information level for each item and preview the resulting view.

Buyers and sellers have mutually exclusive roles, cannot see other users’ same-side offerings, and need granular control over disclosure. The product hypothesis is that clear, predictable sharing will make users more willing to publish useful needs and capabilities. A generic browse-first marketplace risks exposing information before owners understand the audience.

**Buyer job:** Describe a need to selected vendors without exposing it to other buyers or unintended vendors. **Seller job:** Present a capability to selected government buyers without revealing its catalog to competitors.


| Current workflow | Pain hypothesis | Intended improvement |
|---|---|---|
| Buyer describes a need to potential vendors | Broad distribution may expose the need to unintended organizations | Share each wishlist item with selected sellers at a deliberate disclosure level |
| Seller presents capabilities to potential buyers | An openly browsable catalog may expose details to competitors | Let only selected buyers discover the offering; keep operational details separately controlled |
| Owner decides what a recipient can see | Unclear permission settings create uncertainty and risk oversharing | Use explicit Summary or Full details grants with a recipient preview |

These are product hypotheses, not findings from completed customer research. Validate them through the representative sharing and discovery tasks in section 6.

**Assumptions:** The intended product uses a verified organization directory; the prototype simulates it with a fixed directory and one selectable account per organization. Grants apply to organizations; multi-user membership and individual grants are future work. Directory entries expose only organization name and role, never offering existence. Product surfaces use organization display names; fixture labels such as Buyer A or Seller B belong only in the demo account switcher. All prototype data is fictional. Account verification is simulated and clearly labeled.

## 2. Goals, boundaries, and priority

1. Help owners configure the intended audience and disclosure level accurately.
2. Help authorized recipients discover and understand relevant needs or capabilities.
3. Prevent same-role users and unauthorized counterparties from receiving offering content.

| Priority | Capability | Why it matters |
|---|---|---|
| P0 — MVP | Create and edit private catalog or wishlist items | Gives owners control over what they publish before granting access |
| P0 — MVP | Grant Summary or Full details to selected opposite-role organizations | Makes the audience and disclosure level explicit |
| P0 — MVP | Preview, change, and revoke access | Helps owners predict and correct sharing outcomes |
| P0 — MVP | Discover only authorized offerings with persistent account context | Gives recipients useful information while preserving the visibility boundary |
| P1 — Future candidate | Recipient groups, expiration, collection defaults, and individual-user grants | Consider only after repeated sharing needs justify added complexity; no delivery commitment |

**MVP boundary:** Organization-level grants on individual items, two fixed disclosure levels, and mutually exclusive buyer/seller roles. One selected account represents each fictional organization in the prototype. There are no public listings, inherited grants, or conflicting allow/deny rules. Production identity verification and membership management are prerequisites for real-data use; the demo account switcher does not provide them.

**Non-goals:** Payments, checkout, contracts, procurement approvals, matching algorithms, messaging, production onboarding/identity verification, and multi-user organization administration.

**Deferred requirement M7:** Recipient groups, expiration, collection defaults, and individual-user grants remain outside the MVP. The ID is retained for traceability with the implementation audit; current P0 acceptance requirements are M1–M6 and M8.

## 3. Proposed experience and workflow

**Anchor scenario:** Seller A wants Buyer A to discover a capability while withholding implementation details until interest is established.

1. Seller A creates a catalog item with summary and detailed fields. The item saves as Private.
2. Seller A opens Manage visibility, selects Buyer A, and chooses Summary.
3. Before saving, the interface states: “Buyer A will see the summary, capability highlights, diagram, and company information.” Preview shows that exact view.
4. Buyer A sees the item in Discover and can open its summary. Buyer B and Seller B cannot discover or retrieve it.
5. Seller A changes Buyer A's grant to Full details. The additional fields become available on Buyer A's next request.
6. Seller A revokes the grant. Buyer A's next retrieval fails; the item disappears from Discover.
7. Buyer A follows the same process to share a wishlist item with Seller A. Buyer B cannot see that wishlist item.

| Screen/state | Essential behavior |
|---|---|
| My catalog / My wishlist | List own items with a clickable Private or Shared with N audience badge that opens the visibility editor directly; create/edit items |
| Offering editor | Clearly separate summary/marketing and full-detail fields; explain that short copy conveys value while full details explain workflow and fit; show audience when editing an already-shared item |
| Discover | Search title/category/summary only among authorized counterpart items; prominently display the posting organization at the top of each card; seller cards include an illustrative diagram and capability highlights; show useful empty state without mentioning hidden items |
| Offering detail | Display only allowed fields; group seller product details and company information; format specifications, deployment, and evaluation as readable lists. Summary recipients see no restricted values. Returning focus keeps the detail open while rechecking access. |
| Manage visibility | Select eligible organizations, set level, preview, save, or revoke; show pending changes distinctly from saved access |
| Preview as recipient | Owner-only view using the same disclosure rules as recipient retrieval; include “No access” preview |

```text
MANAGE VISIBILITY — Network analysis capability
Only government buyers can receive this catalog item.

Recipient           Access                  Action
Civic Research Office   [Summary v]
Regional Operations     [No access v]

Buyer A will see: summary, highlights, diagram, and company information.
Operational details, availability, and contact remain hidden.
[Preview as Civic Research Office]             [Cancel] [Save access]
```

Recipient identities appear only to the owner. Access changes persist only after Save; failed saves leave effective access unchanged and clearly report the failure. No email notifications or external messages are sent by the prototype.

**Usability requirements:** Keyboard-operable forms, visible focus, native required/email/URL validation and modal server-error messages, text status labels, and no color-only access indicators. A denied or missing item returns the same generic “Item unavailable” experience, avoiding confirmation that a hidden item exists.

The working screens are shown in Appendix D. Those captures use disposable fictional data; they illustrate the implementation without claiming completed user validation. Manual keyboard acceptance remains pending.

## 4. Functional requirements and acceptance criteria

All requirements below are P0 and apply symmetrically to catalogs and wishlists. They define the product acceptance contract; implementation status and test limits are reported in Appendices A and B.

### Visibility model and information boundaries

| Viewer | Own offerings | Another buyer's wishlist | Another seller's catalog |
|---|---|---|---|
| Buyer | Create/edit own wishlist items | Never visible | Only content explicitly granted to their organization |
| Seller | Create/edit own catalog items | Only content explicitly granted to their organization | Never visible |

Evaluate access in this order: **owner → same-role prohibition → explicit opposite-role grant → deny**. Owners can manage their items; only owners can edit or share them. A grant can never override the same-role prohibition. A user has one fixed role; changing the active account must not change that role or transfer access between accounts.

Each item starts **Private** with no grants. Owners add a named opposite-role organization and choose **Summary** or **Full details**. Full details include the summary. One grant exists per item/recipient pair; changing its level replaces the previous level. There are no public listings, inherited grants, custom deny rules, or collection defaults in the prototype.

| Information | Summary grant | Full-detail grant | Owner only |
|---|---|---|---|
| Item title, category, owner organization name, owner-written short summary | Yes | Yes | — |
| Seller capability highlights, selected illustrative diagram, company bio/expertise/website/location | Yes | Yes | — |
| Product overview or buyer need, use cases, requirements/specifications, deployment/integration details or constraints, evaluation/success criteria, timing/availability, contact name/email | No | Yes | — |
| Recipient list, grant levels, visibility management | No | No | Yes |

Both item types share a core schema, with labels adapted to their roles. Seller listings add a value proposition, up to three capability highlights, one optional predefined workflow diagram, and an About the company section. Buyer wishlists emphasize the need, use cases, required capabilities, constraints, timeline, and success criteria; seller marketing fields are not accepted on buyer items. Diagrams are clearly labeled illustrative, not product screenshots. No uploaded attachments, price/budget, private notes, or arbitrary custom fields in MVP. Company information is editable per listing in this prototype; a reusable organization profile is future work. Company content and the diagram selection are returned only after item authorization, never through the organization directory or a public media URL. A summary is written by the owner, never automatically extracted from restricted details. The editor explicitly identifies who can see each field group and warns against putting sensitive details in the summary.

Revocation or downgrade applies to the next retrieval and clears outdated UI content on refresh/account switch or detail revalidation when browser focus returns. There is no push update or polling. Unsaved forms survive focus changes; explicit close, reload, and account switching discard them without a confirmation prompt. It cannot retract copies already made. Ordinary item edits retain existing grants; the edit screen shows the current audience before saving. New fields must receive an explicit disclosure classification before they can be returned.

### Functional acceptance criteria

Access-control behaviors apply symmetrically to catalogs and wishlists; content and presentation follow the owner’s role.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| M1 | Role and ownership | Buyers create wishlist items only; sellers create catalog items only. Nonowners cannot edit content or grants, including through direct requests. Same-role grants are rejected even if manually submitted. |
| M2 | Private creation and editing | New items have zero grants. Owner can edit fields and retain explicit existing grants. Required title/category/summary errors prevent save without losing input. |
| M3 | Granular sharing | Owner adds an eligible organization with Summary or Full details. Save persists the exact recipient/level. Duplicate grants cannot accumulate; updates replace the prior level. Cancel does not change access. |
| M4 | Discovery and detail | Lists, search, counts, and direct item responses use current permissions. No grant means no item metadata or seller marketing content. Summary access returns only summary fields; full-detail fields must be absent from the response, not merely hidden on screen. |
| M5 | Preview and revocation | Preview matches the recipient's permitted fields. Revocation denies the next request; downgrade removes detailed fields on next retrieval. Account switches clear the previous account's content and cached results. Returning browser focus revalidates an open detail without dismissing it, preserving scroll position while removing newly restricted content; unsaved owner forms remain intact. |
| M6 | Persistence and account context | Saved content and access changes survive ordinary browser refresh. The active account and role are visible; changing accounts clears prior-account content and reloads only authorized data. |
| M8 | Role-specific content | Seller editors support up to three capability highlights, one optional predefined illustration, and company bio/expertise/HTTPS website/location. Summary recipients receive these fields; operational details and contacts require Full details. Buyer editors describe needs, use cases, constraints, and success criteria; seller marketing fields are rejected for buyer records. Company profiles are per listing. |

## 5. Execution and rollout

The working prototype follows the delivery sequence below. Proposed responsibilities and exit gates guide further validation; building the prototype does not establish production readiness or customer value.

| Stage | Work and proposed owners | Exit gate and current status |
|---|---|---|
| Scope and policy definition | Product defines roles, field groups, and sharing rules; engineering checks enforcement feasibility | Prototype rules are defined. Validate organization-level recipients and disclosure groups with representative users before expanding scope. |
| Prototype delivery | Engineering implements owner editing, shared server-side access rules, recipient views, preview, and persistence | Working prototype is built. M1–M6 and M8 have implementation evidence; remaining manual acceptance is listed in Appendix B. |
| UX and acceptance validation | Product/design observe sharing and discovery tasks; engineering completes keyboard, focus, and mobile checks | Participants configure and predict access correctly; technical acceptance and section 6 guardrails pass. User study and final manual checks remain pending. |
| Limited real-data pilot | Engineering/security establish verified identity, tenant membership, auditability, and operational controls; product defines pilot scope | Security/operational review and product validation approve the pilot. Private demonstration access alone does not satisfy this gate. |
| Later capabilities | Product prioritizes repeated needs; design/engineering evaluate added permission complexity | Add groups, expiration, defaults, or individual grants only when evidence supports them and the same access/comprehension checks pass. |

**Delivery order:** Define fields and rules → prepare test accounts/items → owner create/edit → server-side access policy and recipient views → visibility editor/preview → revocation/downgrade and persistence checks → usability validation. Build both roles on the same rules to prevent asymmetry.

**After the prototype:** Validate organization versus individual sharing and disclosure groups with users. Add production identity and membership controls before real-data use. Prioritize groups/expiration only if repeated sharing tasks justify their complexity.

## 6. Success metrics and evaluation

The prototype tests comprehension and correctness, not marketplace revenue or liquidity. No user study or baseline exists yet. Proposed targets below guide evaluation, not claims of achieved performance.

| Type | Metric | Validation / proposed target |
|---|---|---|
| Output — primary | Owners who configure the specified audience and level without help / owners attempting the task | Formative test with five representative participants; aim for at least 4/5, investigate every failure |
| Output | Authorized recipients who find the specified offering / recipients attempting discovery | Aim for at least 4/5 in the same small study; not a population-level estimate |
| Input | Completed visibility saves / visibility-edit sessions | Observe abandonment and time to configure; no arbitrary adoption gate |
| Guardrail — comprehension | Correct predictions of who sees summary/details/no content / audience questions asked | Ask before showing preview and after correction; diagnose misunderstanding rather than rewarding fast clicks |
| Guardrail — access | Unauthorized records or fields returned across the automated access matrix | Zero; any failure blocks access-control acceptance until resolved |
| Guardrail — oversharing | Tasks resulting in broader access than the instructed audience/level | Zero in the formative test; revise language/defaults after any occurrence |

Planned instrumentation (not implemented): item creation, visibility edit/save/revoke, recipient discovery/open, and access denial using IDs/status rather than offering contents. Observe confidence and time-on-task alongside success; an easily saved wrong policy is a failure.

## 7. Risks, trade-offs, and open questions

| Decision / risk | Rationale and mitigation |
|---|---|
| Organization-level grants | Makes the recipient boundary easier to understand; explicitly defer internal membership and individual exceptions |
| Summary/full-detail levels rather than per-field toggles | Meaningful disclosure control with fewer configuration errors; validate whether fixed field groups fit real needs |
| Private-by-default limits discovery | Confidentiality takes priority; provide a clear sharing action and recipient directory without exposing item existence |
| Owner puts sensitive text in a summary | Separate fields, explain audience, and require an intentional grant; preview supports checking but cannot judge content sensitivity |
| Frontend-only hiding or cached data leaks | Server-side field projection, access checks on each request, and cache clearing on account change; test direct responses |
| Revocation mistaken for erasure | Explain that it prevents future application access, not prior copying |
| Permission complexity makes access hard to predict | Keep explicit grants in the initial release; defer groups, inheritance, and expiration until user needs justify them. Identity controls remain required before real-data use. |



**Open questions:** Are recipients organizations or named users in the intended product? May organizations have multiple buyers/sellers with internal responsibilities? Is a summary/detail split sufficient for real content? What identity and membership systems would support production access? These questions must be resolved before expanding the declared prototype scope or using real data.


**Validation pending:** Complete physical OS-focus return, keyboard traversal/trap/restoration and scrolled mobile visual checks; evaluate whether users can configure and predict visibility correctly. Existing trace evidence covers automated refresh/account switching and responsive widths. No user-study results are claimed.

## Appendix A Working prototype and implementation

The prototype uses a small application with server-side authorization and persistent local data. The server resolves the active account, checks ownership/role/grant on every read and mutation, and returns only the allowed field projection. The same policy serves discovery, detail, and owner preview to avoid conflicting interpretations. Authorized records are filtered before calculating counts or search results.

Minimum records: organization (ID, name, fixed role), account (organization), item (owner, type, content), and grant (item, recipient organization, level). The local and hosted prototype use a Python standard-library HTTP server, SQLite storage, and a plain browser interface. No existing organization-specific stack is assumed. Account and organization map one-to-one in the fixed demo directory; item type follows its owner’s immutable role.

**Prototype boundary:** Identity verification is simulated; server-side content authorization is still required for the selected account. The demonstration environment permits switching between fictional accounts to inspect access outcomes. This is a testing control, not a customer-facing account-management feature or production authentication. Use synthetic data only. Verified identity, tenant membership management, product audit trails, and a production security/operational review remain prerequisites for real-data use. The private demo safeguards in Appendix C do not satisfy those identity requirements.

Untouched original demo listings receive richer fictional content on startup; edited listings and existing grants are preserved. Reset is a separate explicit action. Seller illustrations use distinct graph and telemetry styles; they are labeled illustrations rather than real product screenshots. No media upload pipeline is implemented.

A frontend-only simulation would not satisfy the server-side access requirements in this draft. Any such change must revise the declared implementation scope and validation claims.

**Implementation limitations:** Search covers title/category/summary, even for Full details recipients. No pagination, item deletion, conflict detection, or general migration framework is implemented. The last successful owner save wins. Same-browser tabs synchronize the selected demo account; concurrent different-account tests need isolated browser contexts. No product-event telemetry exists. These limits do not change the deny-by-default policy.

## Appendix B Verification and acceptance evidence

Eighteen automated service/HTTP-handler tests pass, covering both roles, field projection, denial, preview, invalid mutations, persistence, reset, marketing projection/validation, preservation of edited fixtures during upgrades, and explicit HTTPS proxy-origin handling. These tests exercise the actual HTTP handler using in-memory transport. Five Node regression checks also pass for modal focus retention, downgrade/revocation, late responses after close, unsaved forms, and escaped detail formatting; they use mocked DOM/HTTP rather than a real browser.

A user-run disposable live-server/browser walkthrough now has a recorded trace through its final action, with no traced action/page errors, and eleven inspected captures. It covers both roles, sharing/preview, response omission, downgrade/revoke, account switching, create/edit persistence and responsive widths. OS focus/keyboard behavior and clean scrolled mobile captures remain to verify; focus events in the automated suite are dispatched programmatically. See [browser QA evidence](review/browser-qa-2026-11-14.md).

Historical hosted checks covered authorization, Origin rejection, restart persistence and backup/restore. Private operating records are not included in this repository; these observations do not establish current hosted health or production readiness.

The cases below remain the acceptance checklist; passing backend tests does not establish browser behavior or usability. Exercise the access matrix with both item types, using an owner, a same-role nonowner, an authorized counterparty, and an unauthorized counterparty. Check direct responses as well as rendered screens.

| Case | Expected result |
|---|---|
| Newly created item; all nonowner account types | Absent from discovery/search/counts; direct retrieval unavailable |
| Summary grant to one counterparty | That recipient gets exactly summary fields; other counterpart remains denied |
| Full-detail grant | Selected recipient gets summary/marketing plus defined operational details; never grant roster |
| Same-role grant attempted directly | Rejected; no effective grant created |
| Nonowner attempts content/grant edit or preview | Denied; original item/grants unchanged |
| Full → Summary | Next response excludes restricted fields; visible view refreshes accordingly |
| Revoke → direct retrieval | Generic unavailable response; no stale discovery entry after refresh |
| Item edit after sharing | Existing recipients/levels unchanged; changed content follows those levels |
| Missing item versus unauthorized item | Same external unavailable behavior |
| Account change and refresh | No prior-account content remains; saved content and access changes persist |

**Audit:** [Implementation and evidence reconciliation](review/marketplace-audit.md) maps M1–M8 to source, tests, and gaps. The configured HTTPS origin is implemented and handler-tested; historical hosted results are not a current infrastructure certification.

## Appendix C Demonstration operations

Run the prototype locally using [local-demo.md](local-demo.md). The application stores items and grants in a local SQLite database outside versioned source. Ordinary restarts preserve that data. Use a separate disposable database for automated browser checks and screenshot capture; never reset presentation data for QA.

The demo switcher can select every fictional account. Every selected account can invoke the explicitly confirmed global reset. These demonstration controls are not product identity or administrative security. Use fictional data only.

The [technical specification](technical-spec.md) describes the application, persistence and reference hosting boundaries. The [deployment examples](../../deploy/README.md) use neutral names and require separate operator configuration. They contain no live connection information and are not instructions to modify an existing deployment. No production identity, availability SLA, unattended disaster recovery or completed accessibility certification is claimed.
