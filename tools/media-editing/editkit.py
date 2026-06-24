#!/usr/bin/env python3
"""
editkit.py — local CPU image-editing toolkit (no GPU, no models).
Encodes the proven moves from prior photo-editing sessions:
  - classical object removal (OpenCV inpaint)
  - natural skin retouch (edge-preserving smooth + blemish spot-heal, features protected)
  - tone curve (shadow lift / highlight roll-off)
  - contre-jour rim softening / light wrap
  - feathered masking + film grain
Stack: numpy + scipy + opencv + Pillow.
"""
import numpy as np, cv2
from PIL import Image
from scipy.ndimage import gaussian_filter, binary_dilation

def load(p):  return cv2.cvtColor(np.array(Image.open(p).convert("RGB")), cv2.COLOR_RGB2BGR)
def save(img, p): Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).save(p); return p

def feather(mask, px=25):
    m = gaussian_filter(mask.astype(np.float32), px)
    return np.clip(m/ (m.max() or 1), 0, 1)

def inpaint(img, mask, radius=12, method="telea"):
    """Remove masked region, fill from surroundings. mask: uint8 0/255."""
    flag = cv2.INPAINT_TELEA if method=="telea" else cv2.INPAINT_NS
    return cv2.inpaint(img, (mask>0).astype(np.uint8)*255, radius, flag)

def tone_curve(img, shadow_lift=0.06, highlight_rolloff=0.05):
    x = img.astype(np.float32)/255.0
    x = shadow_lift + x*(1-shadow_lift)              # raise blacks
    x = x*(1-highlight_rolloff) + highlight_rolloff*(x**0.5)  # soft whites
    # gentle S-curve anchored at 0.5
    x = np.clip(0.5 + (x-0.5)*1.06, 0, 1)
    return (x*255).astype(np.uint8)

def skin_retouch(img, strength=0.5, blemish=True):
    """Edge-preserving smooth blended only into skin; keeps eyes/lips via texture mask."""
    out = img.copy()
    if blemish:                                      # spot-heal: median removes small specks
        med = cv2.medianBlur(out, 5)
        diff = cv2.absdiff(out, med).max(2)
        spots = (diff > 18).astype(np.uint8)
        spots = binary_dilation(spots, iterations=1).astype(np.uint8)*255
        out = cv2.inpaint(out, spots, 3, cv2.INPAINT_TELEA)
    smooth = cv2.bilateralFilter(out, 9, 60, 60)     # edge-preserving
    # skin mask (YCrCb) so we don't smear background/eyes
    ycc = cv2.cvtColor(out, cv2.COLOR_BGR2YCrCb)
    cr, cb = ycc[:,:,1], ycc[:,:,2]
    skin = ((cr>133)&(cr<180)&(cb>77)&(cb<127)).astype(np.float32)
    skin = gaussian_filter(skin, 4)[...,None]*strength
    return (out*(1-skin) + smooth*skin).astype(np.uint8)

def contre_jour(img, mask, warm=(0.18,0.32,0.55), rim=0.5):
    """Soft warm rim wrapping the subject edge (sun behind)."""
    m = (mask>0).astype(np.float32)
    edge = np.clip(gaussian_filter(m,4) - gaussian_filter(m,9), 0, 1)
    edge = (edge/ (edge.max() or 1))[...,None]
    glow = np.array(warm[::-1])*255  # BGR
    return np.clip(img.astype(np.float32) + edge*glow*rim, 0, 255).astype(np.uint8)

def grain(img, amount=0.04):
    n = np.random.default_rng(7).normal(0, 255*amount, img.shape)
    return np.clip(img.astype(np.float32)+n, 0, 255).astype(np.uint8)

if __name__ == "__main__":
    print("editkit ready:", [f for f in dir() if not f.startswith("_")])
