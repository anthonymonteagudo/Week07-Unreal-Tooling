"""Check the local static course artifacts and the illustrative Python rule."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import contextlib,io,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
WIKI=ROOT/'Wiki'
class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.ids=[];self.links=[];self.scripts=[];self.images=[];self.title=False;self.main=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='title':self.title=True
        if tag=='main':self.main=True
        if tag in {'a','link'} and 'href' in a:self.links.append(a['href'])
        if tag in {'img','script'} and 'src' in a:self.links.append(a['src'])
        if tag=='img':self.images.append(a)

pages=json.loads((WIKI/'pages.json').read_text(encoding='utf-8'))
assert len(pages)==29
assert {p['slug'] for p in pages}.issuperset({f'week{n:02d}' for n in range(1,13)})
assert sum(p['status']=='Planned' for p in pages)==9
files=[WIKI/(p['slug']+'.html') for p in pages]+[ROOT/'index.html',ROOT/'Slides/index.html',ROOT/'Slides/Week02/Review/WEEK2_SLIDE_BY_SLIDE_REVIEW.html']
docs={};bad=[];links_checked=0
for path in files:
    parser=Document();parser.feed(path.read_text(encoding='utf-8'));parser.close();docs[path.resolve()]=parser
    assert parser.title and parser.main,path
    assert len(parser.ids)==len(set(parser.ids)),('duplicate id',path)
    for im in parser.images:assert im.get('alt'),('image alt',path)
for path,doc in docs.items():
    for ref in doc.links:
        if ref.startswith(('https:','http:','mailto:','data:')):continue
        url=urlparse(ref)
        if url.scheme:continue
        target=(path.parent/unquote(url.path)).resolve() if url.path else path
        if not target.exists():bad.append((str(path.relative_to(ROOT)),ref));continue
        if url.fragment and target in docs and unquote(url.fragment) not in docs[target].ids:bad.append((str(path.relative_to(ROOT)),ref+' (missing anchor)'))
        links_checked+=1
assert not bad,bad
for path in (WIKI/'content').glob('*.md'):
    body=path.read_text(encoding='utf-8')
    assert not re.search(r'\bTODO\b|\bTBD\b|lorem ipsum',body,re.I),path

# Exercise the actual documented Week 3 rule and its boundary cases.
source=(WIKI/'content/week03.md').read_text(encoding='utf-8')
snippet=re.search(r'```python\n([\s\S]*?)\n```',source).group(1)
namespace={}
with contextlib.redirect_stdout(io.StringIO()) as printed:exec(compile(snippet,'wiki-week03-example','exec'),namespace)
check=namespace['needs_attention']
assert printed.getvalue().strip()=="['TD_target_large_cube', 'prop_round_mesh']"
assert check('TD_boundary_low',9.75) is False
assert check('TD_boundary_high',10.75) is False
assert check('TD_too_low',9.74) is True
assert check('prop_valid_density',10.24) is True
result={'wiki_pages':len(pages),'planned_weeks':9,'canonical_html_files':len(files),'local_links_checked':links_checked,'local_links':'pass','unique_ids_and_image_alt':'pass','python_example_and_boundary_cases':'pass'}
print(json.dumps(result,indent=2))
(ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
