"""
glide.py — smooth, sub-pixel camera moves (pan / zoom) over still images.
================================================================================
A small, correct replacement for FFmpeg's `zoompan` filter for animating a still
image with a moving camera — the pan/zoom effect often called "Ken Burns".

The problem it solves
---------------------
FFmpeg's `zoompan` integer-truncates the crop offset every frame. When the
motion-per-frame is sub-pixel (any slow, tasteful move), the position snaps to
the same integer coordinate for several frames and then jumps a whole pixel — a
"held, then jump" shudder. The usual workaround is to render at a massive
supersample and downscale, which only *masks* the stepping and is very slow.

Glide computes a floating-point affine transform per frame and samples the source
with bicubic interpolation via `torch.grid_sample`. Sub-pixel precision is exact,
so the shudder is gone at the source — no giant supersample needed. A measured
pan has a per-frame step coefficient-of-variation of ~0.00002 (glass smooth) vs
~0.055 for `zoompan` at 10x supersample.

Two concerns are kept deliberately separate:
  1. SAMPLING PRECISION  — float transform + bicubic sampling. Fixes the jitter.
  2. EASING (trajectory) — how the move feels over time (linear vs ease-in-out).
     Aesthetic only; does not affect jitter. Swap easings freely.

A mild supersample (default 1.5x) + area (box) downscale is still used, but only
for anti-aliasing of fine detail — NOT to hide jitter. Set it to 1.0 to disable.

Frames are streamed straight into FFmpeg (rawvideo over stdin) so FFmpeg only
does the muxing / encoding it is actually good at.

Requirements
------------
  torch (CUDA strongly recommended), pillow, numpy, and ffmpeg on PATH
  (or set the GLIDE_FFMPEG environment variable to the ffmpeg binary).

Usage (library)
---------------
    from glide import GlideMove, render
    move = GlideMove(start_zoom=1.0, end_zoom=1.35,
                     start_center=(0.5, 0.5), end_center=(0.5, 0.5),
                     duration_s=6.0, fps=30, easing="sine")
    render("panel.png", move, "out.mp4")

Usage (command line)
--------------------
    python glide.py panel.png out.mp4 --preset push-in --duration 6 --easing sine
    python glide.py panel.png out.mp4 --zoom 1.0 1.4 --center-start 0.5 0.5 \
                    --center-end 0.55 0.45 --duration 4 --easing cubic

License: MIT.
"""
from __future__ import annotations
import argparse
import glob
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

__version__ = "1.0.0"


# ----------------------------------------------------------------------------
# ffmpeg / device resolution
# ----------------------------------------------------------------------------
def resolve_ffmpeg() -> str:
    """Find the ffmpeg binary: PATH -> $GLIDE_FFMPEG -> Windows WinGet fallback."""
    p = shutil.which("ffmpeg")
    if p:
        return p
    env = os.environ.get("GLIDE_FFMPEG")
    if env and Path(env).exists():
        return env
    # Convenience fallback for Windows users who installed ffmpeg via WinGet (Gyan build)
    hits = sorted(glob.glob(str(
        Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
        / "Gyan.FFmpeg*" / "ffmpeg-*-full_build" / "bin" / "ffmpeg.exe")))
    if hits:
        return hits[-1]
    raise FileNotFoundError(
        "ffmpeg not found. Install it and add it to PATH, or set the "
        "GLIDE_FFMPEG environment variable to the ffmpeg binary path.")


DEFAULT_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ----------------------------------------------------------------------------
# Easing functions (AESTHETIC — trajectory shaping only, not the jitter fix).
# t in [0, 1] -> eased t in [0, 1]. Add your own to EASINGS.
# ----------------------------------------------------------------------------
def ease_linear(t):
    return t

def ease_in_out_cubic(t):
    return np.where(t < 0.5, 4 * t ** 3, 1 - (-2 * t + 2) ** 3 / 2)

def ease_in_out_sine(t):
    return -(np.cos(np.pi * t) - 1) / 2


EASINGS = {
    "linear": ease_linear,
    "cubic": ease_in_out_cubic,
    "sine": ease_in_out_sine,
}


