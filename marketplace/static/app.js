const $=s=>document.querySelector(s);
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fields=['title','category','summary','description','specifications','timing','contactName','contactEmail'];
const marketingFields=['highlights','visual','companyBio','companyExpertise','companyWebsite','companyLocation'];
const extraDetails=['useCases','deployment','successCriteria'];
const labels={title:'Title',category:'Category',summary:'Short summary',description:'Detailed description',specifications:'Requirements / specifications',timing:'Timing / availability',contactName:'Contact name',contactEmail:'Contact email'};
Object.assign(labels,{highlights:'Capability highlights (one per line, up to 3)',visual:'Illustrative product diagram',companyBio:'Company bio',companyExpertise:'Areas of expertise',companyWebsite:'Company website',companyLocation:'Location',useCases:'Use cases',deployment:'Deployment and integrations',successCriteria:'Success criteria'});
let account=localStorage.getItem('marketplace-account')||'seller-a';
if(!['seller-a','seller-b','buyer-a','buyer-b'].includes(account))account='seller-a';
let context,view='mine',generation=0,dialogVersion=0,requestVersion=0,openDetailId=null;
const dialog=$('#dialog');
$('#account').value=account;
async function api(query={},body){
 const actor=account;
 const res=await fetch('/api/marketplace?'+new URLSearchParams(query),{method:body?'POST':'GET',headers:{'X-Demo-Account':actor,...(body?{'Content-Type':'application/json'}:{})},body:body?JSON.stringify(body):undefined,cache:'no-store'});
 const data=await res.json();
 if(actor!==account)throw new Error('Account changed');
 if(!res.ok)throw new Error(data.error||'Request failed');
 return data;
}
function message(text,error=false){$('#message').textContent=text;$('#message').className=error?'error':'';}
function closeDialog(){openDetailId=null;dialogVersion++;dialog.close();$('#dialog-content').replaceChildren();$('#dialog-error').textContent='';}
$('#close').onclick=closeDialog;
dialog.addEventListener('cancel',e=>{e.preventDefault();closeDialog()});
function show(title,html,kicker='ITEM'){
 openDetailId=null;dialogVersion++;$('#dialog-content').innerHTML=`<h2 id="dialog-title">${esc(title)}</h2>${html}`;$('#dialog-kicker').textContent=kicker;$('#dialog-error').textContent='';
 if(!dialog.open)dialog.showModal();
 return dialogVersion;
}
function failure(error,version){if(version===undefined||version===dialogVersion)$('#dialog-error').textContent=error.message;}
function itemNoun(own=view==='mine'){return (context.actor.role==='buyer')===own?'wishlist item':'offering';}
function labelAccess(item){return item.access==='owner'?(Object.keys(item.grants).length?`Shared with ${Object.keys(item.grants).length}`:'Private'):item.access==='summary'?'Summary access':'Full details';}
function productVisual(item){
 if(!['relationships','telemetry'].includes(item.visual))return '';
 const graph=item.visual==='relationships';
 const art=graph?`
 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 300" role="img" aria-label="Illustrative infrastructure graph linking a seed domain to IP and certificate observations">
 <rect width="600" height="300" fill="#0e2530"/>
 <path d="M390 0H600V300H510Z" fill="#123440"/>
 <text x="28" y="36" fill="#70d7cb" font-family="Arial,sans-serif" font-size="12" font-weight="700" letter-spacing="2">RELATIONSHIP EXPLORER</text>
 <text x="28" y="72" fill="#f1fbfb" font-family="Arial,sans-serif" font-size="27" font-weight="700">Follow the evidence.</text>
 <g stroke="#315563" stroke-width="1"><path d="M28 103H572M28 150H572M28 197H572M28 244H572"/></g>
 <g fill="none" stroke="#56c6b9" stroke-width="2"><path d="M145 190L300 132L462 182M145 190L302 250L462 182M300 132L302 250"/><path d="M462 182L552 113M462 182L547 258" stroke="#648395" stroke-dasharray="5 5"/></g>
 <circle cx="145" cy="190" r="39" fill="#153f49" stroke="#65dfc9" stroke-width="2"/><circle cx="145" cy="190" r="24" fill="#64dfc9"/>
 <path d="M132 190H158M145 177V203" stroke="#12343e" stroke-width="2"/>
 <circle cx="300" cy="132" r="12" fill="#d9f3ed"/><circle cx="302" cy="250" r="12" fill="#9bc7d5"/><circle cx="462" cy="182" r="17" fill="#64dfc9"/><circle cx="552" cy="113" r="6" fill="#648395"/><circle cx="547" cy="258" r="6" fill="#648395"/>
 <g fill="#d9e9ee" font-family="Arial,sans-serif" font-size="14"><text x="98" y="247">Seed domain</text><text x="319" y="126">Observed IP</text><text x="320" y="274">Certificate</text><text x="418" y="221">Related domain</text></g>
 <rect x="30" y="120" width="151" height="27" rx="4" fill="#1b3b47"/><text x="42" y="138" fill="#9cc6d2" font-family="Arial,sans-serif" font-size="12">SOURCE-LINKED VIEW</text>
 </svg>`:`
 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 300" role="img" aria-label="Illustrative telemetry review dashboard with activity trends and a selected review window">
 <rect width="600" height="300" fill="#f4efe7"/><rect width="10" height="300" fill="#e97347"/>
 <text x="32" y="35" fill="#715d80" font-family="Arial,sans-serif" font-size="12" font-weight="700" letter-spacing="2">SIGNAL / ACTIVITY REVIEW</text>
 <text x="32" y="72" fill="#30283e" font-family="Arial,sans-serif" font-size="27" font-weight="700">Make patterns visible.</text>
 <rect x="32" y="94" width="536" height="178" rx="7" fill="#fffdfa" stroke="#dcd5cb"/>
 <path d="M32 132H568M412 132V272" stroke="#e6dfd6"/>
 <circle cx="49" cy="113" r="4" fill="#e97347"/><text x="61" y="118" fill="#544660" font-family="Arial,sans-serif" font-size="13" font-weight="700">NETWORK OBSERVATIONS</text>
 <g stroke="#ece7e0"><path d="M50 163H393M50 195H393M50 227H393"/></g>
 <rect x="238" y="143" width="65" height="99" fill="#fce3d5"/>
 <path d="M51 226L79 222L106 205L133 214L161 198L188 206L216 190L243 159L271 171L298 149L326 185L353 178L391 193L391 243H51Z" fill="#eae3f3"/>
 <path d="M51 226L79 222L106 205L133 214L161 198L188 206L216 190L243 159L271 171L298 149L326 185L353 178L391 193" fill="none" stroke="#75518f" stroke-width="3"/>
 <circle cx="298" cy="149" r="5" fill="#e97347" stroke="#fffdfa" stroke-width="2"/>
 <g font-family="Arial,sans-serif" font-size="11" fill="#83758a"><text x="51" y="258">START</text><text x="236" y="258">REVIEW WINDOW</text></g>
 <g font-family="Arial,sans-serif"><text x="430" y="159" fill="#403548" font-size="12" font-weight="700">SOURCE BREAKDOWN</text><text x="430" y="185" fill="#83758a" font-size="11">Segment A</text><text x="430" y="226" fill="#83758a" font-size="11">Segment B</text></g>
 <rect x="430" y="195" width="112" height="8" rx="4" fill="#efe9f3"/><rect x="430" y="195" width="87" height="8" rx="4" fill="#9977ad"/>
 <rect x="430" y="236" width="112" height="8" rx="4" fill="#f8e6dc"/><rect x="430" y="236" width="62" height="8" rx="4" fill="#e99871"/>
 </svg>`;
 return `<figure class="product-visual ${graph?'visual-graph':'visual-telemetry'}">${art}<figcaption>Illustrative ${graph?'investigation view':'telemetry view'} · Not a product screenshot</figcaption></figure>`;
}

