import glob, yaml
bad=[]; names={}; nofm=[]; mism=[]
for p in sorted(glob.glob("skills/*/SKILL.md")+glob.glob("vendor/skills/*/SKILL.md")):
    t=open(p,encoding="utf-8",errors="replace").read()
    if not t.startswith("---"): nofm.append(p); continue
    end=t.find("\n---",3)
    if end<0: nofm.append(p); continue
    try: d=yaml.safe_load(t[3:end])
    except Exception as e: bad.append((p,str(e).replace("\n"," ")[:100])); continue
    if not isinstance(d,dict): bad.append((p,"not a mapping")); continue
    n=d.get("name"); desc=d.get("description"); dirn=p.split("/")[-2]
    if not n: bad.append((p,"missing name"))
    if not desc: bad.append((p,"missing description"))
    if n:
        names.setdefault(n,[]).append(dirn)
        if n!=dirn: mism.append((dirn,n))
print("YAML parse errors :", bad if bad else "none")
print("missing frontmatter:", nofm if nofm else "none")
print()
print("name != directory:")
for d,n in mism: print(f"   dir {d:34s} declares  {n}")
if not mism: print("   none")
print()
print("DUPLICATE declared names:")
dup=[ (n,ds) for n,ds in sorted(names.items()) if len(ds)>1 ]
for n,ds in dup: print(f"   {n!r}  <-  {ds}")
if not dup: print("   none")
print(f"\nvalidated {sum(len(v) for v in names.values())} skills")
