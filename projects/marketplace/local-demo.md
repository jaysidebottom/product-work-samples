# Run the marketplace locally

From the repository root, with Python 3.9 or later:

```sh
python3 projects/marketplace/app.py
```

Open **http://127.0.0.1:8766**. The server binds to loopback by default. Keep the terminal open; Ctrl+C stops it. Restarting with the same database preserves saved items and grants. No cloud account, VPN, password or external API is required.

## Storage and isolation

The default database is `projects/marketplace/data/marketplace.sqlite3`, ignored by Git. Do not reset or delete an existing database to run tests. For an independent walkthrough, select a new path and port:

```sh
python3 projects/marketplace/app.py --db /tmp/marketplace-walkthrough.sqlite3 --port 8768
```

Open http://127.0.0.1:8768. Reusing that path preserves that walkthrough's data. Choose another new path for a fresh dataset. Local and hosted databases are independent.

The Reset demo action and `--reset` intentionally erase edits and grants in the selected database. Use them only when those edits may be discarded.

## Troubleshooting

If the port is occupied, use `--port 8768` and the matching browser URL. Use HTTP for this local server. If Python is unavailable, install Python before running the prototype. Refresh the page after a code update; restart the server after Python changes.

## Verification

Run unit/UI checks from the root as documented in the README. The browser runner `python3 projects/marketplace/qa/run-disposable.py` creates its own temporary database and never opens presentation data. Browser dependencies and configuration are described in [marketplace instructions](walkthrough.md).
