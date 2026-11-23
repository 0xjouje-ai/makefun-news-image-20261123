#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news poster (1024x1024 PNG).

A newspaper front page: masthead with the date, four story panels and a
bottom sport strip. Every illustration is drawn from flat shapes with PIL;
all text is set in DejaVu Sans / DejaVu Serif.

Layout rule: in each panel the tag sits top-left, the illustration lives
in a fixed top-right box, the headline runs down the left, and the subline
starts below the headline (dynamic y, never a fixed offset).
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 233)
INK = (26, 26, 46)
NAVY = (18, 38, 74)
RED = (179, 38, 30)
TEAL = (14, 124, 107)
GOLD = (200, 144, 26)
GREY = (90, 90, 100)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    leading = leading or int(fnt.size * 1.24)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def tag(draw, x, y, label, color):
    f = font(FB, 20)
    w = draw.textlength(label, font=f) + 22
    draw.rounded_rectangle([x, y, x + w, y + 30], radius=4, fill=color)
    draw.text((x + 11, y + 4), label, font=f, fill=(255, 255, 255))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((512, 16), "T H E   W O R L D   I N   O N E   D A Y",
       font=font(FB, 24), fill=(200, 210, 235), anchor="ma")
d.text((512, 46), "MONDAY, 23 NOVEMBER 2026",
       font=font(FSB, 56), fill=(255, 255, 255), anchor="ma")
d.text((512, 112), "The day's news, in one picture",
       font=font(FSS, 22), fill=(200, 210, 235), anchor="ma")
d.line([24, 148, 1000, 148], fill=RED, width=4)

MX = 24          # outer margin
CW = 476         # column width
GX = 524         # second column x
SUB = (50, 50, 60)


def panel(x, y, w, h, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 8], fill=accent)


def story(x, y, w, h, accent, label, headline, sub, art):
    """One panel: tag, headline (left), subline below it, art top-right.

    The subline stays in the left column (292 px) so it never runs
    under the illustration.
    """
    panel(x, y, w, h, accent)
    tag(d, x + 16, y + 20, label, accent)
    art(x, y)
    hy = text_block(d, x + 16, y + 58, headline, font(FSB, 30), INK, 292)
    text_block(d, x + 16, hy + 10, sub, font(FR, 19), SUB, 292, leading=24)


# ---------------------------------------------- 1. COP31 collapse (lead)
def art_cop31(x, y):
    cx, cy, r = x + 388, y + 78, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(66, 135, 200),
              outline=INK, width=3)
    d.ellipse([cx - 30, cy - 34, cx + 4, cy - 4], fill=(74, 160, 90))
    d.ellipse([cx + 2, cy + 6, cx + 32, cy + 34], fill=(74, 160, 90))
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    # a red crack splits the globe: no deal
    crack = [(cx - 34, cy - 52), (cx - 12, cy - 26), (cx - 26, cy - 2),
             (cx + 2, cy + 22), (cx - 10, cy + 44), (cx + 16, cy + 52)]
    d.line(crack, fill=RED, width=6, joint="curve")
    d.text((cx, cy + 62), "NO DEAL", font=font(FB, 20), fill=RED,
           anchor="ma")


story(MX, 164, CW, 300, TEAL, "CLIMATE  ·  ANTALYA",
      "COP31 COLLAPSES: NO DEAL",
      "The EU and UK reject a text that never names fossil fuels; the longest COP on record ends with nothing.",
      art_cop31)

# ------------------------------------------- 2. Hormuz tankers (lead)
def art_hormuz(x, y):
    bx, by = x + 330, y + 96
    # tanker hull
    d.polygon([(bx, by), (bx + 128, by), (bx + 116, by + 30),
               (bx + 12, by + 30)], fill=(60, 60, 70), outline=INK, width=3)
    d.rectangle([bx + 18, by - 26, bx + 46, by], fill=(200, 200, 210),
                outline=INK, width=2)
    d.rectangle([bx + 58, by - 16, bx + 78, by], fill=(200, 200, 210),
                outline=INK, width=2)
    # flames and smoke above the deck
    for fx, fh, col in [(bx + 30, 34, (230, 120, 30)),
                        (bx + 58, 46, (230, 80, 20)),
                        (bx + 88, 30, (240, 160, 40))]:
        d.polygon([(fx, by - 26), (fx + 12, by - 26 - fh),
                   (fx + 24, by - 26)], fill=col, outline=INK, width=2)
    d.ellipse([bx + 96, by - 78, bx + 122, by - 52], fill=(120, 120, 130))
    d.ellipse([bx + 110, by - 96, bx + 132, by - 74], fill=(150, 150, 160))
    # sea
    d.line([bx - 8, by + 44, bx + 136, by + 44], fill=(66, 135, 200), width=4)
    d.line([bx + 4, by + 56, bx + 124, by + 56], fill=(66, 135, 200), width=3)


