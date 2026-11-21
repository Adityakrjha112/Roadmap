import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root=path.dirname(fileURLToPath(import.meta.url));
const outputDir=path.join(root,'..','outputs','frontend-interview-bank');
await fs.mkdir(outputDir,{recursive:true});
await fs.mkdir(path.join(root,'previews'),{recursive:true});
const rows=JSON.parse(await fs.readFile(path.join(root,'all_questions.json'),'utf8'));
const validation=JSON.parse(await fs.readFile(path.join(root,'validation.json'),'utf8'));
if(validation.errors.length) throw new Error('Data validation must pass before export.');
const headers=Object.keys(rows[0]);
const configs=[
  ['JavaScript','JavaScript (Basic → Advanced)'],['React','React.js & Hooks'],['NextJS','Next.js'],
  ['TypeScript','TypeScript'],['HTML_CSS_Tailwind','HTML, CSS, Tailwind'],['DOM_Browser','DOM & Browser APIs'],
  ['Async_EventLoop','Async JavaScript & Event Loop'],['Perf_A11y_SEO','Performance, Accessibility, SEO'],
  ['Debugging_Scenarios','Debugging & Real-World Scenarios']
];
const safe=value=>/^[=+\-@]/.test(String(value))?"'"+value:String(value);
const wb=Workbook.create();
const overview=wb.worksheets.add('Overview');
const schema=wb.worksheets.add('Schema');
const all=wb.worksheets.add('All_Questions');
const sheets=configs.map(([name,technology])=>({sheet:wb.worksheets.add(name),technology}));
const navy='#17324D', ink='#182B3A', line='#DCE5EC';
function styleHeader(sheet,range){
  sheet.getRange(range).format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',horizontalAlignment:'left',rowHeight:30};
}
function initialize(sheet,range){
  sheet.showGridLines=false;
  sheet.getRange(range).format={font:{name:'Arial',size:10,color:ink},numberFormat:'@',verticalAlignment:'top',wrapText:true};
  sheet.freezePanes.freezeRows(1);
}
const widths=[15,32,24,30,18,21,66,78,62,92,96,38,42,45,78];
function estimatedLines(text,width,mono){
  const capacity=Math.max(6,Math.floor((width-3)*(mono?1.05:1.28)));
  return text.split('\n').reduce((n,line)=>n+Math.max(1,Math.ceil(line.length/capacity)),0);
}
function dataSheet(sheet,data){
  const matrix=[headers,...data.map(r=>headers.map(h=>safe(r[h])))];
  const last=data.length+1;
  initialize(sheet,`A1:O${last}`);
  sheet.getRange(`A1:O${last}`).values=matrix;
  for(let i=0;i<15;i++) sheet.getRangeByIndexes(0,i,last,1).format.columnWidth=widths[i];
  for(const col of ['H','J','N']) sheet.getRange(`${col}2:${col}${last}`).format.font={name:'Consolas',size:10,color:ink};
  const table=sheet.tables.add(`A1:O${last}`,true,`${sheet.name.replaceAll('_','')}Data`);
  table.showFilterButton=true;
  for(let i=0;i<data.length;i++){
    const r=data[i];
    const lines=Math.max(...headers.map((h,j)=>estimatedLines(r[h],widths[j],[7,9,13].includes(j))));
    const range=sheet.getRangeByIndexes(i+1,0,1,15);
    range.format.rowHeight=Math.min(405,Math.max(92,lines*13+12));
    if(i%2===1) range.format.fill='#F3F6F9';
  }
  styleHeader(sheet,'A1:O1');
  sheet.getRange(`A2:A${last}`).format.font={name:'Arial',size:10,bold:true,color:navy};
  sheet.freezePanes.freezeColumns(1);
}
dataSheet(all,rows);
for(const {sheet,technology} of sheets) dataSheet(sheet,rows.filter(r=>r.Technology===technology));

