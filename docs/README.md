# Product documents and visuals

- [Analyst Assistant PRD](analyst-assistant.html): standalone HTML with four embedded concept screens.
- [Controlled Marketplace PRD](marketplace.html): standalone HTML with five embedded screenshots from a disposable fictional-data walkthrough.
- [Marketplace screenshots](screenshots/): original PNG captures, without browser chrome.

The root Markdown PRDs are the publication sources. These HTML documents can be opened directly in a browser. Screenshots show visible portions of scrollable dialogs; they do not prove full accessibility. Native document editing sessions and private formatting snapshots are maintained separately and are not linked here.

To rebuild the HTML, install Node and the `marked` package (`npm install --no-save --package-lock=false marked`), then run `node scripts/build-docs.cjs` from the repository root. `MARKED_MODULE` can point to a separately installed package. The application itself has no Node dependency.
