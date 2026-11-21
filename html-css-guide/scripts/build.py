from pathlib import Path
from html import escape as e
import json
from lessons import LESSONS
from diagrams import create

ROOT=Path(__file__).resolve().parent.parent
PARTS={1:('HTML','Give content meaning',range(1,7)),2:('CSS','Give ideas a visual language',range(7,14)),3:('Layout','Make everything fit',range(14,25))}

def codeblock(code,lang='HTML + CSS'):
    return f'<div class="code-panel"><div class="panel-label"><span>{lang}</span><button class="copy" type="button" aria-label="Copy code example">Copy code</button></div><pre><code>{e(code)}</code></pre></div>'

def preview(code,title):
    # These are authored examples, not user-supplied executable content.
    base='<style>body{margin:20px;font-family:system-ui,sans-serif;color:#253d31;line-height:1.5}*{box-sizing:border-box}a{color:#185c45}button,input,select{font:inherit}button{margin-top:12px}img{max-width:100%}</style>'
    doc=code
    if '<head>' in doc: doc=doc.replace('<head>','<head>'+base,1)
    else: doc='<!doctype html><html lang="en"><head><meta charset="utf-8">'+base+'</head><body>'+doc+'</body></html>'
    return f'<div class="preview-panel"><div class="panel-label"><span><i class="live-dot"></i> Browser preview</span><span class="tiny">HTML + CSS only</span></div><iframe loading="lazy" title="{e(title)} example output" sandbox="" srcdoc="{e(doc,quote=True)}"></iframe></div>'

def diagram(name,caption=''):
    return f'<figure class="diagram"><a href="assets/{name}.svg" target="_blank" rel="noopener" aria-label="Open {e(caption or name)} diagram at full size"><img src="assets/{name}.svg" alt="{e(caption or name)}" loading="lazy" width="800" height="460"></a><figcaption>{e(caption)} <span>Original diagram · open to enlarge ↗</span></figcaption></figure>'

def chapter(r,n):
    rid=r['id']; tags='<span class="tag">🆕 New in this guide</span>'
    if r['added']: tags+='<span class="tag added">➕ Added foundation</span>'
    if r['focus']: tags+='<span class="tag focus">Extra practice</span>'
    see=diagram(r['diagram'],r['title']) if r['diagram'] else '<div class="mental-model"><span>THE MENTAL MODEL</span><p>'+e(r['takeaway'])+'</p></div>'
    notes=''.join(f'<div class="note"><h3>{e(t)}</h3><p>{e(p)}</p></div>' for t,p in r['notes'])
    quiz=''.join(f'<div class="quiz-item"><h3><span>{i+1:02}</span> {e(q)}</h3><details><summary>Reveal answer</summary><p>{e(a)}</p></details></div>' for i,(q,a) in enumerate(r['quiz']))
    sources=''.join(f'<a href="{e(s)}" target="_blank" rel="noopener">{e(s.split("/")[2])} · {e(s.rstrip("/").split("/")[-1].replace("_"," "))} ↗</a>' for s in r['source'])
    prev=f'#chapter-{n-1:02}' if n>1 else '#overview'
    nextid=f'#chapter-{n+1:02}' if n<24 else '#projects'
    return f'''<article id="{rid}" class="view lesson" data-title="{e(r['title'])}" data-part="{r['part']}">
<div class="lesson-breadcrumb">PART {r['part']} / {PARTS[r['part']][0]} <span>CHAPTER {n:02} OF 24</span></div>
<div class="tags">{tags}</div><h1 tabindex="-1">{e(r['title'])}<span class="title-period">.</span></h1>
<p class="lesson-description">{e(r['summary'])}</p><div class="lesson-meta"><span>◷ 5–10 min per section, including practice</span><span>Read · try · explain</span></div>
<section aria-labelledby="{rid}-what"><h2 id="{rid}-what"><span>01</span> 🎯 What is it?</h2><p>{e(r['why'])}</p></section>
<section aria-labelledby="{rid}-see"><h2 id="{rid}-see"><span>02</span> 🖼️ See it</h2>{see}</section>
<section aria-labelledby="{rid}-code"><h2 id="{rid}-code"><span>03</span> 💻 Try the code</h2><p class="muted">Read the code, predict the result, then compare with the browser preview. Copy it into your own HTML file to experiment.</p>{codeblock(r['code'])}</section>
<section aria-labelledby="{rid}-output"><h2 id="{rid}-output"><span>04</span> 👀 What you should see</h2><p>{e(r['output'])}</p>{preview(r['code'],r['title'])}</section>
<section><h2><span>05</span> 🌍 Where this shows up</h2><p>{e(r['use'])}</p><div class="notes-grid">{notes}</div></section>
<section class="watch-out"><h2>⚠️ Easy mistakes to avoid</h2><ul>{''.join('<li>'+e(m)+'</li>' for m in r['mistakes'])}</ul></section>
<div class="takeaway"><span>ONE THING TO REMEMBER</span><p>{e(r['takeaway'])}</p></div>
<section><h2><span>06</span> 🧠 Check your understanding</h2><p class="muted">Try explaining it out loud before revealing an answer.</p>{quiz}</section>
<section class="practice-box"><span class="eyebrow">YOUR TURN</span><h2>A little practice, a lot of clarity.</h2><p>{e(r['practice'])}</p><p class="tiny">Success test: describe the rule behind the result, not just the property you changed.</p></section>
<section class="sources"><h2>Keep exploring</h2>{sources}</section>
<div class="lesson-actions"><button class="button mark-read" data-lesson="{rid}" type="button">Mark chapter as read <span>✓</span></button><span class="muted tiny">Reading progress, not a mastery score.</span></div>
<nav class="lesson-pagination" aria-label="Chapter navigation"><a href="{prev}">← Previous</a><a href="{nextid}">{'Next chapter' if n<24 else 'Build a mini project'} →</a></nav></article>'''

