# Local browser QA evidence — November 14, 2026

The operator ran `python3 marketplace/qa/run-disposable.py` locally using the original repository layout. The current equivalent is `python3 projects/marketplace/qa/run-disposable.py`. The runner creates a separate temporary SQLite database and local server. The review inspected the resulting trace and all eleven fresh PNGs. No Playwright action errors or pageError events appear in the trace; execution reached the final buyer mobile preview and close action. The terminal exit code/stdout was not independently captured, so evidence is the completed trace and screenshots rather than an archived process-success report.

Trace: `projects/marketplace/qa/captures/browser-trace.zip` (ignored by Git).

| Coverage | Evidence |
|---|---|
| Both-role direct HTTP access matrix | Private creation denial, same-role grant rejection, summary/full/downgrade/revoke, exact proposed-preview parity and restricted search omission completed |
| Both-role create/edit | UI creation, unsaved title survives dispatched focus event, role-specific marketing fields, edit and reload persistence completed |
| Sharing and preview | Proposed Summary preview, Cancel without effective grant, Summary save, recipient detail, other-counterparty and same-role direct-link denial completed |
| Full detail / downgrade / revoke | Full detail appears; dispatched focus preserves dialog/scroll; downgrade removes overview; revoke yields Item unavailable |
| Account switching | Sequential role/account changes and permitted/denied views completed |
| Buyer wishlist flow | Saved grant survives reload; seller discovery shows correct organization and read-only recipient badge |
| Mobile | 390×844 page overflow check; both-role editor and full-preview modal width checks; Escape dismissal completed |

## Visual review and limits

All 11 captures were inspected. Desktop cards, access editor, summary/full dialogs, revoked empty state and wishlist discovery are readable in the visible regions. Mobile owner forms and visibility controls fit the viewport. Long dialogs scroll; screenshots show only their visible portions, not the full modal content. The mobile full-page `07-mobile.png` has a duplicated horizontal strip near the bottom; do not use it as a polished fallback screenshot. A viewport-only recapture is required to distinguish capture stitching from a rendering issue. The mobile preview screenshots show the controls above the preview; preview content exists in the traced DOM, but its lower content still needs a scrolled visual check.

Remaining manual acceptance: physically tab away/return with an open detail and unsaved editor/access form; keyboard focus order/trap/restoration; clean mobile viewport captures including scrolled preview/detail bottoms and both seller illustration variants. No assertion of complete accessibility or user validation. HTTPS/proxy/gate and AWS checks remain pending separately.

An earlier run stopped on ambiguous `#preview h3`; test selector was fixed to direct preview title. It was a test-script defect, not an observed application failure. Current backend checks remain 18 Python and 5 mocked Node tests; no application source changed after those passed.
