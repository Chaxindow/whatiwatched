"""WhatIWatched uygulama ikonunu (koyu teal, film bobini halkası, W-göz-W amblemi) üretir.
Çıktı: assets/icon_1024.png ve assets/icon.ico (çoklu boyut)
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

center = (S // 2, S // 2)
radius = 480

# --- background circle with soft radial gradient ---
bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
draw = ImageDraw.Draw(bg)
draw.ellipse(
    [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
    fill=(9, 38, 35, 255),
)

highlight = Image.new("RGBA", (S, S), (0, 0, 0, 0))
hd = ImageDraw.Draw(highlight)
hd.ellipse([center[0] - 60, center[1] - 560, center[0] + 700, center[1] + 120], fill=(46, 143, 120, 160))
highlight = highlight.filter(ImageFilter.GaussianBlur(140))

mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.ellipse(
    [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
    fill=255,
)

bg = Image.alpha_composite(bg, Image.composite(highlight, Image.new("RGBA", (S, S), (0, 0, 0, 0)), mask))

shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([center[0] - 650, center[1] - 60, center[0] + 60, center[1] + 650], fill=(2, 12, 11, 140))
shadow = shadow.filter(ImageFilter.GaussianBlur(140))
bg = Image.alpha_composite(bg, Image.composite(shadow, Image.new("RGBA", (S, S), (0, 0, 0, 0)), mask))

img = Image.alpha_composite(img, bg)
draw = ImageDraw.Draw(img)

# --- film reel ring accent ---
ring_color = (120, 210, 180, 90)
ring_r = radius - 40
bbox = [center[0] - ring_r, center[1] - ring_r, center[0] + ring_r, center[1] + ring_r]
draw.ellipse(bbox, outline=ring_color, width=6)

teeth = 24
for i in range(teeth):
    angle = (2 * math.pi / teeth) * i
    cx = center[0] + ring_r * math.cos(angle)
    cy = center[1] + ring_r * math.sin(angle)
    tw, th = 22, 14
    tooth = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    td = ImageDraw.Draw(tooth)
    td.rounded_rectangle([cx - tw / 2, cy - th / 2, cx + tw / 2, cy + th / 2], radius=4, fill=(150, 225, 195, 130))
    tooth = tooth.rotate(-math.degrees(angle), center=(cx, cy), resample=Image.BICUBIC)
    img = Image.alpha_composite(img, tooth)

draw = ImageDraw.Draw(img)

for (dx, dy, r) in [(-360, -400, 10), (400, -350, 7), (-380, 380, 6), (410, 360, 9)]:
    draw.ellipse(
        [center[0] + dx - r, center[1] + dy - r, center[0] + dx + r, center[1] + dy + r],
        fill=(180, 230, 210, 180),
    )

# --- wordmark: W (eye) W, line-art style ---
white = (255, 255, 255, 255)
BG_MATCH = (9, 38, 35, 255)
stroke = 34


def draw_w(bbox_x0, bbox_y0, bbox_x1, bbox_y1):
    w = bbox_x1 - bbox_x0
    h = bbox_y1 - bbox_y0
    pts = [
        (bbox_x0, bbox_y0),
        (bbox_x0 + 0.26 * w, bbox_y1),
        (bbox_x0 + 0.5 * w, bbox_y0 + 0.32 * h),
        (bbox_x0 + 0.74 * w, bbox_y1),
        (bbox_x1, bbox_y0),
    ]
    draw.line(pts, fill=white, width=stroke, joint="curve")
    for p in pts:
        r = stroke / 2
        draw.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=white)


def lens_polygon(x0, x1, ecy, amp, n=48):
    top = []
    bottom = []
    w = x1 - x0
    for i in range(n + 1):
        t = i / n
        x = x0 + t * w
        top.append((x, ecy - amp * math.sin(math.pi * t)))
        bottom.append((x, ecy + amp * math.sin(math.pi * t)))
    return top + list(reversed(bottom))


def draw_eye(bbox_x0, bbox_y0, bbox_x1, bbox_y1):
    h = bbox_y1 - bbox_y0
    ecx = (bbox_x0 + bbox_x1) / 2
    ecy = (bbox_y0 + bbox_y1) / 2
    amp = h * 0.32

    outer = lens_polygon(bbox_x0, bbox_x1, ecy, amp + stroke * 0.5)
    inner = lens_polygon(bbox_x0, bbox_x1, ecy, max(amp - stroke * 0.5, 4))

    draw.polygon(outer, fill=white)
    draw.polygon(inner, fill=BG_MATCH)

    pupil_r = amp * 0.55
    draw.ellipse([ecx - pupil_r, ecy - pupil_r, ecx + pupil_r, ecy + pupil_r], fill=white)
    hole_r = pupil_r * 0.4
    draw.ellipse([ecx - hole_r, ecy - hole_r, ecx + hole_r, ecy + hole_r], fill=BG_MATCH)


letter_h = 300
letter_top = center[1] - letter_h / 2
letter_bottom = center[1] + letter_h / 2

w1_width = 250
eye_width = 150
w2_width = 250
gap = 26

total = w1_width + gap + eye_width + gap + w2_width
start_x = center[0] - total / 2

draw_w(start_x, letter_top, start_x + w1_width, letter_bottom)
eye_x0 = start_x + w1_width + gap
draw_eye(eye_x0, letter_top, eye_x0 + eye_width, letter_bottom)
w2_x0 = eye_x0 + eye_width + gap
draw_w(w2_x0, letter_top, w2_x0 + w2_width, letter_bottom)

here = os.path.dirname(os.path.abspath(__file__))
png_path = os.path.join(here, "icon_1024.png")
ico_path = os.path.join(here, "icon.ico")

img.save(png_path)
img.save(ico_path, sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("saved", png_path)
print("saved", ico_path)
