import collections, difflib, json, re, sys
from pathlib import Path
from urllib.parse import urlparse
from common import ROOT, HEADERS, CONFIG, KINDS

rows=[r for p in sorted(ROOT.glob('batch*.json')) for r in json.loads(p.read_text())]
rows.sort(key=lambda r:r['ID'])
errors=[]
checks={}
def check(name,condition,detail=''):
  checks[name]=bool(condition)
  if not condition: errors.append(name+(': '+detail if detail else ''))
norm=lambda s:re.sub(r'\s+',' ',s).strip().casefold()
counts=collections.Counter(r['Technology'] for r in rows)
check('Exactly 500 rows and target technology counts',len(rows)==500 and all(counts[c[1]]==c[2] for c in CONFIG.values()))
check('Technology sheet totals reconcile',sum(counts.values())==len(rows)==500)
check('Exact 15-column schema and order',all(list(r)==HEADERS for r in rows))
ids=[r['ID'] for r in rows]
check('Unique correctly prefixed sequential IDs',len(set(ids))==500 and all({r['ID'] for r in rows if r['Technology']==c[1]}=={f'{p}-{i:03d}' for i in range(1,c[2]+1)} for p,c in CONFIG.items()))
check('Unique normalized question text',len({norm(r['Question']) for r in rows})==500)
required=['ID','Technology','Topic','Subtopic','Difficulty','Question Type','Question','Correct Answer','Detailed Explanation','Hint 1','Hint 2','Source URL']
check('Required fields complete',all(all(r[k].strip() for k in required) for r in rows))
check('Allowed difficulty and question-type values',all(r['Difficulty'] in ['Beginner','Intermediate','Advanced'] and r['Question Type'] in KINDS.values() for r in rows))
mcqs=[]
for r in rows:
  if r['Question Type']!='MCQ': continue
  try:
    opts=json.loads(r['Options'])
    mcqs.append(isinstance(opts,list) and len(opts)==4 and [x['id'] for x in opts]==list('ABCD') and all(set(x)=={'id','text'} and isinstance(x['text'],str) and x['text'].strip() for x in opts) and len({norm(x['text']) for x in opts})==4 and r['Correct Answer'] in 'ABCD' and len(r['Correct Answer'])==1)
  except Exception: mcqs.append(False)
check('MCQ JSON, four distinct A–D options, valid answer',all(mcqs))
check('Non-MCQ Options are empty',all(not r['Options'] for r in rows if r['Question Type']!='MCQ'))
check('Output and trace fields are exact and complete',all(r['Code Snippet'] and r['Expected Output'] and r['Expected Output']==r['Correct Answer'] for r in rows if r['Question Type'] in ['Predict Output','Code Trace']))
check('Nonapplicable expected outputs are empty',all(not r['Expected Output'] for r in rows if r['Question Type'] not in ['Predict Output','Code Trace']))
domains={'developer.mozilla.org','react.dev','nextjs.org','www.typescriptlang.org','typescriptlang.org','web.dev','developer.chrome.com','tailwindcss.com','tc39.es','www.w3.org','w3.org','html.spec.whatwg.org','dom.spec.whatwg.org','fetch.spec.whatwg.org'}
check('HTTPS deep links on approved domains',all(urlparse(r['Source URL']).scheme=='https' and urlparse(r['Source URL']).hostname in domains and len(urlparse(r['Source URL']).path.strip('/').split('/'))>=1 and urlparse(r['Source URL']).path not in ('','/','/docs','/docs/') for r in rows))
matrix={}
mixok=True
for prefix,cfg in CONFIG.items():
  group=[r for r in rows if r['Technology']==cfg[1]]
  d=collections.Counter(r['Difficulty'] for r in group)
  matrix[cfg[0]]={k:d[k] for k in ['Beginner','Intermediate','Advanced']}
  mixok &= all(abs(d[k]/len(group)-target)<=.05000001 for k,target in [('Beginner',.25),('Intermediate',.45),('Advanced',.30)])
check('Difficulty mix within ±5 percentage points per technology',mixok)
check('At least six question types per technology',all(len({r['Question Type'] for r in rows if r['Technology']==c[1]})>=6 for c in CONFIG.values()))
def contains_code(snippet):
  return bool(re.sub(r'/\*.*?\*/|<!--.*?-->|//[^\n]*', '', snippet, flags=re.S).strip())
code_count=sum(contains_code(r['Code Snippet']) for r in rows)
check('At least 40 percent include code',code_count>=200)
check('Code coverage excludes comment-only prompts',all(contains_code(r['Code Snippet']) for r in rows if r['Code Snippet']))
followok=True
for r in rows:
  if r['Question Type']=='Follow-up':
    m=re.search(r'Follow-up to ([A-Z]+-\d{3}):',r['Question'])
    followok &= bool(m and m.group(1) in ids and m.group(1)!=r['ID'])
check('Every follow-up references an existing parent',followok)
check('All values are text and below 32000 characters',all(isinstance(v,str) and len(v)<32000 for r in rows for v in r.values()))
check('No placeholder values or Markdown fences',all(v not in ['N/A','None'] and '```' not in v for r in rows for v in r.values()))
bad_indent=[]
for r in rows:
  for line in r['Code Snippet'].splitlines():
    indent=len(line)-len(line.lstrip(' '))
    if '\t' in line or indent%2: bad_indent.append(r['ID'])
check('Raw code uses real line breaks and two-space indentation',not bad_indent,str(bad_indent))
check('Every code question has numbered explanation steps',all(r['Detailed Explanation'].startswith('1. ') and '\n2. ' in r['Detailed Explanation'] for r in rows if r['Code Snippet']))
manifest=json.loads((ROOT/'source_manifest.json').read_text())
sources={s['url']:s for s in manifest}
check('Every cited source retrieved successfully',all(sources.get(r['Source URL'].split('#')[0],{}).get('status')==200 for r in rows))
test=json.loads((ROOT/'output_tests.json').read_text())
check('Every output and trace example executed successfully',test['tested']==sum(r['Question Type'] in ['Predict Output','Code Trace'] for r in rows) and not test['failed'])

# Candidate review report, not an assertion that textual similarity proves duplication.
stop=set('the a an is are to of in and for with this that how what why does do should can it its on from as which when use using you your be by'.split())
tokens=[set(re.findall(r'[a-z0-9]+',r['Question'].lower()))-stop for r in rows]
candidates=[]
for i in range(len(rows)):
  for j in range(i+1,len(rows)):
    score=len(tokens[i]&tokens[j])/max(1,len(tokens[i]|tokens[j]))
    if score>.43: candidates.append((round(score,3),rows[i]['ID'],rows[j]['ID'],rows[i]['Question'],rows[j]['Question']))
candidates.sort(reverse=True)
(ROOT/'similarity_review.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=2))
(ROOT/'all_questions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
summary={'checks':checks,'total':len(rows),'counts':dict(counts),'difficulty':dict(collections.Counter(r['Difficulty'] for r in rows)),'matrix':matrix,'question_types':dict(collections.Counter(r['Question Type'] for r in rows)),'code_count':code_count,'code_percent':round(code_count/len(rows)*100,1),'output_examples_executed':test['tested'],'unique_sources':len({r['Source URL'].split('#')[0] for r in rows}),'similarity_candidates':len(candidates),'errors':errors}
(ROOT/'validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
