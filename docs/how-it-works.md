# How Glide works

## The core idea

A camera move over a still is just a per-frame **crop-and-scale**: for each output
frame you pick a rectangular viewport of the source and resample it to the output size.
The *only* thing that makes motion look smooth or juddery is **how precisely you can
place and size that viewport**.

FFmpeg's `zoompan` places the viewport at **integer** source pixels. On a slow move the
viewport barely changes, so it rounds to the *same* integer for several frames, then
jumps a whole pixel. That is the shudder.

Glide places the viewport at **floating-point** coordinates and resamples with bicubic
interpolation, so a viewport can shift by 0.3 px and the output reflects exactly that.
No stepping, at any speed.

## The transform

A `GlideMove` interpolates three quantities over (eased) time `t ∈ [0,1]`:

- `zoom(t)` — viewport is `1/zoom` of the source.
- `center_x(t)`, `center_y(t)` — viewport center, in normalized `[0,1]` source coords.

The viewport half-extent in normalized space is `half = 0.5 / zoom`. The viewport spans
`[center - half, center + half]` in each axis.

### The sampling grid

`torch.grid_sample` samples a source using a grid in normalized `[-1, 1]` coordinates
(where `-1` and `+1` are the image edges). For each output pixel we map its normalized
output position `base ∈ [-1, 1]` to a source position:

```
source_coord = center_grid + base * half_grid
```

where `center_grid = center * 2 - 1` (maps `[0,1] → [-1,1]`) and `half_grid = half * 2`
(a fraction `half` of the source is `half * 2` in `[-1,1]` units). Because every term is
a float, the sampled position is exact — this is where the sub-pixel precision comes from.

See `build_grids()` in [`glide.py`](../glide.py).

## Why the center is clamped

If `center ± half` leaves `[0,1]`, you are asking to sample outside the image. Padding
then fills those pixels — with a mirror or edge smear — which shows up as a seam on the
art. Glide clamps `center` to `[half, 1-half]` so the viewport always stays inside the
source. (At `zoom = 1.0`, `half = 0.5`, so the center is forced to `0.5` — the only
in-bounds option at full frame.)

## Two separate concerns

1. **Sampling precision** (float transform + bicubic) — this is what removes jitter.
   It is exact regardless of easing.
2. **Easing / trajectory** (`linear`, `cubic`, `sine`) — how the move accelerates over
   time. Purely aesthetic. `sine`/`cubic` ease in and out so the camera starts and
   settles softly. Swapping easings never affects smoothness.

Keeping these separate means you can tune the *feel* without ever reintroducing the
*jitter*.

## Anti-aliasing vs. jitter (don't confuse them)

Sub-pixel **position** precision (above) fixes *jitter*. It does **not** fix *shimmer* —
the fizz you get when fine, high-contrast detail crawls across the pixel grid. That is
temporal aliasing, and the fix is a low-pass: Glide renders at `supersample × output`
(default 1.5×) and downscales with an `area` (box) filter, which averages detail down
cleanly. Set `supersample=1.0` to disable if your source is soft.

## Performance

- Grids are built **per batch** (`build_grids(..., i0, count)`), so VRAM is bounded by
  the batch size, not the clip length. Tune `batch` to your GPU.
- The source image is uploaded to the GPU once and broadcast across the batch.
- Frames are streamed to FFmpeg over stdin, so the encode overlaps with GPU work and no
  intermediate PNGs hit disk.
- In practice the **x264 encode dominates** total time — the sampling is nearly free on
  a modern GPU.
