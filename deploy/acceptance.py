"""Hosted acceptance against a separate database before sharing the URL."""
import sys
if "--disposable" not in sys.argv:
    raise SystemExit("Requires --disposable: temporarily switches the demo to isolated test data. Do not run during demonstrations.")
import base64, concurrent.futures, json, socket, subprocess, time, urllib.request, urllib.error
from pathlib import Path
from runtime import BASE, SSH, CONFIG
AUTH='Basic '+base64.b64encode(b'demo:'+Path('deploy/private/demo-password.txt').read_bytes().strip()).decode()
def remote(script):
    return subprocess.check_output(SSH+['sudo bash -s'],input=script.encode()).decode()
def request(actor='seller-a',query='',body=None,path='/api/marketplace',auth=AUTH,origin=BASE):
    headers={'X-Demo-Account':actor}
    if auth: headers['Authorization']=auth
    if origin: headers['Origin']=origin
    data=None if body is None else json.dumps(body).encode()
    if data:headers['Content-Type']='application/json'
    req=urllib.request.Request(BASE+path+('?' + query if query else ''),data=data,headers=headers)
    try:r=urllib.request.urlopen(req,timeout=20)
    except urllib.error.HTTPError as e:r=e
    raw=r.read()
    try:value=json.loads(raw)
    except ValueError:value=raw.decode()
    return r.status,value,dict(r.headers)

def check():
    for path in ['/','/app.js','/style.css','/api/marketplace']:
        assert request(path=path,auth=None)[0]==401
        assert request(path=path,auth='Basic ZGVtbzpiYWQ=')[0]==401
    assert request(path='/')[0]==200
    assert request(query='view=mine')[2]['Cache-Control']=='no-store'
    assert request(body={'action':'reset'},origin='https://evil.example')[0]==403
    records=[]
    for owner,peer,recipient,other in [('seller-a','seller-b','buyer-a','buyer-b'),('buyer-a','buyer-b','seller-a','seller-b')]:
        content={'title':'Acceptance '+owner,'category':'Demo','summary':'Visible summary','description':'restricted-canary','contactEmail':'qa@example.com'}
        status,data,_=request(owner,body={'action':'create','content':content});assert status==201
        id=data['id'];records.append((owner,id))
        for actor in [peer,recipient,other]:assert request(actor,'view=detail&id='+id)[0]==404
        assert request(owner,body={'action':'access','id':id,'grants':{peer:'full'}})[0]==400
        assert request(other,body={'action':'edit','id':id,'content':content})[0]==404
        for level in ['summary','full','summary','none']:
            proposed=request(owner,f'view=preview&id={id}&recipient={recipient}&level={level}')[1]['item']
            assert request(owner,body={'action':'access','id':id,'grants':{} if level=='none' else {recipient:level}})[0]==200
            status,data,_=request(recipient,'view=detail&id='+id)
            if level=='none': assert status==404 and proposed is None
            else:
                assert data['item']==proposed and 'grants' not in data['item']
                assert ('description' in data['item'])==(level=='full')
            for actor in [peer,other]:assert request(actor,'view=detail&id='+id)[0]==404
        request(owner,body={'action':'access','id':id,'grants':{recipient:'summary'}})
    start=time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(lambda n:request('seller-a','view=mine'),range(25)))
    assert all(r[0]==200 for r in results)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(lambda pair:request(pair[0],body={'action':'access','id':pair[1],'grants':{}}),records))
    assert all(r[0]==200 for r in results)
    print('HTTPS gate, both-role access matrix, previews, revocation, invalid origins, and concurrent reads/writes: PASS')
    print('25 reads / 5 workers elapsed seconds:',round(time.monotonic()-start,2))
    remote('systemctl restart marketplace\n')
    time.sleep(1)
    for owner,id in records:assert request(owner,'view=detail&id='+id)[0]==200
    print('Custom data persisted through service restart: PASS')
    print(remote('''runuser -u marketplace -- python3 - <<'INNER'
import sqlite3,sys
sys.path.insert(0,'/opt/marketplace/current/projects/marketplace')
from app import Store
src='/var/lib/marketplace/acceptance.sqlite3'; dst='/var/lib/marketplace/acceptance-restored.sqlite3'
with sqlite3.connect(src) as source, sqlite3.connect(dst) as target:
    source.backup(target)
    assert target.execute('pragma integrity_check').fetchone()[0]=='ok'
    assert not target.execute('pragma foreign_key_check').fetchall()
a,b=Store(src),Store(dst)
for actor in ['seller-a','seller-b','buyer-a','buyer-b']:
    for view in ['mine','discover']:
        assert a.request('GET',actor,{'view':view}) == b.request('GET',actor,{'view':view})
print('Backup/restore integrity and policy projections: PASS')
INNER
'''))

live_before={(actor,view):request(actor,'view='+view)[1] for actor in ['seller-a','buyer-a','seller-b','buyer-b'] for view in ['mine','discover']}
remote('''mkdir -p /etc/systemd/system/marketplace.service.d
cat > /etc/systemd/system/marketplace.service.d/acceptance.conf <<'UNIT'
[Service]
ExecStart=
ExecStart=/usr/bin/python3 -u /opt/marketplace/current/projects/marketplace/app.py --host 127.0.0.1 --port 8766 --db /var/lib/marketplace/acceptance.sqlite3
UNIT
systemctl daemon-reload
systemctl restart marketplace
''')
try:
    time.sleep(2)
    check()
finally:
    print(remote('''rm /etc/systemd/system/marketplace.service.d/acceptance.conf
systemctl daemon-reload
systemctl restart marketplace
systemctl start marketplace-backup
systemctl is-active marketplace caddy
'''))
for (actor,view),before in live_before.items():
    assert request(actor,'view='+view)[1]==before, 'Live data changed during acceptance'
print('Existing live data and grants preserved exactly: PASS')
try:
    socket.create_connection((CONFIG['host_key_alias'],8766),timeout=3).close()
    raise AssertionError('Application port exposed')
except (socket.timeout,ConnectionRefusedError):print('Raw application port blocked: PASS')
