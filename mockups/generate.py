"""Editable SVG sources and gallery for four annotated analyst concepts."""
from pathlib import Path
from html import escape
out=Path(__file__).parent
W,H=1440,1100
parts=[]
def rect(x,y,w,h,fill='#ffffff',stroke='#dce3eb',r=10):
 parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')
def text(x,y,s,size=17,color='#263449',weight=400):
 parts.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(s)}</text>')
def lines(x,y,ss,size=17,color='#263449',step=26):
 for i,s in enumerate(ss): text(x,y+i*step,s,size,color)
def link(x,y,s,size=16):
 text(x,y,s,size,'#2457d9',600)
 # Underlines visually distinguish clickable evidence and actions from plain text.
 parts.append(f'<path d="M {x} {y+3} h {len(s)*size*.49}" stroke="#2457d9" stroke-width="1"/>')
def button(x,y,w,label,primary=False):
 rect(x,y,w,38,'#244fdd' if primary else '#fff','#244fdd' if primary else '#cdd6e2',7)
 parts.append(f'<text x="{x+w/2}" y="{y+19}" text-anchor="middle" dominant-baseline="central" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="600" fill="{"#fff" if primary else "#263449"}">{escape(label)}</text>')
def badge(x,y,n):
 parts.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#244fdd"/>');text(x-5,y+5,str(n),15,'#fff',700)
def note(x,y,n,title,body):
 badge(x+15,y+10,n);text(x+40,y+16,title,17,'#172b4d',700);lines(x+40,y+45,body,15,'#4d6079',23)
def base(number,title,subtitle):
 global parts
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<rect width="{W}" height="{H}" fill="#f3f6fa"/>']
 text(40,43,'ANALYST ASSISTANT  /  CONCEPT DESIGN',14,'#51647d',700)
 text(40,82,f'{number:02d}  {title}',30,'#142842',700);text(40,115,subtitle,17,'#51647d')
 rect(40,145,1360,730,'#fff','#cdd6e2',12)
 rect(40,145,814,61,'#142842','#142842',12)
 rect(866,145,534,61,'#142842','#142842',12)
 rect(65,157,150,37,'#203b59','#627995',7)
 parts.append('<text x="140" y="175.5" text-anchor="middle" dominant-baseline="central" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="600" fill="#fff">‹ Investigations</text>')
 text(235,183,'example.com',20,'#fff',700)
 text(570,181,'Illustrative data · Concept mockup',14,'#d9e6ff')
 text(890,183,'Assistant',20,'#fff',700);text(1275,181,'Collapse ‹',14,'#d9e6ff')
 text(65,238,'Graph',16,'#244fdd',700);text(139,238,'Table',16);text(209,238,'Sources',16)
 parts.append('<path d="M 860 206 V 874" stroke="#b9c8dc" stroke-width="3"/>')
 rect(856,512,8,55,'#dce3eb','#dce3eb',4)
 text(890,239,'Conversation',16,'#51647d',600)
 rect(880,260,500,48,'#f3f6fa');text(897,290,'Context: example.com · Last 30 days',15)
 text(57,1076,'Concept only • Fictional data and collaborators • Chat controls are illustrative • No working analyst implementation claimed',14,'#51647d')
def user(ss):
 rect(930,325,440,83,'#eef2f8','#eef2f8',15)
 text(947,347,'You',13,'#51647d',600);lines(947,372,ss,16,'#263449',24)
 parts.append('<circle cx="902" cy="438" r="12" fill="#142842"/>');text(897,443,'a',15,'#fff',700)
 text(924,443,'Assistant',14,'#142842',700)
def composer(placeholder='Message the assistant…'):
 # Fixed composer persists beneath the independently scrolling conversation in every state.
 parts.append('<path d="M 880 776 H 1380" stroke="#e5eaf1"/>')
 rect(890,790,480,63,'#f8fafc','#b9c8dc',16)
 text(907,827,placeholder,15,'#5b6d84')
 parts.append('<circle cx="1342" cy="823" r="17" fill="#142842"/>')
 parts.append('<path d="M 1342 831 V 815 M 1336 821 L 1342 815 L 1348 821" fill="none" stroke="#fff" stroke-width="2"/>')
 text(915,865,'Enter to send · Shift+Enter for a new line',11,'#718096')
def save(name):
 parts.append('</svg>');(out/f'{name}.svg').write_text('\n'.join(parts))
