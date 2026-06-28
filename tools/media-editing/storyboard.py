#!/usr/bin/env python3
"""
storyboard.py — pre-visualization / storyboard toolkit.
Turn a concept into: (1) a shot-listed storyboard SHEET, (2) a shot-list markdown,
(3) a timed ANIMATIC video (Ken Burns over panels) that drops into vidkit/editkit.

A "panel" is a dict:
  {"n":1, "shot":"WIDE", "move":"slow push", "dur":3.0,
   "desc":"Establish the skate park sign, pond behind", "vo":"", "img":"path.jpg"|None}

Shot vocabulary (shorthand for boards):
  EWS extreme-wide  WS wide  MS medium  MCU med-closeup  CU closeup  ECU extreme-cu
  OTS over-shoulder  POV point-of-view  INSERT detail  AERIAL/TOP  TWO two-shot
Moves: static, slow push (in), pull (out), pan L/R, tilt up/down, track, handheld, whip.
"""
import os, subprocess, json, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
F="/tmp/adfonts/"
def _f(n,s): return ImageFont.truetype(F+n,s)
EB=lambda s:_f("Poppins-ExtraBold.ttf",s); SB=lambda s:_f("Poppins-SemiBold.ttf",s)
MD=lambda s:_f("Poppins-Medium.ttf",s); RG=lambda s:_f("Poppins-Regular.ttf",s)
INK=(34,38,44); SUB=(110,116,126); LINE=(214,218,224); CARD=(255,255,255); BG=(244,245,247); ACCENT=(46,140,120)

def _ratio(r):
    return {"16:9":(16,9),"9:16":(9,16),"1:1":(1,1),"4:5":(4,5),"2.39:1":(239,100)}.get(r,(16,9))

def render_board(panels, out, ratio="16:9", cols=3, title="STORYBOARD", subtitle=""):
    rw,rh=_ratio(ratio)
    M=46; gut=26; cw=420; fh=int(cw*rh/rw)          # frame size
    caph=120                                         # caption block under frame
    cellh=fh+caph; rows=(len(panels)+cols-1)//cols
    W=M*2+cols*cw+(cols-1)*gut
    H=150+M+rows*(cellh+gut)
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.text((M,40),title,font=EB(46),fill=INK)
    if subtitle: d.text((M,98),subtitle,font=MD(24),fill=SUB)
    d.line((M,140,W-M,140),fill=LINE,width=2)
    for i,p in enumerate(panels):
        r,c=divmod(i,cols); x=M+c*(cw+gut); y=150+M+r*(cellh+gut)
        d.rounded_rectangle((x,y,x+cw,y+cellh),radius=14,fill=CARD,outline=LINE,width=2)
        # frame area
        fx,fy=x,y;
        if p.get("img") and os.path.isfile(p["img"]):
            thumb=ImageOps.exif_transpose(Image.open(p["img"]).convert("RGB"))
            sc=max(cw/thumb.width,fh/thumb.height); thumb=thumb.resize((int(thumb.width*sc),int(thumb.height*sc)),Image.LANCZOS)
            thumb=thumb.crop(((thumb.width-cw)//2,(thumb.height-fh)//2,(thumb.width-cw)//2+cw,(thumb.height-fh)//2+fh))
            im.paste(thumb,(fx,fy))
        else:
            d.rectangle((fx,fy,fx+cw,fy+fh),fill=(28,30,36))
            d.text((fx+cw//2,fy+fh//2-10),p.get("shot","SHOT"),font=EB(40),fill=(90,96,108),anchor="mm")
            d.text((fx+cw//2,fy+fh//2+30),"(frame)",font=MD(20),fill=(70,74,84),anchor="mm")
        # film corner ticks
        for cxx,cyy in [(fx+10,fy+10),(fx+cw-10,fy+10),(fx+10,fy+fh-10),(fx+cw-10,fy+fh-10)]:
            d.line((cxx-8,cyy,cxx+8,cyy),fill=(255,255,255),width=2); d.line((cxx,cyy-8,cxx,cyy+8),fill=(255,255,255),width=2)
        # shot # badge
        d.rounded_rectangle((fx+10,fy+10,fx+58,fy+44),radius=8,fill=ACCENT)
        d.text((fx+34,fy+27),str(p.get("n",i+1)),font=EB(24),fill="white",anchor="mm")
        # caption block
        cy=fy+fh+12
        tag=f"{p.get('shot','')}  ·  {p.get('move','static')}  ·  {p.get('dur','')}s"
        d.text((fx+14,cy),tag.strip(" ·"),font=SB(20),fill=ACCENT)
        desc=textwrap.fill(p.get("desc",""),42)[:160]
        d.multiline_text((fx+14,cy+30),desc,font=RG(20),fill=INK,spacing=4)
        if p.get("vo"):
            vo=textwrap.fill("VO: "+p["vo"],46)[:90]
            d.multiline_text((fx+14,cy+caph-34),vo,font=MD(17),fill=SUB,spacing=2)
    im.save(out); return out

def shotlist_md(panels, out, title="Shot List"):
    L=[f"# {title}","","| # | Shot | Move | Dur | Description | VO / Audio |","|---|---|---|---|---|---|"]
    tot=0
    for p in panels:
        tot+=float(p.get("dur",0) or 0)
        L.append(f"| {p.get('n','')} | {p.get('shot','')} | {p.get('move','')} | {p.get('dur','')}s | {p.get('desc','').replace('|','/')} | {p.get('vo','').replace('|','/')} |")
    L+=["",f"**Total runtime:** ~{tot:.0f}s · **{len(panels)} shots**"]
    open(out,"w").write("\n".join(L)); return out

def animatic(panels, out, W=1920, H=1080, fps=30):
    """Build a timed animatic from panel images (or title-card placeholders)."""
    seg=os.path.dirname(out)+"/_anim_seg"; os.makedirs(seg,exist_ok=True); parts=[]
    for i,p in enumerate(panels):
        d=max(1.0,float(p.get("dur",2) or 2)); df=int(d*fps); sp=f"{seg}/{i:03d}.mp4"
        if p.get("img") and os.path.isfile(p["img"]):
            sw,sh=int(W*1.35),int(H*1.35); z="min(zoom+0.0009,1.10)"
            vf=(f"scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},"
                f"zoompan=z='{z}':d={df}:s={W}x{H}:fps={fps},format=yuv420p,setsar=1")
            src=["-i",p["img"]]; pre=["-frames:v",str(df)]
        else:
            vf=f"drawtext=fontfile={F}Poppins-ExtraBold.ttf:text='{p.get('shot','SHOT')}':fontcolor=white:fontsize={int(H*0.08)}:x=(w-text_w)/2:y=(h-text_h)/2,format=yuv420p"
            src=["-f","lavfi","-i",f"color=c=0x14181c:s={W}x{H}:d={d}:r={fps}"]; pre=[]
        cap=p.get("desc","").replace(":","\\:").replace("'","’")[:60]
        vf+=f",drawbox=x=0:y=ih-90:w=iw:h=90:color=black@0.55:t=fill,drawtext=fontfile={F}Poppins-Medium.ttf:text='{cap}':fontcolor=white:fontsize=34:x=30:y=h-62"
        subprocess.run(["ffmpeg","-y","-loglevel","error",*src,"-vf",vf,*pre,"-r",str(fps),
                        "-c:v","libx264","-crf","20","-preset","medium",sp],check=True)
        parts.append(sp)
    lst=f"{seg}/list.txt"; open(lst,"w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",out],check=True)
    return out

if __name__=="__main__":
    print("storyboard ready: render_board, shotlist_md, animatic")