PROJECTS=[
dict(id='booking',part=1,title='A booking page with good manners',desc='Meaningful structure, visible labels, and native validation. Start with the browser’s own helpful behaviors.',skills='Semantics · forms · accessibility',brief=['Create a header, main region, and footer.', 'Give every control a persistent label and a useful name.', 'Group the rental options and use suitable input types.', 'Test required fields and navigate using only your keyboard.'],
body='''<header><p>Sunday Cycle Club</p><nav aria-label="Main"><a href="#booking">Book a ride</a> · <a href="#questions">Questions</a></nav></header>
<main><h1>A slower Sunday starts here.</h1><p>Tell us a little about your ride.</p>
<p><strong>Practice form:</strong> use made-up details. Valid submission reloads this local page with demo values in the URL; nothing is sent to a booking service.</p>
<form id="booking" method="get"><fieldset><legend>Contact details</legend>
<p><label for="rider">Full name</label><br><input id="rider" name="rider" autocomplete="name" required></p>
<p><label for="email">Email address</label><br><input id="email" name="email" type="email" autocomplete="email" required></p></fieldset>
<fieldset><legend>Your ride</legend><p><label for="date">Pickup date</label><br><input id="date" name="date" type="date" required></p>
<p><label for="bike">Bike style</label><br><select id="bike" name="bike"><option value="city">City cruiser</option><option value="touring">Touring bike</option></select></p>
<label><input type="checkbox" name="helmet" value="yes"> Include a helmet</label></fieldset>
<button type="submit">Check my details</button></form>
<section id="questions"><h2>Before you arrive</h2><details><summary>Where do we meet?</summary><p>At the town square bike stand.</p></details></section></main>
<footer><p>Take the scenic route.</p></footer>''',css=''),
dict(id='rental-card',part=2,title='A rental card worth reading',desc='Turn plain content into a warm, readable component. Give spacing, color, and focus a clear purpose.',skills='Box model · typography · states',brief=['Create a card with an image, heading, description, and navigation link.', 'Use border-box and flexible width constraints.', 'Use an image alternative and a visible keyboard focus style.', 'Style a labeled contact field without depending on placeholder text.'],
body='''<main><article class="card"><img src="../assets/bicycle.svg" width="800" height="480" alt="A green city bicycle beside a warm sun"><div class="content"><p class="eyebrow">THE EVERYDAY EXPLORER</p><h1>Meet the city cruiser.</h1><p>An upright ride, a comfortable saddle, and nowhere you need to rush.</p><p><strong>₹250</strong> / day</p><a class="button" href="booking.html">Plan your ride →</a></div></article>
<section class="contact"><h2>A question before you ride?</h2><form method="get"><label for="email">Your email</label><input id="email" type="email" name="demo-email" placeholder="you@example.com" required><p>Demo only: use made-up details. Submission reloads this page.</p><button type="submit">Check email format</button></form></section></main>''',
css='''* { box-sizing: border-box; }
body { margin: 0; padding: 2rem 1rem; background: #f4f3eb; color: #203c2c; font: 1rem/1.65 system-ui, sans-serif; }
main { max-width: 28rem; margin-inline: auto; }
.card { overflow: hidden; border: 1px solid #cdd7c4; border-radius: 1.2rem; background: #fff; }
.card img { display: block; width: 100%; height: auto; }
.content { padding: 1.5rem; }
h1 { font-size: 2rem; line-height: 1.15; }
.eyebrow { font-size: .75rem; letter-spacing: .12em; }
.button, button { display: inline-block; padding: .8rem 1rem; background: #1d6148; color: white; border: 0; border-radius: .4rem; font: inherit; text-decoration: none; }
a:focus-visible, button:focus-visible, input:focus-visible { outline: 3px solid #b65a20; outline-offset: 4px; }
.contact { margin-block: 2rem; }
label { display: block; }
input { width: 100%; padding: .8rem; border: 1px solid #647c66; border-radius: .3rem; font: inherit; }
input:user-invalid { border: 2px solid #a52b24; }
.contact p { font-size: .85rem; }'''),
dict(id='dashboard',part=3,title='Your first responsive dashboard',desc='Bring the pieces together: Grid for the page, Flexbox for small rows, and container queries for reusable cards.',skills='Grid · Flexbox · responsive · themes',brief=['Build a sticky header and a sidebar with real section links.', 'Make the layout stack when the content needs more room.', 'Use a container query inside each rental card.', 'Contain the table’s horizontal scrolling and test keyboard access.', 'Follow system dark mode and respect user font settings.'],
body='''<header class="top"><a href="#overview">Sunday Cycle Club</a><a href="booking.html">Book a ride ↗</a></header>
<div class="shell"><nav class="side" aria-label="Dashboard"><p>YOUR WEEKEND</p><a href="#overview">Overview</a><a href="#bikes">Available bikes</a><a href="#prices">Rental prices</a><a href="booking.html">Booking form</a></nav>
<main id="overview"><p class="eyebrow">A LITTLE FRESH AIR</p><h1>Your next adventure is around the corner.</h1><p>Pick a bike. Take your time. Find a new favorite street.</p>
<section id="bikes"><h2>Ready when you are</h2><div class="cards">'''+''.join(f'''<div class="slot"><article class="bike-card"><img src="../assets/bicycle.svg" width="800" height="480" alt="Green city bicycle"><div><h3>{name}</h3><p>{description}</p><a href="booking.html">Choose this ride →</a></div></article></div>''' for name,description in [('City cruiser','Upright and easygoing.'),('Weekend explorer','A little further, a little slower.'),('Riverside rider','Made for the scenic route.')])+'''</div></section>
<section id="prices"><h2>Simple daily prices</h2><div class="table-wrap" role="region" tabindex="0" aria-label="Daily rental prices"><table><caption>One-day rentals, helmet included</caption><thead><tr><th scope="col">Bike</th><th scope="col">Duration</th><th scope="col">Daily price</th><th scope="col">Pickup</th></tr></thead><tbody><tr><th scope="row">City cruiser</th><td>24 hours</td><td>₹250</td><td>Town square</td></tr><tr><th scope="row">Touring bike</th><td>24 hours</td><td>₹400</td><td>Riverside</td></tr></tbody></table></div></section></main></div><footer>Built with HTML, CSS, and a little curiosity.</footer>''',
css='''* { box-sizing: border-box; }
:root { --page: #f6f5ed; --surface: #fffef8; --ink: #263e30; --line: #d6ddce; --accent: #1e6148; }
body { margin: 0; background: var(--page); color: var(--ink); font: 1rem/1.6 system-ui, sans-serif; }
a { color: var(--accent); text-underline-offset: .2em; }
:focus-visible { outline: 3px solid #b96c26; outline-offset: 4px; }
.top { position: sticky; top: 0; z-index: 1; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; padding: 1rem 4%; background: var(--surface); border-bottom: 1px solid var(--line); }
.shell { max-width: 90rem; margin: auto; display: grid; grid-template-columns: minmax(0,1fr); }
.side { padding: 1.5rem; }
.side a { display: block; padding: .5rem; }
.side p, .eyebrow { font-size: .75rem; letter-spacing: .12em; }
main { min-width: 0; padding: clamp(1rem,4vw,3rem); }
h1 { max-width: 21ch; font-size: clamp(2rem,1rem + 3vw,3.8rem); line-height: 1.1; font-weight: 550; }
section { margin-block: 3rem; scroll-margin-top: 6rem; }
.cards { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit,minmax(min(100%,20rem),1fr)); }
.slot { container-type: inline-size; }
.bike-card { height: 100%; padding: 1rem; background: var(--surface); border: 1px solid var(--line); border-radius: .8rem; display: grid; gap: 1rem; }
.bike-card img { width: 100%; height: auto; border-radius: .4rem; }
@container (min-width: 27rem) { .bike-card { grid-template-columns: 1fr 1fr; align-items: center; } }
.table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: .5rem; }
table { border-collapse: collapse; width: 100%; min-width: 35rem; background: var(--surface); }
caption { padding: 1rem; text-align: start; }
th,td { padding: 1rem; text-align: start; border-top: 1px solid var(--line); }
footer { padding: 2rem; text-align: center; }
@media (min-width: 55rem) { .shell { grid-template-columns: 13rem minmax(0,1fr); } .side { border-right: 1px solid var(--line); } }
@media (prefers-color-scheme: dark) { :root { --page: #17231b; --surface: #203127; --ink: #eef3e8; --line: #415a48; --accent: #a4d8ad; } }''')]

