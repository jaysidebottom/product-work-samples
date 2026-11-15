// Regression checks for focus/revalidation and text rendering; no browser required.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
function harness(){
 const elements=new Map(),events={},calls=[];
 const el=s=>{
  if(!elements.has(s))elements.set(s,{id:s.slice(1),value:'',textContent:'',innerHTML:'',scrollTop:0,open:false,closed:0,
   addEventListener(){},showModal(){this.open=true},close(){this.open=false;this.closed++},replaceChildren(){this.innerHTML=''},classList:{toggle(){}},setAttribute(){},focus(){},
   querySelector(){return el('#dialog-content').innerHTML.includes('<form')?{}:null}});
  return elements.get(s);
 };
 const state={item:{id:'example',kind:'catalog',access:'full',organization:'Vendor',title:'Offering',summary:'Summary',deployment:'Restricted deployment'},denied:false,delay:null};
 const ctx={document:{querySelector:el,querySelectorAll:()=>[],activeElement:null},localStorage:{getItem:()=>null},window:{addEventListener:(n,f)=>events[n]=f},location:{origin:'http://localhost'},URLSearchParams,console,
 fetch:async url=>{const query=new URL(url,'http://localhost').searchParams;calls.push(query.get('view'));if(query.get('view')==='detail'){if(state.delay)await state.delay;return {ok:!state.denied,json:async()=>state.denied?{error:'Item unavailable'}:{item:state.item}};}return {ok:true,json:async()=>({count:0,items:[]})};}};
 vm.createContext(ctx);let src=fs.readFileSync(path.join(__dirname,'../static/app.js'),'utf8');src=src.slice(0,src.lastIndexOf('await initialize();'));vm.runInContext(src,ctx);vm.runInContext("context={actor:{role:'buyer'},organizations:[]}",ctx);
 return {ctx,el,events,state,calls,run:code=>vm.runInContext(code,ctx),settle:async()=>{await new Promise(setImmediate);await new Promise(setImmediate)}};
}
test('returning focus keeps detail open and scroll position; downgrade removes restricted fields',async()=>{
 const h=harness();await h.run("openItem('example')");h.el('#dialog').scrollTop=240;
 assert.match(h.el('#dialog-content').innerHTML,/Restricted deployment/);
 h.state.item={id:'example',kind:'catalog',access:'summary',organization:'Vendor',title:'Offering',summary:'Summary'};
 h.events.focus();await h.settle();
 assert.equal(h.el('#dialog').open,true);assert.equal(h.el('#dialog').closed,0);assert.equal(h.el('#dialog').scrollTop,240);
 assert.doesNotMatch(h.el('#dialog-content').innerHTML,/Restricted deployment/);assert.equal(h.calls.filter(v=>v==='detail').length,2);
});
test('revocation clears detail content without dismissing the modal',async()=>{
 const h=harness();await h.run("openItem('example')");h.state.denied=true;h.events.focus();await h.settle();
 assert.equal(h.el('#dialog').open,true);assert.match(h.el('#dialog-content').innerHTML,/Item unavailable/);assert.doesNotMatch(h.el('#dialog-content').innerHTML,/Restricted deployment/);
});
test('pending focus refresh cannot reopen a closed detail',async()=>{
 const h=harness();await h.run("openItem('example')");let release;h.state.delay=new Promise(r=>release=r);h.events.focus();h.run('closeDialog()');release();await h.settle();assert.equal(h.el('#dialog').open,false);assert.equal(h.el('#dialog-content').innerHTML,'');
});
test('focus preserves unsaved forms without reloading them',async()=>{
 const h=harness();h.run(`show('Edit','<form>Unsaved input</form>')`);h.events.focus();await h.settle();assert.equal(h.calls.length,0);assert.match(h.el('#dialog-content').innerHTML,/Unsaved input/);
});
test('seller sections render escaped bullets; buyer wording is preserved',()=>{
 const h=harness();assert.equal(h.run(`formattedDetail('specifications','Inputs; Exports; <script>bad</script>',false)`),'<ul class="detail-points"><li>Inputs</li><li>Exports</li><li>&lt;script&gt;bad&lt;/script&gt;</li></ul>');
 assert.match(h.run(`formattedDetail('deployment','Customer-managed. JSON imports.',false)`),/<li>Customer-managed\.<\/li><li>JSON imports\.<\/li>/);
 assert.match(h.run(`formattedDetail('timing','Pilot: setup, review, and handoff.',false)`),/<strong class="detail-lead">Pilot<\/strong>/);
 assert.equal(h.run(`formattedDetail('specifications','A; B',true)`),'A; B');
});
