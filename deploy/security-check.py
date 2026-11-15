"""Bounded read-only probes; never creates, edits, or resets demo data."""
import base64,json,socket,ssl,urllib.request,urllib.error
from pathlib import Path
from runtime import BASE as base, CONFIG
from urllib.parse import urlsplit
host=urlsplit(base).hostname
auth='Basic '+base64.b64encode(b'demo:'+Path('deploy/private/demo-password.txt').read_bytes().strip()).decode()
def req(path,headers=None,body=None):
    r=urllib.request.Request(base+path,headers=headers or {},data=None if body is None else json.dumps(body).encode())
    try:resp=urllib.request.urlopen(r,timeout=10)
    except urllib.error.HTTPError as e:resp=e
    value=resp.read()
    return resp.status,dict(resp.headers),value
out={}
for path in ['/','/app.js','/style.css','/api/marketplace?view=mine','/.env','/.git/config','/marketplace.sqlite3','/../etc/passwd','/%2e%2e/etc/passwd']:
    status,_,_=req(path);assert status==401,(path,status)
    out['unauthenticated '+path]=status
for path in ['/.env','/.git/config','/marketplace.sqlite3','/../etc/passwd','/%2e%2e/etc/passwd']:
    status,_,_=req(path,{'Authorization':auth});assert status==404,(path,status)
out['authenticated_sensitive_paths']='404'
status,headers,_=req('/',{'Authorization':auth});assert status==200
out['security_headers']={k:v for k,v in headers.items() if k.lower() in ['content-security-policy','cache-control','x-content-type-options','strict-transport-security','referrer-policy','server']}
assert req('/api/marketplace?view=mine',{'Authorization':auth})[0]==401
out['missing_demo_identity']=401
for origin in ['https://evil.example','null','http://'+host]:
    status,_,_=req('/api/marketplace',{'Authorization':auth,'X-Demo-Account':'seller-a','Origin':origin,'X-Forwarded-Host':'evil.example','X-Forwarded-Proto':'https'}, {'action':'edit','id':'security-review-nonexistent','content':{}})
    assert status==403,(origin,status)
out['hostile_null_http_origins']='403 even with forged forwarding headers'
for port in [2019,8766,5432]:
    try:
        with socket.create_connection((CONFIG['host_key_alias'],port),timeout=2):out['port '+str(port)]='REACHABLE'
    except (socket.timeout,ConnectionRefusedError,OSError):out['port '+str(port)]='unreachable'
ctx=ssl.create_default_context()
with socket.create_connection((host,443),timeout=10) as raw:
    with ctx.wrap_socket(raw,server_hostname=host) as tls:
        out['tls']={'version':tls.version(),'cipher':tls.cipher()[0],'expires':tls.getpeercert()['notAfter']}
Path('deploy/private/security-probes.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
