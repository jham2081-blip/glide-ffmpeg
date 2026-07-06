"""
example_basic.py — the four core moves, using presets.

    python example_basic.py

Renders push-in, push-out, pan-left, pan-right to ./out/. Generates sample.png
first if it does not exist.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glide import preset_move, render          # noqa: E402
from make_sample_image import make             # noqa: E402

os.makedirs("out", exist_ok=True)
img = "sample.png"
if not os.path.exists(img):
    make(img)

for name in ["push-in", "push-out", "pan-left", "pan-right"]:
    move = preset_move(name, duration_s=6.0, fps=30, easing="sine", amount=0.22)
    out = os.path.join("out", f"{name}.mp4")
    print(f"rendering {name} -> {out}")
    render(img, move, out)
print("done -> ./out/")
