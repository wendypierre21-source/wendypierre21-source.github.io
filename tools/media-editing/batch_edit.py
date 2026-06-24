#!/usr/bin/env python3
"""
batch_edit.py — bulk background-removal + compositing for a photoshoot folder.

Pipeline per image:  auto-orient -> rembg AI matte -> green despill -> edge refine
                     -> crop to subject -> contact shadow -> composite on background
                     -> export transparent PNG + composited JPG.

Usage:
  python3 batch_edit.py --in INDIR --out OUTDIR [--bg "#1E6F6B"] [--rotate auto|0|90|180|270]
                        [--height 2000] [--texture] [--transparent-only]

--bg            background hex (gradient+texture+vignette), or a path to a backdrop image,
                or "transparent" (skip composite).
--rotate        'auto' = honor EXIF; or force a fixed rotation for a whole shoot.
--texture       add canvas grain + studio vignette to solid backgrounds.
"""
import argparse, os, glob, numpy as np, cv2
from PIL import Image, ImageOps
from scipy.ndimage import gaussian_filter, binary_erosion
from rembg import remove, new_session

def orient(im, mode):
    im = ImageOps.exif_transpose(im)
    return {"0":im,"90":im.transpose(Image.ROTATE_90),
            "180":im.transpose(Image.ROTATE_180),"270":im.transpose(Image.ROTATE_270)}.get(mode, im)

def matte(im, sess):
    return np.array(remove(im, session=sess))  # RGBA

def despill(rgb):
    r,g,b = rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    return np.stack([r, np.minimum(g,(r+b)/2*1.10), b],2)

def refine(a):
    m = binary_erosion(a>0.5, iterations=2)
    return np.clip(gaussian_filter(m.astype(np.float32),1.4),0,1)

def make_bg(hx, H, W, texture):
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
    fy=ys.max(); bx=xs[ys>fy-0.04*H]
    if len(bx)==0: bx=xs
    fcx=(bx.min()+bx.max())//2; fw=max(bx.max()-bx.min(),W*0.1)
    yy,xx=np.mgrid[0:H,0:W]
    s=np.clip(1-(((xx-fcx)/(fw*0.75))**2+((yy-(fy-2))/(fw*0.16))**2),0,1)*0.55
    return gaussian_filter(s,7)

def process(path, sess, args, outdir):
    im=orient(Image.open(path).convert("RGB"), args.rotate)
    arr=matte(im, sess); a=arr[:,:,3].astype(np.float32)/255.0; rgb=arr[:,:,:3].astype(np.float32)
    rgb=despill(rgb); a=refine(a)
    ys,xs=np.where(a>0.2)
    if len(ys)==0: print("  ! no subject:",os.path.basename(path)); return
    H,W=a.shape; pad=int(0.05*max(H,W))
    y0,y1=max(0,ys.min()-pad),min(H,ys.max()+pad); x0,x1=max(0,xs.min()-pad),min(W,xs.max()+pad)
    rgb,a=rgb[y0:y1,x0:x1],a[y0:y1,x0:x1]; H,W=a.shape
    base=os.path.splitext(os.path.basename(path))[0]
    Image.fromarray(np.dstack([rgb,a*255]).astype("uint8"),"RGBA").save(f"{outdir}/{base}_cutout.png")
    if args.bg!="transparent" and not args.transparent_only:
        if os.path.isfile(args.bg):
            bg=np.array(Image.open(args.bg).convert("RGB").resize((W,H),Image.LANCZOS)).astype(float)
        else:
            bg=make_bg(args.bg,H,W,args.texture)
        sh=shadow_map(a); bg=bg*(1-sh[...,None]*0.85)
        edge=np.clip(gaussian_filter(a,3)-a,0,1)[...,None]
        out=(rgb*(1-edge*0.6)+bg*(edge*0.6))*a[...,None]+bg*(1-a[...,None])
        im2=Image.fromarray(out.astype("uint8"))
        if args.height: im2=im2.resize((int(W*args.height/H),args.height),Image.LANCZOS)
        im2.save(f"{outdir}/{base}_composited.jpg",quality=90)
    print("  ok:",base)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--in",dest="indir",required=True); ap.add_argument("--out",dest="outdir",required=True)
    ap.add_argument("--bg",default="#1E6F6B"); ap.add_argument("--rotate",default="auto")
    ap.add_argument("--height",type=int,default=2000); ap.add_argument("--texture",action="store_true")
    ap.add_argument("--transparent-only",action="store_true")
    a=ap.parse_args(); os.makedirs(a.outdir,exist_ok=True)
    files=sorted(sum([glob.glob(os.path.join(a.indir,e)) for e in ("*.jpg","*.jpeg","*.png","*.JPG","*.JPEG","*.PNG")],[]))
    print(f"{len(files)} images -> {a.outdir}  (bg={a.bg}, rotate={a.rotate}, texture={a.texture})")
    sess=new_session("u2net")
    for f in files: process(f,sess,a,a.outdir)
    print("DONE")
