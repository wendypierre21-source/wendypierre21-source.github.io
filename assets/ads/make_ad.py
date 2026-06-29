#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math

UP = "/root/.claude/uploads/644cc963-89b0-58cf-ad81-a41d20963af8/"
FONT = "/tmp/adfonts/"

# ---- palette ----
GREEN      = (34, 110, 49)      # deep brand green
GREEN_DK   = (24, 82, 36)
GREEN_LT   = (74, 150, 70)
CREAM      = (250, 246, 235)
CREAM_DK   = (243, 236, 218)
ORANGE     = (240, 150, 30)     # harvest accent
INK        = (40, 46, 38)
WHITE      = (255, 255, 255)

W, H = 1080, 1350

def f(name, size):
    return ImageFont.truetype(FONT + name, size)

ExtraBold = lambda s: f("Poppins-ExtraBold.ttf", s)
Bold      = lambda s: f("Poppins-Bold.ttf", s)
Semi      = lambda s: f("Poppins-SemiBold.ttf", s)
Med       = lambda s: f("Poppins-Medium.ttf", s)
Reg       = lambda s: f("Poppins-Regular.ttf", s)

canvas = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(canvas)

# ============================================================
# HERO PHOTO (top)
# ============================================================
HERO_H = 600
hero = Image.open(UP + "a9fa03fc-IMG_2114.jpeg").convert("RGB")
hero = ImageOps.exif_transpose(hero)
# cover-crop to W x HERO_H
scale = max(W / hero.width, HERO_H / hero.height)
hero = hero.resize((int(hero.width*scale), int(hero.height*scale)), Image.LANCZOS)
left = (hero.width - W)//2
top  = (hero.height - HERO_H)//2
hero = hero.crop((left, top, left+W, top+HERO_H))

# subtle top gradient for badge legibility + slight bottom shade
grad = Image.new("L", (1, HERO_H), 0)
for y in range(HERO_H):
    t = y/HERO_H
    # darker at very top (badge) and a touch at bottom
    v = int(150*max(0,(0.30-t)/0.30)) + int(60*max(0,(t-0.78)/0.22))
    grad.putpixel((0,y), min(v,180))
grad = grad.resize((W, HERO_H))
shade = Image.new("RGB",(W,HERO_H),(10,30,12))
hero = Image.composite(shade, hero, grad)
canvas.paste(hero, (0,0))

# ============================================================
# GREEN BODY PANEL with angled top edge
# ============================================================
panel_top = HERO_H - 46
body = Image.new("RGBA",(W,H),(0,0,0,0))
bd = ImageDraw.Draw(body)
# angled polygon: left lower, right higher (dynamic cut)
bd.polygon([(0, panel_top+46),(W, panel_top-46),(W,H),(0,H)], fill=CREAM+(255,))
canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), body).convert("RGB"),(0,0))
d = ImageDraw.Draw(canvas)

# ============================================================
# TOP BADGE : "ONE WEEK TO OPENING DAY"
# ============================================================
def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)

