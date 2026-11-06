#!/usr/bin/env python3
"""Build glossy doodle variants of the pastel gradient frames (Pillow only)."""
from pathlib import Path
import json, math
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent
S = 3
W, H = 1226, 1750
PALETTES = {
    "pink":  ((225, 105, 210), (153, 139, 239), (255, 239, 255), (255, 178, 235)),
    "blue":  ((91, 151, 239), (159, 132, 232), (238, 249, 255), (176, 218, 255)),
    "mint":  ((89, 183, 157), (130, 150, 232), (238, 255, 248), (176, 238, 216)),
    "gray":  ((76, 82, 98), (144, 150, 164), (255, 255, 255), (210, 215, 225)),
}

def sc(v): return int(round(v*S))
def bezier(p0,p1,p2,p3,n=32):
    out=[]
    for i in range(n+1):
        t=i/n; q=1-t
        out.append((q**3*p0[0]+3*q*q*t*p1[0]+3*q*t*t*p2[0]+t**3*p3[0], q**3*p0[1]+3*q*q*t*p1[1]+3*q*t*t*p2[1]+t**3*p3[1]))
    return out
def line(draw, pts, color, width):
    draw.line([(sc(x),sc(y)) for x,y in pts], fill=color, width=sc(width), joint="curve")
def heart_points(x,y,w,h):
    # A smooth, slightly hand-drawn heart silhouette.
    return (bezier((x+w*.5,y+h*.94),(x+w*.36,y+h*.77),(x+w*.03,y+h*.54),(x+w*.08,y+h*.30),20)
      +bezier((x+w*.08,y+h*.30),(x+w*.14,y+h*.02),(x+w*.42,y+h*.08),(x+w*.5,y+h*.29),20)[1:]
      +bezier((x+w*.5,y+h*.29),(x+w*.64,y+h*.04),(x+w*.96,y+h*.05),(x+w*.94,y+h*.35),20)[1:]
      +bezier((x+w*.94,y+h*.35),(x+w*.92,y+h*.58),(x+w*.65,y+h*.79),(x+w*.5,y+h*.94),20)[1:])
def heart(img, x,y,w,h, c,a, fill=True):
    d=ImageDraw.Draw(img,"RGBA"); pts=[(sc(px),sc(py)) for px,py in heart_points(x,y,w,h)]
    if fill:
        d.polygon(pts, fill=(*a,120))
        d.line(pts+[pts[0]], fill=(*c,240), width=sc(4), joint="curve")
        # small glossy reflection
        d.ellipse((sc(x+w*.23),sc(y+h*.18),sc(x+w*.39),sc(y+h*.29)), fill=(255,255,255,175))
        line(d, bezier((x+w*.17,y+h*.43),(x+w*.19,y+h*.30),(x+w*.24,y+h*.27),(x+w*.30,y+h*.28)), (255,255,255,210), 2)
    else:
        d.line(pts+[pts[0]], fill=(*c,245), width=sc(4), joint="curve")
        line(d, bezier((x+w*.18,y+h*.37),(x+w*.2,y+h*.2),(x+w*.34,y+h*.17),(x+w*.39,y+h*.3)), (255,255,255,210), 1.7)
def star(img,x,y,size,c,a,points=5):
    d=ImageDraw.Draw(img,"RGBA"); p=[]
    for i in range(points*2):
        ang=-math.pi/2+i*math.pi/points
        r=size*(.5 if i%2==0 else .23)
        p.append((sc(x+size/2+math.cos(ang)*r),sc(y+size/2+math.sin(ang)*r)))
    d.polygon(p, fill=(*a,130)); d.line(p+[p[0]],fill=(*c,245),width=sc(3.8),joint="curve")
    d.ellipse((sc(x+size*.39),sc(y+size*.22),sc(x+size*.49),sc(y+size*.34)), fill=(255,255,255,210))
def twinkle(img,x,y,size,c):
    d=ImageDraw.Draw(img,"RGBA")
    p=[(x+size*.5,y),(x+size*.59,y+size*.41),(x+size,y+size*.5),(x+size*.59,y+size*.59),(x+size*.5,y+size),(x+size*.41,y+size*.59),(x,y+size*.5),(x+size*.41,y+size*.41)]
    p=[(sc(a),sc(b)) for a,b in p]
    d.polygon(p,fill=(*c,155)); d.ellipse((sc(x+size*.43),sc(y+size*.43),sc(x+size*.57),sc(y+size*.57)),fill=(255,255,255,230))