function highlights(item){return item.highlights?`<ul class="highlights">${item.highlights.split('\n').filter(Boolean).map(v=>`<li>${esc(v)}</li>`).join('')}</ul>`:'';}
function fieldLabel(f,buyer){return buyer?({summary:'Need at a glance',description:'The need and intended outcome',specifications:'Required capabilities',deployment:'Constraints and evaluation environment',timing:'Evaluation timeline'}[f]||labels[f]):({summary:'Value proposition',description:'Product overview',specifications:'Technical specifications',timing:'Availability and evaluation',successCriteria:'Evaluation criteria'}[f]||labels[f]);}
async function reload(){
 const gen=generation, req=++requestVersion;
 $('#items').replaceChildren();$('#count').textContent='Loading…';
 try{
  const data=await api({view,q:$('#search').value});
  if(gen!==generation||req!==requestVersion)return;
  $('#count').textContent=`${data.count} ${itemNoun()}${data.count===1?'':'s'}`;
  $('#items').innerHTML=data.items.length?data.items.map(item=>`<article class="card">${view==='discover'?`<p class="org"><span class="org-label">${context.actor.role==='seller'?'BUYER':'SELLER'}</span>${esc(item.organization)}</p>`:''}<div class="card-top"><span class="category">${esc(item.category)}</span>${item.access==='owner'?`<button class="badge audience ${labelAccess(item)!=='Private'?'shared':''}" data-access="${esc(item.id)}" aria-label="Manage visibility: ${esc(labelAccess(item))} — ${esc(item.title)}" aria-haspopup="dialog" title="Manage visibility">${esc(labelAccess(item))}<span aria-hidden="true"> ▾</span></button>`:`<span class="badge shared">${esc(labelAccess(item))}</span>`}</div>${productVisual(item)}<h2>${esc(item.title)}</h2><p>${esc(item.summary)}</p>${highlights(item)}<div class="card-actions"><button data-open="${esc(item.id)}">View ${itemNoun()}</button></div></article>`).join(''):`<div class="empty"><h2>${view==='mine'?`No ${itemNoun()}s found`:`No shared ${itemNoun()}s found`}</h2><p>${view==='mine'?`Add a ${itemNoun()} or adjust your search. New items start private.`:`Shared ${itemNoun()}s appear here when an organization grants you access.`}</p></div>`;
  document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>openItem(b.dataset.open));
  document.querySelectorAll('[data-access]').forEach(b=>b.onclick=()=>openAccess(b.dataset.access));
 }catch(e){if(gen===generation&&req===requestVersion){$('#count').textContent='';message(e.message,true)}}
}
function syncNav(){
 const buyer=context.actor.role==='buyer';
 $('#mine').textContent=buyer?'My wishlist':'My catalog';
 $('#title').textContent=view==='mine'?(buyer?'My wishlist':'My catalog'):'Discover';
 $('#eyebrow').textContent=view==='mine'?(buyer?'YOUR PURCHASING NEEDS':'YOUR OFFERINGS'):'SHARED WITH YOUR ORGANIZATION';
 $('#subtitle').textContent=view==='mine'?(buyer?'Describe needs and choose what each seller can see.':'Manage capabilities and choose what each buyer can see.'):(buyer?'Explore capabilities that vendors have shared with you.':'Explore needs that government buyers have shared with you.');
 $('#create').textContent=buyer?'＋ Add wishlist item':'＋ Create offering';
 $('#search-label').textContent=`Search ${itemNoun()}s`;$('#items').setAttribute('aria-label',`${itemNoun()}s`);
 $('#create').hidden=view!=='mine';$('#role').textContent=buyer?'Government buyer workspace':'Commercial seller workspace';
 $('#mine').classList.toggle('active',view==='mine');$('#discover').classList.toggle('active',view==='discover');
}
async function initialize(){
 const gen=++generation;context=null;closeDialog();message('');$('#items').replaceChildren();$('#count').textContent='Loading…';$('#title').textContent='Loading workspace…';$('#subtitle').textContent='';$('#role').textContent='';for(const id of ['create','mine','discover','search','refresh'])$('#'+id).disabled=true;
 try{const data=await api({view:'context'});if(gen!==generation)return;context=data;syncNav();for(const id of ['create','mine','discover','search','refresh'])$('#'+id).disabled=false;await reload();}
 catch(e){if(gen===generation)message(e.message,true)}
}
$('#account').onchange=async e=>{account=e.target.value;localStorage.setItem('marketplace-account',account);$('#search').value='';history.replaceState(null,'','/');await initialize()};
for(const name of ['mine','discover'])$('#'+name).onclick=()=>{view=name;$('#search').value='';message('');syncNav();reload()};
let searchTimer;$('#search').oninput=()=>{requestVersion++;clearTimeout(searchTimer);searchTimer=setTimeout(reload,180)};
$('#refresh').onclick=()=>{closeDialog();message('');reload()};
window.addEventListener('focus',()=>{
 if(!context||dialog.querySelector('form'))return;
 if(dialog.open&&openDetailId)openItem(openDetailId,true);
 reload();
});
window.addEventListener('storage',e=>{if(e.key==='marketplace-account'){account=e.newValue||'seller-a';$('#account').value=account;initialize()}});
function formattedDetail(field,value,buyer){
 if(buyer||!['specifications','deployment','timing'].includes(field))return esc(value);
 // Render text as text, never Markdown/HTML supplied by a listing owner.
 let text=String(value),heading='';
 if(field==='timing'&&text.includes(':')){
  const colon=text.indexOf(':');heading=text.slice(0,colon);text=text.slice(colon+1);
 }
 const points=text.split(/\n+|;\s*|(?<=[.!?])\s+(?=[A-Z])/).map(v=>v.trim()).filter(Boolean);
 const timingPoints=heading?text.split(/,\s*|\n+/).map(v=>v.trim().replace(/^and\s+/, '')).filter(Boolean):points;
 return `${heading?`<strong class="detail-lead">${esc(heading)}</strong>`:''}<ul class="detail-points">${timingPoints.map(v=>`<li>${esc(v)}</li>`).join('')}</ul>`;
}
function detail(item){
 const buyer=item.kind==='wishlist';
 const rows=keys=>keys.filter(f=>f in item&&item[f]).map(f=>`<div class="detail-field"><dt>${esc(fieldLabel(f,buyer))}</dt><dd>${formattedDetail(f,item[f],buyer)}</dd></div>`).join('');
 const company=rows(['companyBio','companyExpertise','companyLocation','companyWebsite']);
 const full=rows(['description','useCases','specifications','deployment','successCriteria','timing','contactName','contactEmail']);
 return `<p><span class="badge">${esc(labelAccess(item))}</span></p><p class="detail-org">${esc(item.organization)}</p>${productVisual(item)}<p class="detail-summary">${esc(item.summary)}</p>${highlights(item)}${full?`<section class="listing-section"><h3>${buyer?'Need and evaluation':'Product details'}</h3><dl>${full}</dl></section>`:''}${company?`<section class="listing-section company-section"><h3>About the company</h3><dl>${company}</dl></section>`:''}`;
}

