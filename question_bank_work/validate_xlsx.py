import collections, json, re, zipfile
from pathlib import Path
import openpyxl
from common import ROOT, HEADERS, CONFIG

file=ROOT.parent/'outputs/frontend-interview-bank/frontend_interview_question_bank.xlsx'
rows=json.loads((ROOT/'all_questions.json').read_text())
summary=json.loads((ROOT/'validation.json').read_text())
w=openpyxl.load_workbook(file,data_only=False)
checks={}
def check(name,condition):
  checks[name]=bool(condition)
  assert condition,name
safe=lambda v:"'"+v if v.startswith(('=','+','-','@')) else v
expected_names=['Overview','Schema','All_Questions']+[c[0] for c in CONFIG.values()]
check('Exact 12-sheet structure and order',w.sheetnames==expected_names)
for name,data in [('All_Questions',rows)]+[(c[0],[r for r in rows if r['Technology']==c[1]]) for c in CONFIG.values()]:
  s=w[name]
  check(name+' exact dimensions',s.max_row==len(data)+1 and s.max_column==15)
  check(name+' exact headers',[c.value for c in s[1]]==HEADERS)
  actual=[[c.value if c.value is not None else '' for c in row] for row in s.iter_rows(min_row=2)]
  check(name+' exact data',actual==[[safe(r[h]) for h in HEADERS] for r in data])
  check(name+' frozen header',s.freeze_panes in ('A2','B2'))
  check(name+' filter',bool(s.auto_filter.ref or any(t.autoFilter is not None and t.autoFilter.ref==f'A1:O{len(data)+1}' for t in s.tables.values())))
  check(name+' bold headers',all(c.font.bold for c in s[1]))
  check(name+' wrapped text',all(c.alignment.wrap_text for row in s for c in row))
  check(name+' monospace code and answers',all(s.cell(i,j).font.name=='Consolas' for i in range(2,s.max_row+1) for j in (8,10,14)))
  check(name+' cells under limit',all(c.value is None or len(str(c.value))<32000 for row in s for c in row))
check('All populated cells stored as text, no formulas',all(c.data_type=='s' for s in w for row in s for c in row if c.value is not None))
check('Formula-like values safely prefixed',all(not c.value.startswith(('=','+','-','@')) for s in w for row in s for c in row if isinstance(c.value,str)))
check('All_Questions sorted by ID',[w['All_Questions'].cell(i,1).value for i in range(2,502)]==sorted(r['ID'] for r in rows))
o=w['Overview']
check('Overview grand totals are 500',o['B3'].value=='500' and o['E30'].value=='500')
check('Overview technology counts computed correctly',all(o.cell(i+8,1).value==c[1] and o.cell(i+8,2).value==str(c[2]) for i,c in enumerate(CONFIG.values())))
for i,c in enumerate(CONFIG.values()):
  group=[r for r in rows if r['Technology']==c[1]]
  check(c[0]+' Overview difficulty matrix',all(o.cell(i+21,j+2).value==str(sum(r['Difficulty']==d for r in group)) for j,d in enumerate(['Beginner','Intermediate','Advanced'])))
check('Schema has one row per field',[w['Schema'].cell(i,1).value for i in range(2,17)]==HEADERS)
with zipfile.ZipFile(file) as z:
  check('Valid ZIP container',z.testzip() is None)
result={'file':str(file),'bytes':file.stat().st_size,'checks_passed':len(checks),'checks':checks,'data_validation':summary['checks']}
(ROOT/'xlsx_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'file':str(file),'bytes':file.stat().st_size,'checks_passed':len(checks),'data_checks_passed':len(summary['checks']),'status':'PASS'},indent=2))
