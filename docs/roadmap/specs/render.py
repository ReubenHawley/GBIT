"""Render docs/roadmap/specs/<ID>.md from the spec data and roadmap JSON.
Usage: python3 -I render.py [issues.json]   (issues.json maps ID -> issue number, optional)"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spec_e0_e1 as base, spec_e2, spec_e3_e5
S = base.S
here = os.path.dirname(os.path.abspath(__file__)); rm = os.path.dirname(here)
epics = {x["id"]: x for x in json.load(open(rm + "/epics.json"))}
feats = {x["id"]: x for x in json.load(open(rm + "/features.json"))}
tasks = {x["id"]: x for x in json.load(open(rm + "/tasks.json"))}
nums = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
AC = {"AC-01":"Language independence","AC-02":"Automatic discovery","AC-03":"Relationship mapping","AC-04":"Change detection","AC-05":"Transitive impact","AC-06":"Precise selection","AC-07":"Plugin extensibility","AC-08":"Incremental updates","AC-09":"Explainability","AC-10":"Safe fallback","AC-11":"CI compatibility","AC-12":"Continuous learning","AC-13":"Reproducibility","AC-14":"Cross-language impact"}
title = lambda i: (epics.get(i) or feats.get(i) or tasks.get(i))["title"]
def ref(i):
    n = nums.get(i); return f"#{n} ({i}) {title(i)}" if n else f"{i} {title(i)}"
def bullets(xs, box=False): return "\n".join(f"- {'[ ] ' if box else ''}{x}" for x in xs)
def render(i):
    d = S[i]; out = []
    if i in epics:
        e = epics[i]; kind = "Epic"; acs = []
        out.append(f"**{kind}** · {e['phase']}\n")
        out.append(f"## Summary\n{d['summary']}\n")
        out.append(f"## Exit criteria\n{e['exitCriteria']}\n")
    elif i in feats:
        f = feats[i]; kind = "Feature"; acs = f["acceptanceCriteria"]
        out.append(f"**{kind}** · Epic: {ref(f['epic'])}\n")
        out.append(f"## Summary\n{d['summary']}\n")
    else:
        t = tasks[i]; kind = "Task"; acs = feats[t["feature"]]["acceptanceCriteria"]
        out.append(f"**{kind}** · Feature: {ref(t['feature'])} · Epic: {ref(t['epic'])}\n")
        out.append(f"## Summary\n{d['summary']}\n")
    if acs: out.append("## Architecture acceptance criteria served\n" + bullets(f"{a}: {AC[a]}" for a in acs) + "\n")
    out.append("## Requirements\n" + bullets(d["requirements"]) + "\n")
    out.append("## Acceptance criteria\n" + bullets(d["acceptance"], True) + "\n")
    if d["tests"]: out.append("## Test-first plan\nWrite these before the implementation:\n" + bullets(d["tests"]) + "\n")
    if i in epics: out.append("## Features\n" + bullets(ref(f) for f in epics[i]["features"]) + "\n")
    if i in feats: out.append("## Tasks\n" + bullets(ref(t) for t in feats[i]["tasks"]) + "\n")
    if d["depends_on"]: out.append("## Depends on\n" + bullets(ref(x) for x in d["depends_on"]) + "\n")
    if d["notes"]: out.append("## Notes\n" + d["notes"] + "\n")
    if kind == "Task":
        out.append("## Definition of done\n- [ ] Tests written first and passing in CI\n- [ ] No new warnings; `dotnet format` clean\n- [ ] Kernel stays language-neutral (no language-specific logic in `Gbit.Core`)\n- [ ] Docs updated where behavior is user-visible\n- [ ] Merged by squash via a feature branch\n")
    out.append(f"---\n*Source: `docs/roadmap/specs/{i}.md` · derived from `docs/GBIT_Architecture_Proposal.html`*\n")
    return "\n".join(out)
for i in S:
    open(f"{here}/{i}.md", "w").write(render(i))
print(len(S), "specs rendered")
