"""Rebuild the catalog without losing existing window coordinates (Python 3)."""
from pathlib import Path
import json
import os
import tempfile
ROOT = Path(__file__).resolve().parent
DEFAULTS = {
    'A': [dict(x=88/1226, y=96/1750, w=1050/1226, h=1400/1750)],
    'B': [dict(x=x/1226, y=400/1750, w=492/1226, h=656/1750) for x in (88,648)],
    'C': [dict(x=x/1226, y=y/1750, w=492/1226, h=656/1750) for y in (96,827) for x in (88,648)]
}
def update(root=ROOT):
    path=root/'frames.json'
    data=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'frames':[]}
    old={f['src']:f for f in data['frames']}
    result=[]
    for count,layout in [(1,'A'),(2,'B'),(4,'C')]:
        folder=root/'assets'/'frames'/f'{count}-photo'
        folder.mkdir(parents=True,exist_ok=True)
        for img in sorted(folder.rglob('*')):
            if not img.is_file() or img.is_symlink() or img.suffix.lower() not in ('.png','.webp'): continue
            src=img.relative_to(root).as_posix()
            result.append(old.get(src,dict(id=src,name=img.stem,src=src,layout=layout,orientation='auto',rects=DEFAULTS[layout])))
    content=json.dumps(dict(frames=result),ensure_ascii=False,indent=2)
    if not path.exists() or path.read_text(encoding='utf-8')!=content:
        with tempfile.NamedTemporaryFile('w',dir=root,encoding='utf-8',delete=False) as temp:
            temp.write(content);tempname=temp.name
        os.replace(tempname,path)
    return len(result)
if __name__=='__main__':
    print('Updated frames.json:',update(),'frames')
