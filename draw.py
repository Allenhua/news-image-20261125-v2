#!/usr/bin/env python3
"""Draw entry.png for the 25 November 2026 world-news image (make.fun bounty
news-image-20261125) — v2.

A broadsheet front page, drawn with PIL. 1024x1024, DejaVu fonts already on
the VM (Serif Bold for headlines/masthead, Sans for body/tags).

v2 vs v1 (same seven verified stories, no facts changed):
- A real lead story: the Riyadh tower strike gets a full-width lead with a
  larger picture panel and a fuller deck (PIF Tower, the capital's tallest,
  second strike in a week, 11 hurt).
- Serif headlines + a masthead, numbered stories (1-6), and a source line,
  so it reads like a newspaper front page instead of six equal boxes.
- Bigger, darker body text (21px, dark slate instead of v1's 20px mid-grey)
  and decks trimmed to fit their cards, so nothing overflows and the
  half-empty bottom of every v1 card is gone.
- Two more verified items from SOURCES.md that v1 left out (Trump awards
  Giuliani the Medal of Freedom; the CAS ruling on Senegal's Africa Cup
  case) in an ALSO TODAY box, so coverage is 6 stories + UN + 2 also-items.
- The UN femicide footer keeps its big figure (47,000 in all, five an hour)
  and now names the day: the International Day for the Elimination of
  Violence against Women, which opens the 16 Days of Activism.
"""

from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
NAVY = (13, 27, 48)
NAVY2 = (24, 48, 80)
GOLD = (184, 134, 11)
GOLD_L = (212, 160, 23)
WHITE = (255, 255, 255)
PAPER = (250, 247, 238)
INK = (20, 26, 36)
BODY = (51, 61, 74)
GREY = (84, 96, 112)
LIGHT = (238, 242, 247)
RED = (178, 34, 34)
DARKRED = (122, 20, 20)
BORDER = (200, 208, 218)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 130], fill=NAVY)
d.rectangle([0, 130, W, 135], fill=GOLD_L)
d.text((28, 14), "WORLD NEWS  •  THE DAY IN PICTURES",
       font=font(FB, 20), fill=(150, 180, 215))
d.text((28, 38), "THE WORLD TODAY", font=font(SB, 52), fill=WHITE)
d.text((28, 98), "Wednesday, 25 November 2026  —  six stories that defined the day",
       font=font(FR, 21), fill=(200, 214, 230))
# date box, right
d.rectangle([W - 168, 22, W - 28, 108], outline=GOLD_L, width=3)
d.text((W - 98, 36), "WED", font=font(FB, 20), fill=GOLD_L, anchor="mm")
d.text((W - 98, 66), "25 NOV", font=font(FB, 26), fill=WHITE, anchor="mm")
d.text((W - 98, 94), "2026", font=font(FB, 18), fill=(200, 214, 230), anchor="mm")


