#!/usr/bin/env python3
"""
event_recap.py — one-command storyboard + animatic generator for ANY event recap.
Encodes the proven cinematic-recap arc; auto-fills beats with available photos,
placeholders where none. Outputs: <slug>_board.png, <slug>_shots.md, <slug>_animatic.mp4.

CLI:
  python3 event_recap.py --name "Farmers Market" --location "Framingham Centre Common" \
      --when "Thursdays 3-7PM" --info "Farms · Food Trucks · Bakeries" \
      --images ./photos --ratio 9:16 [--no-animatic]

Or import make_recap() and pass an images list directly.
"""
import os, sys, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import storyboard as sb

# proven recap arc: (role, shot, move, dur, desc_template, wants_image)
ARC = [
 ("HOOK",     "CU",     "punch in",  2.0, "HOOK at t=0: strongest image of {name} + title overlay", True),
 ("ESTABLISH","WS",     "slow push", 2.5, "Establish: signage / entrance — {name} at {location}",   True),
 ("REVEAL",   "EWS",    "pan",       3.0, "Wide reveal of the whole space / scene",                  True),
 ("ACTIVITY", "MS",     "handheld",  2.5, "Main activity — what people are doing",                    True),
 ("DETAIL",   "INSERT", "static",    2.0, "Insert: a telling detail / texture",                      True),
 ("ACTION",   "MS",     "track",     2.5, "Second activity / movement beat",                          True),
 ("COMMUNITY","CU",     "static",    2.0, "Faces — people enjoying {name}",                           True),
 ("ENERGY",   "WS",     "static",    2.5, "Wide of the crowd / energy of the day",                    True),
 ("ENDCARD",  "GRAPHIC","static",    3.5, "End card: {name} · {when} · {location} · {info}",          True),
]

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

def gather(images):
    if images is None: return []
    if isinstance(images,str):
        if os.path.isdir(images):
            return sorted(sum([glob.glob(os.path.join(images,e)) for e in
                   ("*.jpg","*.jpeg","*.png","*.JPG","*.JPEG","*.PNG")],[]))
        return [images]
    return [p for p in images if p]

def make_recap(name, location="", when="", info="", images=None, ratio="9:16",
               outdir=".", animatic=True, brand=""):
    imgs = gather(images); ii=0; panels=[]
    ctx=dict(name=name, location=location, when=when, info=info)
    for i,(role,shot,move,dur,tmpl,wants) in enumerate(ARC):
        img=None
        if wants and ii < len(imgs): img=imgs[ii]; ii+=1
        panels.append({"n":i+1,"shot":shot,"move":move,"dur":dur,
                       "desc":tmpl.format(**ctx),
                       "vo": ("text: "+name.upper()) if role=="HOOK" else (when if role=="ENDCARD" else ""),
                       "img":img})
    s=slug(name); os.makedirs(outdir,exist_ok=True)
    board=sb.render_board(panels,f"{outdir}/{s}_board.png",ratio=ratio,cols=3,
                          title=name.upper(),subtitle=f"Event recap · {ratio} · {when} {('· '+location) if location else ''}".strip())
    md=sb.shotlist_md(panels,f"{outdir}/{s}_shots.md",title=f"{name} — Recap Shot List")
    out={"board":board,"shotlist":md,"panels":len(panels),"images_used":ii}
    if animatic:
        W,H = (1080,1920) if ratio=="9:16" else (1920,1080) if ratio=="16:9" else (1080,1080)
        out["animatic"]=sb.animatic(panels,f"{outdir}/{s}_animatic.mp4",W,H,30)
    print(f"[{name}] board+shotlist{'+animatic' if animatic else ''}  ({ii} photos, {len(panels)} shots)")
    return out

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--name",required=True); ap.add_argument("--location",default="")
    ap.add_argument("--when",default=""); ap.add_argument("--info",default="")
    ap.add_argument("--images",default=None); ap.add_argument("--ratio",default="9:16")
    ap.add_argument("--out",default="."); ap.add_argument("--no-animatic",action="store_true")
    a=ap.parse_args()
    make_recap(a.name,a.location,a.when,a.info,a.images,a.ratio,a.out,not a.no_animatic)
