"""
make_before_after.py — side-by-side BEFORE (ffmpeg zoompan) vs AFTER (Glide) clips.

For each issue Glide fixes, this renders the SAME move both ways and stitches them
into one labeled side-by-side video so you can see the exact difference:

    out/ba_pan.mp4    pan  — the classic zoompan pan stutter
    out/ba_zoom.mp4   zoom — push-in shudder
    out/ba_fast.mp4   fast — zoompan strobes on quick moves; Glide stays smooth

zoompan is given a fair 4x supersample (its best case), so this is not a straw man.
Uses the neutral demo images in ../assets (mountain / city / library — not anyone's IP).

    python make_before_after.py
"""
from __future__ import annotations
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glide import GlideMove, render, resolve_ffmpeg   # noqa: E402

FF = resolve_ffmpeg()
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
OUT = "out"
os.makedirs(OUT, exist_ok=True)
OW, OH = 1920, 1080
FONT = "C\\:/Windows/Fonts/arial.ttf"          # ffmpeg drawtext wants the colon escaped


def zoompan_render(image, vf_body, n, fps, dst):
    """Render the 'before' with ffmpeg zoompan at 4x supersample (its best case)."""
    vf = f"scale=7680:-2:flags=lanczos,{vf_body},format=yuv420p"
    subprocess.run([FF, "-y", "-loop", "1", "-i", image, "-t", f"{n/fps:.3f}",
                    "-vf", vf, "-frames:v", str(n), "-r", str(fps),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", dst],
                   capture_output=True)


def combine(before, after, dst, label_dur):
    """Scale each to 960x540, label them, and hstack into one side-by-side clip."""
    def lbl(text):
        return (f"scale=960:540,drawtext=fontfile='{FONT}':text='{text}':"
                f"x=(w-tw)/2:y=h-46:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=8")
    fc = (f"[0:v]{lbl('BEFORE — ffmpeg zoompan')}[l];"
          f"[1:v]{lbl('AFTER — Glide')}[r];"
          f"[l][r]hstack=inputs=2[v]")
    subprocess.run([FF, "-y", "-i", before, "-i", after, "-filter_complex", fc,
                    "-map", "[v]", "-c:v", "libx264", "-crf", "22", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", dst], capture_output=True)


CX = "iw/2-(iw/zoom/2)"
CY = "ih/2-(ih/zoom/2)"

DEMOS = [
    # name, image,           glide move,                                              zoompan vf body,                                             n,   fps
    ("pan", "demo_landscape",
     GlideMove(1.10, 1.10, (0.5/1.10, 0.5), (1-0.5/1.10, 0.5), 5.0, 30, "linear"),
     f"zoompan=z='1.10':x='(iw-iw/zoom)*on/149':y='{CY}':d=150:s={OW}x{OH}:fps=30", 150, 30),
    ("zoom", "demo_interior",
     GlideMove(1.0, 1.28, (0.5, 0.5), (0.5, 0.5), 5.0, 30, "sine"),
     f"zoompan=z='min(1.0+0.28*on/149,1.28)':x='{CX}':y='{CY}':d=150:s={OW}x{OH}:fps=30", 150, 30),
    ("fast", "demo_cityscape",
     GlideMove(1.0, 1.40, (0.5, 0.5), (0.55, 0.45), 2.0, 30, "sine"),
     f"zoompan=z='min(1.0+0.40*on/59,1.40)':x='iw/2-(iw/zoom/2)+(0.05*iw)*on/59':y='{CY}':d=60:s={OW}x{OH}:fps=30", 60, 30),
]

if __name__ == "__main__":
    for name, img, move, zp_vf, n, fps in DEMOS:
        image = os.path.join(ASSETS, img + ".png")
        if not os.path.exists(image):
            print(f"missing asset {image} — run gen or add the image"); continue
        before = os.path.join(OUT, f"_zp_{name}.mp4")
        after = os.path.join(OUT, f"_gl_{name}.mp4")
        final = os.path.join(OUT, f"ba_{name}.mp4")
        print(f"[{name}] before (zoompan)…")
        zoompan_render(image, zp_vf, n, fps, before)
        print(f"[{name}] after (glide)…")
        render(image, move, after, out_size=(OW, OH), supersample=1.5, crf=18)
        print(f"[{name}] combine -> {final}")
        combine(before, after, final, n / fps)
        os.remove(before); os.remove(after)
    print("done -> ./out/ba_*.mp4")
