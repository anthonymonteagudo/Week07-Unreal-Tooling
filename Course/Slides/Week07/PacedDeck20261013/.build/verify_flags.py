import zipfile,xml.etree.ElementTree as E
p='../output/Week_7_Paced_150_Minutes_v1.pptx'
with zipfile.ZipFile(p) as z:
 names=[n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
 hidden=[n for n in names if E.fromstring(z.read(n)).get('show')=='0']
 print({'total':len(names),'hidden':len(hidden),'live':len(names)-len(hidden)})
 assert len(names)==71 and len(hidden)==37
