"""
compare_vs_zoompan.py — judge Glide against FFmpeg's zoompan yourself.

Renders the SAME pan two ways and measures per-frame motion evenness (lower =
smoother). Also writes both videos so you can eyeball them side by side.

    python compare_vs_zoompan.py

Outputs to ./out/:
    judge_glide.mp4        (this library)
    judge_zoompan.mp4      (ffmpeg zoompan at 4x supersample)

The metric is the coefficient of variation (CV) of the frame-to-frame movement
of a tracked feature: 0 = perfectly even motion; larger = stepping/shudder.
"""
from __future__ import annotations
import glob
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glide import GlideMove, render, resolve_ffmpeg   # noqa: E402
from make_sample_image import make                     # noqa: E402

FF = resolve_ffmpeg()
OW, OH = 1920, 1080
N, FPS = 90, 30
ZOOM = 1.20
os.makedirs("out", exist_ok=True)


def probe_image():
    """Use the detailed synthetic still — its grid/rings/text give the localized
    texture that phase correlation needs to lock onto for shift estimation."""
    p = "sample.png"
    if not os.path.exists(p):
        make(p)
    return p


def _subpixel_shift(a, b):
    """Sub-pixel horizontal shift mapping profile a -> b via 1D phase correlation.
    Phase correlation normalizes magnitude per frequency, so it is robust to the
    encoder's per-frame brightness wobble and measures pure translation."""
    fa, fb = np.fft.rfft(a), np.fft.rfft(b)
    R = fa * np.conj(fb)
    R /= np.abs(R) + 1e-9
    c = np.fft.irfft(R, n=len(a))
    k = int(np.argmax(c))
    cm, c0, cp = c[(k - 1) % len(c)], c[k], c[(k + 1) % len(c)]
    k = k + 0.5 * (cm - cp) / (cm - 2 * c0 + cp + 1e-9)   # parabolic sub-pixel
    return k - len(a) if k > len(a) / 2 else k


def cv_of_motion(frames_dir):
    """CV of frame-to-frame sub-pixel displacement (0 = perfectly even motion)."""
    import glob as _g
    profs = [np.asarray(Image.open(f).convert("L"), dtype=np.float64).mean(0)
             for f in sorted(_g.glob(f"{frames_dir}/*.png"))]
    shifts = np.array([_subpixel_shift(profs[i - 1], profs[i])
                       for i in range(1, len(profs))])
    return float(shifts.std() / abs(shifts.mean())) if shifts.mean() else 0.0


def glide_pan(probe):
    half = 0.5 / ZOOM
    move = GlideMove(ZOOM, ZOOM, (half, 0.5), (1 - half, 0.5), N / FPS, FPS, "linear")
    out = os.path.join("out", "judge_glide.mp4")
    render(probe, move, out, out_size=(OW, OH), supersample=1.5)
    d = tempfile.mkdtemp()
    subprocess.run([FF, "-y", "-i", out, "-vf", f"fps={FPS}", f"{d}/%03d.png"],
                   capture_output=True)
    return out, cv_of_motion(d)


def zoompan_pan(probe):
    out = os.path.join("out", "judge_zoompan.mp4")
    body = (f"zoompan=z='{ZOOM}':x='(iw-iw/zoom)*on/{N-1}':"
            f"y='ih/2-(ih/zoom/2)':d={N}:s={OW}x{OH}:fps={FPS}")
    vf = f"scale=7680:-2:flags=lanczos,{body},format=yuv420p"   # 4x supersample
    subprocess.run([FF, "-y", "-loop", "1", "-i", probe, "-t", str(N / FPS),
                    "-vf", vf, "-frames:v", str(N), "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", out],
                   capture_output=True)
    d = tempfile.mkdtemp()
    subprocess.run([FF, "-y", "-i", out, "-vf", f"fps={FPS}", f"{d}/%03d.png"],
                   capture_output=True)
    return out, cv_of_motion(d)


if __name__ == "__main__":
    probe = probe_image()
    g_out, g_cv = glide_pan(probe)
    z_out, z_cv = zoompan_pan(probe)
    print("\n================ JUDGE: pan smoothness (lower CV = smoother) ================")
    print(f"  glide         : CV = {g_cv:.5f}   -> {g_out}")
    print(f"  ffmpeg zoompan: CV = {z_cv:.5f}   -> {z_out}   (4x supersample)")
    ratio = (z_cv / g_cv) if g_cv else float("inf")
    print(f"  glide is ~{ratio:,.0f}x smoother on this measure.")
    print("============================================================================")
