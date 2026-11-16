const fs = require('node:fs');
const path = require('node:path');
const {marked} = require(process.env.MARKED_MODULE || 'marked');
const style = 'body{font:16px/1.6 Arial;color:#172b40;max-width:1100px;margin:40px auto;padding:24px}h1,h2,h3{color:#000}table{border-collapse:collapse;width:100%;margin:16px 0}td,th{border:1px solid #d9d9d9;padding:9px;text-align:left}th{background:#eaf0f7}pre{white-space:pre-wrap;font:12px/1.4 monospace}figure{margin:32px 0;break-inside:avoid}img{display:block;max-width:100%;height:auto}figcaption{font-size:14px;margin-top:12px}a{color:#1659a4}@media print{body{font-size:11pt}h2,h3{break-after:avoid}tr{break-inside:avoid}thead{display:table-header-group}}';
const figures = [
 ['01-owner-private','Private seller catalog','The owner sees its private listing and opens visibility controls. The seller diagram is illustrative.'],
 ['02-summary-preview','Proposed recipient visibility','A proposed Summary grant includes one recipient and excludes another. The preview is not saved. The image shows the upper portion of the scrollable editor.'],
 ['03-buyer-summary','Buyer discovery with Summary access','Summary exposes authorized marketing and company content. Restricted operational fields are omitted by the server. The image shows the upper portion of the dialog.'],
 ['04-buyer-full','Buyer discovery with Full details','After an explicit upgrade, the buyer sees Product details. Further operational fields continue below the visible portion of the dialog.'],
 ['06-wishlist-recipient','Mirrored buyer wishlist discovery','A seller discovers an explicitly shared wishlist. Recipient cards have no owner management controls.']
];
for (const [input, output, title] of [
 ['projects/analyst-assistant/prd.md','analyst-assistant.html','Cyber Analyst Assistant PRD'],
 ['projects/marketplace/prd.md','marketplace.html','Controlled Marketplace PRD']
]) {
 const project=path.dirname(input);
 let source=fs.readFileSync(input,'utf8');
 if(output==='marketplace.html') {
  source+='\n\n## Appendix D Prototype screen walkthrough\n';
  figures.forEach(([name,label,caption],i)=>source+=`\n### Figure ${i+1} ${label}\n\n![${label}](docs/screenshots/${name}.png)\n\nFigure ${i+1}. ${caption}\n`);
 }
 let html=marked.parse(source).replace(/src="((?:mockups|docs\/screenshots)\/[^\"]+\.png)"/g,(_,p)=>'src="data:image/png;base64,'+fs.readFileSync(path.join(project,p)).toString('base64')+'"');
 html=html.replace(/href="(?!https?:|#)([^\"]+)"/g,(_,p)=>`href="../${p}"`);
 html=html.replace(/<h3>(Figure [\s\S]*?)<\/h3>\s*<p>(<img[^>]+>)<\/p>\s*<p>(Figure [\s\S]*?)<\/p>/g,'<figure><h3>$1</h3>$2<figcaption>$3</figcaption></figure>');
 fs.mkdirSync(path.join(project,'docs'),{recursive:true});
 fs.writeFileSync(path.join(project,'docs',output),`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>${style}</style></head><body>${html}</body></html>`);
}
console.log('Built two standalone product documents.');
