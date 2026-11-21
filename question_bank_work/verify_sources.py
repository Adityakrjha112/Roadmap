import concurrent.futures, hashlib, json, re, sys, urllib.request
from pathlib import Path
from html.parser import HTMLParser
class TextParser(HTMLParser):
  def __init__(self):
    super().__init__(); self.parts=[]; self.skip=0
  def handle_starttag(self,tag,attrs):
    if tag in ('script','style'): self.skip+=1
    if tag in ('p','h1','h2','h3','li','pre'): self.parts.append('\n')
  def handle_endtag(self,tag):
    if tag in ('script','style') and self.skip: self.skip-=1
    if tag in ('p','h1','h2','h3','li','pre'): self.parts.append('\n')
  def handle_data(self,data):
    if not self.skip: self.parts.append(data)
ROOT=Path(__file__).parent
CACHE=ROOT/'sources'; CACHE.mkdir(exist_ok=True)
rows=[]
for p in sorted(ROOT.glob('batch*.json')): rows.extend(json.loads(p.read_text()))
urls=sorted({r['Source URL'].split('#')[0] for r in rows})
def fetch(url):
  path=CACHE/(hashlib.sha256(url.encode()).hexdigest()+'.json')
  if path.exists(): return json.loads(path.read_text())
  try:
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (documentation verification)'})
    with urllib.request.urlopen(req,timeout=30) as res: html=res.read(); final=res.url
    raw=html.decode('utf-8',errors='replace')
    match=re.search(r'<title[^>]*>(.*?)</title>',raw,re.S)
    title=match.group(1) if match else ''
    main=re.search(r'<main\b[^>]*>(.*?)</main>',raw,re.S)
    parser=TextParser(); parser.feed(main.group(1) if main else raw)
    text=re.sub(r'[ \t]+',' ',''.join(parser.parts))
    text=re.sub(r'\n\s*\n','\n',text)
    result={'url':url,'final':final,'status':200,'title':title,'text':text}
    path.write_text(json.dumps(result,ensure_ascii=False))
    return result
  except Exception as e: return {'url':url,'status':'ERROR','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: results=list(ex.map(fetch,urls))
(ROOT/'source_manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps({'urls':len(urls),'verified':sum(r['status']==200 for r in results),'errors':[r for r in results if r['status']!=200]},indent=2))
if '--evidence' in sys.argv:
  byurl={r['url']:r for r in results}
  for row in rows:
    source=byurl[row['Source URL'].split('#')[0]]
    if source['status']!=200: continue
    terms=re.findall(r'[A-Za-z][A-Za-z0-9]+',row['Subtopic'])
    paragraphs=[s for s in source['text'].split('\n') if len(s)>60]
    score=lambda s:sum(bool(re.search(r'\b'+re.escape(w)+r'\b',s,re.I)) for w in terms)
    best=sorted(paragraphs,key=score,reverse=True)[:2]
    print(row['ID'],source['title'],' | '.join(best)[:1000])