CHECKS=[('HTML & meaning',['I can explain head versus body and title versus h1.','I choose links for navigation and buttons for actions.','My headings and page regions form a useful outline.','Every form control has a persistent label and a name when needed.','I understand native validation and its limits.','My images have meaningful alternatives or empty alt when decorative.']),('CSS & appearance',['I can calculate a box’s width under both box-sizing models.','I can explain which declaration wins without guessing.','I choose units based on their reference size.','Text stays readable with zoom and larger font preferences.','Focus and error states do not depend on color alone.']),('Layout & adaptability',['I can identify a containing block and a stacking context.','I can explain Flexbox axes and automatic minimum sizes.','I can build a Grid with intentional tracks and gaps.','Long text and tables do not force unwanted page overflow.','I can choose between media and container queries.','My image size hints match the actual layout.','I test keyboard use, contrast, reflow, and reduced motion.','I can write a one-sentence root cause for a layout bug.'])]

def build():
    create()
    nav=''; cards=''
    for p,(label,sub,nums) in PARTS.items():
        links=''.join(f'<a href="#{LESSONS[i-1]["id"]}" data-nav="{LESSONS[i-1]["id"]}"><span>{i:02}</span>{e(LESSONS[i-1]["title"])}</a>' for i in nums)
        nav+=f'<details class="nav-group" open><summary><span>0{p}</span> {label}<i>⌄</i></summary><div>{links}</div></details>'
        cards+=f'<a class="path-card part-{p}" href="#chapter-{list(nums)[0]:02}"><span class="part-num">0{p}</span><span class="eyebrow">{len(nums)} CHAPTERS</span><h3>{label}<span>↗</span></h3><p>{sub}.</p><div class="path-footer">{e(LESSONS[list(nums)[0]-1]["title"])} <span>→</span></div></a>'
    projects=''
    for p in PROJECTS:
        document='<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <title>'+p['title']+'</title>\n'+('<style>\n'+p['css']+'\n</style>\n' if p['css'] else '')+'</head>\n<body>\n'+p['body']+'\n</body>\n</html>'
        (ROOT/'projects'/f'{p["id"]}.html').write_text(document)
        projects+=f'''<section class="project" id="project-{p['part']}"><div class="project-heading"><span class="project-number">0{p['part']}</span><div><span class="eyebrow">PART {p['part']} · MINI PROJECT</span><h2>{e(p['title'])}</h2></div></div><p>{e(p['desc'])}</p><div class="tag">{p['skills']}</div><h3>Your brief</h3><ol>{''.join('<li>'+e(x)+'</li>' for x in p['brief'])}</ol><div class="project-links"><a class="button" href="projects/{p['id']}.html" target="_blank" rel="noopener">Open working example ↗</a><a class="text-link" href="projects/{p['id']}.html" download>Download HTML ↓</a></div><details class="solution"><summary>Reveal the complete reference solution</summary>{codeblock(document)}</details></section>'''
    checklist=''.join(f'<section class="check-group"><h2>{e(title)}</h2>'+''.join(f'<label class="check-row"><input type="checkbox" data-check="{g}-{i}"><span>{e(item)}</span></label>' for i,item in enumerate(items))+'</section>' for g,(title,items) in enumerate(CHECKS))
    gallery=''.join(f'<a class="gallery-card" href="assets/{name}.svg" target="_blank" rel="noopener"><img src="assets/{name}.svg" alt="{title}" loading="lazy" width="800" height="460"><h2>{title} <span>↗</span></h2></a>' for name,title in [('document','The HTML document'),('display','Block, inline, inline-block'),('box-model','The box model'),('cascade','The cascade'),('position','Five positioning modes'),('flex','Flexbox axes'),('grid','Grid tracks and cells'),('responsive','Responsive layouts'),('container','Container queries')])
    catalog=[dict(id=r['id'],title=r['title'],part=r['part'],text=' '.join([r['summary'],r['why'],r['code'],r['practice']]+[p for t,p in r['notes']])) for r in LESSONS]
    catalog_json=json.dumps(catalog,ensure_ascii=False).replace('<','\\u003c')
    doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A friendly, visual HTML and CSS field guide. 24 chapters, original diagrams, working examples, and three hands-on projects."><meta name="theme-color" content="#f7f7f0"><title>Fieldnotes — Learn HTML & CSS</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<aside class="sidebar" id="sidebar" aria-label="Learning guide navigation"><a class="brand" href="#overview"><span class="brand-mark">f<span>.</span></span><span>fieldnotes<span class="brand-sub">THE HTML & CSS GUIDE</span></span></a>
