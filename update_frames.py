from pathlib import Path
import json
root=Path(__file__).resolve().parent
p=root/'frames.json'
data=json.loads(p.read_text(encoding='utf-8'))
old={f['src']:f for f in data['frames']}
result=[]
for count,layout in [(1,'A'),(2,'B'),(4,'C')]:
    template=next(f for f in data['frames'] if f['layout']==layout)
    for img in sorted((root/'assets'/'frames'/f'{count}-photo').iterdir()):
        if img.suffix.lower() not in ('.png','.webp'):continue
        src=img.relative_to(root).as_posix()
        result.append(old.get(src,dict(id=src,name=img.stem,src=src,layout=layout,orientation='auto',rects=template['rects'])))
p.write_text(json.dumps(dict(frames=result),ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated frames.json:',len(result),'frames')
