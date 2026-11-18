"""medir.py — uso real de la memoria nativa de Claude Code, solo lectura.

Lee las transcripciones locales (~/.claude/projects/*/*.jsonl) y las carpetas de
memoria (~/.claude/projects/*/memory/) y calcula, sin modificar nada:
  - sesiones y llamadas que leen memoria de OTRO proyecto (lectura cruzada)
  - tokens de contexto al arrancar y máximo por sesión
  - tamaño de cada índice MEMORY.md contra el tope de 200 líneas / 25 KB
  - memorias abiertas al menos una vez; enlaces [[ ]] propios, cruzados y rotos
Los nombres de proyecto se anonimizan en la salida (proyecto-01, ...).

Uso:  python3 medir.py salida.json
Solo biblioteca estándar. No llama a ningún modelo ni requiere API key.
"""
import json,re,glob,os,collections,statistics as st,sys
PREFIX='-'+os.path.expanduser('~').strip('/').replace('/','-')+'-' 
R=os.path.expanduser('~/.claude/projects')
memre=re.compile(r'projects/(-Users-[^/"\s\\\']+)/memory(?:/([\w\-.]+\.md))?')
proj={}  # per project stats
memfiles={}  # (proj,basename)->set(sessions reading)
for d in glob.glob(R+'/*/memory'):
    P=d.split('/')[-2]
    for f in glob.glob(d+'/*.md'):
        if not f.endswith('MEMORY.md'): memfiles[(P,os.path.basename(f))]=set()
bynames=collections.defaultdict(list)
for (P,b) in memfiles: bynames[b].append(P)
S=[]
for f in glob.glob(R+'/*/*.jsonl'):
    P=f.split('/')[-2]; sid=os.path.basename(f)[:8]
    s=dict(p=P,calls=0,own=0,cross=0,hunt=0,start=None,models=collections.Counter(),crossproj=set(),first_ts=None,peak=0,out=0,turns=0)
    try: fh=open(f,errors='ignore')
    except: continue
    for l in fh:
        if '"assistant"' not in l: continue
        try:d=json.loads(l)
        except:continue
        if d.get('type')!='assistant' or d.get('isSidechain'):continue
        m=d.get('message',{}); u=m.get('usage') or {}
        ctx=(u.get('input_tokens') or 0)+(u.get('cache_read_input_tokens') or 0)+(u.get('cache_creation_input_tokens') or 0)
        if ctx:
            if s['start'] is None: s['start']=ctx; s['first_ts']=d.get('timestamp')
            s['peak']=max(s['peak'],ctx)
        s['out']+=u.get('output_tokens') or 0
        if m.get('model') and not m['model'].startswith('<'): s['models'][m['model']]+=1
        for x in m.get('content',[]) or []:
            if x.get('type')!='tool_use':continue
            s['calls']+=1
            inp=json.dumps(x.get('input',{}),ensure_ascii=False)
            write=x['name'] in('Write','Edit')
            hits=memre.findall(inp)
            if '.claude/projects' in inp and re.search(r'\b(for |find |ls |grep )',inp) and x['name']=='Bash': s['hunt']+=1
            seen=set()
            for Q,b in hits:
                if Q==P: seen.add('own')
                else: seen.add('cross'); s['crossproj'].add(Q)
                if b and not write and (Q,b) in memfiles: memfiles[(Q,b)].add(sid)
            if 'own' in seen: s['own']+=1
            if 'cross' in seen: s['cross']+=1
            # bare names read inside own memory dir via cd
            if not write and 'memory' in inp:
                for b in re.findall(r'([\w\-]+\.md)',inp):
                    if (P,b) in memfiles: memfiles[(P,b)].add(sid)
    if s['calls'] or s['start']: S.append(s)
def med(a): return round(st.median(a)) if a else None
out={}
out['sessions']=len(S)
out['sessions_with_cross']=sum(1 for s in S if s['cross'])
out['sessions_with_own_mem_access']=sum(1 for s in S if s['own'])
out['total_calls']=sum(s['calls'] for s in S)
out['cross_calls']=sum(s['cross'] for s in S); out['own_calls']=sum(s['own'] for s in S); out['hunt_calls']=sum(s['hunt'] for s in S)
mods=collections.Counter()
for s in S: mods.update(s['models'])
out['models']=mods.most_common(8)
out['start_ctx_median']=med([s['start'] for s in S if s['start']])
out['peak_ctx_median']=med([s['peak'] for s in S if s['peak']])
pp=collections.defaultdict(list)
for s in S: pp[s['p']].append(s)
rows=[]
for P,ss in pp.items():
    idx=R+'/'+P+'/memory/MEMORY.md'
    ib=os.path.getsize(idx) if os.path.exists(idx) else 0
    il=sum(1 for _ in open(idx)) if ib else 0
    n=sum(1 for k in memfiles if k[0]==P)
    read=sum(1 for k,v in memfiles.items() if k[0]==P and v)
    tgt=collections.Counter()
    for s in ss: tgt.update(s['crossproj'])
    rows.append(dict(p=P.replace(PREFIX,'') or '~',sessions=len(ss),mem=n,idx_bytes=ib,idx_lines=il,start_med=med([s['start'] for s in ss if s['start']]),peak_med=med([s['peak'] for s in ss if s['peak']]),calls=sum(s['calls'] for s in ss),cross_sessions=sum(1 for s in ss if s['cross']),cross_calls=sum(s['cross'] for s in ss),hunt=sum(s['hunt'] for s in ss),mem_read=read,cross_targets=[(k.replace(PREFIX,''),v) for k,v in tgt.most_common(3)]))
rows.sort(key=lambda r:-r['sessions'])
_an={}
def anon(x): return _an.setdefault(x,'proyecto-%02d'%(len(_an)+1))
for r in rows: r['p']=anon(r['p'])
for r in rows: r['cross_targets']=[(anon(a),b) for a,b in r['cross_targets']]
out['projects']=rows
out['mem_total']=len(memfiles); out['mem_ever_read']=sum(1 for v in memfiles.values() if v)
out['mem_read_by_other_project']=0
# wikilinks
own=cross=dang=0
for (P,b) in memfiles:
    t=open(R+'/'+P+'/memory/'+b,errors='ignore').read()
    for l in set(re.findall(r'\[\[([^\]|#]+)',t)):
        n=l.strip()+'.md'
        if (P,n) in memfiles: own+=1
        elif n in bynames: cross+=1
        else: dang+=1
out['links']=dict(own=own,cross=cross,dangling=dang)
tot=sum(r['idx_bytes'] for r in rows); out['unified_index_bytes']=sum(os.path.getsize(f) for f in glob.glob(R+'/*/memory/MEMORY.md')); out['unified_index_lines']=sum(sum(1 for _ in open(f)) for f in glob.glob(R+'/*/memory/MEMORY.md'))
out['all_mem_bytes']=sum(os.path.getsize(R+'/'+P+'/memory/'+b) for (P,b) in memfiles)
out['dup_names']=sum(1 for b,v in bynames.items() if len(v)>1)
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(json.dumps({k:v for k,v in out.items() if k!='projects'},ensure_ascii=False))
for r in rows[:22]: print(r)
