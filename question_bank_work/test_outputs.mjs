import fs from 'node:fs';
import vm from 'node:vm';
import { format } from 'node:util';
import { performance } from 'node:perf_hooks';
const dir = new URL('.', import.meta.url);
const files = fs.readdirSync(dir).filter(x => /^batch.*\.json$/.test(x));
const rows = files.flatMap(file => JSON.parse(fs.readFileSync(new URL(file, dir), 'utf8')));
let tested=0; const failed=[];
for (const row of rows.filter(r => ['Predict Output','Code Trace'].includes(r['Question Type']))) {
  const logs=[];
  const timers=new Set();
  const context=vm.createContext({
    console:{log:(...args)=>logs.push(format(...args))},
    structuredClone, performance, URL, URLSearchParams, AbortController,
    setTimeout:(fn,ms)=>{const id=setTimeout(()=>{timers.delete(id);fn();},ms);timers.add(id);return id;},
    clearTimeout:id=>{clearTimeout(id);timers.delete(id);},queueMicrotask
  });
  try {
    vm.runInContext(row['Code Snippet'],context,{timeout:1000});
    await new Promise(resolve=>setTimeout(resolve,35));
    const actual=logs.join('\n');
    if(actual!==row['Expected Output']) failed.push({id:row.ID,expected:row['Expected Output'],actual});
    tested++;
  } catch(error) { failed.push({id:row.ID,error:String(error)}); }
  for(const timer of timers) clearTimeout(timer);
}
const result={tested,failed};
fs.writeFileSync(new URL('output_tests.json',dir),JSON.stringify(result,null,2));
console.log(JSON.stringify(result,null,2));
if(failed.length) process.exitCode=1;
