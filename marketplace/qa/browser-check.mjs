// Run from a normal terminal after starting app.py. Uses only fictional demo data.
// Optional: PLAYWRIGHT_MODULE=/absolute/path/to/playwright/index.mjs
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const fallback='playwright';
const base=process.env.MARKETPLACE_URL;
if(!base||process.env.MARKETPLACE_QA_DISPOSABLE!=='1')throw new Error('Set MARKETPLACE_URL and MARKETPLACE_QA_DISPOSABLE=1 for a disposable database only.');
const target=new URL(base);
if(!['127.0.0.1','localhost','[::1]'].includes(target.hostname)||target.port==='8766')throw new Error('QA requires a separate local server, never the normal 8766 instance.');
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE||fallback);
const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {})});
const context=await browser.newContext({viewport:{width:1440,height:1000}});
await context.tracing.start({screenshots:true,snapshots:true,sources:true});
const page=await context.newPage();
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const output=fileURLToPath(new URL('./captures/',import.meta.url));await fs.mkdir(output,{recursive:true});
const shot=name=>page.screenshot({path:output+name+'.png',fullPage:true});
const close=()=>page.getByRole('button',{name:'Close dialog',exact:true}).click();
async function account(id){await page.getByLabel('Demo account',{exact:true}).selectOption(id);await page.getByRole('button',{name:'Refresh',exact:true}).waitFor();await page.waitForFunction(()=>!document.querySelector('#refresh').disabled)}
async function mine(){await page.locator('#mine').click();await page.locator('.card [data-access]').waitFor()}
async function grant(level){await page.locator('.card [data-access]').click();await page.locator('#grant-buyer-a').selectOption(level);await page.getByRole('button',{name:'Save access',exact:true}).click();await page.getByRole('status').filter({hasText:'Access saved'}).waitFor()}
try{
 await page.goto(base);await page.waitForFunction(()=>!document.querySelector('#refresh').disabled);
 const request=async(actor,query,body)=>{
  const url=base+'/api/marketplace?'+new URLSearchParams(query);
  const response=body?await page.request.post(url,{headers:{'X-Demo-Account':actor},data:body}):await page.request.get(url,{headers:{'X-Demo-Account':actor}});
  return {status:response.status(),data:await response.json()};
 };
 // Direct live HTTP matrix for both roles, including exact preview parity and search omission.
 for(const [owner,peer,recipient,other] of [['seller-a','seller-b','buyer-a','buyer-b'],['buyer-a','buyer-b','seller-a','seller-b']]){
  const content={title:'QA '+owner,category:'QA',summary:'Visible summary',description:'restricted-canary',contactEmail:'qa@example.com'};
  const created=await request(owner,{}, {action:'create',content});assert.equal(created.status,201);const id=created.data.id;
  for(const actor of [peer,recipient,other])assert.equal((await request(actor,{view:'detail',id})).status,404);
  assert.equal((await request(owner,{}, {action:'access',id,grants:{[peer]:'full'}})).status,400);
  for(const level of ['summary','full','summary','none']){
   const proposed=await request(owner,{view:'preview',id,recipient,level});
   assert.equal((await request(owner,{}, {action:'access',id,grants:level==='none'?{}:{[recipient]:level}})).status,200);
   const detail=await request(recipient,{view:'detail',id});
   if(level==='none'){assert.equal(detail.status,404);assert.equal(proposed.data.item,null);}
   else {assert.deepEqual(proposed.data.item,detail.data.item);assert.equal('description' in detail.data.item,level==='full');assert.equal('grants' in detail.data.item,false);}
   for(const actor of [peer,other])assert.equal((await request(actor,{view:'detail',id})).status,404);
   assert.equal((await request(recipient,{view:'discover',q:'restricted-canary'})).data.count,0);
  }
 }

 await page.getByRole('button',{name:'Reset demo',exact:true}).click();await page.getByRole('button',{name:'Reset demo data',exact:true}).click();await page.getByRole('status').filter({hasText:'Demo reset'}).waitFor();

 for(const actor of ['seller-a','buyer-a']){
  await account(actor);await mine();await page.locator('#create').click();
  await page.locator('[name=title]').fill('QA unsaved '+actor);
  await page.evaluate(()=>window.dispatchEvent(new Event('focus')));
  assert.equal(await page.locator('[name=title]').inputValue(),'QA unsaved '+actor);
  assert.equal(await page.locator('[name=companyBio]').count(),actor==='seller-a'?1:0);
  await page.locator('[name=category]').fill('QA');await page.locator('[name=summary]').fill('QA summary');
  await page.locator('#editor [type=submit]').click();await page.getByRole('status').filter({hasText:'created privately'}).waitFor();
  const card=page.locator('.card').filter({hasText:'QA unsaved '+actor});await card.locator('[data-open]').click();await page.locator('#edit').click();
  await page.locator('[name=summary]').fill('QA edited summary');await page.locator('#editor [type=submit]').click();await page.getByRole('status').filter({hasText:'Item updated'}).waitFor();
  await page.reload();await page.locator('.card').filter({hasText:'QA edited summary'}).waitFor();
 }
 await page.getByRole('button',{name:'Reset demo',exact:true}).click();await page.locator('#confirm-reset').click();await page.getByRole('status').filter({hasText:'Demo reset'}).waitFor();
 await account('seller-a');await mine();await shot('01-owner-private');
 await page.locator('.card [data-access]').click();await page.locator('#grant-buyer-a').selectOption('summary');await page.getByRole('button',{name:'Preview as Civic Research Office',exact:true}).click();await page.locator('#preview > .preview > h3').waitFor();assert.equal(await page.locator('#preview').getByText('Product overview',{exact:true}).count(),0);await shot('02-summary-preview');
 await page.getByRole('button',{name:'Cancel',exact:true}).click();
 const before=await page.request.get(base+'/api/marketplace?view=detail&id=catalog-a',{headers:{'X-Demo-Account':'buyer-a'}});assert.equal(before.status(),404);
 await grant('summary');await account('buyer-a');await page.locator('#discover').click();await page.getByRole('button',{name:'View offering',exact:true}).click();await page.getByRole('heading',{name:'Infrastructure relationship analysis',exact:true}).waitFor();assert.equal(await page.getByRole('dialog').getByText('Product overview',{exact:true}).count(),0);await page.getByRole('heading',{name:'About the company'}).waitFor();assert.equal(await page.locator('.product-visual').count(),2);await shot('03-buyer-summary');await close();
 for(const id of ['buyer-b','seller-b']){await account(id);await page.locator('#discover').click();await page.getByRole('heading',{name:id==='seller-b'?'No shared wishlist items found':'No shared offerings found'}).waitFor();await page.goto(base+'/?item=catalog-a');await page.getByRole('heading',{name:'Item unavailable',exact:true}).waitFor();await close()}
 await account('seller-a');await mine();await grant('full');await account('buyer-a');await page.locator('#discover').click();await page.getByRole('button',{name:'View offering',exact:true}).click();await page.getByText('Product overview',{exact:true}).waitFor();await shot('04-buyer-full');
 await page.locator('#dialog').evaluate(el=>{el.scrollTop=180});const scroll=await page.locator('#dialog').evaluate(el=>el.scrollTop);
 await Promise.all([page.waitForResponse(r=>r.url().includes('view=detail')),page.evaluate(()=>window.dispatchEvent(new Event('focus')))]);
 await page.getByText('Product overview',{exact:true}).waitFor();
 assert.equal(await page.locator('#dialog').evaluate(el=>el.open),true);
 assert.ok(Math.abs(await page.locator('#dialog').evaluate(el=>el.scrollTop)-scroll)<2);
 await request('seller-a',{}, {action:'access',id:'catalog-a',grants:{'buyer-a':'summary'}});
 await page.evaluate(()=>window.dispatchEvent(new Event('focus')));
 await page.getByRole('dialog').getByText('Product overview',{exact:true}).waitFor({state:'hidden'});
 await request('seller-a',{}, {action:'access',id:'catalog-a',grants:{}});
 await page.evaluate(()=>window.dispatchEvent(new Event('focus')));await page.getByRole('heading',{name:'Item unavailable',exact:true}).waitFor();await close();
 await account('seller-a');await mine();await grant('none');await account('buyer-a');await page.locator('#discover').click();await page.getByRole('heading',{name:'No shared offerings found'}).waitFor();await shot('05-revoked');
 // Mirrored wishlist flow and persistence.
 await mine();await page.locator('.card [data-access]').click();await page.locator('#grant-seller-a').selectOption('summary');await page.getByRole('button',{name:'Save access',exact:true}).click();await page.getByRole('status').filter({hasText:'Access saved'}).waitFor();await page.reload();await page.waitForFunction(()=>!document.querySelector('#refresh').disabled);
 await account('seller-a');await page.locator('#discover').click();await page.getByRole('heading',{name:'Map related infrastructure',exact:true}).waitFor();assert.match(await page.locator('.card .org').innerText(),/Civic Research Office/);assert.equal(await page.locator('.card [data-access]').count(),0);await shot('06-wishlist-recipient');
 await page.setViewportSize({width:390,height:844});await shot('07-mobile');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 // Mobile owner editor, visibility preview and detail must fit, including keyboard dismissal.
 for(const actor of ['seller-a','buyer-a']){
  await account(actor);await mine();await page.locator('#create').click();
  assert.equal(await page.locator('#dialog').evaluate(el=>el.scrollWidth>el.clientWidth),false);
  await page.locator('[name=title]').fill('Mobile unsaved');await shot('08-mobile-'+actor+'-editor');
  await page.keyboard.press('Escape');assert.equal(await page.locator('#dialog').evaluate(el=>el.open),false);
  await page.locator('.card [data-access]').click();
  const recipient=actor==='seller-a'?'buyer-a':'seller-a';
  await page.locator('#grant-'+recipient).selectOption('full');
  await page.locator('[data-preview="'+recipient+'"]').click();await page.locator('#preview > .preview > h3').waitFor();
  assert.equal(await page.locator('#dialog').evaluate(el=>el.scrollWidth>el.clientWidth),false);
  await shot('09-mobile-'+actor+'-preview');await close();
 }
 assert.deepEqual(errors,[]);console.log('Browser walkthrough passed; screenshots saved in '+output);
}finally{await context.tracing.stop({path:output+'browser-trace.zip'});await browser.close()}