<div class="sidebar-intro">A little curiosity.<br>A whole lot you can build.</div>
<nav aria-label="Chapters"><a class="overview-link" href="#overview" data-nav="overview">◈ <span>Start here</span><span>↗</span></a>{nav}<div class="nav-extras"><a href="#projects" data-nav="projects">↗ <span>Mini projects</span><span>03</span></a><a href="#visuals" data-nav="visuals">▧ <span>Visual library</span><span>09</span></a><a href="#checklist" data-nav="checklist">✓ <span>Revision checklist</span></a></div></nav>
<div class="sidebar-progress"><div><span>YOUR READING JOURNEY</span><strong id="progress-count">0 / 24</strong></div><progress id="reading-progress" max="24" value="0" aria-label="Chapters marked as read"></progress><p>One small lesson at a time.</p></div></aside>
<div class="app"><header class="topbar"><button id="menu-toggle" class="icon-button menu-toggle" aria-expanded="false" aria-controls="sidebar" aria-label="Open chapter navigation" type="button">☰</button><a class="top-brand" href="#overview">fieldnotes.</a><span class="topbar-label">YOUR POCKET GUIDE TO THE WEB</span><div class="top-actions"><label class="search-box"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="Find a concept…" aria-label="Search all lessons" autocomplete="off"><kbd>/</kbd></label><button id="theme-toggle" class="icon-button" type="button" aria-label="Switch to dark theme">◐</button></div></header>
<main id="main" tabindex="-1"><div id="search-view" class="view search-view" hidden><span class="eyebrow">FIND YOUR NEXT AHA MOMENT</span><h1>Search the guide.</h1><p id="search-count" role="status"></p><div id="search-results"></div><button type="button" class="button secondary" id="clear-search">Back to the guide</button></div>
<section id="overview" class="view home"><div class="hero"><div class="hero-copy"><span class="eyebrow"><i class="live-dot"></i> A VISUAL GUIDE FOR CURIOUS BEGINNERS</span><h1>Make the web<br><em>make sense.</em></h1><p>From your first HTML tag to layouts that just fit. Learn the why, see it in action, then make something of your own.</p><div class="hero-actions"><a class="button" id="continue-link" href="#chapter-01">Start learning <span>↗</span></a><a class="text-link" href="#visuals">I learn by seeing →</a></div><div class="hero-note"><span>✳</span> Just HTML & CSS. A whole world of possibilities.</div></div><div class="hero-art"><img src="assets/hero.svg" alt="An HTML page and CSS rule card: structure, style, and layout working together" width="800" height="460"><span class="art-caption">A SMALL IDEA → A REAL THING</span></div></div>
<div class="stats-strip"><div><strong>24</strong><span>bite-size chapters</span></div><div><strong>03</strong><span>real-world projects</span></div><div><strong>09</strong><span>visual explainers</span></div><div><strong>100%</strong><span>learn at your pace</span></div></div>
<section class="learning-path"><div class="section-heading"><div><span class="eyebrow">THE LEARNING PATH</span><h2>Small steps. Solid foundations.</h2></div><span class="muted tiny">Start at the beginning. Build as you go.</span></div><div class="path-grid">{cards}</div></section>
<section class="featured"><div class="featured-copy"><span class="eyebrow">LESS GUESSING, MORE UNDERSTANDING</span><h2>Every pixel has<br>a reason.</h2><p>Padding or margin? A stubborn flex item? We’ll turn the invisible rules into things you can see.</p><a class="text-link" href="#chapter-09">Meet the box model →</a></div><a class="featured-visual" href="#chapter-09"><img src="assets/box-model.svg" alt="A box model diagram showing content, padding, border, and margin" width="800" height="460" loading="lazy"></a></section>
<section class="how-to"><span class="eyebrow">MAKE IT STICK</span><h2>A better way to learn a little.</h2><div class="habit-grid"><div><span>01 / READ</span><h3>Get the idea.</h3><p>One concept. Plain English. No need to memorize every property.</p></div><div><span>02 / TRY</span><h3>Change something.</h3><p>Predict the output, run the example, and see what surprises you.</p></div><div><span>03 / EXPLAIN</span><h3>Find your words.</h3><p>Explain why it works. Then tackle the challenge without peeking.</p></div></div></section>
<div class="personal-note"><strong>A guide built around your roadmap.</strong><p>Extra care goes into labels, keyboard access, Flexbox shrinking, and intrinsic sizing. “New” means not yet covered together; it does not assume you have never studied a topic. Added foundations fill gaps before the advanced material.</p><a href="guide.md" download>Download the full Markdown guide ↓</a></div>
</section>
{''.join(chapter(r,i+1) for i,r in enumerate(LESSONS))}
<section id="projects" class="view lesson"><span class="eyebrow">LEARNING, MADE TANGIBLE</span><h1>Make something<br><em>of your own.</em></h1><p class="lesson-description">Three little projects that put the ideas together. Try the brief first, then open the working example or reveal its complete code.</p>{projects}</section>
<section id="visuals" class="view"><span class="eyebrow">THE VISUAL LIBRARY</span><h1>See the idea.<br><em>Keep the picture.</em></h1><p class="lesson-description">Nine original diagrams. Clear labels, simple comparisons, and no blurry screenshots. Open any illustration to zoom or save it.</p><div class="gallery">{gallery}</div><p class="muted">Original SVG illustrations created for this guide. All assets are included locally; the guide does not depend on remote images.</p></section>
<section id="checklist" class="view lesson"><span class="eyebrow">BEFORE YOU CALL IT DONE</span><h1>Can you explain<br><em>the why?</em></h1><p class="lesson-description">Use this as a revision conversation with yourself. Check a statement when you can demonstrate it, not just recognize the words.</p>{checklist}<div class="practice-box"><h2>Your final challenge</h2><p>Build the responsive dashboard from a blank file. Then introduce a long title, increase text size, use a narrow viewport, navigate by keyboard, and explain each adjustment you make.</p><a class="button" href="#projects">Choose a project ↗</a></div><p class="muted tiny">Progress is stored in this browser when local storage is available. It is not synced between devices.</p><button class="text-button" id="reset-progress" type="button">Reset reading progress and checklist</button></section>
<footer class="site-footer"><span class="footer-brand">fieldnotes<span>.</span></span><p>Built for small steps and big aha moments.</p><a href="#overview">Back to the beginning ↑</a></footer></main></div>
<div id="toast" class="toast" role="status" aria-live="polite"></div><script id="lesson-index" type="application/json">{catalog_json}</script>
</body></html>'''
    (ROOT/'index.html').write_text(doc)
    (ROOT/'assets'/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#234d39"/><text x="13" y="36" font-family="Georgia" font-size="40" fill="#e6f0c8">f.</text></svg>')
    md=['# Fieldnotes — The HTML & CSS Guide','Read → predict → try → explain. Work through one small topic at a time. New means new in this guide, not proof of your prior experience. Added marks foundational material added to the roadmap.','## Table of contents']
    md += [f'{i+1}. {r["title"]}' for i,r in enumerate(LESSONS)]
    for i,r in enumerate(LESSONS):
        md += [f'## Chapter {i+1}: {r["title"]}', '🆕 New for you'+(' · ➕ Added' if r['added'] else ''),'### 🎯 What is it?',r['summary'],r['why'],'### 🖼️ See it']
        md += [f'![{r["title"]}](assets/{r["diagram"]}.svg)' if r['diagram'] else r['takeaway'],'### 💻 Code example','```html\n'+r['code']+'\n```','### 👀 Output',r['output'],'### 🌍 Real-world use',r['use']]
        for title,body in r['notes']:md += ['### '+title,body]
        md += ['### ⚠️ Common mistakes','\n'.join('- '+m for m in r['mistakes']),'### ✅ Quick takeaway',r['takeaway'],'### 🧠 Challenge',r['practice']]
        for q,a in r['quiz']:md += [q,'<details><summary>Answer</summary>\n\n'+a+'\n\n</details>']
        md += ['### Sources','\n'.join('- ['+s.split('/')[2]+']('+s+')' for s in r['source'])]
    md += ['## Three mini projects']
    for p in PROJECTS:md += ['### '+p['title'],p['desc'],'\n'.join('- '+s for s in p['brief']),f'[Working example](projects/{p["id"]}.html)']
    md += ['## Final revision checklist']
    for title,items in CHECKS:md += ['### '+title,'\n'.join('- [ ] '+s for s in items)]
    (ROOT/'guide.md').write_text('\n\n'.join(md))
    (ROOT/'README.md').write_text('''# Fieldnotes — HTML & CSS guide