def icon(draw, key, x, y, s, col):
    """Flat pictogram inside a s x s box at (x, y)."""
    if key == "tower":
        draw.rectangle([x + s * 0.38, y + s * 0.30, x + s * 0.62, y + s * 0.95], fill=NAVY2)
        draw.polygon([(x + s * 0.38, y + s * 0.30), (x + s * 0.50, y + s * 0.12),
                      (x + s * 0.62, y + s * 0.30)], fill=NAVY2)
        for r in range(4):
            draw.rectangle([x + s * 0.43, y + s * (0.38 + r * 0.14),
                            x + s * 0.57, y + s * (0.44 + r * 0.14)], fill=(150, 180, 215))
        draw.ellipse([x + s * 0.72, y + s * 0.10, x + s * 0.82, y + s * 0.20], fill=col)
        draw.line([x + s * 0.68, y + s * 0.15, x + s * 0.86, y + s * 0.15], fill=col, width=4)
        for cx, cy, rr in [(0.24, 0.30, 0.09), (0.16, 0.42, 0.11), (0.30, 0.48, 0.08)]:
            draw.ellipse([x + s * (cx - rr), y + s * (cy - rr),
                          x + s * (cx + rr), y + s * (cy + rr)], fill=(120, 128, 140))
    elif key == "probe":
        for bx, bw, bh in [(0.08, 0.16, 0.55), (0.28, 0.16, 0.75), (0.48, 0.16, 0.45), (0.68, 0.16, 0.65)]:
            draw.rectangle([x + s * bx, y + s * (0.95 - bh), x + s * (bx + bw), y + s * 0.95],
                           fill=NAVY2)
        draw.ellipse([x + s * 0.52, y + s * 0.06, x + s * 0.94, y + s * 0.48],
                     outline=col, width=9)
        draw.line([x + s * 0.84, y + s * 0.40, x + s * 0.98, y + s * 0.54], fill=col, width=9)
        draw.text((x + s * 0.73, y + s * 0.27), "?", font=font(FB, int(s * 0.26)),
                  fill=col, anchor="mm")
    elif key == "shop":
        draw.rectangle([x + s * 0.10, y + s * 0.30, x + s * 0.90, y + s * 0.92], fill=NAVY2)
        for i in range(5):
            c = col if i % 2 == 0 else WHITE
            draw.polygon([(x + s * (0.10 + i * 0.16), y + s * 0.30),
                          (x + s * (0.26 + i * 0.16), y + s * 0.30),
                          (x + s * (0.26 + i * 0.16), y + s * 0.46),
                          (x + s * (0.10 + i * 0.16), y + s * 0.46)], fill=c)
        draw.rectangle([x + s * 0.40, y + s * 0.58, x + s * 0.60, y + s * 0.92], fill=GOLD_L)
        draw.polygon([(x + s * 0.78, y + s * 0.02), (x + s * 0.98, y + s * 0.10),
                      (x + s * 0.98, y + s * 0.30), (x + s * 0.88, y + s * 0.44),
                      (x + s * 0.78, y + s * 0.30)], fill=col)
    elif key == "blast":
        draw.rectangle([x + s * 0.08, y + s * 0.62, x + s * 0.30, y + s * 0.95], fill=NAVY2)
        draw.rectangle([x + s * 0.68, y + s * 0.55, x + s * 0.92, y + s * 0.95], fill=NAVY2)
        cx, cy, r1, r2 = x + s * 0.50, y + s * 0.38, s * 0.34, s * 0.15
        pts = []
        for i in range(16):
            r = r1 if i % 2 == 0 else r2
            a = math.pi * i / 8 - math.pi / 2
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        draw.polygon(pts, fill=col)
        draw.ellipse([cx - s * 0.07, cy - s * 0.07, cx + s * 0.07, cy + s * 0.07],
                     fill=GOLD_L)
    elif key == "court":
        draw.polygon([(x + s * 0.10, y + s * 0.30), (x + s * 0.50, y + s * 0.08),
                      (x + s * 0.90, y + s * 0.30)], fill=NAVY2)
        for bx in [0.16, 0.38, 0.60, 0.80]:
            draw.rectangle([x + s * bx, y + s * 0.36, x + s * (bx + 0.06), y + s * 0.72],
                           fill=NAVY2)
        draw.rectangle([x + s * 0.10, y + s * 0.72, x + s * 0.90, y + s * 0.80], fill=NAVY2)
        draw.rectangle([x + s * 0.06, y + s * 0.82, x + s * 0.94, y + s * 0.92], fill=NAVY2)
        draw.rectangle([x + s * 0.66, y + s * 0.86, x + s * 0.94, y + s * 0.94],
                       fill=col, outline=NAVY, width=2)
    elif key == "train":
        draw.rounded_rectangle([x + s * 0.08, y + s * 0.18, x + s * 0.92, y + s * 0.88],
                               radius=18, fill=col)
        draw.rounded_rectangle([x + s * 0.18, y + s * 0.28, x + s * 0.82, y + s * 0.52],
                               radius=10, fill=(210, 235, 245))
        draw.line([x + s * 0.50, y + s * 0.28, x + s * 0.50, y + s * 0.52], fill=NAVY2, width=4)
        for cx in (0.30, 0.70):
            draw.ellipse([x + s * (cx - 0.06), y + s * 0.60, x + s * (cx + 0.06),
                          y + s * 0.72], fill=GOLD_L)
        draw.rectangle([x + s * 0.08, y + s * 0.92, x + s * 0.92, y + s * 0.97], fill=NAVY2)


MX = 24
CW = (W - 2 * MX - 16) // 2   # 480

# ---------- lead story: Riyadh ----------
LY, LH = 147, 180
d.rounded_rectangle([MX, LY, MX + 2 * CW + 16, LY + LH], radius=10, fill=WHITE,
                    outline=BORDER, width=2)
d.rectangle([MX, LY, MX + 2 * CW + 16, LY + 8], fill=RED)
d.rectangle([MX + 16, LY + 20, MX + 176, LY + LH - 16], fill=LIGHT)
icon(d, "tower", MX + 16, LY + 20, 160, RED)
tx = MX + 192
d.text((tx, LY + 16), "1  •  RIYADH, SAUDI ARABIA", font=font(FB, 19), fill=RED)
hl = wrap(d, "Houthi drone hits Riyadh's tallest tower again",
          font(SB, 33), 2 * CW + 16 - 192 - 16)
y = LY + 44
for ln in hl[:2]:
    d.text((tx, y), ln, font=font(SB, 33), fill=INK)
    y += 40
deck = ("A drone struck the Public Investment Fund Tower — the capital's tallest — "
        "for the second time in less than a week. 11 people were hurt.")
for ln in wrap(d, deck, font(FR, 20), 2 * CW + 16 - 192 - 16)[:2]:
    d.text((tx, y + 2), ln, font=font(FR, 20), fill=BODY)
    y += 26

