"""
make_sample_image.py — generate a detailed synthetic test still (no external asset).

The image is deliberately full of fine, high-contrast detail (thin lines, small
text, a grid, gradients) because that is the worst case for motion shimmer — it
makes any jitter or aliasing easy to see. Run this first, then the other examples.

    python make_sample_image.py            # writes sample.png (3840x2160)
"""
from __future__ import annotations
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 2160


def make(path: str = "sample.png") -> str:
    img = Image.new("RGB", (W, H), (18, 20, 28))
    d = ImageDraw.Draw(img)

    # Diagonal gradient background
    for y in range(0, H, 4):
        c = int(20 + 60 * y / H)
        d.line([(0, y), (W, y)], fill=(c, c // 2, 90 - c // 3), width=4)

    # Fine grid (thin lines = shimmer stress test)
    for x in range(0, W, 48):
        d.line([(x, 0), (x, H)], fill=(60, 70, 90), width=1)
    for y in range(0, H, 48):
        d.line([(0, y), (W, y)], fill=(60, 70, 90), width=1)

    # Concentric rings (curved high-frequency detail)
    cx, cy = W // 2, H // 2
    for r in range(40, 1100, 26):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 200, 255), width=2)

    # Corner registration marks + small text (readability under motion)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
        big = ImageFont.truetype("arial.ttf", 120)
    except Exception:
        font = ImageFont.load_default()
        big = font
    for (x, y) in [(80, 80), (W - 400, 80), (80, H - 120), (W - 400, H - 120)]:
        d.rectangle([x, y, x + 300, y + 40], outline=(255, 255, 255), width=2)
        d.text((x + 8, y + 4), "GLIDE TEST", fill=(255, 255, 255), font=font)
    d.text((cx - 500, 200), "sub-pixel smooth", fill=(255, 240, 200), font=big)

    img.save(path)
    print(f"wrote {path} ({W}x{H})")
    return path


if __name__ == "__main__":
    make(sys.argv[1] if len(sys.argv) > 1 else "sample.png")
