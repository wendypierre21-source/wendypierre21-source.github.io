#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
UP="/root/.claude/uploads/644cc963-89b0-58cf-ad81-a41d20963af8/"
FONT="/tmp/adfonts/"
GREEN=(28,98,44); GREEN_DK=(17,60,29); GREEN_BR=(46,140,66); ORANGE=(242,150,28)
WHITE=(255,255,255); CREAM=(250,246,235); INK=(40,52,40); GRAY=(95,110,95)
def f(n,s): return ImageFont.truetype(FONT+n,s)
EB=lambda s:f("Poppins-ExtraBold.ttf",s); BD=lambda s:f("Poppins-Bold.ttf",s)
SB=lambda s:f("Poppins-SemiBold.ttf",s); MD=lambda s:f("Poppins-Medium.ttf",s)
def spaced(t,n=2): return (" "*n).join(list(t))

W=H=1080
cv=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(cv)

# ---- HERO (top) ----
HERO=540
hero=ImageOps.exif_transpose(Image.open(UP+"a9fa03fc-IMG_2114.jpeg").convert("RGB"))
sc=max(W/hero.width,HERO/hero.height)
hero=hero.resize((int(hero.width*sc),int(hero.height*sc)),Image.LANCZOS)
hero=hero.crop(((hero.width-W)//2,(hero.height-HERO)//2,(hero.width-W)//2+W,(hero.height-HERO)//2+HERO))
cv.paste(hero,(0,0))

# ---- OPEN TODAY tab on hero (top-left) ----
d=ImageDraw.Draw(cv)
tf=EB(34); tt="OPEN TODAY"; tw=d.textlength(tt,font=tf)
d.rounded_rectangle((40,36,40+tw+64,36+66),radius=33,fill=ORANGE)
d.ellipse((40+26,36+25,40+42,36+41),fill=WHITE)
d.text((40+56,36+33),tt,font=tf,fill=WHITE,anchor="lm")

# ---- LOGO badge at seam (right) ----
L=210
logo=Image.open(UP+"4824ed75-IMG_2112.jpeg").convert("RGB").resize((L-20,L-20),Image.LANCZOS)
ring=Image.new("RGBA",(L,L),(0,0,0,0)); rd=ImageDraw.Draw(ring)
rd.ellipse((0,0,L-1,L-1),fill=WHITE); m=Image.new("L",(L-20,L-20),0)
ImageDraw.Draw(m).ellipse((0,0,L-21,L-21),fill=255); ring.paste(logo,(10,10),m)
rd.ellipse((3,3,L-4,L-4),outline=GREEN,width=6)
sh=Image.new("RGBA",(W,H),(0,0,0,0))
ImageDraw.Draw(sh).ellipse((W-48-L+6,HERO-L//2+10,W-48+6,HERO+L//2+10),fill=(0,0,0,70))
cv=Image.alpha_composite(cv.convert("RGBA"),sh.filter(ImageFilter.GaussianBlur(12)))
cv.paste(ring,(W-48-L,HERO-L//2),ring); cv=cv.convert("RGB"); d=ImageDraw.Draw(cv)

# ---- TITLE ----
y=HERO+78
d.text((56,y),"FRAMINGHAM",font=EB(62),fill=GREEN_DK); y+=64
d.text((56,y),"FARMERS MARKET",font=EB(62),fill=GREEN);  y+=86
d.rounded_rectangle((58,y,58+140,y+8),radius=4,fill=ORANGE); y+=34

# ---- INFO ROWS with simple icons ----
def cal(cx,cy):
    s=22; d.rounded_rectangle((cx-s,cy-s+5,cx+s,cy+s),radius=5,outline=GREEN,width=5)
    d.line((cx-s,cy-s+16,cx+s,cy-s+16),fill=GREEN,width=5)
def clock(cx,cy):
    r=22; d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=GREEN,width=5)
    d.line((cx,cy,cx,cy-12),fill=GREEN,width=5); d.line((cx,cy,cx+9,cy+5),fill=GREEN,width=5)
def pin(cx,cy):
    r=16; d.ellipse((cx-r,cy-r-4,cx+r,cy+r-4),outline=GREEN,width=5)
    d.polygon([(cx-11,cy+5),(cx+11,cy+5),(cx,cy+24)],fill=GREEN)
    d.ellipse((cx-6,cy-10,cx+6,cy+2),fill=CREAM)
rows=[(cal,"EVERY THURSDAY · 3–7 PM","June 18 – October 8  ·  Rain or shine, all season long"),
      (pin,"FRAMINGHAM CENTRE COMMON","2 Oak Street, Framingham, MA 01701")]
ry=y+12
for ic,big,small in rows:
    d.ellipse((56,ry,56+58,ry+58),fill=(233,242,230)); ic(56+29,ry+29)
    d.text((140,ry-2),big,font=BD(33),fill=INK)
    d.text((140,ry+38),small,font=MD(24),fill=GRAY)
    ry+=92

# ---- FOOTER strip ----
FB=86
d.rectangle((0,H-FB,W,H),fill=GREEN)
d.text((W//2,H-FB+FB*0.33),"FARMS · FOOD TRUCKS · BAKERIES · ARTISANS",font=BD(27),fill=WHITE,anchor="mm")
d.text((W//2,H-FB+FB*0.72),"Locally grown · Locally made · Locally loved",font=MD(22),fill=(208,226,204),anchor="mm")

cv.save("/tmp/fm/fm_today_square.png"); print("saved",cv.size)