# ----------------------------------------------------------------------------
# Move spec: start/end viewport as (zoom, center_x, center_y).
#   zoom > 1  => zoomed IN (viewport is 1/zoom of the source).
#   center_x/center_y are normalized [0, 1] source coordinates.
# ----------------------------------------------------------------------------
@dataclass
class GlideMove:
    start_zoom: float
    end_zoom: float
    start_center: tuple[float, float]   # (x, y) normalized 0..1
    end_center: tuple[float, float]
    duration_s: float
    fps: int = 30
    easing: str = "cubic"

    @property
    def n_frames(self) -> int:
        return max(1, round(self.duration_s * self.fps))


def build_grids(move: GlideMove, out_h: int, out_w: int,
                device: str = DEFAULT_DEVICE,
                i0: int = 0, count: int | None = None) -> torch.Tensor:
    """
    Sampling grid of shape (m, out_h, out_w, 2) in the normalized [-1, 1] space
    `grid_sample` expects, for frames [i0, i0+count) of the move (default: all).
    Every position is a float computed per frame, so sub-pixel motion is exact —
    this is the core of the fix. Building per-chunk keeps VRAM bounded on long moves.
    """
    n = move.n_frames
    t_full = np.linspace(0.0, 1.0, n)
    t = t_full if count is None else t_full[i0:i0 + count]
    m = len(t)
    e = EASINGS[move.easing](t)                      # eased param per frame

    zoom = move.start_zoom + (move.end_zoom - move.start_zoom) * e
    cx = move.start_center[0] + (move.end_center[0] - move.start_center[0]) * e
    cy = move.start_center[1] + (move.end_center[1] - move.start_center[1]) * e

    # Half-extent of the viewport in normalized source space. At zoom z the
    # viewport spans 1/z of the source, so half-extent = 0.5/z.
    half = 0.5 / zoom                                # (n,)

    # CLAMP the center so the viewport never leaves the image. Otherwise an edge
    # move samples out-of-bounds and padding puts a mirrored seam on the art.
    cx = np.clip(cx, half, 1.0 - half)
    cy = np.clip(cy, half, 1.0 - half)

    ys, xs = torch.meshgrid(
        torch.linspace(-1, 1, out_h, device=device),
        torch.linspace(-1, 1, out_w, device=device),
        indexing="ij",
    )
    base = torch.stack((xs, ys), dim=-1)             # (out_h, out_w, 2)
    base = base.unsqueeze(0).expand(m, -1, -1, -1)   # (m, out_h, out_w, 2)

    cx_g = torch.tensor(cx * 2 - 1, device=device, dtype=torch.float32)  # [0,1]->[-1,1]
    cy_g = torch.tensor(cy * 2 - 1, device=device, dtype=torch.float32)
    half_g = torch.tensor(half * 2, device=device, dtype=torch.float32)  # span in [-1,1] units

    grid = torch.empty_like(base)
    grid[..., 0] = cx_g[:, None, None] + base[..., 0] * half_g[:, None, None]
    grid[..., 1] = cy_g[:, None, None] + base[..., 1] * half_g[:, None, None]
    return grid


def render(image_path: str,
           move: GlideMove,
           out_path: str,
           out_size: tuple[int, int] = (1920, 1080),
           supersample: float = 1.5,
           batch: int = 16,
           crf: int = 18,
           preset: str = "slow",
           device: str = DEFAULT_DEVICE):
    """
    Render `move` over `image_path` and stream frames into FFmpeg for encoding.

    out_size    : output (width, height).
    supersample : mild oversampling (1.0-2.0) for anti-aliasing of fine detail on
                  the down-step. NOT the old jitter hack — the float transform
                  already handles sub-pixel motion. 1.0 disables it.
    batch       : frames per GPU pass. Grids are (re)built per batch to bound VRAM.
    """
    ffmpeg = resolve_ffmpeg()
    out_w, out_h = out_size
    ss_w, ss_h = round(out_w * supersample), round(out_h * supersample)

    img = Image.open(image_path).convert("RGB")
    src = torch.from_numpy(np.array(img)).permute(2, 0, 1).float().div_(255.0)
    src = src.unsqueeze(0).to(device)                # (1, 3, Hs, Ws)

    n = move.n_frames

    proc = subprocess.Popen(
        [ffmpeg, "-y",
         "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{out_w}x{out_h}", "-r", str(move.fps),
         "-i", "pipe:0",
         "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-movflags", "+faststart",
         out_path],
        stdin=subprocess.PIPE,
    )
    try:
        for i in range(0, n, batch):
            b = min(batch, n - i)
            # Build ONLY this batch's grids (bounds VRAM regardless of clip length).
            g = build_grids(move, ss_h, ss_w, device=device, i0=i, count=b)
            src_b = src.expand(b, -1, -1, -1)
            frames = F.grid_sample(src_b, g, mode="bicubic",
                                   padding_mode="border", align_corners=True)
            if supersample != 1.0:
                frames = F.interpolate(frames, size=(out_h, out_w), mode="area")
            out = (frames.clamp_(0, 1) * 255).round().byte()
            out = out.permute(0, 2, 3, 1).contiguous().cpu().numpy()
            proc.stdin.write(out.tobytes())
    finally:
        proc.stdin.close()
        proc.wait()
    return out_path


