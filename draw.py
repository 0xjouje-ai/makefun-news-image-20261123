#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summing up Monday 23 November 2026.

Layout (my own design): a navy masthead, then a 2x2 grid of story cards
with a text column on the left and a small pictogram on the right, then a
full-width sport strip and a footer line. Rendered with Pillow only.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
PAPER = (248, 244, 233)
CARD = (255, 255, 255)
INK = (22, 28, 52)
NAVY = (18, 36, 72)
NAVY_LIGHT = (178, 190, 216)
RULE_RED = (178, 34, 34)
BODY_GREY = (58, 62, 78)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font, falling back to Pillow's built-in font."""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default(size)


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)  # noqa: E731
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit inside width."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    """Draw stacked lines; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, text, cx, y, fnt, fill):
    """Draw text centred on cx."""
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def tag_chip(draw, x, y, label, colour):
    """A small coloured label chip; returns its width."""
    fnt = SANS_BOLD(17)
    w = draw.textlength(label, font=fnt) + 22
    draw.rounded_rectangle([x, y, x + w, y + 30], radius=6, fill=colour)
    draw.text((x + 11, y + 5), label, font=fnt, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- pictograms

def globe_icon(draw, cx, cy, r):
    """Cracked globe: blue disc, green land blobs, a red zig-zag crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(66, 135, 200),
                 outline=INK, width=3)
    draw.ellipse([cx - r + 12, cy - r + 14, cx - 8, cy - 2],
                 fill=(74, 160, 90))
    draw.ellipse([cx + 2, cy + 6, cx + r - 10, cy + r - 12],
                 fill=(74, 160, 90))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=NAVY_LIGHT, width=2)
    crack = [(cx - 14, cy - r + 4), (cx + 6, cy - r // 2), (cx - 10, cy),
             (cx + 10, cy + r // 2), (cx - 4, cy + r - 6)]
    draw.line(crack, fill=(200, 30, 30), width=5, joint="curve")
    draw.text((cx - 34, cy + r + 8), "NO DEAL", font=SANS_BOLD(16),
              fill=(178, 34, 34))


def tanker_icon(draw, cx, cy):
    """A tanker hull with flames and smoke above a wavy sea."""
    draw.polygon([(cx - 62, cy + 6), (cx + 62, cy + 6), (cx + 48, cy + 34),
                  (cx - 48, cy + 34)], fill=(52, 58, 84), outline=INK, width=2)
    draw.rectangle([cx - 34, cy - 12, cx - 8, cy + 6], fill=(200, 200, 205),
                   outline=INK, width=2)
    draw.rectangle([cx + 8, cy - 12, cx + 30, cy + 6], fill=(180, 185, 195),
                   outline=INK, width=2)
    for fx, fh in ((-46, 34), (-16, 46), (16, 36), (42, 28)):
        draw.polygon([(cx + fx - 9, cy - 12), (cx + fx, cy - 12 - fh),
                      (cx + fx + 9, cy - 12)],
                     fill=(232, 110, 28), outline=(160, 60, 10), width=1)
    for sx, sy, sr in ((-52, -62, 9), (-34, -76, 12), (-12, -66, 8)):
        draw.ellipse([cx + sx - sr, cy + sy - sr, cx + sx + sr, cy + sy + sr],
                     fill=(150, 150, 155))
    for wy, wl in ((cy + 48, 120), (cy + 62, 96)):
        draw.line([(cx - wl // 2, wy), (cx + wl // 2, wy)],
                  fill=(66, 135, 200), width=3)


def drone_ship_icon(draw, cx, cy):
    """A listing warship hull with a small drone hovering above it."""
    draw.polygon([(cx - 58, cy - 6), (cx + 56, cy + 18), (cx + 40, cy + 38),
                  (cx - 44, cy + 26)], fill=(96, 104, 122), outline=INK, width=2)
    draw.rectangle([cx - 18, cy - 34, cx + 8, cy - 8], fill=(70, 76, 94),
                   outline=INK, width=2)
    draw.line([(cx - 30, cy - 8), (cx - 30, cy + 14)], fill=INK, width=3)
    draw.line([(cx + 22, cy + 2), (cx + 22, cy + 24)], fill=INK, width=3)
    # drone: body + four rotors
    draw.ellipse([cx - 14, cy - 78, cx + 14, cy - 62], fill=(40, 44, 66),
                 outline=INK, width=2)
    for rx in (-26, 26):
        draw.line([(cx + rx - 12, cy - 74), (cx + rx + 12, cy - 74)],
                  fill=INK, width=3)
    draw.line([(cx - 14, cy - 70), (cx - 26, cy - 70)], fill=INK, width=2)
    draw.line([(cx + 14, cy - 70), (cx + 26, cy - 70)], fill=INK, width=2)
    draw.arc([cx - 58, cy + 48, cx + 58, cy + 78], 0, 180,
             fill=(66, 135, 200), width=3)
    draw.arc([cx - 40, cy + 60, cx + 40, cy + 86], 0, 180,
             fill=(66, 135, 200), width=2)


def badge_icon(draw, cx, cy):
    """A gold star badge marked $5m above a pair of handcuffs."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 52 if i % 2 == 0 else 22
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=(216, 164, 32), outline=(120, 84, 10), width=2)
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(255, 255, 255),
                 outline=INK, width=2)
    draw.text((cx - 21, cy - 11), "$5m", font=SANS_BOLD(17), fill=INK)
    for hx in (-26, 26):
        draw.ellipse([cx + hx - 15, cy + 62, cx + hx + 15, cy + 92],
                     outline=INK, width=4)
    draw.line([(cx - 11, cy + 77), (cx + 11, cy + 77)], fill=INK, width=4)


