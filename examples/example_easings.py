"""
example_easings.py — the same push-in with each easing, to feel the difference.

    python example_easings.py

'linear' moves at constant speed. 'cubic' / 'sine' ease in and out, so the camera
starts and settles softly (a more cinematic feel). Easing is aesthetic only — it
does not affect smoothness.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glide import GlideMove, render            # noqa: E402
from make_sample_image import make             # noqa: E402

os.makedirs("out", exist_ok=True)
img = "sample.png"
if not os.path.exists(img):
    make(img)

for easing in ["linear", "cubic", "sine"]:
    move = GlideMove(start_zoom=1.0, end_zoom=1.35,
                     start_center=(0.5, 0.5), end_center=(0.52, 0.46),
                     duration_s=5.0, fps=30, easing=easing)
    out = os.path.join("out", f"ease_{easing}.mp4")
    print(f"rendering ease_{easing} -> {out}")
    render(img, move, out)
print("done -> ./out/")