const schemaHeaders=['Column Name','Data Type','Required (Yes/Conditional)','Description','Allowed Values / Format','Example'];
const descriptions={
  ID:['Yes','Stable unique question identifier.','PREFIX-000; JS, REACT, NEXT, TS, HCT, DOM, ASYNC, PAS, DBG'],
  Technology:['Yes','Technology label used for sheet membership and filtering.','Exact labels listed in Overview'],
  Topic:['Yes','Broad subject grouping within the technology.','Nonempty text'],
  Subtopic:['Yes','Specific behavior or reasoning skill assessed.','Nonempty text'],
  Difficulty:['Yes','Calibrated for developers with 2–5 years of experience.','Beginner; Intermediate; Advanced'],
  'Question Type':['Yes','Question interaction and answer contract.','MCQ; Predict Output; Code Trace; Find the Bug; Fix the Code; Write Code; Conceptual; Scenario; Architecture; Follow-up'],
  Question:['Yes','Interview prompt with assumptions; Follow-up includes its parent ID.','Plain text; Follow-up to PREFIX-000: ...'],
  'Code Snippet':['Conditional','Prompt code or relevant configuration. Empty when not applicable.','Raw code, real line breaks, 2-space indentation; no Markdown fences'],
  Options:['Conditional','Required only for MCQ. Empty for every other type.','JSON array of exactly 4 objects with id A, B, C, D and text'],
  'Correct Answer':['Yes','MCQ letter, exact output, corrected bug lines, working solution, or concise model answer according to type.','MCQ: A–D; output/trace: exact output; other types: text or raw code'],
  'Detailed Explanation':['Yes','Reasoning, common incorrect interpretations and relevant edge cases; numbered steps for code.','Plain text with real line breaks'],
  'Hint 1':['Yes','Gentle conceptual guidance without the full answer.','Nonempty text'],
  'Hint 2':['Yes','More specific guidance without the full answer.','Nonempty text'],
  'Expected Output':['Conditional','Required only for Predict Output and Code Trace. Empty otherwise.','Exact console text, one line per log, matching Correct Answer'],
  'Source URL':['Yes','One approved documentation page supporting the answer.','Single https:// deep link; approved domain']
};
const example=rows.find(r=>r.ID==='JS-039');
const mcq=rows.find(r=>r.ID==='JS-002');
const schemaData=headers.map(h=>[h,'Text',descriptions[h][0],descriptions[h][1],descriptions[h][2],h==='Options'?mcq.Options:example[h]]);
initialize(schema,'A1:F16');
schema.getRange('A1:F16').values=[schemaHeaders,...schemaData.map(r=>r.map(safe))];
const sw=[27,14,27,80,85,90];
sw.forEach((w,i)=>schema.getRangeByIndexes(0,i,16,1).format.columnWidth=w);
schema.getRange('A2:F16').format.rowHeight=112;
styleHeader(schema,'A1:F1');
const schemaTable=schema.tables.add('A1:F16',true,'SchemaDefinitions');schemaTable.showFilterButton=true;

