#!/usr/bin/env python3
"""Draw the front page for news-image-20261122.

Renders one 1024x1024 PNG summing up the world news of Sunday
22 November 2026 as a newspaper front page: a masthead naming the
day in full, a lead story on the COP31 collapse, four more stories
across regions and fields, one more in a bottom strip, and an
"also on the day" box. Every picture is a flat pictogram drawn
with Pillow primitives and every word is real rendered text
(DejaVu fonts) -- nothing AI-generated, nothing garbled.

Run:  python3 render.py            (writes entry.png next to this file)
Deterministic: no clock, no randomness, no network.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

PAPER = (247, 242, 229)
INK = (22, 35, 58)          # navy
RED = (166, 30, 34)         # headline red
TEAL = (15, 107, 92)
GOLD = (176, 124, 18)
SKY = (58, 122, 178)
LEAF = (74, 140, 74)
CARD = (255, 253, 246)
TINT = (236, 229, 210)
GREY = (90, 88, 80)
ORANGE = (224, 110, 30)
FLAME = (240, 178, 40)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)          # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centre(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- pictograms
def pic_globe(draw, x, y, s):
    """Blue globe, green land, red thermometer, NO DEAL stamp."""
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 6
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=INK, width=3)
    # crude continents, clipped by the disc via a mask-free trick: keep
    # every polygon point inside the circle's bounding box with margin.
    land = [
        [(cx - r + 14, cy - r + 26), (cx - 6, cy - r + 18), (cx + 8, cy - r + 34),
         (cx - 2, cy - r + 52), (cx - r + 22, cy - r + 48)],
        [(cx + 12, cy - 8), (cx + r - 16, cy - 18), (cx + r - 10, cy + 6),
         (cx + 26, cy + 18), (cx + 10, cy + 2)],
        [(cx - r + 20, cy + 22), (cx - 4, cy + 14), (cx + 4, cy + 34),
         (cx - r + 34, cy + r - 14), (cx - r + 12, cy + r - 22)],
    ]
    for poly in land:
        draw.polygon(poly, fill=LEAF)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=(255, 255, 255), width=2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    # thermometer, right of the globe
    tx = x + s - 34
    draw.rounded_rectangle([tx, y + 18, tx + 22, y + s - 44], radius=11,
                           fill=(255, 255, 255), outline=INK, width=3)
    draw.rectangle([tx + 6, y + 34, tx + 16, y + s - 58], fill=RED)
    draw.ellipse([tx - 6, y + s - 58, tx + 28, y + s - 24], fill=RED, outline=INK, width=3)


def pic_scales(draw, x, y, s):
    """Scales of justice in navy and gold."""
    cx = x + s // 2
    top = y + 12
    draw.line([cx, top, cx, y + s - 26], fill=INK, width=5)
    draw.line([x + 30, top + 16, x + s - 30, top + 16], fill=INK, width=5)
    draw.ellipse([cx - 7, top - 8, cx + 7, top + 6], fill=GOLD, outline=INK, width=2)
    for px in (x + 30, x + s - 30):
        draw.line([px, top + 16, px, top + 52], fill=INK, width=3)
        draw.pieslice([px - 24, top + 44, px + 24, top + 84], 0, 180, fill=GOLD,
                      outline=INK, width=3)
    draw.polygon([(cx - 34, y + s - 26), (cx + 34, y + s - 26), (cx + 18, y + s - 8),
                  (cx - 18, y + s - 8)], fill=INK)


def pic_tanker(draw, x, y, s):
    """Oil tanker on waves with a flame above the deck."""
    wy = y + s - 42
    # flame (kept short so it stays inside the tile)
    fx = x + s // 2
    draw.polygon([(fx - 18, wy - 34), (fx - 4, wy - 58), (fx + 6, wy - 42),
                  (fx + 20, wy - 60), (fx + 24, wy - 34)], fill=ORANGE)
    draw.polygon([(fx - 8, wy - 34), (fx, wy - 50), (fx + 10, wy - 34)], fill=FLAME)
    # hull
    draw.polygon([(x + 8, wy - 34), (x + s - 8, wy - 34), (x + s - 26, wy - 6),
                  (x + 22, wy - 6)], fill=INK)
    draw.rectangle([x + 14, wy - 62, x + s - 60, wy - 34], fill=RED)
    draw.rectangle([x + s - 56, wy - 76, x + s - 18, wy - 34], fill=CARD,
                   outline=INK, width=2)
    for i in range(3):
        draw.rectangle([x + 18 + i * 34, wy - 62, x + 44 + i * 34, wy - 40],
                       fill=TEAL, outline=INK, width=2)
    # waves
    for i, wx in enumerate(range(x + 4, x + s - 20, 34)):
        draw.arc([wx, wy + 2, wx + 34, wy + 22], 0, 180, fill=SKY, width=4)


def pic_factory(draw, x, y, s):
    """Sawtooth factory with chimney smoke and a flame, all inside the tile."""
    by = y + s - 14
    draw.rectangle([x + 8, y + 52, x + s - 32, by], fill=INK)
    for i in range(3):
        draw.polygon([(x + 8 + i * 30, y + 52), (x + 26 + i * 30, y + 34),
                      (x + 38 + i * 30, y + 52)], fill=INK)
    for i in range(3):
        draw.rectangle([x + 16 + i * 26, y + 70, x + 32 + i * 26, y + 90],
                       fill=FLAME)
    # chimney + smoke (smoke stays inside the tile)
    draw.rectangle([x + s - 28, y + 40, x + s - 12, by], fill=GREY)
    for (sx, sy, sr) in [(x + s - 20, y + 30, 6), (x + s - 27, y + 20, 7)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(200, 200, 196), outline=GREY, width=2)
    # small flame on the roof
    fx = x + 44
    draw.polygon([(fx - 12, y + 52), (fx - 2, y + 32), (fx + 5, y + 44),
                  (fx + 14, y + 34), (fx + 15, y + 52)], fill=ORANGE)


def pic_flag(draw, x, y, s):
    """Chequered flag on a pole beside a small trophy."""
    # pole + flag
    draw.line([x + 18, y + 12, x + 18, y + s - 10], fill=INK, width=5)
    cw, ch = 24, 20
    for r in range(3):
        for c in range(4):
            col = INK if (r + c) % 2 == 0 else CARD
            draw.rectangle([x + 20 + c * cw, y + 12 + r * ch,
                            x + 20 + (c + 1) * cw, y + 12 + (r + 1) * ch],
                           fill=col, outline=INK, width=2)
    # trophy
    tx = x + s - 62
    draw.polygon([(tx, y + s - 66), (tx + 44, y + s - 66), (tx + 36, y + s - 34),
                  (tx + 8, y + s - 34)], fill=GOLD, outline=INK, width=3)
    draw.arc([tx - 14, y + s - 64, tx + 10, y + s - 36], 90, 270, fill=INK, width=4)
    draw.arc([tx + 34, y + s - 64, tx + 58, y + s - 36], 270, 90, fill=INK, width=4)
    draw.rectangle([tx + 18, y + s - 34, tx + 26, y + s - 18], fill=INK)
    draw.rectangle([tx + 6, y + s - 18, tx + 38, y + s - 10], fill=INK)
    # big 8 for the eighth title, below the flag
    draw.text((x + 22, y + s - 50), "8", font=SANS_B(44), fill=RED)


def pic_boat(draw, x, y, s):
    """Small boat, listing on the waves. All coords are fractions of s,
    so it draws correctly at any tile size."""
    wy = y + 0.72 * s
    # sail
    draw.polygon([(x + 0.45 * s, wy - 0.55 * s), (x + 0.82 * s, wy - 0.28 * s),
                  (x + 0.45 * s, wy - 0.28 * s)], fill=RED, outline=INK, width=2)
    draw.line([x + 0.45 * s, wy - 0.55 * s, x + 0.45 * s, wy - 0.20 * s],
              fill=INK, width=3)
    # hull, listing to starboard
    draw.polygon([(x + 0.10 * s, wy - 0.16 * s), (x + 0.88 * s, wy - 0.30 * s),
                  (x + 0.78 * s, wy - 0.02 * s), (x + 0.20 * s, wy - 0.02 * s)],
                 fill=TEAL, outline=INK, width=3)
    # waves
    for i in range(3):
        wx = x + 0.04 * s + i * 0.30 * s
        draw.arc([wx, wy + 0.04 * s, wx + 0.28 * s, wy + 0.18 * s], 0, 180,
                 fill=SKY, width=4)


# ---------------------------------------------------------------- page build
def story_card(draw, x, y, w, h, pic, kicker, headline, body, head_size=24):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=INK, width=2)
    tile = 118
    draw.rounded_rectangle([x + 10, y + 10, x + 10 + tile, y + 10 + tile], radius=8,
                           fill=TINT, outline=INK, width=2)
    pic(draw, x + 10, y + 10, tile)
    tx = x + 10 + tile + 14
    tw = x + w - 14 - tx
    draw.text((tx, y + 12), kicker, font=SANS_B(16), fill=RED)
    lines = wrap(draw, headline, SERIF_B(head_size), tw)
    ly = y + 36
    for ln in lines[:2]:
        draw.text((tx, ly), ln, font=SERIF_B(head_size), fill=INK)
        ly += head_size + 4
    ly += 2
    for ln in wrap(draw, body, SANS(17), tw)[:2]:
        draw.text((tx, ly), ln, font=SANS(17), fill=INK)
        ly += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=4)

    # ---- masthead
    centre(d, 24, "THE WORLD'S NEWS  ·  ONE DAY  ·  ONE PICTURE", SANS_B(19), GREY)
    centre(d, 50, "THE WORLD TODAY", SERIF_B(62), INK)
    d.line([40, 124, W - 40, 124], fill=INK, width=3)
    d.line([40, 130, W - 40, 130], fill=INK, width=1)
    centre(d, 140, "SUNDAY  22  NOVEMBER  2026", SANS_B(42), RED)
    centre(d, 190, "Six stories from every corner of the globe",
           SERIF(20), GREY)

    # ---- lead story: COP31
    ly = 222
    d.line([40, ly - 8, W - 40, ly - 8], fill=INK, width=2)
    d.text((40, ly), "CLIMATE  ·  ANTALYA, TURKEY", font=SANS_B(19), fill=RED)
    d.text((40, ly + 28), "CLIMATE TALKS", font=SERIF_B(56), fill=INK)
    d.text((40, ly + 88), "COLLAPSE", font=SERIF_B(56), fill=INK)
    deck = ("COP31 ends with no deal after the EU and island states reject "
            "a draft that never mentions fossil fuels — the first failed "
            "summit since Copenhagen in 2009.")
    dy = ly + 158
    for ln in wrap(d, deck, SANS(21), 580):
        d.text((40, dy), ln, font=SANS(21), fill=INK)
        dy += 27
    # lead pictogram tile
    tx0, ty0, tw, th = 648, ly - 2, 336, 238
    d.rounded_rectangle([tx0, ty0, tx0 + tw, ty0 + th], radius=10, fill=TINT,
                        outline=INK, width=2)
    pic_globe(d, tx0 + 14, ty0 + 8, 180)
    d.rounded_rectangle([tx0 + 182, ty0 + 100, tx0 + 322, ty0 + 142], radius=6,
                        outline=RED, width=4)
    d.text((tx0 + 192, ty0 + 107), "NO DEAL", font=SANS_B(24), fill=RED)
    d.text((tx0 + 14, ty0 + 196), "Longest COP ever — no pact.",
           font=SANS(17), fill=GREY)

    # ---- four story cards, 2 x 2
    gy = 472
    cw, chh, gap = 472, 156, 14
    story_card(d, 32, gy, cw, chh, pic_scales,
               "JUSTICE  ·  THE HAGUE",
               "MYANMAR GUILTY OF GENOCIDE",
               "Guilty of genocide against the Rohingya in 2017.")
    story_card(d, 32 + cw + gap, gy, cw, chh, pic_tanker,
               "ENERGY  ·  STRAIT OF HORMUZ",
               "IRAN HITS TANKERS AT HORMUZ",
               "Three tankers struck as Tehran shows off missile "
               "launchers.")
    story_card(d, 32, gy + chh + gap, cw, chh, pic_factory,
               "DISASTER  ·  CIKANDE, INDONESIA",
               "FACTORY FIRE: 3 DEAD, 36 MISSING",
               "A candy factory burns in Cikande; rescuers search "
               "the ruins.")
    story_card(d, 32 + cw + gap, gy + chh + gap, cw, chh, pic_flag,
               "SPORT  ·  PORTIMÃO, PORTUGAL",
               "MARQUEZ SEALS 8TH TITLE",
               "Eighth at Portimão seals the crown, level with "
               "Agostini.")

    # ---- bottom strip: Nigeria boat
    by = 812
    d.rounded_rectangle([32, by, W - 32, by + 72], radius=10, fill=CARD,
                        outline=INK, width=2)
    d.rounded_rectangle([42, by + 8, 42 + 92, by + 64], radius=8, fill=TINT,
                        outline=INK, width=2)
    pic_boat(d, 42 + 16, by + 8, 60)
    d.text((150, by + 10), "NIGERIA: BOAT CAPSIZES — AT LEAST 24 DEAD",
           font=SERIF_B(24), fill=INK)
    d.text((150, by + 42), "A boat carrying mourners to a funeral overturns.",
           font=SANS(19), fill=INK)

    # ---- also on the day
    ay = 896
    d.text((40, ay), "ALSO ON THE DAY", font=SANS_B(18), fill=RED)
    d.line([40, ay + 26, W - 40, ay + 26], fill=INK, width=2)
    also1 = ("KYIV — Russian strike on an apartment block kills 3   ·   "
             "WEST BANK — Settlers torch 12 vehicles")
    also2 = ("CRICKET — India declare 720/9 against New Zealand   ·   "
             "NEPAL — PM Balendra Shah visits India")
    d.text((40, ay + 36), also1, font=SANS(18), fill=INK)
    d.text((40, ay + 62), also2, font=SANS(18), fill=INK)

    # ---- footer
    centre(d, 984, "Sources: Reuters · AP · CNN · Le Monde — all events of 22 November 2026",
           SANS(14), GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
