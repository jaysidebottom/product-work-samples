#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
systemctl start marketplace-backup
apt-get update
apt-get upgrade -y
apt-get install -y linux-aws linux-headers-aws linux-image-aws
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/noble.noarmor.gpg -o /usr/share/keyrings/tailscale-archive-keyring.gpg
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/noble.tailscale-keyring.list -o /etc/apt/sources.list.d/tailscale.list
apt-get update
apt-get install -y tailscale
systemctl enable --now tailscaled
# This sorts before Ubuntu's cloud-init SSH settings; validate before reload.
printf 'PermitRootLogin no\nPasswordAuthentication no\nKbdInteractiveAuthentication no\n' > /etc/ssh/sshd_config.d/00-marketplace-hardening.conf
sshd -t
systemctl reload ssh
cat > /etc/systemd/system/caddy.service.d/hardening.conf <<'UNIT'
[Service]
NoNewPrivileges=true
ProtectHome=true
PrivateDevices=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
LockPersonality=true
AmbientCapabilities=
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
UNIT
systemctl daemon-reload
systemctl restart caddy
systemctl is-active caddy marketplace tailscaled
sshd -T | grep -E '^(permitrootlogin|passwordauthentication) '