def bow(img,x,y,w,h,c,a):
    d=ImageDraw.Draw(img,"RGBA")
    left=bezier((x+w*.5,y+h*.43),(x+w*.3,y+h*.05),(x+w*.04,y+h*.1),(x+w*.10,y+h*.45),24)+bezier((x+w*.10,y+h*.45),(x+w*.19,y+h*.63),(x+w*.36,y+h*.52),(x+w*.5,y+h*.43),24)[1:]
    right=bezier((x+w*.5,y+h*.43),(x+w*.7,y+h*.05),(x+w*.96,y+h*.1),(x+w*.90,y+h*.45),24)+bezier((x+w*.90,y+h*.45),(x+w*.81,y+h*.63),(x+w*.64,y+h*.52),(x+w*.5,y+h*.43),24)[1:]
    for p in (left,right):
        d.polygon([(sc(px),sc(py)) for px,py in p], fill=(*a,135))
        line(d,p,c,4); line(d,p[:12],(255,255,255,210),1.8)
    # ribbon tails
    for p in [bezier((x+w*.46,y+h*.5),(x+w*.37,y+h*.7),(x+w*.3,y+h*.86),(x+w*.22,y+h*.98),18),bezier((x+w*.54,y+h*.5),(x+w*.63,y+h*.7),(x+w*.7,y+h*.86),(x+w*.78,y+h*.98),18)]:
        line(d,p,c,4); line(d,p[:10],(255,255,255,205),1.6)
    d.ellipse((sc(x+w*.43),sc(y+h*.33),sc(x+w*.57),sc(y+h*.53)),fill=(*a,255),outline=(*c,240),width=sc(2))
    d.ellipse((sc(x+w*.46),sc(y+h*.36),sc(x+w*.49),sc(y+h*.40)),fill=(255,255,255,230))
def flourish(img,x,y,w,h,c):
    d=ImageDraw.Draw(img,"RGBA")
    p=bezier((x,y+h*.72),(x+w*.26,y+h*.02),(x+w*.56,y+h*.98),(x+w,y+h*.24),42)
    line(d,p,c,2.8); line(d,p[:22],(255,255,255,185),1.0)
    heart(img,x+w*.36,y+h*.05,w*.22,h*.35,c,(255,255,255),False)

def placements(layout):
    if layout == "1-photo":
        return [("heart",16,13,64,61,1),("twinkle",1142,22,38),("star",1140,1592,58),("bow",20,1578,94,128),("twinkle",1074,1680,32),("heart",1114,1634,65,64,0),("heart",145,1645,56,53,1),("flourish",42,150,88,108)]
    if layout == "2-photo":
        return [("heart",20,25,65,62,0),("star",1140,22,58),("twinkle",599,704,32),("twinkle",610,754,24),("heart",18,1120,56,53,1),("bow",1102,1145,104,122),("flourish",1100,245,90,125),("bow",562,202,102,126),("heart",112,238,74,70,1),("star",1024,277,55)]
    return [("heart",16,15,58,54,0),("star",1140,12,58),("twinkle",598,774,30),("twinkle",615,797,23),("heart",18,1538,53,50,1),("bow",1113,1528,88,102),("star",590,1572,36),("flourish",1141,770,44,62),("heart",125,1580,58,54,0)]

def main():
    manifest_path=ROOT/"frames.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    additions=[]
    for layout,key in (("1-photo","A"),("2-photo","B"),("4-photo","C")):
        for color,(primary,secondary,white,accent) in PALETTES.items():
            base_path=ROOT/"assets"/"frames"/layout/f"{color}.png"
            base=Image.open(base_path).convert("RGBA")
            layer=Image.new("RGBA",(W*S,H*S),(0,0,0,0))
            for item in placements(layout):
                typ,*v=item
                if typ=="heart":
                    x,y,w,h,filled=v; heart(layer,x,y,w,h,primary,accent,bool(filled))
                elif typ=="star": star(layer,*v,secondary,accent)
                elif typ=="twinkle": twinkle(layer,*v,white)
                elif typ=="bow": bow(layer,*v,primary,accent)
                elif typ=="flourish": flourish(layer,*v,secondary)
            layer=layer.resize((W,H),Image.Resampling.LANCZOS)
            # A restrained pastel glow gives the doodles a glossy sticker finish.
            glow=layer.getchannel("A").filter(ImageFilter.GaussianBlur(7))
            glow_color=Image.new("RGBA",(W,H),(*accent,0)); glow_color.putalpha(glow.point(lambda a: int(a*.32)))
            # Enforce exact, fully clear photo apertures regardless of any stroke antialiasing.
            mask=Image.new("L",(W,H),255); md=ImageDraw.Draw(mask)
            source=next(f for f in manifest["frames"] if f["layout"]==key and f["src"].endswith(f"/{color}.png"))
            for r in source["rects"]:
                x=round(r["x"]*W); y=round(r["y"]*H); w=round(r["w"]*W); h=round(r["h"]*H)
                md.rectangle((x,y,x+w-1,y+h-1),fill=0)
            alpha=layer.getchannel("A"); alpha=Image.composite(alpha,Image.new("L",(W,H),0),mask); layer.putalpha(alpha)
            glow_alpha=glow_color.getchannel("A"); glow_alpha=Image.composite(glow_alpha,Image.new("L",(W,H),0),mask); glow_color.putalpha(glow_alpha)
            result=Image.alpha_composite(Image.alpha_composite(base,glow_color),layer)
            dest=ROOT/"assets"/"frames"/layout/f"{color}-decor.png"
            result.save(dest,optimize=True)
            additions.append({"id":f"{color}-decor-{key}","name":f"{dict(pink='ピンク',blue='ブルー',mint='ミント',gray='モノクロ')[color]}・デコ","src":dest.relative_to(ROOT).as_posix(),"layout":key,"orientation":"portrait","rects":source["rects"]})
    known={f["src"] for f in manifest["frames"]}
    manifest["frames"].extend(f for f in additions if f["src"] not in known)
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Added {len(additions)} decorated frame variants")
if __name__=="__main__": main()
