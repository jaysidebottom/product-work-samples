"""Local, synthetic-data marketplace. Python standard library only."""
import argparse
import json
import os
import re
import sqlite3
import sys
import uuid
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
BASE_FIELDS = ('title', 'category', 'summary', 'description', 'specifications', 'timing', 'contactName', 'contactEmail')
MARKETING_FIELDS = ('highlights', 'visual', 'companyBio', 'companyExpertise', 'companyWebsite', 'companyLocation')
DETAIL_FIELDS = ('useCases', 'deployment', 'successCriteria')
FIELDS = BASE_FIELDS + MARKETING_FIELDS + DETAIL_FIELDS
SUMMARY_FIELDS = BASE_FIELDS[:3] + MARKETING_FIELDS
VISUALS = ('', 'relationships', 'telemetry')
ORGS = {o['id']: o for o in [
    dict(id='buyer-a', name='Civic Research Office', role='buyer'),
    dict(id='buyer-b', name='Regional Operations', role='buyer'),
    dict(id='seller-a', name='Northstar Analytics', role='seller'),
    dict(id='seller-b', name='Signal Works', role='seller'),
]}
FIXTURES = [
    ('catalog-a','seller-a','Infrastructure relationship analysis','Threat intelligence','Explore relationships across domains, IPs, and certificates.','A configurable workspace with source-linked observations.','JSON and CSV exports; customer-managed dataset entitlements.','Pilot available in Q1','Morgan Lee','morgan@northstar.example'),
    ('catalog-b','seller-b','Network telemetry workspace','Network analytics','A workspace for reviewing network observations.','Private implementation detail for Signal Works.','On-premises deployment evaluation.','Availability on request','Alex Chen','alex@signal.example'),
    ('wishlist-a','buyer-a','Map related infrastructure','Threat intelligence','Seeking source-linked infrastructure discovery capabilities.','Analysts need historical relationships across multiple datasets.','Evidence timestamps, saved views, and access controls required.','Evaluation planned for Q1','Jordan Ellis','jordan@civic.example'),
    ('wishlist-b','buyer-b','Review operational telemetry','Network analytics','Seeking tools to explore operational observations.','Private evaluation scope for Regional Operations.','Structured exports and configurable time windows.','Discovery phase','Taylor Reed','taylor@regional.example'),
]

