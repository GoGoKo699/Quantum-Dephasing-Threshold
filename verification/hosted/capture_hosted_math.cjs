#!/usr/bin/env node
'use strict';
// Read-only collector for the real GitHub host. See ../references/hosted-rendering.md.
// Importing this module has no network effects; dependencies load only in run().
const fs = require('node:fs');
const path = require('node:path');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const VIEWPORTS = [{width:1440,height:1000}, {width:760,height:1000}];
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');

function argumentsFor(argv) {
  const args = {pages:[], python:'python3'};
  for (let i=0; i<argv.length; i++) {
    const key=argv[i];
    if (key==='--help') return {help:true};
    if (!['--root','--repository','--revision','--output','--page','--contract','--python'].includes(key) || !argv[i+1])
      throw new Error('Unknown option or missing value: '+key);
    const value=argv[++i];
    if (key==='--page') args.pages.push(value);
    else {
      const name=key.slice(2);
      if (Object.hasOwn(args,name) && name!=='python') throw new Error('Duplicate option: '+key);
      args[name]=value;
    }
  }
  for (const key of ['root','repository','revision','output']) if (!args[key]) throw new Error('Missing --'+key);
  if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(args.repository) ||
      args.repository.split('/').some(p=>['.','..'].includes(p))) throw new Error('Use exact owner/name');
  if (!/^[a-f0-9]{40}$/.test(args.revision)) throw new Error('Use a full lowercase commit SHA');
  if (new Set(args.pages).size!==args.pages.length || args.pages.some(p=>!safePath(p))) throw new Error('Use unique safe page paths');
  return args;
}
function safePath(p) {
  return typeof p==='string' && p.length>0 && !p.includes('\\') && !p.includes('\0') &&
    !p.startsWith('/') && p.split('/').every(x=>x && x!=='.' && x!=='..');
}
function git(root, argv) {
  return cp.execFileSync('git',['--no-replace-objects',...argv],{cwd:root,encoding:'utf8',maxBuffer:32*1024*1024});
}
function pinnedPages(args) {
  const commit=git(args.root,['rev-parse',args.revision+'^{commit}']).trim();
  if (commit!==args.revision) throw new Error('Revision does not identify the supplied commit');
  const files=git(args.root,['ls-tree','-r','--name-only','-z',commit]).split('\0').filter(Boolean);
  const pages=args.pages.length?args.pages:files.filter(p=>/\.(md|markdown|mdown|mkdn|mkd)$/i.test(p));
  if (!pages.length || pages.some(p=>!safePath(p) || !files.includes(p))) throw new Error('No pages or a page is absent from the pinned tree');
  // Git symlinks are not rendered Markdown source and must not be followed.
  for (const p of pages) {
    const item=git(args.root,['ls-tree',commit,'--',p]);
    if (!/^100644 blob |^100755 blob /.test(item)) throw new Error('Page must be a regular tracked file: '+p);
  }
  return {pages,tree:git(args.root,['rev-parse',commit+'^{tree}']).trim()};
}
function mathCompiler() {
  const {mathjax}=require('mathjax-full/js/mathjax.js');
  const {TeX}=require('mathjax-full/js/input/tex.js');
  const {SVG}=require('mathjax-full/js/output/svg.js');
  const {liteAdaptor}=require('mathjax-full/js/adaptors/liteAdaptor.js');
  const {RegisterHTMLHandler}=require('mathjax-full/js/handlers/html.js');
  const {AllPackages}=require('mathjax-full/js/input/tex/AllPackages.js');
  const {SerializedMmlVisitor}=require('mathjax-full/js/core/MmlTree/SerializedMmlVisitor.js');
  const {STATE}=require('mathjax-full/js/core/MathItem.js');
  RegisterHTMLHandler(liteAdaptor());
  const doc=mathjax.document('',{InputJax:new TeX({packages:AllPackages,tags:'none'}),OutputJax:new SVG({fontCache:'none'})});
  const visitor=new SerializedMmlVisitor();
  return (tex,display)=>visitor.visitTree(doc.convert(tex,{display,end:STATE.CONVERT}));
}

