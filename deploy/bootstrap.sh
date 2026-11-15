#!/bin/bash
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl gnupg python3
curl -1fsSL https://dl.cloudsmith.io/public/caddy/stable/gpg.key | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1fsSL https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt > /etc/apt/sources.list.d/caddy-stable.list
chmod o+r /usr/share/keyrings/caddy-stable-archive-keyring.gpg /etc/apt/sources.list.d/caddy-stable.list
apt-get update
apt-get install -y caddy
systemctl stop caddy
useradd --system --home /var/lib/marketplace --shell /usr/sbin/nologin marketplace
install -d -o marketplace -g marketplace -m 700 /var/lib/marketplace /var/lib/marketplace/backups
install -d -m 755 /opt/marketplace/releases /etc/marketplace
install -d -m 755 /etc/systemd/journald.conf.d
printf '[Journal]\nSystemMaxUse=100M\nMaxRetentionSec=7day\n' > /etc/systemd/journald.conf.d/marketplace.conf
systemctl restart systemd-journald
touch /var/lib/marketplace-bootstrap-ready