async function openItem(id,revalidate=false){
 const scroll=dialog.scrollTop,focusId=document.activeElement?.id;
 const version=revalidate?++dialogVersion:show('Loading item…','');
 try{const {item}=await api({view:'detail',id});if(version!==dialogVersion)return;
  show(item.title,detail(item)+`<p class="link-copy">Direct link: ${esc(location.origin)}/?item=${esc(id)}</p>`+(item.access==='owner'?`<div class="form-actions"><button id="edit">Edit ${itemNoun(true)}</button><button id="manage" class="primary">Manage visibility</button></div>`:''));
  openDetailId=id;
  if(item.access==='owner'){$('#edit').onclick=()=>editor(item);$('#manage').onclick=()=>openAccess(id)}
  if(revalidate){dialog.scrollTop=scroll;if(['edit','manage','close'].includes(focusId))$('#'+focusId)?.focus({preventScroll:true});}
 }catch(e){if(version===dialogVersion)show(e.message,'<p>This item is unavailable for the selected account.</p>')}
}
function editor(item){
 const audience=item?Object.entries(item.grants).map(([id,level])=>`${context.organizations.find(o=>o.id===id).name}: ${level==='full'?'Full details':'Summary'}`).join('; '):'';
 const buyer=context.actor.role==='buyer';
 const field=f=>{
  const required=fields.slice(0,3).includes(f);
  if(f==='visual')return `<label class="field">${labels[f]}<select name="visual">${[['','No diagram'],['relationships','Infrastructure relationships'],['telemetry','Network telemetry review']].map(([v,t])=>`<option value="${v}" ${item?.visual===v?'selected':''}>${t}</option>`).join('')}</select></label>`;
  const multiline=['summary','description','specifications','highlights','companyBio','useCases','deployment','successCriteria','timing'].includes(f);
  return `<label class="field">${esc(fieldLabel(f,buyer))}${required?' *':''}${multiline?`<textarea name="${f}" ${required?'required':''} maxlength="5000">${esc(item?.[f])}</textarea>`:`<input name="${f}" type="${f==='contactEmail'?'email':f==='companyWebsite'?'url':'text'}" value="${esc(item?.[f])}" ${required?'required':''} maxlength="5000">`}</label>`;
 };
 const version=show(item?`Edit ${itemNoun(true)}`:`Create ${itemNoun(true)}`,`<p class="notice">${audience?`Current audience: ${esc(audience)}. Editing retains these grants.`:'Private until you explicitly share it with an organization.'}</p><form id="editor"><section class="form-section"><h3>${buyer?'Need at a glance':'Marketing overview'}</h3><p>Visible to Summary and Full-detail recipients. Keep restricted information out of these fields.${buyer?'':' Company information is saved with this listing; review it for each offering.'}</p>${[...fields.slice(0,3),...buyer?[]:marketingFields].map(field).join('')}</section><section class="form-section"><h3>Full details</h3><p>Visible only to organizations you grant Full details. Explain the workflow, requirements, and evaluation rather than repeating the short summary. Put each specification, deployment detail, or evaluation step on its own line.</p>${['description',...extraDetails,'specifications','timing','contactName','contactEmail'].map(field).join('')}</section><div class="form-actions"><button type="button" id="cancel-edit">Cancel</button><button class="primary" type="submit">${item?'Save changes':`Create private ${itemNoun(true)}`}</button></div></form>`);
 $('#cancel-edit').onclick=closeDialog;
 $('#editor').onsubmit=async e=>{
  e.preventDefault();const content=Object.fromEntries(new FormData(e.target));const submit=e.target.querySelector('[type=submit]');submit.disabled=true;
  try{await api({}, {action:item?'edit':'create',...(item?{id:item.id}:{}),content});if(version!==dialogVersion)return;closeDialog();message(item?'Item updated. Existing audience retained.':`${context.actor.role==='buyer'?'Wishlist item':'Offering'} created privately. Click its Private badge to choose an audience.`);await reload();}
  catch(err){failure(err,version);submit.disabled=false}
 };
}
$('#create').onclick=()=>editor(null);
async function openAccess(id){
 const loading=show('Loading visibility…','');
 try{
  const {item}=await api({view:'detail',id});if(loading!==dialogVersion)return;
  if(item.access!=='owner')throw new Error('Item unavailable');
  const recipients=context.organizations.filter(o=>o.role!==context.actor.role);
  const version=show('Manage visibility',`<p>${esc(item.title)}</p><p class="notice">Choose access for each ${context.actor.role==='buyer'?'seller':'buyer'}. Changes take effect only after Save access.</p><form id="access-form">${recipients.map(o=>`<div class="recipient"><label for="grant-${o.id}">${esc(o.name)}<small>Saved access: ${item.grants[o.id]==='full'?'Full details':item.grants[o.id]==='summary'?'Summary':'No access'}</small></label><select name="${o.id}" id="grant-${o.id}"><option value="none" ${!item.grants[o.id]?'selected':''}>No access</option><option value="summary" ${item.grants[o.id]==='summary'?'selected':''}>Summary</option><option value="full" ${item.grants[o.id]==='full'?'selected':''}>Full details</option></select><button type="button" data-preview="${o.id}">Preview as ${esc(o.name)}</button></div>`).join('')}<p id="effect" class="notice"></p><p class="small">Revoking access blocks future retrieval. It cannot retract information already copied.</p><div id="preview"></div><div class="form-actions"><button type="button" id="cancel-access">Cancel</button><button class="primary" type="submit">Save access</button></div></form>`,'AUDIENCE & DISCLOSURE');
  const form=$('#access-form');let previewRequest=0;
  const explain=()=>{previewRequest++;$('#preview').replaceChildren();$('#effect').textContent=recipients.map(o=>{const level=form.elements.namedItem(o.id).value;return `${o.name}: ${level==='none'?'no access':level==='summary'?(item.kind==='catalog'?'title, category, organization, value proposition, highlights, diagram, and company information':'title, category, organization, and need summary'):'all summary content plus overview, use cases, specifications, constraints/deployment, evaluation criteria, timing, and contact'}.`}).join(' ')};
  form.querySelectorAll('select').forEach(s=>s.onchange=explain);explain();
  form.querySelectorAll('[data-preview]').forEach(b=>b.onclick=async()=>{
   const recipient=b.dataset.preview,level=form.elements.namedItem(recipient).value,req=++previewRequest;
   try{const data=await api({view:'preview',id,recipient,level});if(version!==dialogVersion||req!==previewRequest)return;
    $('#preview').innerHTML=`<div class="preview"><p class="eyebrow">PROPOSED VIEW · NOT SAVED</p><p>${esc(context.organizations.find(o=>o.id===recipient).name)}</p>${data.item?`<h3>${esc(data.item.title)}</h3>${detail(data.item)}`:'<h3>No access</h3><p>No item information is available to this recipient.</p>'}</div>`;
   }catch(e){failure(e,version)}
  });
  $('#cancel-access').onclick=closeDialog;
  form.onsubmit=async e=>{e.preventDefault();const grants=Object.fromEntries([...new FormData(form)].filter(([,v])=>v!=='none'));const submit=form.querySelector('[type=submit]');submit.disabled=true;
   try{await api({}, {action:'access',id,grants});if(version!==dialogVersion)return;closeDialog();message('Access saved. New permissions apply on the next retrieval.');await reload()}
   catch(err){failure(err,version);submit.disabled=false}
  };
 }catch(e){if(loading===dialogVersion)show(e.message,'<p>Only the owner can manage visibility.</p>')}
}
$('#reset').onclick=()=>{
 const version=show('Reset fictional demo data?','<p>This removes demo edits and restores two private wishlist items and two private catalog offerings. All sharing grants will be removed.</p><div class="form-actions"><button id="cancel-reset">Cancel</button><button id="confirm-reset" class="primary">Reset demo data</button></div>','DEMO CONTROL');
 $('#cancel-reset').onclick=closeDialog;$('#confirm-reset').onclick=async()=>{const b=$('#confirm-reset');b.disabled=true;try{await api({}, {action:'reset'});if(version!==dialogVersion)return;closeDialog();message('Demo reset. All wishlist and catalog items are private.');await reload()}catch(e){failure(e,version);b.disabled=false}};
};
await initialize();
const direct=new URLSearchParams(location.search).get('item');if(direct&&context)await openItem(direct);
