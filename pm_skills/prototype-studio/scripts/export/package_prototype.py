#!/usr/bin/env python3
"""Package an explicit runtime root; never rewrite business JavaScript.
Static analysis is conservative and does not prove all dynamic runtime paths.
"""
from __future__ import annotations
import argparse,hashlib,html,json,re,shutil,subprocess,sys,tempfile,zipfile
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote,unquote,urlsplit
PACKAGE=Path(__file__).resolve().parents[2]
IGNORE={'node_modules','__pycache__','.git','.cache','coverage','tests','test','scripts','work','outputs'}
SUFFIX={'.py','.pyc','.map','.zip','.log','.ts','.tsx','.jsx'}
EXT=r'(?:html?|css|m?js|json|md|png|jpe?g|webp|svg|gif|ico|woff2?|ttf|otf|mp[34]|wav|pdf)'
CSS=re.compile(r'url\(\s*[\'"]?([^\)\'"\s]+)[\'"]?\s*\)|@import\s+[\'"]([^\'"]+)[\'"]',re.I)

def js_views(text):
    """Skip JS comments; retain actual strings separately from executable tokens.
    Regex literals/template expressions are not a complete JS parser.
    """
    clean=[];code=[];strings=[];i=0
    while i<len(text):
        if text.startswith('//',i):
            j=text.find('\n',i);i=len(text) if j<0 else j;clean.append('\n');code.append('\n');continue
        if text.startswith('/*',i):
            j=text.find('*/',i+2);i=len(text) if j<0 else j+2;clean.append(' ');code.append(' ');continue
        if text[i] in "\"'`":
            q=text[i];j=i+1;value=[]
            while j<len(text):
                if text[j]=='\\' and j+1<len(text):value.extend((text[j],text[j+1]));j+=2;continue
                if text[j]==q:break
                value.append(text[j]);j+=1
            val=''.join(value);clean.append(text[i:j+1]);code.append(' STRING ')
            if q=='`' and '${' in val:code.append(' TEMPLATE_EXPRESSION ')
            strings.append(val);i=j+1;continue
        clean.append(text[i]);code.append(text[i]);i+=1
    return ''.join(clean),''.join(code),strings

class HTMLRefs(HTMLParser):
    def __init__(self):
        super().__init__();self.refs=[];self.modules=False;self.scripts=[];self.styles=[];self.script=False;self.style=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        self.refs.extend(a[k] for k in ('src','href','poster','data-src') if a.get(k))
        if a.get('srcset'):
            self.refs.extend(x.strip().split()[0] for x in a['srcset'].split(',') if x.strip())
        if a.get('style'):self.styles.append(a['style'])
        if tag=='script':self.script=True;self.modules|=a.get('type','').lower()=='module'
        if tag=='style':self.style=True
    def handle_endtag(self,tag):
        if tag=='script':self.script=False
        if tag=='style':self.style=False
    def handle_data(self,text):
        if self.script:self.scripts.append(text)
        if self.style:self.styles.append(text)

