# Storyboard & Pre-Viz Guide  (terminal = storyboard expert)

Turn a concept into a planned visual sequence: **shot list → storyboard sheet → animatic → edit.**
Tool: `storyboard.py` (`render_board`, `shotlist_md`, `animatic`) — pairs with `vidkit.py`/`editkit.py`.

## The pipeline
1. **Break the idea into shots** (panels) — each a single visual beat.
2. `shotlist_md()` → a table (shot, move, duration, description, VO/audio) = the plan/runtime.
3. `render_board()` → a storyboard SHEET (panels with real frames or placeholders).
4. `animatic()` → a timed rough-cut video from the panels (Ken Burns + captions) to feel pacing before shooting/editing.
5. Hand approved panels to `vidkit`/`batch_edit` for the finish.

## Shot vocabulary (use in boards)
EWS extreme-wide · WS wide · MS medium · MCU med-closeup · CU closeup · ECU extreme-closeup ·
OTS over-shoulder · POV point-of-view · TWO two-shot · INSERT detail · TOP/AERIAL overhead.
**Moves:** static · slow push (in) · pull (out) · pan L/R · tilt up/down · track · handheld · whip · burst (motor-drive).

## Composition & continuity (the expert rules)
- **Rule of thirds / lead room** — subject off-center, space to look/move into.
- **Vary the size** — never two same-size shots back-to-back; cut WS→MS→CU for rhythm.
- **180° rule** — keep screen direction consistent so geography reads.
- **Match on action / eyeline** — cut on movement; honor where people look.
- **Establish → develop → detail → resolve** — orient the viewer before going close.
- **Motivate moves** — push for intimacy, pull for reveal; don't move without reason.

## Story arcs that work
- **Cinematic recap** (what we used for the skate park): *arrive → reveal the space → action build → human/community → quiet beat → close on identity (sign/logo).*
- **Hook-first (social/Shorts):** strongest 1-sec image at t=0 → context → payoff → CTA. (Hyperion's Shorts rule.)
- **Three-act:** setup → escalation → resolution.

## Pacing / rhythm
- Social: **1.5–2.5s** per shot; let hero/emotional beats breathe (3–4s).
- Bursts/motor-drive: **0.2–0.3s** per frame for energy spikes.
- Crossfade ~0.4–0.5s for cinematic; hard cuts for punch.
- **Cut to the beat** when there's music; sync SFX (shutter clicks, skate wheels) to the visual hit.

## Platform framing
- **9:16** Reels/TikTok/Stories · **1:1** feed · **16:9** YouTube/web · **2.39:1** cinematic.
- Storyboard in the delivery ratio so composition is correct from the start (`render_board(ratio=…)`).

## Genre look (ties to Hyperion design system)
Carry the palette/typography per genre (gothic, philosophy, true-crime, etc.) into title cards and
grade so the board, animatic, and final share one identity.

## Quick use
```python
import storyboard as sb
board=[{"n":1,"shot":"WS","move":"slow push","dur":3,"desc":"Establish…","img":None}, ...]
sb.render_board(board,"board.png",ratio="9:16",cols=3,title="PROJECT")
sb.shotlist_md(board,"shots.md")
sb.animatic(board,"animatic.mp4",1080,1920)   # rough pre-viz video
```
Panels with `img` use that frame; without, they render a labeled placeholder to fill later.
