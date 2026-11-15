"""Audit reachable Git blobs without printing secret values. No external service."""
import io,json,re,subprocess,sys,zipfile
from pathlib import Path
repo=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args])
patterns={
'private_key':rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
'aws_access_key':rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
'github_token':rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})',
'tailscale_auth_key':rb'tskey-(?:auth|api|client)-[A-Za-z0-9_-]{12,}',
'google_oauth_token':rb'ya29\.[A-Za-z0-9_-]{20,}',
'credential_assignment':rb'(?im)^\s*(?:AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN|aws_secret_access_key|aws_session_token)\s*[=:]\s*[\x22\x27]?[A-Za-z0-9/+=]{20,}'
}
known=[]
for name in ['deploy/private/demo-password.txt','deploy/private/backup-encryption-password.txt']:
    p=Path(name)
    if p.exists(): known.append((p.name,p.read_bytes().strip()))
# Compare locally cached AWS credentials in memory; never write or print values.
def walk(value):
    if isinstance(value,dict):
        for key,val in value.items():
            if isinstance(val,str) and key.lower() in ['accesskeyid','secretaccesskey','sessiontoken','refreshtoken','accesstoken'] and len(val)>15:known.append(('cached_credential',val.encode()))
            else:walk(val)
    elif isinstance(value,list):
        for val in value:walk(val)
for p in (Path.home()/'.aws'/'login').rglob('*.json'):
    try:walk(json.loads(p.read_text()))
    except (ValueError,OSError):pass
entries={line.split(b' ',1)[0].decode():line.split(b' ',1)[1].decode(errors='replace') for line in git('rev-list','--objects','--all').splitlines() if b' ' in line}
# Include the index so the same check can reject newly staged secrets.
for line in git('ls-files','--stage').splitlines():
    meta,name=line.split(b'\t',1)
    entries[meta.split()[1].decode()]=name.decode(errors='replace')
findings=[];count=0
for oid,name in entries.items():
    if git('cat-file','-t',oid).strip()!=b'blob':continue
    count+=1;data=git('cat-file','blob',oid);parts=[(name,data)]
    if data.startswith(b'PK'):
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                parts += [(name+'!'+n,z.read(n)) for n in z.namelist() if n.endswith(('.xml','.txt','.json','.rels','.md'))]
        except zipfile.BadZipFile:pass
    for path,content in parts:
        for label,pat in patterns.items():
            if re.search(pat,content):findings.append({'object':oid,'path':path,'rule':label})
        for label,secret in known:
            if secret and secret in content:findings.append({'object':oid,'path':path,'rule':'exact_'+label})
tracked=git('ls-files').decode().splitlines()
for name in tracked:
    if re.search(r'(^|/)(?:private|\.aws)/|\.(?:pem|key)$|(^|/)tokens\.json$|(^|/)\.env(?:$|\.(?!example$))',name):findings.append({'path':name,'rule':'sensitive_path'})
print(json.dumps({'reachable_blobs_checked':count,'findings':findings},indent=2))
sys.exit(bool(findings))