def inspect(root,mode):
    broken=set();risks=set();remote=set();dynamic=set()
    def check(doc,ref,js=False):
        value=html.unescape(ref.strip())
        if not value or value.startswith(('#','data:','blob:','mailto:','tel:','javascript:')):return
        u=urlsplit(value)
        if u.scheme or u.netloc:
            if u.scheme in ('http','https') or u.netloc:remote.add(value)
            else:risks.add(f'{doc.relative_to(root)}: absolute URL {value}')
            return
        path=unquote(u.path)
        if not path:return
        if '${' in path:dynamic.add(f'{doc.relative_to(root)}: constructed URL');return
        if path.startswith('/'):
            if mode=='direct':risks.add(f'{doc.relative_to(root)}: root-relative URL {value}');return
            target=(root/path.lstrip('/')).resolve()
        else:target=(doc.parent/path).resolve()
        if not target.is_relative_to(root):broken.add(f'{doc.relative_to(root)}: outside root {value}');return
        if not target.exists():
            # JS src/location values are document-relative; imports are file-relative.
            candidates=[p.parent/path for p in root.rglob('*.html')] if js else []
            if not any(p.resolve().is_relative_to(root) and p.exists() for p in candidates):broken.add(f'{doc.relative_to(root)}: {value}')
    def scan_js(doc,text):
        clean,code,strings=js_views(text)
        pattern=r'\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|Worker|SharedWorker|importScripts|eval)\s*\(|\bimport\s*(?:\(|\.|STRING|\{|\*)|\bimport\s+\w+\s+from\b|\bexport\s+(?:\{|\*).*?\bfrom\b|\bserviceWorker\b|\bpushState\s*\('
        if re.search(pattern,code,re.S):risks.add(f'{doc.relative_to(root)}: module/source-origin/network API; use server and verify dependencies')
        if 'TEMPLATE_EXPRESSION' in code:dynamic.add(f'{doc.relative_to(root)}: template expressions require runtime resource verification')
        for val in strings:
            if re.fullmatch(r'[^\s<>]*\.'+EXT+r'(?:[?#][^\s<>]*)?',val,re.I):check(doc,val,True)
        for value in strings:
            if 'url(' in value:
                for m in CSS.finditer(value):check(doc,m.group(1) or m.group(2),True)
    for doc in sorted(root.rglob('*')):
        if not doc.is_file() or doc.suffix.lower() not in {'.html','.htm','.css','.js','.mjs'}:continue
        text=doc.read_text(encoding='utf-8');suffix=doc.suffix.lower()
        if suffix in {'.html','.htm'}:
            p=HTMLRefs();p.feed(text)
            for ref in p.refs:check(doc,ref)
            if p.modules:risks.add(f'{doc.relative_to(root)}: module script requires a local origin')
            for s in p.scripts:scan_js(doc,s)
            for s in p.styles:
                for m in CSS.finditer(s):check(doc,m.group(1) or m.group(2))
        elif suffix=='.css':
            for m in CSS.finditer(re.sub(r'/\*.*?\*/','',text,flags=re.S)):check(doc,m.group(1) or m.group(2))
        else:scan_js(doc,text)
    return dict(brokenReferences=sorted(broken),runtimeRisks=sorted(risks),remoteResources=sorted(remote),dynamicUnverified=sorted(dynamic))

def source_checks(root):
    if not (root/'pages.json').exists():return []
    for f in ('pages.json','data.json','decisions.json'):
        if not (root/f).is_file():raise ValueError(f'Missing source contract: {f}')
    checks=[]
    for rel,args in [('scripts/sync/sync_review.py',['--project',str(root),'--check']),('scripts/check/check_project.py',['--project',str(root)])]:
        script=PACKAGE/rel
        if not script.is_file():raise ValueError(f'Required validator unavailable: {rel}')
        run=subprocess.run([sys.executable,str(script),*args],capture_output=True,text=True)
        if run.returncode:raise ValueError(f'{rel} rejected source:\n{run.stdout}\n{run.stderr}')
        checks.append(dict(validator=rel,exitCode=0))
    return checks

SERVER='''#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from functools import partial
import argparse
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765);a=p.parse_args()
server=ThreadingHTTPServer(('127.0.0.1',a.port),partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parent)))
print('Open http://127.0.0.1:%d/ENTRY' % server.server_address[1],flush=True)
try:server.serve_forever()
except KeyboardInterrupt:pass
finally:server.server_close()
'''