initialize(overview,'A1:J42');
const ow=[49,15,16,16,16,30,14,3,30,14];
ow.forEach((w,i)=>overview.getRangeByIndexes(0,i,42,1).format.columnWidth=w);
overview.getRange('A1').values=[['Frontend interview question bank']];
overview.getRange('A1:J1').format.font={name:'Arial',size:14,bold:true,color:navy};
overview.getRange('A1:J1').format.rowHeight=28;
overview.getRange('A3:B5').values=[['Total unique questions',String(rows.length)],['Questions containing code',String(validation.code_count)],['Code coverage',`${validation.code_percent}%`]];
overview.getRange('A3:B3').format.font={name:'Arial',size:12,bold:true,color:navy};
overview.getRange('F3:G5').values=[['Target experience','2–5 years'],['Output examples executed',String(validation.output_examples_executed)],['Source pages checked',String(validation.unique_sources)]];
overview.getRange('A7:B16').values=[['Technology','Count'],...configs.map(([,t])=>[t,String(rows.filter(r=>r.Technology===t).length)])];
overview.getRange('F7:G10').values=[['Difficulty','Count'],...['Beginner','Intermediate','Advanced'].map(d=>[d,String(rows.filter(r=>r.Difficulty===d).length)])];
const types=['MCQ','Predict Output','Code Trace','Find the Bug','Fix the Code','Write Code','Conceptual','Scenario','Architecture','Follow-up'];
overview.getRange('I7:J17').values=[['Question Type','Count'],...types.map(t=>[t,String(rows.filter(r=>r['Question Type']===t).length)])];
for(const range of ['A7:B7','F7:G7','I7:J7']) styleHeader(overview,range);
overview.getRange('A8:J17').format.rowHeight=31;
overview.getRange('A20:E30').values=[['Technology','Beginner','Intermediate','Advanced','Total'],...configs.map(([,t])=>[t,...['Beginner','Intermediate','Advanced'].map(d=>String(rows.filter(r=>r.Technology===t&&r.Difficulty===d).length)),String(rows.filter(r=>r.Technology===t).length)]),['Grand total',...['Beginner','Intermediate','Advanced'].map(d=>String(rows.filter(r=>r.Difficulty===d).length)),String(rows.length)]];
styleHeader(overview,'A20:E20');
overview.getRange('A21:E30').format.rowHeight=32;
overview.getRange('A30:E30').format={fill:'#E6EEF5',font:{name:'Arial',size:10,bold:true,color:navy}};
overview.getRange('F20:J20').values=[['Version scope','','','','']];styleHeader(overview,'F20:J20');
const versionRows=[
  ['ECMAScript','ES2024+; standardized features. ES2026 published.','https://tc39.es/ecma262/2026/'],
  ['React','19.3 stable','https://react.dev/versions'],
  ['Next.js','16.4.5 App Router; cache model stated per question.','https://nextjs.org/docs/app/getting-started/caching'],
  ['TypeScript','5.9-compatible; 6.0 is the newer stable line.','https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html'],
  ['Tailwind CSS','4.3 (v4 CSS-first model)','https://tailwindcss.com/blog/tailwindcss-v4-3'],
  ['Browser assumptions','Current evergreen; deterministic output examples.',''],
  ['Verification date','2026-11-08 (research started 2026-11-07).','']
];
for(let i=0;i<versionRows.length;i++){
  const n=21+i*2;
  overview.getRange(`F${n}`).values=[[versionRows[i][0]]];
  overview.getRange(`G${n}`).values=[[versionRows[i][1]]];overview.getRange(`G${n}`).format.wrapText=false;
  overview.getRange(`F${n}:J${n}`).format.rowHeight=35;
  if(versionRows[i][2]){overview.getRange(`F${n+1}`).values=[[versionRows[i][2]]];overview.getRange(`F${n+1}:J${n+1}`).format={font:{name:'Arial',size:9,color:'#466078'},rowHeight:28,wrapText:false};}
}
const notes=[
  ['Computed counts','All totals, counts and the matrix are computed from the question records at export. They are stored as text to honor the import specification.'],
  ['Code assumptions','JavaScript snippets use modern Node.js or browser APIs as stated. React snippets use function components. TypeScript examples assume strict checking and a .tsx file for JSX.'],
  ['Import handling','Every cell is text. A leading apostrophe protects values beginning with =, +, - or @. If an importer retains that escape, remove exactly that protective prefix. Empty cells mean not applicable.'],
  ['Source review','Each row cites one retrieved approved documentation page. Output/trace snippets were executed; reference solutions and version-sensitive behavior were reviewed against their sources.']
];
for(let i=0;i<notes.length;i++){
  const n=36+i*2;
  overview.getRange(`A${n}`).values=[[notes[i][0]]];
  overview.getRange(`B${n}`).values=[[notes[i][1]]];overview.getRange(`B${n}`).format.wrapText=false;
  overview.getRange(`A${n}:J${n}`).format.rowHeight=34;
}
overview.tabColor=navy;all.tabColor='#486F90';schema.tabColor='#A7B8C8';
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Overview!A3:B16',include:'values,formulas',tableMaxRows:14,tableMaxCols:2,maxChars:2200})).ndjson);
const output=await SpreadsheetFile.exportXlsx(wb);
const outputPath=path.join(outputDir,'frontend_interview_question_bank.xlsx');
await output.save(outputPath);
console.log('EXPORTED '+outputPath);
const renderRanges=[['Overview','A1:J34'],['Schema','A1:F3'],...['All_Questions',...configs.map(c=>c[0])].map(n=>[n,'G1:K3'])];
for(const [sheetName,range] of renderRanges){
  const preview=await wb.render({sheetName,range,scale:1,format:'png'});
  await fs.writeFile(path.join(root,'previews',sheetName+'.png'),new Uint8Array(await preview.arrayBuffer()));
  console.log('RENDERED '+sheetName);
}
await fs.writeFile(path.join(root,'build_output.json'),JSON.stringify({outputPath,sheets:['Overview','Schema','All_Questions',...configs.map(c=>c[0])]},null,2));
