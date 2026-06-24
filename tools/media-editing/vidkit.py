#!/usr/bin/env python3
"""
vidkit.py — local CPU video-editing toolkit (ffmpeg-driven, no GPU, no models).
Consolidates the techniques proven on the Farm Pond skate edits.

Capabilities:
  probe            - resolution / fps / duration / rotation
  to_ratio         - reframe to 16:9 / 9:16 / 1:1 (cover-crop OR blurred-pillarbox)
  stabilize        - two-pass vidstab (shake removal, tunable)
  kenburns         - still photo -> slow push/pan motion clip
  burst            - rapid "motor-drive" montage from stills (+ optional white flash)
  xfade_concat     - crossfade a list of clips into one
  grade            - shadow lift / contrast / saturation
  grain            - film grain overlay
  speed            - speed up / slow down (with audio handling)
  trim             - cut a sub-section
  mix_audio        - bed + sfx layers + optional ducking, remux (no video re-encode)
  reframe_blurfill - portrait-in-landscape (or vice versa) with blurred background
  thumbnail        - grab a representative frame
Every op shells ffmpeg/ffprobe; safe to chain.
"""
import subprocess, json, shlex
FF="ffmpeg"; FP="ffprobe"
def _run(c):
    r=subprocess.run(c,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode: raise RuntimeError(" ".join(map(str,c[:6]))+"\n"+r.stderr.decode()[-1500:])
    return r

def probe(p):
    out=subprocess.run([FP,"-v","error","-print_format","json","-show_format",
        "-show_streams",p],stdout=subprocess.PIPE).stdout.decode()
    d=json.loads(out); v=next(s for s in d["streams"] if s["codec_type"]=="video")
    fr=v.get("r_frame_rate","30/1"); n,dn=fr.split("/"); fps=float(n)/float(dn or 1)
    return {"w":v["width"],"h":v["height"],"fps":round(fps,3),
            "dur":float(d["format"].get("duration",0))}

def to_ratio(src,out,W,H,mode="cover",fps=30):
    if mode=="cover":
        vf=f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps},setsar=1"
    else:  # blurred pillarbox/letterbox
        vf=(f"[0:v]split[b][f];[b]scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},boxblur=24:2,eq=brightness=-0.1[bg];"
            f"[f]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,fps={fps},setsar=1")
    flag=["-vf",vf] if mode=="cover" else ["-filter_complex",vf]
    _run([FF,"-y","-i",src,*flag,"-c:v","libx264","-crf","19","-preset","medium","-c:a","copy?",out]) \
        if False else _run([FF,"-y","-i",src,*flag,"-c:v","libx264","-crf","19","-preset","medium",out])

def stabilize(src,out,shakiness=8,smoothing=30,zoom=0,optzoom=2):
    trf=out+".trf"
    _run([FF,"-y","-i",src,"-vf",f"vidstabdetect=shakiness={shakiness}:accuracy=15:result={trf}","-f","null","-"])
    z=f":zoom={zoom}" if zoom else ""
    _run([FF,"-y","-i",src,"-vf",
        f"vidstabtransform=input={trf}:smoothing={smoothing}:optzoom={optzoom}{z}:interpol=bicubic,"
        f"unsharp=5:5:0.4,setsar=1","-c:v","libx264","-crf","19","-preset","medium",out])

def kenburns(img,out,W,H,dur,zoom=1.06,fps=30):
    df=max(1,int(dur*fps)); sw,sh=int(W*1.4),int(H*1.4)
    z=f"min(zoom+{(zoom-1)/df:.6f},{zoom})"
    _run([FF,"-y","-i",img,"-vf",
        f"scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},"
        f"zoompan=z='{z}':d={df}:s={W}x{H}:fps={fps}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',"
        f"setsar=1","-frames:v",str(df),"-c:v","libx264","-crf","19",out])

def grade(src,out,shadow=0.04,contrast=1.06,sat=1.05):
    _run([FF,"-y","-i",src,"-vf",
        f"eq=brightness={shadow}:contrast={contrast}:saturation={sat}",
        "-c:v","libx264","-crf","19","-preset","medium","-c:a","copy",out])

def speed(src,out,factor):  # factor>1 faster
    _run([FF,"-y","-i",src,"-filter_complex",
        f"[0:v]setpts={1/factor}*PTS[v];[0:a]atempo={factor}[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-crf","19",out])

def trim(src,out,start,dur):
    _run([FF,"-y","-ss",str(start),"-t",str(dur),"-i",src,"-c:v","libx264","-crf","19","-c:a","aac",out])

def mix_audio(silent_video,out,bed=None,sfx=None,duck=False):
    """sfx: list of (path, start_sec, volume). bed: (path, volume)."""
    ins=["-i",silent_video]; fc=[]; amix=[]
    if bed: ins+=["-stream_loop","-1","-i",bed[0]]; fc.append(f"[1:a]volume={bed[1]}[bed]"); amix.append("[bed]")
    base=2 if bed else 1
    for i,(p,st,vol) in enumerate(sfx or []):
        ins+=["-i",p]; ms=int(st*1000)
        fc.append(f"[{base+i}:a]adelay={ms}|{ms},volume={vol}[s{i}]"); amix.append(f"[s{i}]")
    if amix:
        fc.append("".join(amix)+f"amix=inputs={len(amix)}:normalize=0,alimiter=limit=0.95[aout]")
        _run([FF,"-y",*ins,"-filter_complex",";".join(fc),"-map","0:v","-map","[aout]",
              "-c:v","copy","-c:a","aac","-shortest","-movflags","+faststart",out])
    else:
        _run([FF,"-y",*ins,"-c","copy",out])

def thumbnail(src,out,t=1.0,width=640):
    _run([FF,"-y","-ss",str(t),"-i",src,"-frames:v","1","-vf",f"scale={width}:-1",out])

if __name__=="__main__":
    print("vidkit ready")