// Self-contained function executed inside the hosted page, also exercised by the
// local-browser regression fixture. It never injects styling or renders TeX there.
function inspectArticle(root, expected) {
  function canonical(e, inherited='') {
    const tag=e.localName;
    if (['annotation','annotation-xml','mspace'].includes(tag)) return [];
    const variant=e.getAttribute('mathvariant') || inherited;
    if (['mi','mo','mn','mtext','ms'].includes(tag)) {
      const text=e.textContent.trim();
      return text?[[tag,text,variant]]:[];
    }
    // Preserve each structural child slot: flattening numerator and denominator
    // together would confuse (a+b)/c with a/(b+c), and similarly for scripts.
    const children=[...e.children].filter(c=>!['annotation','annotation-xml','mspace'].includes(c.localName))
      .map(c=>canonical(c,variant));
    if (['math','mrow','mstyle','semantics'].includes(tag)) return children.flat();
    const semantic={};
    for (const name of ['notation','accent','accentunder','linethickness','bevelled','open','close','separators']) if(e.hasAttribute(name)) semantic[name]=e.getAttribute(name);
    // A table cell is an inferred row (a sequence), not a fixed-arity operator.
    // GitHub inserts empty mrow alignment nodes; ignore those inside the cell
    // while preserving the cell and row themselves, including empty cells.
    return [[tag,semantic,tag==='mtd'?children.flat():children]];
  }
  function plain(math) {
    const copy=math.cloneNode(true);
    for (const e of copy.querySelectorAll('annotation,annotation-xml')) e.remove();
    return copy.textContent;
  }
  function geometry(math, host) {
    const boxes=[...math.querySelectorAll('mi,mo,mn,mtext,ms')].map(e=>e.getBoundingClientRect()).filter(b=>b.width && b.height);
    if (!boxes.length) return {measurable:false};
    const left=Math.min(...boxes.map(b=>b.left)),right=Math.max(...boxes.map(b=>b.right));
    const top=Math.min(...boxes.map(b=>b.top)),bottom=Math.max(...boxes.map(b=>b.bottom));
    const width=right-left,height=bottom-top;
    return {measurable:true,width,height,available_width:root.clientWidth,
      overflow:width>root.clientWidth+4,collapsed:height>Math.max(200,3*width),host_width:host.getBoundingClientRect().width};
  }
  let hosts=[...root.querySelectorAll('math-renderer')];
  // Some host versions expose native MathML without a custom-element wrapper.
  if (!hosts.length) hosts=[...root.querySelectorAll('math')].filter(e=>!e.parentElement?.closest('math,annotation,annotation-xml'));
  const pageErrors=[...root.querySelectorAll('merror,[data-mjx-error],.katex-error,math-renderer .flash-error')]
    .map(e=>e.textContent.trim() || 'empty renderer error');
  const math=hosts.map((host,i)=>{
    const nodes=host.localName==='math'?[host]:[...host.querySelectorAll('math')].filter(e=>!e.parentElement?.closest('math,annotation,annotation-xml'));
    const errors=[];
    if(nodes.length!==1) errors.push('Expected one accessible MathML representation; found '+nodes.length);
    const actual=nodes[0],want=expected[i];
    let expectedSignature=null,actualSignature=null;
    if(actual) actualSignature=JSON.stringify(canonical(actual));
    if(want) {
      const parsed=new DOMParser().parseFromString(want.mml,'application/xml');
      if(parsed.querySelector('parsererror,merror')) errors.push('Source compiler returned invalid/error MathML');
      else expectedSignature=JSON.stringify(canonical(parsed.documentElement));
    }
    if(!want) errors.push('Unexpected extra hosted expression');
    const match=!!actual && !!expectedSignature && expectedSignature===actualSignature;
    if(!match) errors.push('Source-to-host MathML structure mismatch');
    const measure=actual?geometry(actual,host):{measurable:false};
    if(want && ['math-fence','dollar-display'].includes(want.kind) && (!measure.measurable || measure.overflow || measure.collapsed))
      errors.push('Display geometry is unmeasurable, overflowing or collapsed');
    return {rendered:!!actual,errors,text_source:'mathml',text:actual?plain(actual):'',
      source_sha256:want?.source_sha256,structural_match:match,
      expected_signature:expectedSignature,actual_signature:actualSignature,geometry:measure};
  });
  return {errors:pageErrors,math};
}

