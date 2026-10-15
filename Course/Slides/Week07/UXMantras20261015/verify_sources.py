"""Verify preserved originals, slide coverage and exact authored contrast pairs."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
source=json.loads((OUT/'source-manifest.json').read_text(encoding='utf-8'))
proposal=json.loads((OUT/'slide-proposals.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
changed=[n['source'] for n in source['notes'] if sha(n['source'])!=n['sha256']]
missing=[{'lesson':n['lesson'],'captures':n['missing_captures']} for n in source['notes'] if n['missing_captures']]
expected=set(range(39,61))|{62}
actual={s['old'] for s in proposal['slides'] if s['old'] is not None}
ids=[s['id'] for s in proposal['slides']]
def luminance(value):
    channels=[int(value[i:i+2],16)/255 for i in [1,3,5]]
    linear=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in channels]
    return sum(a*b for a,b in zip(linear,[.2126,.7152,.0722]))
def ratio(a,b):
    hi,lo=sorted([luminance(a),luminance(b)],reverse=True)
    return round((hi+.05)/(lo+.05),2)
pairs=[('Primary action text','#142033','#a9cfff'),('Secondary action text','#eef2f8','#303e53'),('Main text / canvas','#eef2f8','#171d27'),('Focus / secondary surface','#9ccaff','#303e53'),('Disabled text / surface','#8793a6','#252d39')]
report={
 'date':'2026-10-15','original_notes_checked':len(source['notes']),'changed_original_notes':changed,
 'deck_unchanged':sha(source['deck'])==source['deck_sha256'],'deck_sha256':source['deck_sha256'],
 'refined_notes':len(list((OUT/'notes').glob('*-refined.md'))),'unique_copied_course_images':len(source['images']),
 'missing_source_captures':missing,'proposal_count':len(ids),'unique_ids':len(set(ids))==len(ids),
 'current_slide_coverage_exact':actual==expected,'preserved_preparation_boundary':proposal['proposed_order'][-2:]==['61','62'],
 'existing_test_suite':{'command':'Week07UnrealPython/Scripts/dev.py test','passed':87,'scope':'offline unit/widget/workflow suite; no live engine validation'},
 'rendered_after_states':sorted(p.name for p in (OUT/'after').glob('*.png')),
 'contrast_pairs':[{'role':n,'foreground':a,'background':b,'ratio':ratio(a,b)} for n,a,b in pairs],
 'contrast_limit':'Computed from explicit opaque color pairs; not a screenshot pixel audit or full accessibility conformance test. Disabled content has different standards treatment. Text size, rendering, other surfaces and user testing remain separate.',
 'skill_validation':'quick_validate.py passed with task-local PyYAML dependency',
 'pending':['Live Unreal / native Slate integration','Actual target display scaling','Fresh GOLF+ matched captures','Final PowerPoint authoring, rendering and pacing'],
}
report['preserved_media']=[{'file':str(p.relative_to(OUT)),'sha256':sha(p)} for p in sorted((OUT/'assets').glob('*.png')) if not p.name.startswith('note-')]
(OUT/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert not changed and report['deck_unchanged'] and report['current_slide_coverage_exact'] and report['unique_ids'] and report['preserved_preparation_boundary']
print(json.dumps({k:v for k,v in report.items() if k not in ['preserved_media','rendered_after_states']},indent=2))
