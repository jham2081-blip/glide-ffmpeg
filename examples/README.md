# Glide examples

Run these from the `examples/` folder. Each one auto-generates `sample.png` (a detailed
synthetic still) on first run, so you need no external assets. Outputs go to `./out/`.

```bash
cd examples
python make_sample_image.py        # (optional) just make the test image
python example_basic.py            # push-in, push-out, pan-left, pan-right
python example_easings.py          # same push-in with linear / cubic / sine easing
python make_before_after.py        # side-by-side BEFORE (zoompan) vs AFTER (Glide) clips
python compare_vs_zoompan.py       # THE JUDGE: Glide vs ffmpeg zoompan, with numbers
```

## Be the judge

`compare_vs_zoompan.py` renders the **same** pan two ways and prints a smoothness number
for each (coefficient of variation of per-frame displacement — lower is smoother), then
writes both videos to `out/judge_glide.mp4` and `out/judge_zoompan.mp4`.

Play them back-to-back and watch the pan: the `zoompan` clip has the characteristic
"held, then jump" micro-stutter; the Glide clip glides. The printed ratio quantifies it
(typically ~15× smoother through the full encode).

Want to stress it harder? Slow the move down (`duration` up), or make the source more
detailed — slow moves over fine detail are the worst case, and where Glide's advantage is
most obvious.