function classifyFailure(error) {
  const message=String(error);
  if (/ERR_BLOCKED_BY_ADMINISTRATOR|blocked by.*policy|URLBlocklist|policy denied/i.test(message)) return 'policy_denied';
  if (/HTTP (401|403)|redirected away|sign.in|authentication/i.test(message)) return 'access_required';
  if (/Cannot find module|Executable doesn't exist|browser executable/i.test(message)) return 'capability_unavailable';
  if (/ERR_NAME_NOT_RESOLVED|ENOTFOUND|ERR_CONNECTION|ERR_EMPTY_RESPONSE|ERR_INTERNET_DISCONNECTED|ECONNRESET|Timeout|timed out/i.test(message)) return 'transport_failure';
  return 'verification_failure';
}
function writeJSON(filename, value) {fs.writeFileSync(filename,JSON.stringify(value,null,2)+'\n');}
function artifact(directory, relative, kind) {
  const bytes=fs.readFileSync(path.join(directory,relative));
  return {path:relative,sha256:sha256(bytes),size_bytes:bytes.length,kind};
}
function boundReport(inventory, tree, viewports, artifacts, failures, at) {
  const boundaries=inventory.pages.map(p=>{
    const counts=viewports.map(v=>v.boundaries?.find(b=>b.path===p.path)?.captured_hosts);
    return {path:p.path,url:p.url,revision:inventory.revision,source_sha256:p.source_sha256,
      source_expressions:p.expressions.length,
      captured_hosts:counts.length===VIEWPORTS.length && counts.every(n=>Number.isInteger(n) && n===counts[0])?counts[0]:null};
  });
  const wanted=inventory.pages.reduce((n,p)=>n+p.expressions.length,0);
  failures=[...failures];
  if(JSON.stringify(viewports.map(v=>({width:v.width,height:v.height})))!==JSON.stringify(VIEWPORTS))
    failures.push('Missing, duplicate or unexpected viewport coverage');
  for(const viewport of viewports) {
    if(JSON.stringify((viewport.boundaries||[]).map(b=>b.path))!==JSON.stringify(inventory.pages.map(p=>p.path)))
      failures.push(viewport.width+': page coverage differs from inventory');
    for(const source of inventory.pages) {
      const boundary=viewport.boundaries?.find(b=>b.path===source.path);
      if(!boundary || boundary.source_sha256!==source.source_sha256 || boundary.revision!==inventory.revision ||
         boundary.url!==source.url || boundary.source_expressions!==source.expressions.length || boundary.captured_hosts!==source.expressions.length)
        failures.push(viewport.width+': incomplete source/host coverage for '+source.path);
    }
  }
  const structural=viewports.length===VIEWPORTS.length && viewports.every(v=>v.structural_matches===wanted);
  const pass=!failures.length && structural && viewports.length===VIEWPORTS.length && viewports.every(v=>v.status==='pass');
  return {schema_version:1,kind:'hosted_math',repository:inventory.repository,revision:inventory.revision,tree,
    renderer_profile:'github',captured_at:at,capture_method:'playwright-github',status:pass?'pass':'fail',
    required_pages:inventory.pages.map(p=>p.path),boundaries,viewports,artifacts,failures,
    structural_comparison:{status:structural?'pass':'fail',expressions_checked:structural?wanted:0},
    visual_review_required:true,
    limits:'Observed GitHub MathML structure, counts, labels, relations and bounded geometry only. No independent scientific proof, exhaustive pixel review, host authenticity certificate or cross-browser guarantee.'};
}

async function run(args) {
  const output=path.resolve(args.output);
  if(fs.existsSync(output) && fs.readdirSync(output).length) throw new Error('Use an empty output directory; preserve earlier failed evidence');
  fs.mkdirSync(output,{recursive:true});
  const pinned=pinnedPages(args);
  const helper=path.join(__dirname,'check_rendered_math.py');
  cp.execFileSync(args.python,[helper,'inventory','--root',args.root,'--repository',args.repository,
    '--revision',args.revision,...pinned.pages.flatMap(p=>['--page',p]),'--output',path.join(output,'math-source.json')],{stdio:'pipe'});
  const inventory=JSON.parse(fs.readFileSync(path.join(output,'math-source.json'),'utf8'));
  const at=new Date().toISOString(),failures=[],artifacts=[artifact(output,'math-source.json','source_inventory')],viewports=[];
  let browser;
  const runtime={node:process.version};
  if(args.contract) {
    fs.copyFileSync(path.resolve(args.contract),path.join(output,'math-contract.json'));
    artifacts.push(artifact(output,'math-contract.json','text_contract'));
  }
  try {
    const {chromium}=require('playwright');
    runtime.playwright=require('playwright/package.json').version;
    runtime.mathjax=require('mathjax-full/package.json').version;
    const compile=mathCompiler();
    const expected=Object.fromEntries(inventory.pages.map(p=>[p.path,p.expressions.map(e=>({...e,
      mml:compile(e.tex,['math-fence','dollar-display'].includes(e.kind))}))]));
    writeJSON(path.join(output,'expected-mathml.json'),expected);
    artifacts.push(artifact(output,'expected-mathml.json','expected_mathml'));
    browser=await chromium.launch({headless:true});
    runtime.browser=browser.version();
    for(const viewport of VIEWPORTS) {
      const context=await browser.newContext({viewport,deviceScaleFactor:1,colorScheme:'light'});
      const capture={schema_version:1,repository:args.repository,revision:args.revision,renderer_profile:'github',
        captured_at:at,capture_method:'playwright-github',pages:[]};
      let fatal=false;
      try {
        for(let index=0;index<inventory.pages.length;index++) {
          const source=inventory.pages[index],page=await context.newPage();
          const prefix=String(index+1).padStart(4,'0')+'-'+viewport.width;
          const item={path:source.path,url:source.url,revision:args.revision,source_sha256:source.source_sha256,errors:[],math:[]};
          try {
            const response=await page.goto(source.url,{waitUntil:'domcontentloaded',timeout:60000});
            if(response?.status()!==200) throw new Error('HTTP '+response?.status());
            if(page.url()!==source.url) throw new Error('Browser redirected away from exact pinned source URL');
            const article=page.locator('article.markdown-body').first();
            await article.waitFor({state:'visible',timeout:30000});
            await page.evaluate(async()=>{
              for(let y=0,steps=0;y<document.body.scrollHeight && steps<200;y+=900,steps++) {
                window.scrollTo(0,y);await new Promise(r=>setTimeout(r,50));
              }
              window.scrollTo(0,0);
            });
            await page.waitForTimeout(1000);
            Object.assign(item,await article.evaluate(inspectArticle,expected[source.path]));
            const html=prefix+'.html',png=prefix+'.png';
            fs.writeFileSync(path.join(output,html),await page.content());
            await page.screenshot({path:path.join(output,png),fullPage:true,timeout:30000});
            artifacts.push(artifact(output,html,'hosted_html'),artifact(output,png,'screenshot'));
            item.artifacts={html,screenshot:png};
          } catch(error) {
            item.errors.push(String(error));
            const category=classifyFailure(error);
            failures.push(source.path+' at '+viewport.width+': '+category+': '+String(error));
            // Do not seek another route after an access or policy block.
            fatal=['policy_denied','access_required','transport_failure'].includes(category);
          } finally {capture.pages.push(item);await page.close();}
          if(fatal) break;
        }
      } finally {await context.close();}
      const captureFile='math-capture-'+viewport.width+'.json',resultFile='math-result-'+viewport.width+'.json';
      writeJSON(path.join(output,captureFile),capture);artifacts.push(artifact(output,captureFile,'hosted_capture'));
      const command=[helper,'check','--inventory',path.join(output,'math-source.json'),'--capture',path.join(output,captureFile),
        '--output',path.join(output,resultFile)];
      if(args.contract) command.push('--contract',path.resolve(args.contract));
      const check=cp.spawnSync(args.python,command,{encoding:'utf8'});
      if(check.error || !fs.existsSync(path.join(output,resultFile))) throw new Error('Math checker did not produce a result: '+(check.error||check.stderr));
      const result=JSON.parse(fs.readFileSync(path.join(output,resultFile),'utf8'));
      artifacts.push(artifact(output,resultFile,'math_result'));
      failures.push(...result.failures.map(f=>viewport.width+': '+f));
      const matches=capture.pages.reduce((n,p)=>n+p.math.filter(m=>m.structural_match && !m.errors.length).length,0);
      viewports.push({...viewport,status:result.status,structural_matches:matches,capture_path:captureFile,result_path:resultFile,boundaries:result.boundaries});
      if(fatal) break;
    }
  } catch(error) {failures.push(classifyFailure(error)+': '+String(error));}
  finally {if(browser) await browser.close();}
  const report={...boundReport(inventory,pinned.tree,viewports,artifacts,failures,at),runtime};
  writeJSON(path.join(output,'hosted-report.json'),report);
  console.log(JSON.stringify({status:report.status,report:path.join(output,'hosted-report.json'),sha256:sha256(fs.readFileSync(path.join(output,'hosted-report.json'))),pages:report.required_pages.length,failures:report.failures.length}));
  return report.status==='pass'?0:1;
}
module.exports={argumentsFor,safePath,pinnedPages,mathCompiler,inspectArticle,classifyFailure,artifact,boundReport,VIEWPORTS,run};
if(require.main===module) {
  (async()=>{
    const args=argumentsFor(process.argv.slice(2));
    if(args.help) {console.log('capture_hosted_math.cjs --root REPO --repository owner/name --revision FULLSHA --output EMPTY_DIR [--page PATH ...] [--contract JSON] [--python python3]');return;}
    process.exitCode=await run(args);
  })().catch(error=>{console.error(String(error));process.exitCode=2;});
}