def graph():
 rect(65,265,770,310,'#f8faff')
 for x1,y1,x2,y2 in [(235,410,450,370),(450,370,660,460)]: parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#4778de" stroke-width="4"/>')
 for x,y,label in [(235,410,'example.com'),(450,370,'192.0.2.10'),(660,460,'related.example')]:
  parts.append(f'<circle cx="{x}" cy="{y}" r="28" fill="#e5edff" stroke="#244fdd" stroke-width="3"/>');text(x-65,y+57,label,16,'#142842',600)
 text(81,291,'Selected: 3 nodes · 2 relationships',14,'#51647d');text(344,330,'Shared IP · DNS observations',14,'#51647d')
def seed():
 rect(65,275,770,85,'#f8faff');text(85,307,'Indicators',14,'#51647d',700);text(85,338,'example.com',18);button(670,297,140,'Edit indicators')

def brief(review=False):
 seed()
 text(85,401,'INVESTIGATION BRIEF',12,'#51647d',700)
 text(85,435,'Find related infrastructure',26,'#142842',700)
 text(85,467,'example.com  /  Last 30 days',16,'#51647d')
 rect(65,494,770,76,'#f3f6fa','#e5eaf1',8)
 text(85,523,'Scope ready' if review else 'One decision before planning',17,'#142842',700)
 text(85,550,'Shared IPs + shared certificates' if review else 'Choose what “related” means in the conversation →',16,'#51647d')
 text(85,610,'PROPOSED COVERAGE' if review else 'AVAILABLE INVESTIGATION PATHS',12,'#51647d',700)
 for y,title,body in [(632,'DNS observations','Connect domains through observed IP addresses.'),(714,'Certificate observations','Explore relationships through certificate records.')]:
  rect(65,y,770,69,'#fff','#e5eaf1',8)
  text(85,y+27,title,17,'#142842',600)
  text(85,y+51,body,15,'#51647d')
  text(698,y+28,'Planned' if review else 'Option',13,'#51647d',600)
 text(85,821,'Awaiting confirmation · No observations retrieved' if review else 'No job started · Sources shown as options, not findings',14,'#51647d')

base(1,'Clarify the question','Ask naturally, then click a suggested response or keep typing. The assistant remains a conversation.')
brief()
user(['Find related infrastructure for example.com','observed in the last 30 days.'])
text(895,483,'What should “related” mean here?',20,'#142842',700)
lines(895,519,['I can look for:', '• Shared IPs — domains observed at the same IP.', '• Shared certificates — certificate relationships.'],16,'#263449',28)
text(895,612,'Choose an option, or describe what you need below.',15,'#51647d')
button(895,634,133,'Shared IPs');button(1040,634,188,'Shared certificates');button(1240,634,105,'Both')
rect(890,705,480,45,'#fff7e6','#ecd6a7');text(905,733,'No job started. I’ll show you a plan before running it.',15,'#715323')
composer('Describe the relationship you want to explore…')
badge(812,289,1);badge(1378,628,2);badge(1378,784,3)
note(50,918,1,'Preserve existing input',['One domain illustrates this scenario.','Existing multi-indicator behavior remains.'])
note(515,918,2,'Click or type',['Suggested replies are shortcuts.','Free-text clarification is always available.'])
note(980,918,3,'A persistent conversation',['The composer stays visible in every state.','Scroll replies without losing the input box.'])
save('01-clarify')

base(2,'Review and confirm enrichments','The assistant replies with a structured plan. Edit its controls or ask for a change in chat.')
brief(True)
user(['Use both. Show me the plan before running it.'])
text(895,480,'Here’s the proposed enrichment plan',20,'#142842',700)
rect(890,497,480,210,'#f8faff','#dce3eb')
text(905,520,'example.com · Shared IPs + certificates',16,'#142842',600)
lines(905,545,['15 Oct 2026, 10:00 → 14 Nov 2026, 10:00','America/New_York · UTC−04:00 → UTC−05:00'],14,'#51647d',22)
text(905,596,'☑ DNS observations',16,'#142842',600);text(924,618,'Connect domains to observed IP addresses.',14,'#51647d')
text(905,648,'☑ Certificate observations',16,'#142842',600);text(924,670,'Add relationships through certificate records.',14,'#51647d')
text(905,694,'Authorized sources · Cost / duration unavailable',13,'#51647d')
button(895,726,130,'Edit plan');button(1040,726,220,'Run 2 enrichments',True)
composer('Change the dates or datasets in this plan…')
badge(1378,492,1);badge(1378,632,2);badge(1378,784,3)
note(50,918,1,'Structured reply, same chat',['Scope, dates, and rationale live in a reply.','Keep the surrounding conversation visible.'])
note(515,918,2,'Two ways to refine the plan',['Click a dataset or type “Use DNS only.”','Both update the same proposed plan.'])
note(980,918,3,'Refine first, confirm execution',['Chat stays available during plan review.','Only explicit confirmation creates a job.'])
save('02-review-plan')