btxt = "ONE WEEK TO OPENING DAY"
bf = ExtraBold(30)
tb = d.textbbox((0,0), btxt, font=bf)
bw = tb[2]-tb[0]
pad = 30
bh = 64
bx0 = 48
by0 = 44
rounded(d,(bx0,by0,bx0+bw+pad*2+50,by0+bh), bh//2, ORANGE)
# little dot
d.ellipse((bx0+24,by0+bh//2-7,bx0+38,by0+bh//2+7), fill=WHITE)
d.text((bx0+54,by0+bh//2), btxt, font=bf, fill=WHITE, anchor="lm")

# ============================================================
# LOGO emblem — circular, overlapping hero / panel seam
# ============================================================
logo = Image.open(UP + "2cac560f-IMG_2112.jpeg").convert("RGB")
LSZ = 250
logo = logo.resize((LSZ-24, LSZ-24), Image.LANCZOS)
# white circle backing with green ring
ring = Image.new("RGBA",(LSZ,LSZ),(0,0,0,0))
rd = ImageDraw.Draw(ring)
rd.ellipse((0,0,LSZ-1,LSZ-1), fill=WHITE)
# mask the logo into circle
mask = Image.new("L",(LSZ-24,LSZ-24),0)
ImageDraw.Draw(mask).ellipse((0,0,LSZ-25,LSZ-25), fill=255)
ring.paste(logo,(12,12),mask)
rd = ImageDraw.Draw(ring)
rd.ellipse((4,4,LSZ-5,LSZ-5), outline=GREEN, width=8)
# soft shadow
sh = Image.new("RGBA",(W,H),(0,0,0,0))
ImageDraw.Draw(sh).ellipse((W-48-LSZ+6, panel_top-LSZ//2+10, W-48+6, panel_top+LSZ//2+10), fill=(0,0,0,70))
sh = sh.filter(ImageFilter.GaussianBlur(12))
canvas = Image.alpha_composite(canvas.convert("RGBA"), sh)
canvas.paste(ring,(W-48-LSZ, panel_top-LSZ//2), ring)
canvas = canvas.convert("RGB")
d = ImageDraw.Draw(canvas)

# ============================================================
# TITLE
# ============================================================
y = panel_top + 80
d.text((56, y), "FRAMINGHAM", font=ExtraBold(76), fill=GREEN_DK)
y += 78
d.text((56, y), "FARMERS MARKET", font=ExtraBold(76), fill=GREEN)
y += 100
# accent rule
d.rounded_rectangle((58,y,58+150,y+9), radius=5, fill=ORANGE)
y += 34

# ============================================================
# INFO ROWS with icons
# ============================================================
ICON = GREEN
def icon_circle(cx, cy, r):
    d.ellipse((cx-r,cy-r,cx+r,cy+r), fill=(233,242,230))
LX = 58
TXX = 150
rowgap = 104
iconR = 40

def draw_calendar(cx,cy):
    s=34
    d.rounded_rectangle((cx-s, cy-s+6, cx+s, cy+s), radius=7, outline=GREEN, width=6)
    d.line((cx-s, cy-s+22, cx+s, cy-s+22), fill=GREEN, width=6)
    d.line((cx-16, cy-s-2, cx-16, cy-s+12), fill=GREEN, width=6)
    d.line((cx+16, cy-s-2, cx+16, cy-s+12), fill=GREEN, width=6)

def draw_clock(cx,cy):
    r=34
    d.ellipse((cx-r,cy-r,cx+r,cy+r), outline=GREEN, width=6)
    d.line((cx,cy,cx,cy-20), fill=GREEN, width=6)
    d.line((cx,cy,cx+15,cy+8), fill=GREEN, width=6)

def draw_pin(cx,cy):
    r=26
    d.ellipse((cx-r,cy-r-6,cx+r,cy+r-6), outline=GREEN, width=6)
    d.polygon([(cx-18,cy+8),(cx+18,cy+8),(cx,cy+38)], fill=GREEN)
    d.ellipse((cx-9,cy-15,cx+9,cy+3), fill=CREAM)

rows = [
    (draw_calendar, "EVERY THURSDAY", "June 18  –  October 8, 2026"),
    (draw_clock,    "3:00 – 7:00 PM", "Rain or shine, all season long"),
    (draw_pin,      "FRAMINGHAM CENTRE COMMON", "2 Oak Street, Framingham, MA 01701"),
]
ry = y + 14
for icon, big, small in rows:
    icon_circle(LX+iconR, ry+iconR, iconR+12)
    icon(LX+iconR, ry+iconR)
    d.text((LX+iconR*2+42, ry+6), big, font=Bold(38), fill=INK)
    d.text((LX+iconR*2+42, ry+54), small, font=Med(29), fill=(95,105,92))
    ry += rowgap

# ============================================================
# FOOTER STRIP : who you'll find
# ============================================================
FOOT_H = 150
fy = H - FOOT_H
d.rectangle((0, fy, W, H), fill=GREEN)
d.text((W//2, fy+54), "FARMS · FOOD TRUCKS · BAKERIES · ARTISANS",
       font=Bold(31), fill=WHITE, anchor="mm")
d.text((W//2, fy+104), "Locally grown  ·  Locally made  ·  Locally loved",
       font=Med(27), fill=(206,230,200), anchor="mm")

canvas.save("/tmp/framingham_ad.png")
print("saved", canvas.size)
