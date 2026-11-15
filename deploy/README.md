# Reference deployment configuration

These examples illustrate a private single-host marketplace deployment. All service names, filesystem paths and public hostnames are generic. Actual hosts, owner/device identities, pinned keys and passwords must be supplied privately. These examples are not a migration plan for an existing installation and have not been deployed as part of this portfolio publication.

## Architecture

Tailscale Serve HTTPS → owner/device-restricted loopback Caddy → loopback Python → SQLite. The selectable application account is still a demonstration identity, not production authentication. Network access does not create buyer/seller membership.

`Caddyfile.private` checks trusted gateway identity and configured device addresses before Basic Auth. `caddy-hardening.conf` restricts the proxy process. `marketplace.service` runs the app without privileges and keeps its data separate from code releases. The older public `Caddyfile` uses `marketplace.example.com` as a placeholder; choose an access design deliberately rather than applying both configurations.

## Operator configuration

Use `connection.example.json` as a schema for ignored `private/connection.json`. Keep `private/marketplace.pem`, `private/known_hosts`, passwords and connection details outside Git. The helpers require this private configuration; they are not a one-command hosting setup. Environment settings use the `MARKETPLACE_` prefix.

Provisioning, gateway cutover, patching and release scripts can change a host. Review them against the intended environment before use. This repository provides examples, not a complete provisioning or migration system. Do not run them against an existing deployment simply to update documentation.

## Data and recovery

Reference data lives at `/var/lib/marketplace/marketplace.sqlite3`, independently of `/opt/marketplace/releases/`. Releases must preserve data. The backup timer uses SQLite's backup API and integrity checks, retaining seven copies. The encrypted off-host helper is operator-run, not unattended disaster recovery. Restore into a separate path and verify before switching; code rollback must not overwrite newer data.

`acceptance.py --disposable` temporarily switches a configured host to test data. It is disruptive and must not run during a demonstration. Prefer the local disposable browser runner for routine review.

## Limits

These examples do not establish production identity, a recovery SLA, delivered alerts, a tested load capacity or completed accessibility review. See the [technical specification](../TECH_SPEC_Marketplace.md).

Before publishing, run `python3 scripts/audit-secrets.py .`. Enable the commit guard with `git config core.hooksPath .githooks`. Exclude credentials, keys, private directories, local databases and backups.