def football_icon(draw, cx, cy, r):
    """A simple football: circle, centre pentagon, spokes."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=INK, width=3)
    pts = []
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((cx + 20 * math.cos(ang), cy + 20 * math.sin(ang)))
    draw.polygon(pts, fill=INK)
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        ex = cx + r * math.cos(ang)
        ey = cy + r * math.sin(ang)
        px = cx + 20 * math.cos(ang)
        py = cy + 20 * math.sin(ang)
        draw.line([(px, py), (ex, ey)], fill=INK, width=2)


# ------------------------------------------------------------------- cards

def story_card(draw, box, accent, tag, headline, body, icon):
    """One grid card: accent bar, tag chip, headline + body on the left,
    pictogram on the right."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=(44, 48, 70),
                           width=2)
    draw.rectangle([x0 + 12, y0, x1 - 12, y0 + 8], fill=accent)
    tag_chip(draw, x0 + 18, y0 + 22, tag, accent)
    text_w = (x1 - x0) - 36 - 138
    y = y0 + 64
    y = draw_lines(draw, wrap(draw, headline, SERIF_BOLD(31), text_w),
                   x0 + 18, y, SERIF_BOLD(31), INK, 37)
    y += 8
    draw_lines(draw, wrap(draw, body, SANS(18), text_w),
               x0 + 18, y, SANS(18), BODY_GREY, 25)
    icon(draw, x1 - 82, y0 + 150)


def sport_strip(draw, box, headline, body):
    """Full-width bottom strip for the sport story."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=(44, 48, 70),
                           width=2)
    draw.rectangle([x0 + 12, y0, x1 - 12, y0 + 8], fill=(150, 100, 16))
    tag_chip(draw, x0 + 18, y0 + 22, "SPORT", (150, 100, 16))
    text_w = (x1 - x0) - 36 - 170
    # Shrink the headline until it fits on a single line.
    size = 30
    while size > 22:
        fnt = SERIF_BOLD(size)
        if len(wrap(draw, headline, fnt, text_w)) == 1:
            break
        size -= 1
    y = draw_lines(draw, [headline], x0 + 18, y0 + 60, fnt, INK, size + 6)
    draw_lines(draw, wrap(draw, body, SANS(18), text_w),
               x0 + 18, y + 8, SANS(18), BODY_GREY, 25)
    football_icon(draw, x1 - 96, y0 + (y1 - y0) // 2 + 6, 52)


def masthead(draw):
    """Navy banner naming the day, with a red rule underneath."""
    draw.rectangle([0, 0, CANVAS[0], 148], fill=NAVY)
    centred(draw, "T H E   W O R L D   I N   O N E   D A Y", 512, 20,
            SANS_BOLD(23), NAVY_LIGHT)
    centred(draw, "MONDAY, 23 NOVEMBER 2026", 512, 50, SERIF_BOLD(56),
            (255, 255, 255))
    centred(draw, "The day's news, in one picture", 512, 118, SERIF(23),
            NAVY_LIGHT)
    draw.rectangle([0, 148, CANVAS[0], 153], fill=RULE_RED)


def build():
    img = Image.new("RGB", CANVAS, PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)

    margin, gap = 26, 16
    col_w = (CANVAS[0] - 2 * margin - gap) // 2
    row_h = 310
    top = 166

    cards = [
        ((margin, top, margin + col_w, top + row_h),
         (14, 128, 110), "CLIMATE  ·  ANTALYA",
         "COP31 COLLAPSES: NO DEAL",
         "The EU and UK reject a text that never names fossil fuels; "
         "the longest COP on record ends with nothing.",
         lambda d, cx, cy: globe_icon(d, cx, cy, 56)),
        ((margin + col_w + gap, top, CANVAS[0] - margin, top + row_h),
         (178, 34, 34), "MIDDLE EAST  ·  HORMUZ",
         "TANKERS BURN IN THE GULF",
         "More tankers are struck and hit mines in the Strait of "
         "Hormuz; attacks on shipping hit their highest level since "
         "the war began.",
         tanker_icon),
        ((margin, top + row_h + gap, margin + col_w, top + 2 * row_h + gap),
         NAVY, "AFRICA  ·  LIBYA",
         "SEA DRONES SINK WARSHIP",
         "Suspected Ukrainian drones hit the Russian corvette Merkury "
         "at Benghazi; the ship capsizes, 10 hurt.",
         drone_ship_icon),
        ((margin + col_w + gap, top + row_h + gap,
          CANVAS[0] - margin, top + 2 * row_h + gap),
         (178, 130, 24), "AMERICAS  ·  MEXICO",
         "CHAPO ISIDRO CAPTURED",
         "Mexican forces seize the FBI's $5m-wanted Fausto Isidro "
         "Meza-Flores in Sinaloa after firefights kill 11.",
         badge_icon),
    ]
    for box, accent, tag, headline, body, icon in cards:
        story_card(draw, box, accent, tag, headline, body, icon)

    sport_y = top + 2 * row_h + 2 * gap
    sport_strip(draw, (margin, sport_y, CANVAS[0] - margin, sport_y + 162),
                "LIVERPOOL ROUT UNITED IN POCHETTINO'S DEBUT",
                "Ten-man United are hammered at Anfield; Marquez seals "
                "an eighth MotoGP crown.")

    draw.line([(margin, 994), (CANVAS[0] - margin, 994)], fill=INK, width=2)
    centred(draw,
            "Every story above happened, or was first reported, on "
            "Monday 23 November 2026.",
            512, 1002, SERIF(18), BODY_GREY)
    return img


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().save(out, optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")
