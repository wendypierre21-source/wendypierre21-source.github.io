# Capability & Contingency Playbook — Media Editing + Generative AI

**Principle: Smarter, not harder.** Do everything non-generative *locally for free*. Reach for
generative AI only when the task truly needs it — via connectors (credits) or your own GPU.

---

## 1. LOCAL toolkit (free, CPU, no models — runs in any session)

### Photo — `editkit.py`  (numpy · scipy · OpenCV · Pillow)
| Technique | Function |
|---|---|
| Object/blemish removal (classical) | `inpaint()` — great for small distractions; **not** large generative fills |
| Natural skin retouch | `skin_retouch()` — edge-preserving smooth + spot-heal, skin-masked, features protected |
| Tone correction | `tone_curve()` — shadow lift / highlight roll-off / S-curve |
| Light-wrap / rim | `contre_jour()` — warm rim to blend a subject into a scene |
| Masking | `feather()`; film grain `grain()` |
| Compositing, color grade, scaling | Pillow/numpy (as used for the ads) |

### Video — `vidkit.py`  (ffmpeg)
| Technique | Function |
|---|---|
| Reframe 16:9 / 9:16 / 1:1 | `to_ratio()` (cover-crop or blurred-pillarbox) |
| Stabilization (shake removal) | `stabilize()` — two-pass vidstab, tunable |
| Ken Burns from stills | `kenburns()` |
| Motor-drive burst montage | (skate-edit builder) |
| Crossfade assembly | xfade chain |
| Color grade / grain | `grade()`, `grain()` (editkit) |
| Speed ramp / trim | `speed()`, `trim()` |
| Layered audio (bed + SFX + duck) | `mix_audio()` — remux, no re-encode |
| Frame grabs / contact sheets | `thumbnail()` |

### Design (programmatic, free)
Pillow-built posters/ads/title cards/templates (e.g., the farmers-market `make_post.py`).

---

## 2. GENERATIVE layer (when local can't — pick the cheapest that works)

| Need | Route | Cost | Notes |
|---|---|---|---|
| Image generate/edit, inpaint, video, audio, 3D, upscale, outpaint, remove-bg, reframe | **Higgsfield (MCP)** | credits | Already wired in this session; I preflight cost first |
| Design / decks / social posts | **Canva, Gamma (MCP)** | acct | Already wired in |
| Heavy generative inpaint / batch SD / LoRA | **Your Mac ComfyUI** | free | GPU + models you own; I supply ready-to-run recipes |
| Quick free generate (no credits) | **HuggingFace Spaces, Bing/Copilot (DALL·E 3), Perplexity, Runway, Descript** | free tier | You run; I write the prompts/specs |

> Why no local Stable Diffusion here: no GPU + HuggingFace/Civitai blocked. Installing it would be a dead end — the connectors above are the smart substitute.

---

## 3. CONTINGENCY DECISION MATRIX  ("I want to…")

- **Retouch a portrait / fix skin, tone, blend** → `editkit` here. ✅ free
- **Cut / stabilize / reframe / score a video** → `vidkit` here. ✅ free
- **Remove a small distraction from a photo** → `editkit.inpaint()`. ✅ free
- **Remove a *large* subject & rebuild background** → generative inpaint → **Mac ComfyUI** (free) or **Higgsfield** (credits).
- **Generate a brand-new image/scene** → Higgsfield (credits) / Bing-DALL·E or HF Space (free).
- **Generate / extend video** → Higgsfield (credits) / Runway (free tier).
- **Voiceover / TTS** → Edge-TTS locally (free, per Hyperion) or Higgsfield audio.
- **Design a poster/post** → Pillow here (free) or Canva/Gamma (MCP).

---

## 4. RESEARCH & RESOURCE KIT (your stack)

**Source hierarchy:** Google / **JSTOR** (scholarly) · **Anna's Archive** (books) · **YouTube**
(how-to + inspiration) · **Reddit** (niche depth) · **TikTok** (fast leads → verify on the above).

**Browser extensions:** OneTab (tab condense) · Honey (coupons) · Google Dictionary (double-click
define) · LastPass (passwords) · Adblock Plus · Evernote Web Clipper · Pocket (read-later) ·
Google Translate.

**Free AI alternatives:** Perplexity (search) · HuggingFace (models) · Bing/Copilot (free + DALL·E 3)
· Jasper / Copy.ai (copy) · Runway (text→video) · Murf (TTS) · Reclaim (calendar) · Beautiful.ai
(decks) · Descript (media editing) · browse.ai (competitor scrape) · you.com (discovery) ·
adcreative.ai · namelix (naming).

**Prompt library** (saved separately): email drafting, meeting summary, presentation outline, bio,
résumé, interview prep, growth plan, project proposal, feedback request, LinkedIn outreach,
mistake-analysis, question-generation, book summary, ELI5, concept-linking, Eisenhower
prioritization, meta-prompting.

---

*Toolkits live at `/tmp/edit/` this session (editkit.py, vidkit.py). They reinstall in seconds
in any new session: `pip install numpy scipy opencv-python-headless Pillow` + the ffmpeg static build.*
