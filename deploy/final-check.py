"""Read-only HTTPS smoke test and encrypted off-host backup receipt."""
import base64,hashlib,json,os,secrets,subprocess,urllib.request
from pathlib import Path
from runtime import PRIVATE as root, SSH as ssh, BASE, CONFIG
os.umask(0o077)
password=(root/'demo-password.txt').read_bytes().strip()
auth='Basic '+base64.b64encode(b'demo:'+password).decode()
for actor in ['seller-a','buyer-a','seller-b','buyer-b']:
    req=urllib.request.Request(BASE+'/api/marketplace?view=mine',headers={'Authorization':auth,'X-Demo-Account':actor})
    with urllib.request.urlopen(req,timeout=15) as response:
        data=json.load(response)
        assert data['count']==len(data['items'])
key=root/'backup-encryption-password.txt'
if not key.exists():key.write_text(secrets.token_urlsafe(48));key.chmod(0o600)
backup=subprocess.check_output(ssh+['sudo sh -c \'cat "$(ls -1 /var/lib/marketplace/backups/*.sqlite3 | tail -1)"\''])
subprocess.run(['openssl','enc','-aes-256-cbc','-pbkdf2','-salt','-pass','file:'+str(key),'-out',str(root/'initial-backup.sqlite3.enc')],input=backup,check=True)
restored=subprocess.check_output(['openssl','enc','-d','-aes-256-cbc','-pbkdf2','-pass','file:'+str(key),'-in',str(root/'initial-backup.sqlite3.enc')])
assert restored==backup
receipt={'url':BASE,'instance':'marketplace-demo-web','ip':CONFIG['host'],'region':'us-east-1','release':(root/'release-sha.txt').read_text().strip(),'backup_sha256':hashlib.sha256(backup).hexdigest(),'backup_encryption_roundtrip':'passed'}
(root/'inventory.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('All four accounts healthy; encrypted off-host backup verified.')
