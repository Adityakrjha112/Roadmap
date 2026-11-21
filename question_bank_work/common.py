import json
from pathlib import Path

ROOT = Path(__file__).parent
HEADERS = ['ID','Technology','Topic','Subtopic','Difficulty','Question Type','Question','Code Snippet','Options','Correct Answer','Detailed Explanation','Hint 1','Hint 2','Expected Output','Source URL']
CONFIG = {
  'JS': ('JavaScript','JavaScript (Basic → Advanced)',150,38,67),
  'REACT': ('React','React.js & Hooks',100,25,45),
  'NEXT': ('NextJS','Next.js',65,16,29),
  'TS': ('TypeScript','TypeScript',45,11,20),
  'HCT': ('HTML_CSS_Tailwind','HTML, CSS, Tailwind',45,11,20),
  'DOM': ('DOM_Browser','DOM & Browser APIs',25,6,11),
  'ASYNC': ('Async_EventLoop','Async JavaScript & Event Loop',25,6,11),
  'PAS': ('Perf_A11y_SEO','Performance, Accessibility, SEO',25,6,11),
  'DBG': ('Debugging_Scenarios','Debugging & Real-World Scenarios',20,5,9)
}
KINDS = {'M':'MCQ','P':'Predict Output','T':'Code Trace','B':'Find the Bug','F':'Fix the Code','W':'Write Code','C':'Conceptual','S':'Scenario','A':'Architecture','U':'Follow-up'}
BASES = {'mdn':'https://developer.mozilla.org/en-US/docs/', 'react':'https://react.dev/', 'next':'https://nextjs.org/docs/', 'ts':'https://www.typescriptlang.org/docs/', 'tw':'https://tailwindcss.com/docs/', 'web':'https://web.dev/articles/', 'wai':'https://www.w3.org/WAI/ARIA/apg/patterns/'}

class Batch:
  def __init__(self,prefix,start):
    self.prefix,self.start,self.rows=prefix,start,[]
  def add(self,kind,topic,sub,q,a,e,h1,h2,src,code='',wrong=None):
    n=self.start+len(self.rows)
    cfg=CONFIG[self.prefix]
    diff='Beginner' if n<=cfg[3] else 'Intermediate' if n<=cfg[3]+cfg[4] else 'Advanced'
    url=src if src.startswith('https://') else BASES[src.split(':',1)[0]]+src.split(':',1)[1]
    opts=''
    if kind=='M':
      assert wrong and len(wrong)==3
      choices=list(wrong); position=(n-1)%4; choices.insert(position,a)
      opts=json.dumps([{'id':chr(65+i),'text':x} for i,x in enumerate(choices)],ensure_ascii=False,separators=(',',':'))
      a=chr(65+position)
    if '~' in e:
      e='\n'.join(f'{i+1}. {x.strip()}' for i,x in enumerate(e.split('~')))
    values=[f'{self.prefix}-{n:03d}',cfg[1],topic,sub,diff,KINDS[kind],q,code,opts,a,e,h1,h2,a if kind in ('P','T') else '',url]
    self.rows.append(dict(zip(HEADERS,values)))
  def save(self,name):
    (ROOT/(name+'.json')).write_text(json.dumps(self.rows,ensure_ascii=False,indent=2))
    print(name,len(self.rows),self.rows[0]['ID'],self.rows[-1]['ID'])
