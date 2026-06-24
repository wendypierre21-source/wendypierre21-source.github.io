#!/usr/bin/env python3
"""
batch_edit.py — bulk background-removal + compositing + studio lighting.

Pipeline per image:  auto-orient -> rembg AI matte -> green despill -> edge refine
                     -> crop -> background -> studio LIGHTING (spotlight + relight +
                     rim) -> contact shadow -> export transparent PNG + composited JPG.

Usage:
  python3 batch_edit.py --in INDIR --out OUTDIR [--bg "#1E6F6B"] [--light soft]
                        [--rotate auto|0|90|180|270] [--height 2000] [--texture]
                        [--transparent-only]

--light : one of  none soft studio side_left side_right butterfly split backlit
          rim moody high_key spotlight   — OR  'all' to render every look per photo.
--bg    : hex (gradient+texture+vignette), a backdrop image path, or 'transparent'.
"""
import argparse, os, glob, numpy as np
from PIL import Image, ImageOps
from scipy.ndimage import gaussian_filter, binary_erosion
from rembg import remove, new_session

# ---- lighting presets: spot=(cx,cy,amt) dark=bg mult  key=(dx,dy,amp,ambient)
#      rim=(side,strength)  glow=warm edge-glow (backlight) ----
LIGHTS = {
 "none":       dict(spot=(.5,.5,0.0), dark=1.00, key=(0,0,0.0,1.0),     rim=(0,0.0),  glow=0.0),
 "soft":       dict(spot=(.50,.38,.55), dark=.64, key=(0,-.5,.5,.85),   rim=(0,0.0),  glow=0.0),
 "studio":     dict(spot=(.50,.40,.50), dark=.68, key=(0,-.4,.4,.88),   rim=(0,0.0),  glow=0.0),
 "side_left":  dict(spot=(.34,.34,.60), dark=.56, key=(-.7,-.3,.6,.70), rim=(-1,.50), glow=0.0),
 "side_right": dict(spot=(.66,.34,.60), dark=.56, key=(.7,-.3,.6,.70),  rim=(1,.50),  glow=0.0),
 "butterfly":  dict(spot=(.50,.30,.62), dark=.60, key=(0,-.8,.55,.80),  rim=(0,0.0),  glow=0.0),
 "split":      dict(spot=(.30,.40,.55), dark=.50, key=(-.95,0,.75,.55), rim=(-1,.45), glow=0.0),
 "backlit":    dict(spot=(.50,.33,.85), dark=.50, key=(0,-.4,.35,.78),  rim=(0,0.0),  glow=0.60),
 "rim":        dict(spot=(.50,.40,.45), dark=.70, key=(0,0,0.0,1.0),    rim=(0,0.0),  glow=0.55),
 "moody":      dict(spot=(.42,.30,.70), dark=.32, key=(-.6,-.4,.7,.55), rim=(-1,.55), glow=0.0),
 "high_key":   dict(spot=(.50,.40,1.0), dark=.92, key=(0,-.4,.35,1.0),  rim=(0,0.0),  glow=0.0),
 "spotlight":  dict(spot=(.50,.40,.95), dark=.30, key=(0,-.4,.5,.70),   rim=(0,0.0),  glow=0.0),
}
WARM = np.array([255,240,210])

def orient(im, mode):
    im = ImageOps.exif_transpose(im)
    return {"0":im,"90":im.transpose(Image.ROTATE_90),
            "180":im.transpose(Image.ROTATE_180),"270":im.transpose(Image.ROTATE_270)}.get(mode, im)

def despill(rgb):
    r,g,b = rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    return np.stack([r, np.minimum(g,(r+b)/2*1.10), b],2)

def refine(a):
    m = binary_erosion(a>0.5, iterations=2)
    return np.clip(gaussian_filter(m.astype(np.float32),1.4),0,1)

def make_bg(hx,H,W,texture):
    col=np.array([int(hx[1:][k:k+2],16) for k in (0,2,4)],float)
    bg=np.zeros((H,W,3),float)
    for y in range(H):
        t=y/H; bg[y,:]=col*(1-0.18*t)+(col*0.6)*(0.18*t)
    if texture:
        rng=np.random.default_rng(3)
        tex=gaussian_filter(rng.normal(0,1,(H,W)),0.7)*0.025+gaussian_filter(rng.normal(0,1,(H,W)),9)*0.05
        vy,vx=np.mgrid[0:H,0:W]; rad=np.sqrt(((vx-W/2)/(W*0.62))**2+((vy-H/2)/(H*0.62))**2)
        vig=np.clip(1-0.16*np.clip(rad-0.4,0,1)*1.6,0.7,1)
        bg=bg*(1+tex[...,None])*vig[...,None]
    return np.clip(bg,0,255)