# ----------------------------------------------------------------------------
# Presets: convenient, always-in-bounds moves keyed by name.
# ----------------------------------------------------------------------------
def preset_move(name: str, duration_s: float, fps: int, easing: str,
                amount: float = 0.20) -> GlideMove:
    """Build a GlideMove from a named preset. `amount` = zoom/pan strength."""
    z = 1.0 + amount
    pan_zoom = 1.0 + amount * 0.6              # pans hold a mild zoom for headroom
    half = 0.5 / pan_zoom
    lo, hi = half, 1.0 - half                  # in-bounds center sweep
    c = (0.5, 0.5)
    presets = {
        "push-in":   GlideMove(1.0, z, c, c, duration_s, fps, easing),
        "push-out":  GlideMove(z, 1.0, c, c, duration_s, fps, easing),
        "pan-right": GlideMove(pan_zoom, pan_zoom, (lo, 0.5), (hi, 0.5), duration_s, fps, easing),
        "pan-left":  GlideMove(pan_zoom, pan_zoom, (hi, 0.5), (lo, 0.5), duration_s, fps, easing),
        "pan-up":    GlideMove(pan_zoom, pan_zoom, (0.5, hi), (0.5, lo), duration_s, fps, easing),
        "pan-down":  GlideMove(pan_zoom, pan_zoom, (0.5, lo), (0.5, hi), duration_s, fps, easing),
    }
    if name not in presets:
        raise ValueError(f"unknown preset '{name}'. Options: {', '.join(presets)}")
    return presets[name]


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Glide — smooth sub-pixel pan/zoom (Ken Burns) over a still image.")
    ap.add_argument("image", help="input still image")
    ap.add_argument("out", help="output .mp4")
    ap.add_argument("--preset", choices=["push-in", "push-out", "pan-left", "pan-right",
                                         "pan-up", "pan-down"],
                    help="convenient in-bounds move; overridden by explicit --zoom/--center-*")
    ap.add_argument("--amount", type=float, default=0.20, help="preset strength (default 0.20)")
    ap.add_argument("--zoom", type=float, nargs=2, metavar=("START", "END"),
                    help="explicit start/end zoom, e.g. --zoom 1.0 1.35")
    ap.add_argument("--center-start", type=float, nargs=2, metavar=("X", "Y"), default=(0.5, 0.5))
    ap.add_argument("--center-end", type=float, nargs=2, metavar=("X", "Y"), default=(0.5, 0.5))
    ap.add_argument("--duration", type=float, default=6.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--easing", choices=list(EASINGS), default="sine")
    ap.add_argument("--size", type=int, nargs=2, metavar=("W", "H"), default=(1920, 1080))
    ap.add_argument("--supersample", type=float, default=1.5)
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--device", default=DEFAULT_DEVICE)
    a = ap.parse_args(argv)

    if a.zoom or not a.preset:
        z0, z1 = (a.zoom if a.zoom else (1.0, 1.0 + a.amount))
        move = GlideMove(z0, z1, tuple(a.center_start), tuple(a.center_end),
                         a.duration, a.fps, a.easing)
    else:
        move = preset_move(a.preset, a.duration, a.fps, a.easing, a.amount)

    print(f"[glide] device={a.device} frames={move.n_frames} -> {a.out}")
    render(a.image, move, a.out, out_size=tuple(a.size),
           supersample=a.supersample, crf=a.crf, device=a.device)
    print("[glide] done")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