# Fictional listing content. Generic diagrams are illustrations, not product screenshots.
ENRICHED = {
 'catalog-a': dict(
  summary='Connect domains, IPs, and certificates to investigate related infrastructure.',
  description='Start with a domain or IP, choose available observation sources, and explore relationships in a linked graph and table. Analysts can inspect the record and observation time behind each connection, refine the time window, and save an evidence-backed view for colleagues. Shared infrastructure is a lead to investigate, not proof of common ownership.',
  highlights='Source-linked relationship exploration\nSynchronized graph and table views\nSaved findings with evidence context', visual='relationships',
  companyBio='Northstar Analytics is a fictional specialist in investigation software for research and cyber analysis teams. Its product focus is making infrastructure observations easier to explore, explain, and hand off.',
  companyExpertise='Infrastructure analysis; evidence provenance; collaborative investigations',companyWebsite='https://northstar.example',companyLocation='Arlington, Virginia · Fictional demo company',
  useCases='Investigate domains sharing observed infrastructure.\nReview changes across a selected time window.\nPrepare an evidence-backed handoff to another analyst.',
  deployment='Customer-managed evaluation environment. JSON and CSV imports/exports; source access depends on customer entitlements. Integration scope is agreed during discovery.',
  specifications='Domain and IP inputs; timestamped DNS and certificate observations; graph/table navigation; saved views; JSON/CSV export. No automatic attribution or maliciousness verdict.',
  timing='Illustrative four-week pilot: source mapping, sample-data setup, analyst walkthrough, and evaluation review.'),
 'catalog-b': dict(
  summary='Turn network observations into a focused review of activity, exceptions, and operational patterns.',
  description='Bring supported network observations into a common review workspace. Filter by time and source, compare activity across segments, and inspect the underlying records behind a notable pattern. Teams can record review notes and export selected observations for follow-up. The workspace supports analyst triage; it does not automatically block traffic.',
  highlights='Time-based activity review\nSource-level observation drill-down\nExportable investigation context', visual='telemetry',
  companyBio='Signal Works is a fictional software company focused on helping operations teams understand network telemetry. Its tools emphasize traceable observations and practical analyst workflows.',
  companyExpertise='Network telemetry; operational analytics; analyst triage',companyWebsite='https://signal.example',companyLocation='Raleigh, North Carolina · Fictional demo company',
  useCases='Review unusual activity within an operational time window.\nCompare observations across network segments.\nExport a bounded set of records for specialist investigation.',
  deployment='On-premises evaluation with customer-provided sample data. Batch CSV/JSON ingestion; schema mapping and refresh cadence are scoped during evaluation.',
  specifications='Timestamp and source filters; segment comparison; record drill-down; review notes; CSV/JSON export. No packet capture appliance or automated response capability included.',
  timing='Illustrative evaluation: agree sample schema, ingest a bounded dataset, and run a two-week operator review.'),
 'wishlist-a': dict(
  summary='Seeking a way to investigate related infrastructure and explain findings with traceable evidence.',
  description='Our research analysts currently compare domain and IP observations in separate tools. We need a workflow that keeps the investigation question, relationship view, and supporting records together so a second analyst can reproduce the finding.',
  useCases='Start with a domain and identify shared infrastructure in a specified time range.\nInspect supporting records and distinguish observations from assumptions.\nHand off a saved view without losing provenance.',
  specifications='Required: timestamped evidence, source attribution, graph and table views, and access-controlled saved findings. Preferred: JSON/CSV interchange. Shared infrastructure must not be presented as proof of common ownership.',
  deployment='Evaluation uses synthetic or approved sample data only. Existing source entitlements must be respected. No external transfer of operational datasets during the initial evaluation.',
  successCriteria='An analyst can reproduce a finding from linked records; a colleague can reopen the saved context; restricted evidence is unavailable to unauthorized users.',
  timing='Illustrative schedule: requirements review in Q1, followed by a four-week sample-data evaluation.'),
 'wishlist-b': dict(
  summary='Seeking a workspace to review operational network activity and hand off unusual patterns for investigation.',
  description='Our operations team needs to compare activity across time windows and segments without manually stitching together multiple exports. The initial evaluation will focus on bounded analyst review rather than automated detection or response.',
  useCases='Compare two time windows for one network segment.\nTrace a notable pattern to its original observations.\nExport selected records and review notes for a specialist.',
  specifications='Required: source/time filters, record drill-down, structured export, and clear handling of missing observations. Preferred: repeatable saved filters and review notes.',
  deployment='Must support a customer-managed evaluation environment. Sample schemas and data volume will be agreed before ingestion; production access is outside the initial evaluation.',
  successCriteria='Operators can locate the source records behind a pattern, export the relevant subset, and explain coverage gaps without relying on vendor assistance.',
  timing='Illustrative schedule: discovery workshops followed by a two-week operator evaluation.')
}

def fixture_content(row):
    return {**dict(zip(BASE_FIELDS, row[2:])), **ENRICHED[row[0]]}

class Problem(Exception):
    def __init__(self, status, message):
        self.status, self.message = status, message

def unavailable():
    raise Problem(404, 'Item unavailable')

def clean_content(value, role):
    if not isinstance(value, dict) or set(value) - set(FIELDS):
        raise Problem(400, 'Unknown or invalid offering fields')
    result = {}
    for field in FIELDS:
        v = value.get(field, '')
        if not isinstance(v, str) or len(v) > 5000:
            raise Problem(400, f'Check {field}: maximum 5,000 characters')
        result[field] = v.strip()
    for field in FIELDS[:3]:
        if not result[field]:
            raise Problem(400, f'{field} is required')
    if result['contactEmail'] and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', result['contactEmail']):
        raise Problem(400, 'Enter a valid contact email')
    if role == 'buyer' and any(result[f] for f in MARKETING_FIELDS):
        raise Problem(400, 'Marketing fields are for seller offerings')
    if result['visual'] not in VISUALS:
        raise Problem(400, 'Choose an available illustrative diagram')
    if len(result['highlights'].splitlines()) > 3 or any(len(line) > 100 for line in result['highlights'].splitlines()):
        raise Problem(400, 'Use up to three capability highlights, 100 characters each')
    try:
        website = urlsplit(result['companyWebsite'])
    except ValueError:
        raise Problem(400, 'Enter a valid HTTPS company website')
    if result['companyWebsite'] and (website.scheme != 'https' or not website.hostname or website.username or website.password):
        raise Problem(400, 'Company website must be an HTTPS URL without credentials')
    return result

def clean_grants(value, actor):
    if not isinstance(value, dict):
        raise Problem(400, 'Invalid access settings')
    for recipient, level in value.items():
        if recipient not in ORGS or ORGS[recipient]['role'] == actor['role'] or level not in ('summary','full'):
            raise Problem(400, 'Choose an opposite-role organization and valid access level')
    return value