def shadow_map(a):
    H,W=a.shape; ys,xs=np.where(a>0.3)
    if len(ys)==0: return np.zeros((H,W))
    fy=ys.max(); bx=xs[ys>fy-0.04*H]; bx=bx if len(bx) else xs
    fcx=(bx.min()+bx.max())//2; fw=max(bx.max()-bx.min(),W*0.1)
    yy,xx=np.mgrid[0:H,0:W]
    return gaussian_filter(np.clip(1-(((xx-fcx)/(fw*0.75))**2+((yy-(fy-2))/(fw*0.16))**2),0,1)*0.55,7)

def light_composite(rgb,a,L,bg_base):
    H,W=a.shape; yy,xx=np.mgrid[0:H,0:W]; nx=(xx-W/2)/(W/2); ny=(yy-H/2)/(H/2)
    edge=np.clip(gaussian_filter(a,3)-a,0,1)
    scx,scy,samt=L["spot"]; bg=bg_base*L["dark"]
    r=np.sqrt(((xx-scx*W)/(W*0.55))**2+((yy-scy*H)/(H*0.55))**2)
    bg=np.clip(bg*(1+(np.clip(1-r,0,1)**1.5*samt)[...,None]),0,255)
    sh=shadow_map(a); bg=bg*(1-sh[...,None]*0.85)
    dx,dy,amp,amb=L["key"]; lm=np.clip(0.5+0.5*(nx*dx+ny*dy),0,1)
    lit=np.clip(rgb*(amb+amp*lm)[...,None],0,255)
    if L["glow"]>0: lit=np.clip(lit+edge[...,None]*L["glow"]*WARM,0,255)
    side,strn=L["rim"]
    if strn>0:
        m=np.clip(nx*side+0.2,0,1); lit=np.clip(lit+(edge*m*strn)[...,None]*WARM,0,255)
    body=lit*(1-edge[...,None]*0.5)+bg*(edge[...,None]*0.5)
    return (body*a[...,None]+bg*(1-a[...,None])).astype("uint8")

def process(path, sess, args, outdir):
    im=orient(Image.open(path).convert("RGB"), args.rotate)
    arr=np.array(remove(im, session=sess)); a=arr[:,:,3].astype(np.float32)/255.0
    rgb=despill(arr[:,:,:3].astype(np.float32)); a=refine(a)
    ys,xs=np.where(a>0.2)
    if len(ys)==0: print("  ! no subject:",os.path.basename(path)); return
    H,W=a.shape; pad=int(0.05*max(H,W))
    y0,y1=max(0,ys.min()-pad),min(H,ys.max()+pad); x0,x1=max(0,xs.min()-pad),min(W,xs.max()+pad)
    rgb,a=rgb[y0:y1,x0:x1],a[y0:y1,x0:x1]; H,W=a.shape
    base=os.path.splitext(os.path.basename(path))[0]
    Image.fromarray(np.dstack([rgb,a*255]).astype("uint8"),"RGBA").save(f"{outdir}/{base}_cutout.png")
    if args.bg=="transparent" or args.transparent_only: print("  ok:",base); return
    bg=(np.array(Image.open(args.bg).convert("RGB").resize((W,H),Image.LANCZOS)).astype(float)
        if os.path.isfile(args.bg) else make_bg(args.bg,H,W,args.texture))
    styles=list(LIGHTS) if args.light=="all" else [args.light]
    for st in styles:
        out=light_composite(rgb,a,LIGHTS.get(st,LIGHTS["soft"]),bg)
        im2=Image.fromarray(out)
        if args.height: im2=im2.resize((int(W*args.height/H),args.height),Image.LANCZOS)
        suffix=f"_{st}" if args.light=="all" else ""
        im2.save(f"{outdir}/{base}{suffix}_composited.jpg",quality=90)
    print("  ok:",base, f"({len(styles)} look{'s' if len(styles)>1 else ''})")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--in",dest="indir",required=True); ap.add_argument("--out",dest="outdir",required=True)
    ap.add_argument("--bg",default="#1E6F6B"); ap.add_argument("--rotate",default="auto")
    ap.add_argument("--light",default="soft",help="none/soft/studio/side_left/side_right/butterfly/split/backlit/rim/moody/high_key/spotlight/all")
    ap.add_argument("--height",type=int,default=2000); ap.add_argument("--texture",action="store_true")
    ap.add_argument("--transparent-only",action="store_true")
    a=ap.parse_args(); os.makedirs(a.outdir,exist_ok=True)
    files=sorted(sum([glob.glob(os.path.join(a.indir,e)) for e in ("*.jpg","*.jpeg","*.png","*.JPG","*.JPEG","*.PNG")],[]))
    print(f"{len(files)} imgs -> {a.outdir} (bg={a.bg}, light={a.light}, rotate={a.rotate}, texture={a.texture})")
    sess=new_session("u2net")
    for f in files: process(f,sess,a,a.outdir)
    print("DONE")
