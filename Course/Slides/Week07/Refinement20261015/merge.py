"""Integrate Artifact Tool compositions while preserving the source's media and masters."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import posixpath, json, hashlib, re

OUT=Path(__file__).resolve().parent
inv=json.loads((OUT/'source-inventory.json').read_text(encoding='utf-8'))
plan=json.loads((OUT/'content-plan.json').read_text(encoding='utf-8'))
source_notes=json.loads((OUT/'source-notes.json').read_text(encoding='utf-8'))
src=Path(inv['source'])
assert hashlib.sha256(src.read_bytes()).hexdigest()==inv['sha256']
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
R='http://schemas.openxmlformats.org/package/2006/relationships'; CT='http://schemas.openxmlformats.org/package/2006/content-types'
def xml(b):return E.fromstring(b)
def dump(r):return E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
def tag(s):return '{'+NS[s.split(':')[0]]+'}'+s.split(':')[1]
def rp(part):return posixpath.dirname(part)+'/_rels/'+posixpath.basename(part)+'.rels'
with ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
with ZipFile(OUT/'build/authored.pptx') as z:overlay={n:z.read(n) for n in z.namelist()}
ct=xml(data['[Content_Types].xml']);pres=xml(data['ppt/presentation.xml']);ids=pres.find('p:sldIdLst',NS);prels=xml(data['ppt/_rels/presentation.xml.rels'])
source_parts={s['number']:s['part'] for s in inv['slides']}
source_ids={s['number']:deepcopy(x) for s,x in zip(inv['slides'],ids)}
notes_ct='application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml'
slide_ct='application/vnd.openxmlformats-officedocument.presentationml.slide+xml'
def ctype(part,kind):E.SubElement(ct,'{'+CT+'}Override',PartName='/'+part,ContentType=kind)

# Remove empty trailing paragraphs that produced false overflow and reserve real
# height for the remaining inherited text. Do not shrink the source typography.
for number in (5,6,8,11,15,16,17,24,29,35,42,44,49,52):
    part=source_parts[number];r=xml(data[part])
    for sh in r.findall('.//p:sp',NS):
        tx=sh.find('p:txBody',NS)
        if tx is None:continue
        pars=tx.findall('a:p',NS)
        while len(pars)>1 and not ''.join(pars[-1].xpath('.//a:t/text()',namespaces=NS)).strip():
            tx.remove(pars.pop())
        bp=tx.find('a:bodyPr',NS)
        if bp is not None:
            for attr in ('tIns','bIns'):bp.set(attr,'0')
        words=''.join(tx.xpath('.//a:t/text()',namespaces=NS))
        ph=sh.find('.//p:ph',NS)
        if number==42 and ph is not None and ph.get('type')=='title':
            sp=sh.find('p:spPr',NS)
            oldx=sp.find('a:xfrm',NS)
            if oldx is not None:sp.remove(oldx)
            xf=E.SubElement(sp,tag('a:xfrm'))
            x,y,w,h=(36,72,890,130)
            E.SubElement(xf,tag('a:off'),x=str(x*12700),y=str(y*12700))
            E.SubElement(xf,tag('a:ext'),cx=str(w*12700),cy=str(h*12700))
            if number==42:
                for run in tx.findall('.//a:r',NS):
                    props=run.find('a:rPr',NS)
                    if props is None:props=E.SubElement(run,tag('a:rPr'))
                    props.set('sz','4800')
        if number==42 and 'What proves success' in words:
            for t in tx.findall('.//a:t',NS):
                if t.text=='What proves success, and how do we recover?':
                    t.text='What would you like clarified about success or recovery?'
        xfrm=sh.find('p:spPr/a:xfrm',NS)
        if xfrm is None:continue
        off=xfrm.find('a:off',NS);ext=xfrm.find('a:ext',NS)
        if number==8 and words.startswith('{'):
            ext.set('cy',str(180*12700))
        # Empty paragraph cleanup is enough for the code boxes; these explanatory
        # labels need room for their actual line count.
        if words.startswith(('Python Editor Script Plugin','Save in .vscode','get_selected_level_actors() returns','bpy.context.selected_objects','Three placements.')):
            ext.set('cy',str(max(int(ext.get('cy')),int(83*12700))))
        if number==42 and words=='Python in Unreal: questions':
            ext.set('cy',str(175*12700))
    data[part]=dump(r)
def set_notes(part,body,number):
    n_part='ppt/notesSlides/refinementNotes'+str(number)+'.xml'
    sample=next(n for n in data if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml'))
    r=xml(data[sample]); found=False
    for sh in r.findall('.//p:sp',NS):
        ph=sh.find('.//p:ph',NS)
        if ph is None:continue
        if ph.get('type')=='body':
            tx=sh.find('p:txBody',NS)
            for x in list(tx):
                if x.tag==tag('a:p'):tx.remove(x)
            for line in body.split('\n'):
                p=E.SubElement(tx,tag('a:p'));run=E.SubElement(p,tag('a:r'));E.SubElement(run,tag('a:t')).text=line
            found=True
        elif ph.get('type')=='sldNum':
            for t in sh.findall('.//a:t',NS):t.text=str(number)
    assert found
    nr=xml(data[rp(sample)])
    for x in nr:
        if x.get('Type','').endswith('/slide'):x.set('Target','../slides/'+posixpath.basename(part))
    data[n_part]=dump(r);data[rp(n_part)]=dump(nr);ctype(n_part,notes_ct)
    rel=xml(data[rp(part)])
    for old in list(rel):
        if old.get('Type','').endswith('/notesSlide'):rel.remove(old)
    E.SubElement(rel,'{'+R+'}Relationship',Id='rIdRefinementNotes',Type=NS['r']+'/notesSlide',Target='../notesSlides/'+posixpath.basename(n_part))
    data[rp(part)]=dump(rel)

newparts={};newids={}; newrecords={s['id']:s for s in plan['slides']}
for ix,a in enumerate(plan['slides'],1):
    part=f'ppt/slides/refinementSlide{ix}.xml'; template=source_parts[a['template']]
    r=xml(data[template]);r.attrib.pop('show',None);tree=r.find('p:cSld/p:spTree',NS)
    for node in list(tree):
        local=E.QName(node).localname
        if local in ('nvGrpSpPr','grpSpPr'):continue
        nv=node.find('.//p:cNvPr',NS);ph=node.find('.//p:ph',NS)
        keep=(nv is not None and nv.get('name')=='Section border') or (ph is not None and ph.get('type') in ('ftr','sldNum'))
        if not keep:tree.remove(node)
    # New content inherits the exact source layout and its gradient artwork.
    rel=xml(data[rp(template)])
    for x in list(rel):
        if not x.get('Type','').endswith('/slideLayout'):rel.remove(x)
    ovpart=f'ppt/slides/slide{ix}.xml';ov=xml(overlay[ovpart]);ovrels=xml(overlay[rp(ovpart)]) if rp(ovpart) in overlay else []
    remap={}
    for rr in ovrels:
        if rr.get('Type','').endswith('/image'):
            target=rr.get('Target').lstrip('/')
            old=target if target in overlay else posixpath.normpath(posixpath.dirname(ovpart)+'/'+target)
            new=f'ppt/media/refinement-{ix}-{posixpath.basename(old)}';data[new]=overlay[old]
            rid='rIdRefinementImage'+str(len(remap)+1);remap[rr.get('Id')]=rid
            E.SubElement(rel,'{'+R+'}Relationship',Id=rid,Type=NS['r']+'/image',Target='../media/'+posixpath.basename(new))
            ext=Path(new).suffix[1:]
            if not any(x.get('Extension')==ext for x in ct):E.SubElement(ct,'{'+CT+'}Default',Extension=ext,ContentType='image/'+ext)
    last=max([int(x.get('id')) for x in r.findall('.//p:cNvPr',NS)]+[1])
    for node in ov.find('p:cSld/p:spTree',NS):
        if E.QName(node).localname not in ('sp','pic','graphicFrame'):continue
        sh=deepcopy(node);last+=1;sh.find('.//p:cNvPr',NS).set('id',str(last))
        for el in sh.iter():
            for attr,val in list(el.attrib.items()):
                if attr.startswith('{'+NS['r']+'}') and val in remap:el.set(attr,remap[val])
        for bp in sh.findall('.//a:bodyPr',NS):
            # Tables keep their cell margins; shape text follows the source canvas grid.
            if E.QName(sh).localname=='sp':
                for k in ('lIns','rIns','tIns','bIns'):bp.set(k,'0')
            for child in list(bp):
                if E.QName(child).localname in ('normAutofit','spAutoFit'):bp.remove(child)
            E.SubElement(bp,tag('a:noAutofit'))
        tree.append(sh)
    data[part]=dump(r);data[rp(part)]=dump(rel);ctype(part,slide_ct)
    rid='rIdRefinementSlide'+str(ix)
    E.SubElement(prels,'{'+R+'}Relationship',Id=rid,Type=NS['r']+'/slide',Target='slides/'+posixpath.basename(part))
    sid=E.Element(tag('p:sldId'),id=str(1000+ix));sid.set('{'+NS['r']+'}id',rid)
    newparts[a['id']]=part;newids[a['id']]=sid

# Rename stale preview images only at the intended slide relationship; preserve source bytes.
image_changes={62:['material_preview.png'],65:[None,'material_complete.png'],71:['vfx_warning.png','vfx_blocked.png']}
for number,files in image_changes.items():
    part=source_parts[number];r=xml(data[part]);rr=xml(data[rp(part)]);pics=r.findall('.//p:pic',NS)
    for pic,file in zip(pics,files):
        if not file:continue
        blip=pic.find('.//a:blip',NS)
        if blip is None:continue
        rid='rIdFreshPractice'+str(number)+'_'+str(len(rr))
        new='ppt/media/fresh-'+str(number)+'-'+file;data[new]=(OUT/'assets/practice'/file).read_bytes()
        E.SubElement(rr,'{'+R+'}Relationship',Id=rid,Type=NS['r']+'/image',Target='../media/'+posixpath.basename(new))
        blip.set('{'+NS['r']+'}embed',rid)
    data[part]=dump(r);data[rp(part)]=dump(rr)

# Keep inherited captions legible across the brightest part of the gradient.
for number in (62,65):
    part=source_parts[number];r=xml(data[part])
    for sh in r.findall('.//p:sp',NS):
        words=''.join(sh.xpath('.//a:t/text()',namespaces=NS))
        if not words.startswith(('Assessment question:','Do not make color','UI/UX course connection','Left: Week 2')):continue
        props=sh.find('p:spPr',NS)
        for fill in list(props):
            if E.QName(fill).localname in ('solidFill','noFill','gradFill','blipFill','pattFill','grpFill'):props.remove(fill)
        fill=E.Element(tag('a:solidFill'));color=E.SubElement(fill,tag('a:srgbClr'),val='0C0B12')
        E.SubElement(color,tag('a:alpha'),val='90000')
        before=next((i for i,x in enumerate(props) if E.QName(x).localname in ('ln','effectLst','effectDag','scene3d','sp3d','extLst')),len(props))
        props.insert(before,fill)
    data[part]=dump(r)

for x in list(ids):ids.remove(x)
final_map=[]
for final,key in enumerate(plan['order'],1):
    part=source_parts[key] if isinstance(key,int) else newparts[key]
    sid=deepcopy(source_ids[key] if isinstance(key,int) else newids[key]);ids.append(sid)
    r=xml(data[part])
    for sh in r.findall('.//p:sp',NS):
        ph=sh.find('.//p:ph',NS)
        if ph is not None and ph.get('type')=='sldNum':
            for t in sh.findall('.//a:t',NS):t.text=str(final)
            if final >= 100:
                # The source footer was sized for two digits. Preserve its
                # vertical position while reserving space for the full number.
                props=sh.find('p:spPr',NS)
                xf=props.find('a:xfrm',NS)
                if xf is None:
                    xf=E.SubElement(props,tag('a:xfrm'))
                    E.SubElement(xf,tag('a:off'),x=str(885*12700),y=str(20*12700))
                    E.SubElement(xf,tag('a:ext'),cx=str(40*12700),cy=str(18*12700))
                else:
                    xf.find('a:off',NS).set('x',str(885*12700))
                    xf.find('a:ext',NS).set('cx',str(40*12700))
                for paragraph in sh.findall('.//a:p',NS):
                    pr=paragraph.find('a:pPr',NS)
                    if pr is None:
                        pr=E.Element(tag('a:pPr'));paragraph.insert(0,pr)
                    pr.set('algn','r')
    data[part]=dump(r)
    if not isinstance(key,int):
        a=newrecords[key]; body=a['notes']+'\n\nSources\n'+'\n'.join(a['sources'])
        body+='\n\nInstructor pacing\n'+('Timed route. Use the stated question; fuller examples remain available.' if key in plan['timed_route'] else 'Prepared depth. Use for a question or a fuller explanation; do not add time to the fixed schedule.')
        set_notes(part,body,final)
    else:
        sn=source_notes[str(key)]
        body=sn['narration']+'\n\nSources\n'+'\n'.join(sn['sources'])
        body+='\n\nInstructor guidance\n'+sn.get('facilitation','')
        body+='\n'+('Timed route.' if key in plan['timed_route'] else 'Prepared depth; use for questions or a fuller explanation.')
        set_notes(part,body,final)
    final_map.append({'number':final,'key':key,'part':part,'timed':key in plan['timed_route'],'source_slide':key if isinstance(key,int) else None,'title':newrecords[key]['title'] if not isinstance(key,int) else ''})

# A real PowerPoint custom show makes the paced route usable without deleting detail.
oldshows=pres.find('p:custShowLst',NS)
if oldshows is None:
    oldshows=E.Element(tag('p:custShowLst'))
    # PowerPoint ignores custom shows placed after defaultTextStyle/extLst.
    before=next((i for i,x in enumerate(pres) if E.QName(x).localname in ('photoAlbum','custDataLst','kinsoku','defaultTextStyle','modifyVerifier','extLst')),len(pres))
    pres.insert(before,oldshows)
existing_ids=[int(s.get('id','0')) for s in oldshows]
show=E.SubElement(oldshows,tag('p:custShow'),name='Week 7 timed class route',id=str(max(existing_ids+[0])+1));lst=E.SubElement(show,tag('p:sldLst'))
bykey={str(k):sid for k,sid in zip(plan['order'],ids)}
for key in plan['timed_route']:
    s=E.SubElement(lst,tag('p:sld'));s.set('{'+NS['r']+'}id',bykey[str(key)].get('{'+NS['r']+'}id'))

data['ppt/presentation.xml']=dump(pres);data['ppt/_rels/presentation.xml.rels']=dump(prels);data['[Content_Types].xml']=dump(ct)
(OUT/'slide-map.json').write_text(json.dumps(final_map,ensure_ascii=False,indent=2),encoding='utf-8')
candidate=OUT/'build/candidate.pptx'
with ZipFile(candidate,'w',ZIP_DEFLATED) as z:
    for n,b in data.items():z.writestr(n,b)
assert all(hashlib.sha256(data[n]).hexdigest()==h for n,h in inv['media'].items())
print(json.dumps({'candidate':str(candidate),'slides':len(ids),'source_media_preserved':len(inv['media']),'custom_show_slides':len(plan['timed_route'])}))