def project(item, viewer, grants):
    """Allowlisted projection, shared by lists/detail/preview; private values never leave here."""
    owner = ORGS[item['owner']]
    if owner['id'] == viewer['id']:
        access = 'owner'
    elif owner['role'] == viewer['role']:
        return None
    else:
        access = grants.get(viewer['id'])
    if not access:
        return None
    content = json.loads(item['content'])
    allowed = SUMMARY_FIELDS if access == 'summary' else FIELDS
    if owner['role'] == 'buyer':
        allowed = tuple(f for f in allowed if f not in MARKETING_FIELDS)
    result = dict(id=item['id'], organization=owner['name'], kind='wishlist' if owner['role']=='buyer' else 'catalog', access=access,
                  **{f: content.get(f, '') for f in allowed})
    if access == 'owner':
        result['grants'] = grants
    return result

class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS items(id TEXT PRIMARY KEY, owner TEXT NOT NULL, content TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS grants(item TEXT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
                    recipient TEXT NOT NULL, level TEXT NOT NULL CHECK(level IN ('summary','full')), PRIMARY KEY(item,recipient));
                CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY);
            ''')
            if not db.execute("SELECT 1 FROM settings WHERE key='seeded'").fetchone():
                self.seed(db)
            # Upgrade only untouched original fixtures; never overwrite edited listings or grants.
            if not db.execute("SELECT 1 FROM settings WHERE key='rich-listings-v1'").fetchone():
                for row in FIXTURES:
                    saved = db.execute('SELECT content FROM items WHERE id=? AND owner=?', row[:2]).fetchone()
                    if saved and json.loads(saved['content']) == dict(zip(BASE_FIELDS, row[2:])):
                        db.execute('UPDATE items SET content=? WHERE id=?', (json.dumps(fixture_content(row)), row[0]))
                db.execute("INSERT INTO settings VALUES ('rich-listings-v1')")

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            with db:
                yield db
        finally:
            db.close()

    def seed(self, db):
        db.execute('DELETE FROM grants')
        db.execute('DELETE FROM items')
        db.executemany('INSERT INTO items VALUES (?,?,?)',
                       [(v[0],v[1],json.dumps(fixture_content(v))) for v in FIXTURES])
        db.execute("INSERT OR IGNORE INTO settings VALUES ('seeded')")

    def request(self, method, actor_id, query=None, body=None):
        """Demo identity is intentionally selectable. Role always resolves from fixed server directory."""
        if not isinstance(actor_id, str) or actor_id not in ORGS:
            raise Problem(401, 'Select a demo account')
        actor = ORGS[actor_id]
        query = query or {}
        with self.connect() as db:
            def get_item(id):
                item = db.execute('SELECT * FROM items WHERE id=?',(id,)).fetchone()
                return item if item else unavailable()
            def grants(id):
                return dict(db.execute('SELECT recipient,level FROM grants WHERE item=?',(id,)).fetchall())
            def own(item):
                if item['owner'] != actor_id:
                    unavailable()
            if method == 'GET':
                view = query.get('view')
                if view == 'context':
                    return 200, dict(actor=actor, organizations=list(ORGS.values()))
                if view in ('mine','discover'):
                    items = []
                    for item in db.execute('SELECT * FROM items ORDER BY id'):
                        if (item['owner'] == actor_id) != (view == 'mine'):
                            continue
                        visible = project(item,actor,grants(item['id']))
                        if visible and any(query.get('q','').lower() in visible[f].lower() for f in FIELDS[:3]):
                            items.append(visible)
                    return 200, dict(items=items,count=len(items))
                if view in ('detail','preview'):
                    item = get_item(query.get('id',''))
                    access = grants(item['id'])
                    if view == 'detail':
                        visible = project(item,actor,access)
                        return 200, dict(item=visible if visible else unavailable())
                    own(item)
                    recipient = ORGS.get(query.get('recipient'))
                    if not recipient:
                        raise Problem(400, 'Choose a recipient')
                    proposed = query.get('level')
                    if proposed is not None:
                        if proposed not in ('none','summary','full') or recipient['role'] == actor['role']:
                            raise Problem(400, 'Invalid preview')
                        access = {} if proposed == 'none' else {recipient['id']:proposed}
                    return 200, dict(item=project(item,recipient,access),proposed=proposed is not None)
                raise Problem(400, 'Unknown view')
            if method != 'POST' or not isinstance(body,dict):
                raise Problem(400, 'Invalid request')
            action = body.get('action')
            if action == 'reset':
                self.seed(db)
                return 200, dict(ok=True)
            if action == 'create':
                values = clean_content(body.get('content'), actor['role'])
                id = str(uuid.uuid4())
                db.execute('INSERT INTO items VALUES (?,?,?)',(id,actor_id,json.dumps(values)))
                return 201, dict(id=id)
            id = body.get('id')
            item = get_item(id if isinstance(id,str) else '')
            own(item)
            if action == 'edit':
                values = clean_content(body.get('content'), actor['role'])
                db.execute('UPDATE items SET content=? WHERE id=?',(json.dumps(values),id))
                return 200, dict(ok=True)
            if action == 'access':
                next_grants = clean_grants(body.get('grants'),actor)
                # Validation precedes a single transaction replacing the whole grant set.
                db.execute('DELETE FROM grants WHERE item=?',(id,))
                db.executemany('INSERT INTO grants VALUES (?,?,?)',[(id,r,l) for r,l in next_grants.items()])
                return 200, dict(ok=True)
            raise Problem(400, 'Unknown action')

class Handler(BaseHTTPRequestHandler):
    server_version = 'MarketplaceDemo/1.0'
    def send(self, status, content, mime='application/json'):
        if status >= 400:
            # Never record URLs, query strings, submitted fields, or credentials.
            print(json.dumps({'event': 'http_failure', 'method': getattr(self, 'command', 'unknown'),
                              'status': status}), file=sys.stderr, flush=True)
        if mime == 'application/json':
            content = json.dumps(content).encode()
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length',str(len(content)))
        self.send_header('Cache-Control','no-store')
        self.send_header('Vary','X-Demo-Account')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == '/api/marketplace':
            self.api('GET',dict((k,v[-1]) for k,v in parse_qs(url.query,keep_blank_values=True).items()))
            return
        files={'/':('index.html','text/html; charset=utf-8'), '/app.js':('app.js','text/javascript; charset=utf-8'), '/style.css':('style.css','text/css; charset=utf-8')}
        if url.path not in files:
            self.send(404,{'error':'Page unavailable'})
            return
        name,mime = files[url.path]
        self.send(200,(ROOT/'static'/name).read_bytes(),mime)

    def do_POST(self):
        if urlsplit(self.path).path != '/api/marketplace':
            self.send(404,{'error':'Page unavailable'})
            return
        # Reject browser cross-origin mutations. No CORS or public-data endpoint.
        origin = self.headers.get('Origin')
        # A configured public origin is authoritative behind TLS termination.
        # Never trust client-supplied Forwarded/X-Forwarded-* headers.
        expected_origin = getattr(self.server, 'public_origin', None) or 'http://' + self.headers.get('Host','')
        if origin and origin != expected_origin:
            self.send(403,{'error':'Origin not allowed'})
            return
        try:
            length = int(self.headers.get('Content-Length','0'))
            if length < 0 or length > 120000:
                raise Problem(413,'Offering is too large')
            body = json.loads(self.rfile.read(length))
        except Problem as e:
            self.send(e.status,{'error':e.message}); return
        except (ValueError, UnicodeDecodeError):
            self.send(400,{'error':'Invalid request'}); return
        self.api('POST',body=body)

    def api(self,method,query=None,body=None):
        try:
            status,result = self.server.store.request(method,self.headers.get('X-Demo-Account'),query,body)
            self.send(status,result)
        except Problem as e:
            self.send(e.status,{'error':e.message})
        except Exception:
            self.log_error('Request failed')
            self.send(500,{'error':'Could not complete the request. Please try again.'})

    def log_message(self,format,*args):
        pass  # Do not log offering queries or contents.

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8766)
    parser.add_argument('--host',default='127.0.0.1')
    parser.add_argument('--public-origin',default=os.environ.get('MARKETPLACE_PUBLIC_ORIGIN'),
                        help='Exact HTTPS origin behind the demo reverse proxy, without trailing slash')
    parser.add_argument('--db',default=os.environ.get('MARKETPLACE_DB',str(ROOT/'data'/'marketplace.sqlite3')))
    parser.add_argument('--reset',action='store_true',help='Reset fictional fixtures and exit')
    args = parser.parse_args()
    if args.public_origin:
        try:
            public = urlsplit(args.public_origin)
            valid = (public.scheme == 'https' and public.hostname and not public.username
                     and not public.password and not public.path and not public.query
                     and not public.fragment and public.port != 0)
        except ValueError:
            valid = False
        if not valid:
            parser.error('--public-origin must be an HTTPS origin without credentials, path, query, or fragment')
    store = Store(args.db)
    if args.reset:
        store.request('POST','seller-a',body={'action':'reset'})
        print('Demo fixtures reset.'); raise SystemExit(0)
    server = ThreadingHTTPServer((args.host,args.port),Handler)
    server.store = store
    server.public_origin = args.public_origin
    print(f'Marketplace demo: http://{args.host}:{args.port}',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