base(3,'Explore a finding with its evidence','Read a grounded answer, open its citations, or ask a follow-up without leaving the graph.')
graph();badge(809,302,1)
rect(65,592,770,151,'#fff');text(85,621,'Evidence 1–2 · DNS observations',17,'#142842',700)
lines(85,653,['example.com → 192.0.2.10 · observed 12 Nov 2026, 14:20 UTC','related.example → 192.0.2.10 · observed 12 Nov 2026, 14:22 UTC','Records DNS-101 and DNS-102 · Selection and time range match the answer.'],15,'#51647d',27)
user(['Which domains share an IP with example.com','in this time range?'])
text(895,481,'One match in completed data',20,'#142842',700)
text(895,517,'• related.example shares the observed IP 192.0.2.10.',16)
link(911,547,'[1] DNS-101',15);link(1030,547,'[2] DNS-102',15)
lines(895,586,['Shared IP does not establish common ownership','or maliciousness.'],15,'#51647d',23)
rect(890,630,480,69,'#fff7e6','#ecd6a7');text(905,655,'Coverage: DNS complete · Certificates failed',15,'#715323',600)
text(905,680,'This answer uses completed sources only.',14,'#715323');link(1215,680,'Retry source',14)
button(895,726,160,'Undo view change');button(1070,726,150,'Save finding')
composer('Ask about a node, source, or follow-up question…')
badge(1378,545,2);badge(1378,784,3)
note(50,918,1,'Evidence works both ways',['Citations highlight matching graph records.','Manual selections update the chat context.'])
note(515,918,2,'Readable, inspectable answers',['Headings, bullets, and clickable citations','make the finding and its limits easy to scan.'])
note(980,918,3,'Continue the investigation',['Ask another question or click an action.','Partial data never removes the composer.'])
save('03-evidence-partial')

base(4,'Share a graph with useful context','Refine a draft through conversation, review its audience, then explicitly confirm sharing.')
graph();text(85,623,'Saved view',18,'#142842',700);lines(85,658,['3 nodes · 2 relationships · Time filter: 15 Oct–14 Nov 2026','Snapshot: 14 Nov 2026, 15:05 UTC · DNS records DNS-101 / DNS-102'],15,'#51647d',27);badge(811,623,1)
user(['Share this graph and finding with Analyst Lee.'])
text(895,480,'Here’s a draft to review before sharing',19,'#142842',700)
rect(890,497,480,211,'#f8faff','#dce3eb')
text(905,522,'Shared IP observed for example.com',16,'#142842',700)
lines(905,549,['example.com and related.example were observed','at 192.0.2.10. Shared IP does not establish ownership.'],14,'#263449',22)
link(905,598,'[1] DNS-101',14);link(1017,598,'[2] DNS-102',14);link(1237,598,'Edit finding',14)
text(905,627,'Coverage caveat: certificate enrichment failed.',14,'#715323')
text(905,655,'Recipient: Analyst Lee',15,'#142842',600);link(1250,655,'Change',14)
text(905,681,'Access checked · All evidence available',14,'#247257');text(905,699,'Graph + saved view + finding · Raw chat excluded',12,'#51647d')
button(895,726,100,'Cancel');button(1010,726,170,'Confirm share',True)
composer('Revise the finding or change its recipients…')
badge(1378,653,2);badge(1378,784,3)
note(50,918,1,'Share the graph and context',['Recipients open the saved view and graph,','inspect evidence, and continue exploration.'])
note(515,918,2,'Clickable review controls',['Edit the finding or choose recipients in chat.','Block sharing if any evidence is restricted.'])
note(980,918,3,'Chat can revise, not bypass',['Typed revisions update the draft and checks.','Sharing still requires explicit confirmation.'])
save('04-share-graph')

(out/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Analyst Assistant — annotated mockups</title><style>body{margin:24px;background:#e5eaf0;font:16px Arial}h1,p{margin:16px auto;max-width:1440px}img{display:block;width:100%;max-width:1440px;height:auto;margin:24px auto;background:white} @media print{img{break-after:page;margin:0}h1,p{display:none}@page{size:landscape;margin:0}}</style><h1>Analyst Assistant · annotated concepts</h1><p>Revised November 14: persistent chat composer in all four states, conversational replies, and inline controls. Fictional content; not a working analyst prototype.</p>'+''.join(f'<img src="{s}.svg" alt="{s}">' for s in ['01-clarify','02-review-plan','03-evidence-partial','04-share-graph'])+'</html>')
