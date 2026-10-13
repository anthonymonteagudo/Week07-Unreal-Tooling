"""Check generated readers/library links and current source fingerprints."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
from hashlib import sha256
import json
import re

COURSE=Path(__file__).resolve().parent.parent
WORKSPACE=COURSE.parent

class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.refs=[];self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for key in ('href','src'):
            if key in a:self.refs.append(a[key])
        if tag=='img':self.images.append(a)

def main():
    missing=[];links=0;pages=0
    for folder in ('Readers','Visuals'):
        for file in (COURSE/folder).rglob('*.html'):
            page=Page();page.feed(file.read_text(encoding='utf-8'));pages+=1
            assert len(page.ids)==len(set(page.ids)),str(file)
            assert all(im.get('alt') for im in page.images),str(file)
            for ref in page.refs:
                url=urlsplit(ref)
                if url.scheme or url.netloc:continue
                if url.path:
                    dest=(file.parent/unquote(url.path)).resolve();links+=1
                    if not dest.exists():missing.append({'page':str(file.relative_to(COURSE)),'target':ref})
                    elif dest.suffix=='.html' and url.fragment:
                        target=Page();target.feed(dest.read_text(encoding='utf-8'))
                        if unquote(url.fragment) not in target.ids:missing.append({'page':str(file.relative_to(COURSE)),'target':ref,'issue':'anchor'})
                elif url.fragment:
                    assert unquote(url.fragment) in page.ids,(str(file),ref)
    manifest=json.loads((COURSE/'Readers/manifest.json').read_text(encoding='utf-8'))
    for doc in manifest['documents']:
        raw=(WORKSPACE/doc['source']).read_bytes().decode('utf-8-sig')
        assert sha256(raw.encode()).hexdigest()==doc['sha256'],doc['source']
    result={'pages':pages,'local_links':links,'reader_sources':len(manifest['documents']),'missing':missing,'browser_visual_qa':'Not performed; SVG/PNG inspection is separate.'}
    (COURSE/'Readers/verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
    if missing:raise SystemExit(1)

if __name__=='__main__':main()
