"""Asset and transparency checks. Inspect the PNGs separately for visual QA."""
from pathlib import Path
from PIL import Image
from hashlib import sha256
from collections import Counter
import json
import xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parent.parent

def main():
    data=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    pngs=[]
    for icon in data['icons']:
        E.parse(ROOT/icon['svg'])
        for file in icon['png']:
            with Image.open(ROOT/file) as im:
                size=int(Path(file).stem.rsplit('-',1)[1])
                assert im.mode=='RGBA' and im.size==(size,size),file
                alpha=im.getchannel('A')
                assert alpha.getextrema()==(0,255),file
                assert alpha.getpixel((0,0))==0 and alpha.getpixel((size-1,size-1))==0,file
                bbox=alpha.getbbox(); assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<size and bbox[3]<size,file
                assert any(alpha.histogram()[1:255]),file
            pngs.append(file)
    for asset in data['legacy']:
        raw=(ROOT/asset['path']).read_bytes()
        assert sha256(raw).hexdigest()==asset['sha256']
        with Image.open(ROOT/asset['path']) as im:
            assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
    transparent_diagrams=[]
    real_crops=0
    for diagram in data['diagrams']:
        tree=E.parse(ROOT/diagram['svg'])
        with Image.open(ROOT/diagram['png']) as im:
            assert im.size==(2560,1440)
            if diagram.get('transparent'):
                assert im.mode=='RGBA'
                alpha=im.getchannel('A')
                assert alpha.getextrema()==(0,255)
                for xy in [(0,0),(2559,0),(0,1439),(2559,1439),(600,600)]:
                    assert alpha.getpixel(xy)==0,(diagram['id'],xy)
                assert alpha.histogram()[0] > im.width*im.height*0.35
                transparent_diagrams.append(diagram['id'])
        for crop in diagram.get('image_sources',[]):
            raw=(ROOT/crop['source']).read_bytes()
            assert sha256(raw).hexdigest()==crop['source_sha256']
            x,y,w,h=crop['crop_xywh']
            with Image.open(ROOT/crop['source']) as source, Image.open(ROOT/crop['file']) as actual:
                assert source.size==tuple(crop['source_size'])
                assert actual.size==(w,h)
                assert actual.convert('RGBA').tobytes()==source.crop((x,y,x+w,y+h)).convert('RGBA').tobytes(),crop['id']
            real_crops+=1
        if diagram.get('transparent'):
            ns={'s':'http://www.w3.org/2000/svg'}
            # No accidental sentence migration back into visible labels.
            for el in tree.findall('.//s:text',ns):
                assert len(''.join(el.itertext()).split())<=5
            assert len(tree.findall('.//s:image',ns))==len(diagram['image_sources'])
        assert (ROOT/diagram['html']).exists()
    result={'status':'passed','legacy_badges':len(data['legacy']),'companion_icons':len(data['icons']),'transparent_pngs':len(pngs),'diagrams':len(data['diagrams']),'transparent_diagrams':transparent_diagrams,'verified_real_crops':real_crops,'scope':'Alpha, bounds, SVG syntax, dimensions, exact legacy hashes, source hashes and pixel-exact rectangular crops, concise labels. Visual composition checked separately.'}
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__':main()
