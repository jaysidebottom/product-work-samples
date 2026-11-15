"""Cut over to owner/device-restricted Tailscale Serve; config stays ignored."""
import json,shlex,subprocess
from pathlib import Path
cfg=json.loads(Path('deploy/private/connection.json').read_text())
for field in ['owner','device_ipv4','device_ipv6','url','host','host_key_alias']:
    if not cfg.get(field):raise SystemExit('Missing required private configuration: '+field)
ssh=['ssh','-i','deploy/private/marketplace.pem','-o','IdentitiesOnly=yes','-o','UserKnownHostsFile=deploy/private/known_hosts','-o','HostKeyAlias='+cfg['host_key_alias'],'ubuntu@'+cfg['host']]
def remote(command,data=None):
    result=subprocess.run(ssh+[command],input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if result.returncode:
        print(result.stderr.decode());raise SystemExit(result.returncode)
    return result.stdout
remote('sudo cp -n /etc/caddy/Caddyfile /etc/caddy/Caddyfile.pre-private; sudo systemctl start marketplace-backup')
env=''.join(k+'='+shlex.quote(v)+'\n' for k,v in {'MARKETPLACE_OWNER':cfg['owner'],'MARKETPLACE_DEVICE_IPV4':cfg['device_ipv4'],'MARKETPLACE_DEVICE_IPV6':cfg['device_ipv6'],'MARKETPLACE_PUBLIC_ORIGIN':cfg['url']}.items())
remote('sudo install -m 600 /dev/stdin /etc/marketplace/private.env',env.encode())
remote('sudo install -m 644 /dev/stdin /etc/caddy/Caddyfile',Path('deploy/Caddyfile.private').read_bytes())
remote('sudo install -m 644 /dev/stdin /etc/systemd/system/caddy.service.d/hardening.conf',Path('deploy/caddy-hardening.conf').read_bytes())
script='''set -eu
sudo mkdir -p /etc/systemd/system/marketplace.service.d
printf '[Service]\\nEnvironmentFile=/etc/marketplace/private.env\\n' | sudo tee /etc/systemd/system/caddy.service.d/private.conf >/dev/null
printf '[Service]\\nEnvironmentFile=/etc/marketplace/private.env\\n' | sudo tee /etc/systemd/system/marketplace.service.d/private.conf >/dev/null
sudo sh -c 'set -a; . /etc/marketplace/caddy.env; . /etc/marketplace/private.env; caddy validate --config /etc/caddy/Caddyfile'
sudo systemctl daemon-reload
sudo systemctl restart marketplace caddy
sudo tailscale serve --bg --https=443 http://127.0.0.1:8767
sudo systemctl is-active marketplace caddy tailscaled
sudo tailscale serve status --json
'''
print(remote('bash -s',script.encode()).decode())
