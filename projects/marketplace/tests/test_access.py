import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import FIELDS, BASE_FIELDS, MARKETING_FIELDS, SUMMARY_FIELDS, FIXTURES, ORGS, Handler, Problem, Store

class MarketplaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/'test.sqlite3'
        self.store=Store(self.path)
    def tearDown(self):
        self.tmp.cleanup()
    def get(self,actor,view='detail',**q):
        return self.store.request('GET',actor,dict(view=view,**q))[1]
    def post(self,actor,action,**body):
        return self.store.request('POST',actor,body=dict(action=action,**body))[1]
    def deny(self,fn,status=404):
        with self.assertRaises(Problem) as caught: fn()
        self.assertEqual(caught.exception.status,status)
        if status==404:self.assertEqual(caught.exception.message,'Item unavailable')
    def create(self,owner):
        return self.post(owner,'create',content={f:f+' private-canary' if f not in BASE_FIELDS[:3] else f+' public-marker' for f in BASE_FIELDS if f!='contactEmail'})['id']
    def cases(self):
        return [('seller-a','seller-b','buyer-a','buyer-b'),('buyer-a','buyer-b','seller-a','seller-b')]

    def test_private_creation_and_both_role_matrix(self):
        for owner,peer,recipient,other in self.cases():
            id=self.create(owner)
            self.assertEqual(self.get(owner,id=id)['item']['grants'],{})
            for viewer in (peer,recipient,other):
                with self.subTest(owner=owner,viewer=viewer):
                    self.deny(lambda:self.get(viewer,id=id))
                    self.assertEqual(self.get(viewer,'discover'),{'items':[],'count':0})
                    self.assertEqual(self.get(viewer,'discover',q='public-marker')['count'],0)

    def test_summary_projection_in_list_detail_and_preview(self):
        allowed={'id','organization','kind','access','title','category','summary'}
        for owner,peer,recipient,other in self.cases():
            id=self.create(owner);self.post(owner,'access',id=id,grants={recipient:'summary'})
            visible=self.get(recipient,id=id)['item']
            self.assertEqual(set(visible),allowed | (set(MARKETING_FIELDS) if owner.startswith('seller') else set()))
            self.assertEqual(self.get(recipient,'discover')['items'],[visible])
            self.assertEqual(self.get(owner,'preview',id=id,recipient=recipient)['item'],visible)
            self.assertNotIn('private-canary',json.dumps(visible))
            self.assertEqual(self.get(recipient,'discover',q='private-canary')['count'],0)
            for viewer in (peer,other):self.deny(lambda:self.get(viewer,id=id))

    def test_full_downgrade_and_revoke(self):
        for owner,peer,recipient,other in self.cases():
            id=self.create(owner)
            self.post(owner,'access',id=id,grants={recipient:'full'})
            full=self.get(recipient,id=id)['item']
            self.assertEqual(set(full),{'id','organization','kind','access',*(f for f in FIELDS if owner.startswith('seller') or f not in MARKETING_FIELDS)})
            self.assertNotIn('grants',full)
            self.post(owner,'access',id=id,grants={recipient:'summary'})
            self.assertNotIn('description',self.get(recipient,id=id)['item'])
            self.post(owner,'access',id=id,grants={})
            self.deny(lambda:self.get(recipient,id=id))
            self.assertEqual(self.get(recipient,'discover')['count'],0)

    def test_nonowners_cannot_mutate_or_preview(self):
        for owner,peer,recipient,other in self.cases():
            id=self.create(owner);self.post(owner,'access',id=id,grants={recipient:'full'})
            original=self.get(owner,id=id)
            for viewer in (peer,recipient,other):
                self.deny(lambda:self.post(viewer,'edit',id=id,content={'title':'changed','category':'changed','summary':'changed'}))
                self.deny(lambda:self.post(viewer,'access',id=id,grants={other:'full'}))
                self.deny(lambda:self.get(viewer,'preview',id=id,recipient=recipient))
            self.assertEqual(self.get(owner,id=id),original)

    def test_invalid_grant_keeps_entire_existing_policy(self):
        for owner,peer,recipient,other in self.cases():
            id=self.create(owner);self.post(owner,'access',id=id,grants={recipient:'summary'})
            for bad in ({peer:'full'},{owner:'full'},{recipient:'public'},{'unknown':'full'},None,[]):
                self.deny(lambda:self.post(owner,'access',id=id,grants=bad),400)
                self.assertEqual(self.get(owner,id=id)['item']['grants'],{recipient:'summary'})
            self.post(owner,'access',id=id,grants={recipient:'full'})
            self.post(owner,'access',id=id,grants={recipient:'full'})
            self.assertEqual(self.get(owner,id=id)['item']['grants'],{recipient:'full'})

    def test_same_role_deny_even_if_database_contains_bad_grant(self):
        for owner,peer,recipient,other in self.cases():
            id=self.create(owner)
            with self.store.connect() as db: db.execute('INSERT INTO grants VALUES (?,?,?)',(id,peer,'full'))
            self.deny(lambda:self.get(peer,id=id))
            self.assertEqual(self.get(peer,'discover')['count'],0)
            self.assertIsNone(self.get(owner,'preview',id=id,recipient=peer)['item'])

    def test_proposed_preview_is_nonmutating_and_matches_later_view(self):
        id=self.create('seller-a')
        for level in ('summary','full','none'):
            preview=self.get('seller-a','preview',id=id,recipient='buyer-a',level=level)
            self.assertTrue(preview['proposed'])
            self.assertEqual(self.get('seller-a',id=id)['item']['grants'],{})
            self.deny(lambda:self.get('buyer-a',id=id))
            if level!='none':
                self.post('seller-a','access',id=id,grants={'buyer-a':level})
                self.assertEqual(preview['item'],self.get('buyer-a',id=id)['item'])
                self.post('seller-a','access',id=id,grants={})
            else:self.assertIsNone(preview['item'])

    def test_edit_retains_grants_and_persistence_across_store_restart(self):
        id=self.create('buyer-a');self.post('buyer-a','access',id=id,grants={'seller-a':'summary','seller-b':'full'})
        self.post('buyer-a','edit',id=id,content={'title':'Updated','category':'New','summary':'New summary','description':'Still restricted'})
        self.store=Store(self.path)
        self.assertEqual(self.get('buyer-a',id=id)['item']['grants'],{'seller-a':'summary','seller-b':'full'})
        self.assertEqual(self.get('seller-a',id=id)['item']['title'],'Updated')
        self.assertNotIn('description',self.get('seller-a',id=id)['item'])
        self.assertEqual(self.get('seller-b',id=id)['item']['description'],'Still restricted')

    def test_fields_validation_and_injection(self):
        for bad in ({},{'title':' ','category':'cat','summary':'sum'}, {'title':[],'category':'cat','summary':'sum'}, {'title':'x','category':'c','summary':'s','owner':'buyer-b'}, {'title':'x','category':'c','summary':'s','contactEmail':'invalid'}, {'title':'x'*5001,'category':'c','summary':'s'}, []):
            self.deny(lambda:self.post('seller-a','create',content=bad),400)
        self.deny(lambda:self.get('buyer-a',id="' OR 1=1 --"))
        self.assertEqual(self.get('seller-a','mine',q="' OR 1=1 --")['count'],0)

    def test_missing_and_unauthorized_are_identical(self):
        for id in ('catalog-a','not-an-item'):
            self.deny(lambda:self.get('buyer-a',id=id))
            self.deny(lambda:self.post('buyer-a','edit',id=id,content={}))
        self.deny(lambda:self.get(None,'context'),401)
        self.deny(lambda:self.get('admin','context'),401)

    def test_context_roles_are_immutable_and_directory_has_no_items(self):
        for actor in ORGS:
            context=self.get(actor,'context')
            self.assertEqual(context['actor'],ORGS[actor])
            self.assertTrue(all(set(o)=={'id','name','role'} for o in context['organizations']))
        self.deny(lambda:self.post('seller-a','change-role',id='catalog-a',role='buyer'),400)

    def test_reset_reestablishes_only_private_fixtures(self):
        id=self.create('seller-a');self.post('seller-a','access',id=id,grants={'buyer-a':'full'})
        self.post('seller-a','reset')
        self.store=Store(self.path)
        self.deny(lambda:self.get('seller-a',id=id))
        for actor in ORGS:
            self.assertEqual(self.get(actor,'mine')['count'],1)
            self.assertEqual(self.get(actor,'discover')['count'],0)

    def test_marketing_projection_and_full_detail_boundaries(self):
        self.post('seller-a','access',id='catalog-a',grants={'buyer-a':'summary'})
        summary=self.get('buyer-a',id='catalog-a')['item']
        self.assertEqual(summary['visual'],'relationships')
        self.assertTrue(summary['companyBio'])
        self.assertEqual(len(summary['highlights'].splitlines()),3)
        for field in ('description','useCases','deployment','successCriteria','contactEmail'):
            self.assertNotIn(field,summary)
        self.assertEqual(self.get('seller-a','preview',id='catalog-a',recipient='buyer-a')['item'],summary)
        self.assertEqual(self.get('buyer-a','discover')['items'],[summary])
        for actor in ('seller-b','buyer-b'):
            self.deny(lambda:self.get(actor,id='catalog-a'))
        self.assertNotIn('companyBio',json.dumps(self.get('buyer-a','context')))
        self.post('seller-a','access',id='catalog-a',grants={'buyer-a':'full'})
        self.assertTrue(self.get('buyer-a',id='catalog-a')['item']['deployment'])
        self.post('seller-a','access',id='catalog-a',grants={'buyer-a':'summary'})
        self.assertNotIn('deployment',self.get('buyer-a',id='catalog-a')['item'])
        self.post('seller-a','access',id='catalog-a',grants={})
        self.deny(lambda:self.get('buyer-a',id='catalog-a'))
        self.assertEqual(self.get('buyer-a','discover')['items'],[])
        # No product-specific media endpoint bypasses the item projection.
        self.assertEqual(self.wire('GET','/media/catalog-a.svg','buyer-a')[0],404)

    def test_new_field_validation_and_buyer_scope(self):
        content=dict(title='Product',category='Tools',summary='Value')
        for extra in ({'visual':'https://external.example/image.png'}, {'companyWebsite':'javascript:alert(1)'}, {'companyWebsite':'https://['}, {'companyWebsite':'https://user:pass@example.com'}, {'highlights':'a\nb\nc\nd'}):
            self.deny(lambda:self.post('seller-a','create',content={**content,**extra}),400)
        self.deny(lambda:self.post('buyer-a','create',content={**content,'companyBio':'Seller marketing'}),400)
        id=self.post('seller-a','create',content={**content,'companyBio':'New bio','visual':'telemetry','highlights':'First\nSecond','companyWebsite':'https://vendor.example'})['id']
        self.post('seller-a','access',id=id,grants={'buyer-a':'summary'})
        self.assertEqual(self.get('buyer-a',id=id)['item']['companyBio'],'New bio')
        self.post('seller-a','edit',id=id,content={**content,'companyBio':'Updated bio','visual':''})
        self.assertEqual(self.get('buyer-a',id=id)['item']['companyBio'],'Updated bio')
        self.assertEqual(self.get('buyer-a',id=id)['item']['visual'],'')

    def test_upgrade_preserves_user_edits_and_grants(self):
        with self.store.connect() as db:
            db.execute("DELETE FROM settings WHERE key='rich-listings-v1'")
            for row in FIXTURES:
                content=dict(zip(BASE_FIELDS,row[2:]))
                if row[0]=='catalog-b':content['summary']='User-authored summary'
                db.execute('UPDATE items SET content=? WHERE id=?',(json.dumps(content),row[0]))
        self.post('seller-a','access',id='catalog-a',grants={'buyer-a':'summary'})
        self.store=Store(self.path)
        self.assertTrue(self.get('seller-a',id='catalog-a')['item']['companyBio'])
        self.assertEqual(self.get('seller-a',id='catalog-a')['item']['grants'],{'buyer-a':'summary'})
        edited=self.get('seller-b',id='catalog-b')['item']
        self.assertEqual(edited['summary'],'User-authored summary')
        self.assertEqual(edited['companyBio'],'')
        self.post('seller-a','edit',id='catalog-a',content={'title':'New','category':'Tools','summary':'My copy'})
        self.store=Store(self.path)
        self.assertEqual(self.get('seller-a',id='catalog-a')['item']['summary'],'My copy')

    def wire(self,method,target,actor=None,body=None,extra=None):
        """Run the actual HTTP handler on in-memory transport; no port binding required."""
        payload=json.dumps(body).encode() if body is not None else b''
        headers={'Host':'127.0.0.1:8766','Connection':'close','Content-Length':str(len(payload)),**(extra or {})}
        if actor:headers['X-Demo-Account']=actor
        raw=(f'{method} {target} HTTP/1.1\r\n'+''.join(f'{k}: {v}\r\n' for k,v in headers.items())+'\r\n').encode()+payload
        class Connection:
            def __init__(self):self.output=io.BytesIO()
            def makefile(self,*args):return io.BytesIO(raw)
            def sendall(self,data):self.output.write(data)
        sock=Connection();Handler(sock,('127.0.0.1',12345),SimpleNamespace(store=self.store,public_origin=getattr(self,'public_origin',None)))
        header,body=sock.output.getvalue().split(b'\r\n\r\n',1)
        return int(header.split()[1]),header.decode(),body

    def test_http_field_projection_and_unavailable_response(self):
        self.post('seller-a','access',id='catalog-a',grants={'buyer-a':'summary'})
        status,headers,body=self.wire('GET','/api/marketplace?view=detail&id=catalog-a','buyer-a')
        self.assertEqual(status,200);self.assertIn('Cache-Control: no-store',headers)
        self.assertNotIn(b'contactEmail',body);self.assertNotIn(b'grants',body)
        denied=self.wire('GET','/api/marketplace?view=detail&id=catalog-a','buyer-b')
        missing=self.wire('GET','/api/marketplace?view=detail&id=missing','buyer-b')
        self.assertEqual(denied[0],missing[0]);self.assertEqual(denied[2],missing[2])

    def test_http_mutation_origin_limits_static_allowlist_and_identity(self):
        self.assertEqual(self.wire('POST','/api/marketplace','seller-a',{'action':'reset'},{'Origin':'https://elsewhere.example'})[0],403)
        self.assertEqual(self.wire('POST','/api/marketplace','seller-a',{'action':'reset'},{'Origin':'http://127.0.0.1:8766'})[0],200)
        self.assertEqual(self.wire('POST','/api/marketplace','seller-a',{'action':'reset'},{'Content-Length':'130000'})[0],413)
        self.assertEqual(self.wire('GET','/api/marketplace?view=mine')[0],401)
        for path in ('/data/marketplace.sqlite3','/app.py','/../app.py'):
            self.assertEqual(self.wire('GET',path)[0],404)
        for path in ('/','/app.js','/style.css'):
            status,headers,body=self.wire('GET',path)
            self.assertEqual(status,200);self.assertGreater(len(body),100)
            self.assertIn('Content-Security-Policy:',headers)

    def test_https_proxy_origin_is_explicit_and_forwarded_headers_cannot_override_it(self):
        self.public_origin='https://demo.example'
        body={'action':'access','id':'catalog-a','grants':{'buyer-a':'summary'}}
        self.assertEqual(self.wire('POST','/api/marketplace','seller-a',body,{'Origin':self.public_origin})[0],200)
        for origin in ('http://demo.example','https://evil.example','null','http://127.0.0.1:8766'):
            self.assertEqual(self.wire('POST','/api/marketplace','seller-a',{'action':'reset'},
                {'Origin':origin,'X-Forwarded-Proto':'https','X-Forwarded-Host':'evil.example'})[0],403)
        self.assertEqual(self.get('seller-a',id='catalog-a')['item']['grants'],{'buyer-a':'summary'})
        # The origin check is a browser defense, not an authentication mechanism.
        self.assertEqual(self.wire('POST','/api/marketplace','seller-a',body)[0],200)

if __name__=='__main__':unittest.main(verbosity=2)