story(GX, 164, CW, 300, RED, "MIDDLE EAST  ·  HORMUZ",
      "TANKERS BURN IN THE GULF",
      "More tankers are struck and hit mines in the Strait of Hormuz; attacks on shipping hit their highest level since the war began.",
      art_hormuz)

# ------------------------------------------------------- 3. Libya
def art_libya(x, y):
    bx, by = x + 388, y + 104
    # capsized corvette: tilted hull, bow down
    d.polygon([(bx - 52, by - 6), (bx + 52, by + 26), (bx + 40, by + 44),
               (bx - 44, by + 18)], fill=(90, 100, 115), outline=INK, width=3)
    d.rectangle([bx - 30, by - 30, bx - 6, by - 4], fill=(60, 60, 70),
                outline=INK, width=2)
    # sea drone skimming the water
    d.ellipse([bx - 6, by + 52, bx + 34, by + 66], fill=(40, 40, 55),
              outline=INK, width=2)
    d.line([bx + 4, by + 52, bx + 4, by + 44], fill=INK, width=3)
    d.line([bx + 24, by + 52, bx + 24, by + 44], fill=INK, width=3)
    # waves
    d.arc([bx - 58, by + 58, bx + 58, by + 96], 0, 180,
          fill=(66, 135, 200), width=4)
    d.arc([bx - 40, by + 72, bx + 40, by + 106], 0, 180,
          fill=(66, 135, 200), width=3)


story(MX, 484, CW, 252, NAVY, "AFRICA  ·  LIBYA",
      "SEA DRONES SINK WARSHIP",
      "Suspected Ukrainian drones hit the Russian corvette Merkury at Benghazi; the ship capsizes, 10 hurt.",
      art_libya)

# ------------------------------------------------------- 4. Mexico
def art_mexico(x, y):
    cx, cy = x + 388, y + 100
    # badge star
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rr = 52 if i % 2 == 0 else 24
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=GOLD, outline=INK, width=3)
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(255, 255, 255),
              outline=INK, width=2)
    d.text((cx, cy - 14), "$5m", font=font(FB, 20), fill=INK, anchor="ma")
    # handcuff link below the badge
    d.ellipse([cx - 44, cy + 58, cx - 12, cy + 90], outline=INK, width=5)
    d.ellipse([cx + 12, cy + 58, cx + 44, cy + 90], outline=INK, width=5)
    d.line([cx - 12, cy + 74, cx + 12, cy + 74], fill=INK, width=5)


story(GX, 484, CW, 252, GOLD, "AMERICAS  ·  MEXICO",
      "CHAPO ISIDRO CAPTURED",
      "Mexican forces seize the FBI's $5m-wanted Fausto Isidro Meza-Flores in Sinaloa after firefights kill 11.",
      art_mexico)

# ------------------------------------------------------- 5. Sport strip
PY3 = 756
panel(MX, PY3, 976, 190, (120, 90, 40))
tag(d, MX + 16, PY3 + 18, "SPORT", (120, 90, 40))
# football, top right
cx, cy, r = MX + 880, PY3 + 95, 46
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
          outline=INK, width=3)
d.polygon([(cx, cy - 16), (cx + 15, cy - 5), (cx + 9, cy + 13),
           (cx - 9, cy + 13), (cx - 15, cy - 5)], fill=INK)
for vx, vy in [(cx, cy - 16), (cx + 15, cy - 5), (cx + 9, cy + 13),
               (cx - 9, cy + 13), (cx - 15, cy - 5)]:
    ex = cx + (vx - cx) * 2.4
    ey = cy + (vy - cy) * 2.4
    d.line([vx, vy, ex, ey], fill=INK, width=2)
d.line([MX + 500, PY3 + 30, MX + 500, PY3 + 168], fill=(200, 200, 200), width=2)
hy = text_block(d, MX + 16, PY3 + 56,
                "LIVERPOOL ROUT UNITED IN POCHETTINO'S DEBUT",
                font(FSB, 26), INK, 460)
text_block(d, MX + 16, hy + 10,
           "Ten-man United are hammered at Anfield; Marquez seals an eighth MotoGP crown.",
           font(FR, 21), SUB, 460)

# ---------------------------------------------------------------- footer
d.line([MX, 962, 1000, 962], fill=INK, width=2)
d.text((512, 972),
       "Every story above happened, or was first reported, on Monday 23 November 2026.",
       font=font(FR, 19), fill=GREY, anchor="ma")

img.save("/home/hatch/workspace/makefun/news-image-20261123-entry/entry.png",
         optimize=True)
print("saved")
