"""Check that GitHub has every LFS object for this repository's selected revision.

Uses the authenticated GitHub CLI. Only download metadata is requested; signed
URLs and authentication credentials are never printed or written to disk.
"""
import argparse
import base64
import json
import subprocess
import urllib.error
import urllib.request

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('revision', nargs='?', default='HEAD')
args = parser.parse_args()
files = json.loads(subprocess.check_output(['git','lfs','ls-files','--json',args.revision]))['files']
objects = {f['oid']:f['size'] for f in files}
token = subprocess.check_output(['gh','auth','token','--user','anthonymonteagudo'],text=True).strip()
authorization = base64.b64encode(('anthonymonteagudo:'+token).encode()).decode()
items = [dict(oid=key,size=size) for key,size in objects.items()]
available = total_bytes = 0
try:
    for start in range(0,len(items),100):
        payload = json.dumps({'operation':'download','transfers':['basic'],'objects':items[start:start+100]}).encode()
        request = urllib.request.Request(
            'https://github.com/anthonymonteagudo/Week07-Unreal-Tooling.git/info/lfs/objects/batch',
            data=payload,headers={'Authorization':'Basic '+authorization,
                                 'Content-Type':'application/vnd.git-lfs+json',
                                 'Accept':'application/vnd.git-lfs+json'})
        with urllib.request.urlopen(request,timeout=30) as response:
            result=json.load(response)
        for obj in result['objects']:
            if obj.get('actions',{}).get('download'):
                available+=1
                total_bytes+=objects[obj['oid']]
except urllib.error.HTTPError as error:
    raise SystemExit('GitHub LFS metadata check failed with HTTP '+str(error.code)) from None
print(json.dumps(dict(revision=args.revision,available_objects=available,total_objects=len(items),
                     available_bytes=total_bytes,total_bytes=sum(objects.values()),
                     complete=available==len(items)),indent=2))
raise SystemExit(0 if available==len(items) else 1)
