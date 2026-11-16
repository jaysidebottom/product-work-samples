"""Deploy a committed release to the existing private Marketplace host, preserving data."""
import argparse,subprocess
from pathlib import Path
from runtime import SSH
parser=argparse.ArgumentParser()
parser.add_argument('--repo',required=True,help='Clean Git checkout containing the release')
args=parser.parse_args()
repo=Path(args.repo).resolve()
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args])
def remote(command,data=None):
    return subprocess.check_output(SSH+[command],input=data)
if git('status','--porcelain').strip():raise SystemExit('Release checkout must be clean')
sha=git('rev-parse','HEAD').decode().strip()
archive=git('archive','--format=tar',sha,'projects/marketplace/app.py','projects/marketplace/static','projects/marketplace/tests','deploy/backup.py','deploy/marketplace.service','deploy/marketplace-backup.service','deploy/marketplace-backup.timer')
remote('sudo test -f /etc/marketplace/private.env && sudo test -f /etc/systemd/system/caddy.service.d/private.conf')
remote(f'sudo mkdir -p /opt/marketplace/releases/{sha} && sudo tar xf - -C /opt/marketplace/releases/{sha}',archive)
script=f'''set -eu
sudo systemctl start marketplace-backup
sudo systemctl stop marketplace
sudo ln -sfn /opt/marketplace/releases/{sha} /opt/marketplace/current
sudo cp /opt/marketplace/current/deploy/marketplace*.service /opt/marketplace/current/deploy/marketplace-backup.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now marketplace marketplace-backup.timer
sudo systemctl restart marketplace
sudo systemctl is-active marketplace caddy tailscaled
'''
print(remote('bash -s',script.encode()).decode())
Path('deploy/private/release-sha.txt').write_text(sha+'\n')
print('Installed release',sha)
