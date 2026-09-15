"""ComboBox acilir menu oku (chevron) ikonlarini uretir: koyu ve acik tema icin ayri renk."""
import os

from PIL import Image, ImageDraw

here = os.path.dirname(os.path.abspath(__file__))


def draw_chevron(color, out_name, size=64, stroke=7):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = size * 0.26
    top = size * 0.36
    mid = size * 0.62
    pts = [(margin, top), (size / 2, mid), (size - margin, top)]
    draw.line(pts, fill=color, width=stroke, joint="curve")
    r = stroke / 2
    for p in pts:
        draw.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)
    img.save(os.path.join(here, out_name))
    print("saved", out_name)


draw_chevron((60, 60, 66, 255), "chevron_dark.png")
draw_chevron((225, 228, 232, 255), "chevron_light.png")
