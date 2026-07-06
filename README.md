# Glide — smooth, sub-pixel pan & zoom over still images

**A small, correct replacement for FFmpeg's `zoompan` for animating still images** —
the pan/zoom move often called the *"Ken Burns"* effect. Glide removes the
per-frame shudder that `zoompan` produces on slow moves, and it does it *cheaply*.

> **TL;DR:** FFmpeg's `zoompan` snaps the crop to whole pixels every frame, so slow
> moves stutter ("held, then jump"). Glide computes a floating-point transform per
> frame and samples with bicubic interpolation on the GPU, so motion is sub-pixel
> exact. Measured **~15× smoother** end-to-end, at **no extra render cost** — and it
> unlocks *fast* moves that `zoompan` simply can't do without strobing.

---

## The problem

`zoompan` integer-truncates the pan/zoom offset each frame. When your motion-per-frame
is a fraction of a pixel (i.e. any tasteful, slow move), the crop lands on the *same*
integer coordinate for several frames and then jumps a whole pixel. Your eye reads that
as a shudder or vibration.

The common workaround is to render at a huge supersample (e.g. 8K) and downscale. That
only *masks* the stepping, it never removes it, and it is expensive.

## What Glide does instead

- **Float affine transform per frame** → positions are exact real numbers.
- **Bicubic sampling via `torch.grid_sample`** on the GPU → true sub-pixel precision.
- **A mild 1.5× supersample + area (box) downscale** → clean anti-aliasing of fine
  detail. This is kept *separate* from the motion and is only for shimmer, not jitter.
- **Frames streamed straight to FFmpeg** (rawvideo over stdin) → FFmpeg only encodes.
- **Easing** (`linear` / `cubic` / `sine`) → optional ease-in-out for a cinematic
  "camera settle". Aesthetic only; does not affect smoothness.

## Benchmark (reproduce it yourself)

Run [`examples/compare_vs_zoompan.py`](examples/compare_vs_zoompan.py). It renders the
same pan with both methods and measures per-frame displacement evenness (coefficient of
variation of the sub-pixel shift, via phase correlation — lower = smoother):

| method | pan smoothness (CV, lower is better) | render time (6 s clip) |
|---|---|---|
| **Glide** (this library) | **~0.005** | ~3.5 s |
| FFmpeg `zoompan` @ 4× supersample | ~0.076 | ~4.3 s |

That is **~15× smoother, measured through the full H.264 encode**, at *lower* render
cost. (The raw sampling precision is far higher still — the encoder, not Glide, is the
floor on that metric.) Numbers from an RTX 4060 Ti; your ratios will be similar.

## Install

```bash
pip install torch pillow numpy      # CUDA build of torch strongly recommended
# and have ffmpeg on PATH, or set GLIDE_FFMPEG=/path/to/ffmpeg
```

Glide runs on CPU too (it auto-detects), but a CUDA GPU is dramatically faster.

## Quickstart

**Command line** (no Python needed):

```bash
# generate a test image, then a smooth push-in
python examples/make_sample_image.py
python glide.py sample.png out.mp4 --preset push-in --duration 6 --easing sine

# explicit move: zoom 1.0 -> 1.4 while drifting the center up-right
python glide.py sample.png out.mp4 --zoom 1.0 1.4 \
    --center-start 0.5 0.5 --center-end 0.55 0.45 --duration 4 --easing cubic
```

Presets: `push-in`, `push-out`, `pan-left`, `pan-right`, `pan-up`, `pan-down`.

**Library:**

```python
from glide import GlideMove, render

move = GlideMove(
    start_zoom=1.0, end_zoom=1.35,
    start_center=(0.5, 0.5), end_center=(0.52, 0.46),   # normalized 0..1
    duration_s=6.0, fps=30, easing="sine",
)
render("panel.png", move, "out.mp4", out_size=(1920, 1080))
```

## API

- **`GlideMove(start_zoom, end_zoom, start_center, end_center, duration_s, fps=30, easing="cubic")`**
  A move spec. `zoom > 1` is zoomed in (viewport is `1/zoom` of the source). Centers are
  normalized `[0,1]` source coordinates; they are automatically clamped so the viewport
  never leaves the image.
- **`render(image_path, move, out_path, out_size=(1920,1080), supersample=1.5, batch=16, crf=18, preset="slow", device=...)`**
  Render the move and encode to `out_path`.
- **`preset_move(name, duration_s, fps, easing, amount=0.20)`** → a ready `GlideMove`.
- **`build_grids(move, out_h, out_w, ...)`** → the raw sampling grids, if you want to do
  your own sampling / compositing.
- **`resolve_ffmpeg()`** → the ffmpeg path Glide will use.

## Examples

| file | what it shows |
|---|---|
| [`examples/make_sample_image.py`](examples/make_sample_image.py) | generates a detailed synthetic test still |
| [`examples/example_basic.py`](examples/example_basic.py) | the four core preset moves |
| [`examples/example_easings.py`](examples/example_easings.py) | linear vs cubic vs sine easing |
| [`examples/compare_vs_zoompan.py`](examples/compare_vs_zoompan.py) | **the judge** — Glide vs `zoompan`, with numbers |

## How it works

See [`docs/how-it-works.md`](docs/how-it-works.md) for the math (the affine grid, the
`grid_sample` mapping, why the center clamp matters, and the sampling-vs-easing split).

## Notes & limitations

- Assumes the **source and output share an aspect ratio** (e.g. 16:9 → 16:9). A
  mismatched source will be stretched; letterbox/crop it first.
- `bicubic` sampling can overshoot slightly on hard edges; output is clamped to `[0,1]`.
- Very fast moves benefit from a touch of motion blur (not built in yet — PRs welcome).

## License

MIT — see [LICENSE](LICENSE).