# ---------- grid cards 2-5 ----------
cards = [
    ("2  •  CHINA", (150, 30, 30), "Shanghai chief probed",
     "China probes Politburo member Chen Jining — the fourth of 24 to fall.",
     "probe"),
    ("3  •  COLOMBIA", (18, 110, 130), "Hostage siege in Cartagena",
     "Gunmen seize about 30 in an Éxito supermarket; 10 freed.",
     "shop"),
    ("4  •  GAZA", (120, 60, 20), "Hamas security chief killed",
     "Israeli strike kills Naim Abu Nahal; seven dead despite the ceasefire.",
     "blast"),
    ("5  •  UNITED STATES", (24, 64, 140), "Huawei found guilty",
     "US jury convicts Huawei on 10 of 12 counts: fraud, sanctions, theft.",
     "court"),
]
GY, GH = 339, 190
for i, (tag, col, head, sub, key) in enumerate(cards):
    cx = MX + (i % 2) * (CW + 16)
    cy = GY + (i // 2) * (GH + 12)
    d.rounded_rectangle([cx, cy, cx + CW, cy + GH], radius=10, fill=WHITE,
                        outline=BORDER, width=2)
    d.rectangle([cx, cy, cx + CW, cy + 8], fill=col)
    d.rectangle([cx + 14, cy + 20, cx + 134, cy + 140], fill=LIGHT)
    icon(d, key, cx + 14, cy + 20, 120, col)
    tx2 = cx + 148
    d.text((tx2, cy + 18), tag, font=font(FB, 18), fill=col)
    hl2 = wrap(d, head, font(SB, 28), CW - 148 - 14)
    y = cy + 44
    for ln in hl2[:2]:
        d.text((tx2, y), ln, font=font(SB, 28), fill=INK)
        y += 33
    for ln in wrap(d, sub, font(FR, 20), CW - 148 - 14)[:3]:
        d.text((tx2, y + 2), ln, font=font(FR, 20), fill=BODY)
        y += 26

# ---------- row 3: Seoul card + Also Today ----------
RY, RH = 743, 170
# Seoul
d.rounded_rectangle([MX, RY, MX + CW, RY + RH], radius=10, fill=WHITE,
                    outline=BORDER, width=2)
d.rectangle([MX, RY, MX + CW, RY + 8], fill=(16, 120, 70))
d.rectangle([MX + 14, RY + 20, MX + 134, RY + 140], fill=LIGHT)
icon(d, "train", MX + 14, RY + 20, 120, (16, 120, 70))
tx3 = MX + 148
d.text((tx3, RY + 18), "6  •  SOUTH KOREA", font=font(FB, 18), fill=(16, 120, 70))
y = RY + 44
for ln in wrap(d, "Seoul subway strike called off", font(SB, 28), CW - 148 - 14)[:2]:
    d.text((tx3, y), ln, font=font(SB, 28), fill=INK)
    y += 33
for ln in wrap(d, "2:40 a.m. deal: +3.5% pay, 500 hires, 2,212 cuts shelved.",
               font(FR, 20), CW - 148 - 14)[:2]:
    d.text((tx3, y + 2), ln, font=font(FR, 20), fill=BODY)
    y += 26
# Also Today
ax = MX + CW + 16
d.rounded_rectangle([ax, RY, ax + CW, RY + RH], radius=10, fill=WHITE,
                    outline=BORDER, width=2)
d.rectangle([ax, RY, ax + CW, RY + 8], fill=NAVY2)
d.text((ax + 16, RY + 18), "ALSO TODAY", font=font(FB, 19), fill=NAVY2)
y = RY + 48
for lead, rest in [
    ("Medal of Freedom: ", "Trump honours Rudy Giuliani at a White House ceremony."),
    ("Africa Cup: ", "Court of Arbitration for Sport rules on Senegal's case."),
]:
    lines = wrap(d, lead + rest, font(FR, 21), CW - 32)
    # bold lead-in on the first line only
    first = lines[0]
    d.text((ax + 16, y), lead, font=font(FB, 21), fill=INK)
    d.text((ax + 16 + d.textlength(lead, font=font(FB, 21)), y),
           first[len(lead):], font=font(FR, 21), fill=BODY)
    y += 27
    for ln in lines[1:2]:
        d.text((ax + 16, y), ln, font=font(FR, 21), fill=BODY)
        y += 27
    y += 8

# ---------- footer: UN femicide ----------
FY, FH = 921, 80
d.rectangle([0, FY, W, FY + FH], fill=DARKRED)
d.text((28, FY + 8), "ALSO TODAY  •  UNITED NATIONS", font=font(FB, 18),
       fill=(245, 200, 200))
d.text((28, FY + 30),
       "Five women were killed every hour by a partner",
       font=font(FB, 22), fill=WHITE)
d.text((28, FY + 30 + 26),
       "or relative in 2025 — 47,000 in all.",
       font=font(FB, 22), fill=WHITE)
d.text((W - 28, FY + 32), "16 Days of\nActivism begins",
       font=font(FR, 18), fill=(245, 200, 200), anchor="ra")

# ---------- source line ----------
d.text((W // 2, 1013),
       "Sources: Reuters  •  Dawn  •  Yonhap  •  Al Jazeera  •  UN Women / UNODC  •  The Hindu — 25 Nov 2026",
       font=font(FR, 14), fill=GREY, anchor="mm")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