def package(source,output,entry='index.html',mode='direct',zip_path=None,title='原型'):
    source=Path(source).resolve();output=Path(output).resolve();zip_path=Path(zip_path).resolve() if zip_path else None
    if not source.is_dir():raise ValueError('Source directory does not exist')
    if output.exists():raise ValueError('Output exists; choose a new directory')
    if output==source or output.is_relative_to(source):raise ValueError('Output must be outside source')
    if zip_path and (zip_path.exists() or zip_path.is_relative_to(output) or zip_path.is_relative_to(source)):raise ValueError('ZIP must be new and outside source/output')
    u=urlsplit(entry);target=(source/unquote(u.path)).resolve()
    if u.scheme or u.netloc or u.path.startswith('/') or not target.is_relative_to(source) or not target.is_file() or target.suffix.lower() not in {'.html','.htm'}:raise ValueError('Entry must be an existing relative HTML file inside source')
    checks=source_checks(source);output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='prototype-package-',dir=output.parent) as temp:
        stage=Path(temp)/'bundle';stage.mkdir();files=[]
        for path in sorted(source.rglob('*')):
            rel=path.relative_to(source)
            if any(p.startswith('.') or p in IGNORE for p in rel.parts):continue
            if path.is_symlink():raise ValueError(f'Localize symlink before export: {rel}')
            if not path.is_file() or path.suffix.lower() in SUFFIX:continue
            out=stage/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,out);files.append(rel)
        if not (stage/unquote(u.path)).is_file():raise ValueError('Entry excluded by runtime filters')
        scan=inspect(stage,mode)
        if scan['brokenReferences']:raise ValueError('Broken references:\n'+'\n'.join(scan['brokenReferences']))
        if mode=='direct' and (scan['runtimeRisks'] or scan['remoteResources']):raise ValueError('Cannot certify direct-open package. Use --mode server or adapt runtime.\n'+'\n'.join(scan['runtimeRisks']+scan['remoteResources']))
        launcher=unquote(u.path)
        if entry!='index.html':
            launcher='__start__.html' if (stage/'index.html').exists() else 'index.html'
            if (stage/launcher).exists():raise ValueError('Reserved launcher exists: '+launcher)
            url=quote(u.path,safe='/%')+('?' + u.query if u.query else '')+('#'+quote(u.fragment) if u.fragment else '')
            safe=html.escape(url,quote=True)
            (stage/launcher).write_text(f'<!doctype html><meta charset="utf-8"><title>{html.escape(title)}</title><meta http-equiv="refresh" content="0;url={safe}"><a href="{safe}">打开原型</a>',encoding='utf-8')
        if mode=='server':(stage/'serve.py').write_text(SERVER.replace('ENTRY',quote(launcher,safe='/')),encoding='utf-8')
        groups=defaultdict(list);types=defaultdict(int);total=0
        for rel in files:
            blob=(stage/rel).read_bytes();total+=len(blob);types[rel.suffix.lower() or '(none)']+=len(blob);groups[hashlib.sha256(blob).hexdigest()].append(dict(path=rel.as_posix(),bytes=len(blob)))
        report=dict(schemaVersion=1,title=title,mode=mode,entry=entry,launcher=launcher,fileCount=len(files),runtimeBytes=total,bytesByType=dict(sorted(types.items())),duplicates=[v for v in groups.values() if len(v)>1],sourceChecks=checks,**scan,browserVerified=False,offlineVerified=False,staticAnalysisLimit='No JS AST/runtime execution. Constructed URLs, regex literals, document-base assumptions and backend behavior require browser verification.')
        (stage/'bundle-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        method=f'完整解压后双击 {launcher}。' if mode=='direct' else '完整解压，在本目录运行 python3 serve.py，然后访问终端提示的本机地址。'
        (stage/'打开说明.txt').write_text(title+'\n\n'+method+'\n原型目录和PRD均随包保留。\n静态检查不代替浏览器交互/断网验证，请查看bundle-manifest.json。\n本地服务器不提供业务后端或替代外部API。\n',encoding='utf-8')
        shutil.move(str(stage),str(output))
    if zip_path:
        zip_path.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(zip_path,'x',zipfile.ZIP_DEFLATED) as archive:
            for f in sorted(output.rglob('*')):
                if f.is_file():archive.write(f,Path(output.name)/f.relative_to(output))
        with zipfile.ZipFile(zip_path) as archive:
            if archive.testzip():raise RuntimeError('ZIP integrity failed')
        report['zipBytes']=zip_path.stat().st_size
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--entry',default='index.html');p.add_argument('--mode',choices=['direct','server'],default='direct');p.add_argument('--zip');p.add_argument('--title',default='原型');a=p.parse_args()
    try:print(json.dumps(package(a.source,a.output,a.entry,a.mode,a.zip,a.title),ensure_ascii=False,indent=2))
    except (ValueError,OSError,UnicodeError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
