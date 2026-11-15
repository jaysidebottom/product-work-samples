# Controlled Marketplace prototype

A local prototype for buyers and sellers to selectively share needs and capabilities. Start with [local setup](../local-demo.md). Python 3.9+ and a modern browser are sufficient; the application has no package or external-service dependencies.

## Walkthrough


1. On a disposable walkthrough database, select **Seller A · Northstar Analytics**. Open its seeded catalog item, or create a new private offering. The Summary and Full details fields are separate.
2. Click the item’s **Private** or **Shared with N** badge (or open **Manage visibility** from its detail). Set Buyer A to **Summary**, leave Buyer B at **No access**, and **Preview as Civic Research Office**. Preview is marked proposed until saved. Save access.
3. Switch to **Buyer A**, open **Discover**, and inspect the offering. Summary fields, capability highlights, the illustrative diagram, and company information appear; operational details and contact remain absent. Copy the direct link shown in detail if useful.
4. Switch to **Buyer B**, then **Seller B**. The offering is absent from Discover. A direct link gives the same unavailable experience as a nonexistent item.
5. Return to Seller A. Upgrade Buyer A to **Full details** and save. Buyer A's next retrieval includes description, specifications, timing, and contact. It never includes the grant roster.
6. Change Full details back to Summary, then revoke by selecting No access and saving. Verify each change as Buyer A. Canceling a draft change leaves saved access unchanged.
7. Select Buyer A → My wishlist. Share its wishlist with Seller A and demonstrate the mirrored flow. Buyer B can never see Buyer A's wishlist.
8. Refresh to demonstrate persistence. Explain organization-level grants and the demo identity boundary.


## Visibility rules

New items are private. Owners can manage their own records; other same-role accounts can never view them. An opposite-role account needs an explicit Summary or Full details grant. Summary exposes only its allowlisted fields; Full details adds operational content and contact information. Grant rosters remain owner-only.

Owner preview uses the same server-side projection as recipient reads. Saving a visibility change atomically replaces the recipient map. Ordinary content edits preserve grants. Downgrade or revoke takes effect on the next retrieval; already copied information cannot be recalled.

## Verification

```sh
python3 -B -m unittest discover -s marketplace/tests -v
node --test marketplace/tests/test_ui.cjs
```

For real-browser checks, install Node and Playwright (`npm install --no-save --package-lock=false playwright`, then `npx playwright install chromium`). Run:

```sh
python3 marketplace/qa/run-disposable.py
```

The runner creates a temporary database and loopback server. It never opens the presentation database. `PLAYWRIGHT_MODULE` can select an externally installed module; `CHROME_PATH` can select a browser executable. Otherwise Playwright uses its installed Chromium. Captures and traces are ignored by Git.

For a manually started disposable server, set both `MARKETPLACE_URL` and `MARKETPLACE_QA_DISPOSABLE=1`. The browser suite rejects remote targets and the normal presentation port 8766. Its reset flows must never target data you intend to retain.

## Boundaries

The account switcher and `X-Demo-Account` header allow selecting any fictional account. Every demo account can invoke global reset. This demonstrates authorization for a selected identity, not authenticated membership. Use fictional data only.

SQLite preserves edits and grants across restarts. Untouched original fixtures may receive richer sample content; edited fixtures and grants are preserved. Unsaved forms survive focus refresh but not an explicit close, reload or account switch. Concurrent owner saves use last-write-wins behavior.

See the [technical specification](../TECH_SPEC_Marketplace.md), [implementation audit](../review/marketplace-audit.md) and [browser evidence](../review/browser-qa-2026-11-14.md). Manual focus/keyboard/scrolled-mobile checks and customer validation remain incomplete.
