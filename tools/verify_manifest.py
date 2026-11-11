#!/usr/bin/env python3
"""Check listed release file digests; independent of publication/rights verification."""
import json, hashlib, sys
from pathlib import Path

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
manifest=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
errors=[]
for rel, expected in manifest['files'].items():
    candidate=root/rel
    if not candidate.is_file(): errors.append('missing:'+rel); continue
    actual=hashlib.sha256(candidate.read_bytes()).hexdigest()
    if actual!=expected: errors.append('hash_mismatch:'+rel)
print({'manifest_release':manifest['release'],'files_checked':len(manifest['files']),'status':'PASS' if not errors else 'FAIL','errors':errors})
raise SystemExit(1 if errors else 0)
