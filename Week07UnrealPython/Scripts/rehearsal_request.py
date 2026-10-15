"""Send an authored script to the explicitly started local rehearsal editor."""
from pathlib import Path
import json
import sys
import time
import uuid
root = Path(__file__).resolve().parents[1]
out = root/'Saved/LiveRehearsal'
identity = uuid.uuid4().hex
source = Path(sys.argv[1]).read_text(encoding='utf-8-sig')
out.mkdir(parents=True, exist_ok=True)
temp = out/'request.tmp'
temp.write_text(json.dumps({'id': identity, 'code': source}), encoding='utf-8')
temp.replace(out/'request.json')
result = out/('response-'+identity+'.json')
deadline = time.monotonic()+180
while not result.exists():
    if time.monotonic()>deadline: raise TimeoutError(str(result))
    time.sleep(.2)
data=json.loads(result.read_text(encoding='utf-8'))
print(json.dumps(data,indent=2))
sys.exit(0 if data['ok'] else 1)