Open `index.html` in a browser. All lessons, images, styles, and examples are local. A small vanilla script enables chapter navigation, search, copy buttons, theme choice, and local reading progress; the teaching content and projects cover HTML and CSS only. Without that script, all chapters remain readable in one document.

## Included

- 24 chapters with examples, browser previews, common mistakes, exercises, and 48 quiz answers.
- 9 original explanatory SVG diagrams, a cover illustration, and a bicycle illustration.
- 3 standalone projects in `projects/` with complete reference solutions.
- `guide.md`: the complete printable/source-friendly Markdown guide.

## Local preview

Run `python3 -m http.server 8766 --directory html-css-guide` from the parent directory, then open `http://localhost:8766`.

## Editing

The static document is generated from `scripts/lessons.py` and `scripts/build.py`. Run `python3 html-css-guide/scripts/build.py` from the parent directory after editing. Styles and client interactions live in `styles.css` and `app.js`.

## Sources and assets

Each chapter links to its official documentation. The roadmap was read from the local project's converted roadmap content because the public URL could not be retrieved. All SVG artwork is original and included in `assets/`; no external fonts, image hotlinks, analytics, or API keys are required.

Browser examples use sandboxed frames with scripts and form submission disabled. The standalone form projects use local GET submissions with demo values; no real booking or external data processing is implemented. Reading completion is self-reported and is not presented as mastery. Local storage is best-effort and may vary for file URLs.
''')
    print(f'Built {len(LESSONS)} chapters, {len(PROJECTS)} projects, and guide.md.')

if __name__=='__main__': build()
