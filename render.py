#!/usr/bin/env python3
"""Render the news-image-20261126 entry: one 1024x1024 PNG summing up
Thursday 26 November 2026 world news. PIL + DejaVu only, no network,
no randomness, no timestamps. Deterministic: same input -> same bytes."""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1024, 1024
BG = (247, 243, 234)
GREEN = (18, 59, 42)
GOLD = (232, 184, 75)
RED = (176, 58, 46)
NAVY = (14, 42, 71)
DARK = (51, 51, 51)
GREY = (68, 68, 68)
WHITE = (255, 255, 255)
PANEL = (220, 230, 238)
CHARCOAL = (34, 34, 34)
LIGHTGREY = (200, 200, 200)

MAP_RANGES = {
    0: [(8, 14), (30, 33), (40, 48)], 1: [(6, 16), (29, 34), (38, 52)],
    2: [(5, 17), (28, 35), (37, 55)], 3: [(6, 18), (29, 34), (38, 56)],
    4: [(7, 18), (30, 33), (38, 55)], 5: [(8, 17), (31, 33), (39, 54)],
    6: [(9, 16), (31, 34), (40, 53)], 7: [(10, 16), (31, 35), (40, 52)],
    8: [(11, 15), (32, 35), (41, 50)], 9: [(12, 15), (33, 35), (42, 49)],
    10: [(13, 15), (33, 35), (43, 48)], 11: [(14, 16), (31, 35), (44, 48)],
    12: [(15, 17), (30, 35), (45, 49)], 13: [(16, 18), (30, 34), (46, 49)],
    14: [(17, 19), (31, 33), (46, 48)], 15: [(18, 20), (31, 33), (47, 49)],
    16: [(18, 21), (31, 33), (48, 50)], 17: [(19, 21), (32, 33), (48, 51)],
    18: [(19, 22), (48, 51)], 19: [(20, 22), (49, 51)],
    20: [(20, 22), (49, 52)], 21: [(20, 22), (50, 53)],
    22: [(20, 21), (51, 54)], 23: [(20, 21), (51, 55)],
    24: [(20, 21), (52, 55)], 25: [(20, 21), (52, 55)],
    26: [(20, 21), (53, 56)], 27: [(20, 20), (53, 56)],
    28: [(53, 55)], 29: [(53, 55)], 30: [(54, 55)], 31: [],
}


def font(bold, size):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def fit(text, fnt, max_w, draw):
    """Truncate text with ellipsis to fit max_w pixels."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "…"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if draw.textlength(text[:mid] + ell, font=fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + ell


def wrap(text, fnt, max_w, draw, max_lines=None):
    """Greedy word wrap; returns list of lines."""
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
            if max_lines and len(lines) >= max_lines:
                break
    if cur and (not max_lines or len(lines) < max_lines):
        lines.append(cur)
    return lines


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead (0-84) ----
    d.rectangle([0, 0, W, 84], fill=GREEN)
    d.text((24, 16), "THE WORLD TODAY", font=font(True, 48), fill=WHITE)
    date_txt = "THURSDAY 26 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=font(True, 22))
    d.text((W - 24 - dw, 30), date_txt, font=font(True, 22), fill=GOLD)
    d.rectangle([0, 84, W, 87], fill=GOLD)

    # ---- Lead hero (92-260) ----
    lx0, ly0, lx1, ly1 = 16, 92, 1008, 260
    d.rectangle([lx0, ly0, lx1, ly1], fill=WHITE)
    d.rectangle([lx0, ly0, lx0 + 8, ly1], fill=RED)
    lead = data["lead"]
    chip = " " + lead["kicker"] + " "
    cf = font(True, 16)
    cw = d.textlength(chip, font=cf)
    d.rectangle([lx0 + 20, ly0 + 12, lx0 + 20 + cw, ly0 + 12 + 24], fill=RED)
    d.text((lx0 + 20, ly0 + 14), chip, font=cf, fill=WHITE)
    dc = " " + lead["date"] + " "
    df = font(True, 15)
    dcw = d.textlength(dc, font=df)
    d.rectangle([lx1 - 16 - dcw, ly0 + 12, lx1 - 16, ly0 + 12 + 22], fill=RED)
    d.text((lx1 - 16 - dcw, ly0 + 13), dc, font=df, fill=WHITE)
    hf = font(True, 36)
    d.text((lx0 + 20, ly0 + 44), "TRUMP UNVEILS NEW TARIFFS", font=hf, fill=GREEN)
    d.text((lx0 + 20, ly0 + 84), "ON 14 PARTNERS", font=hf, fill=GREEN)
    blines = wrap(lead["body"], font(False, 19), 620, d, max_lines=2)
    for i, ln in enumerate(blines):
        d.text((lx0 + 20, ly0 + 122 + i * 22), ln, font=font(False, 19), fill=DARK)
    for j, st in enumerate(lead["stats"]):
        sx = lx1 - 200 + j * 100
        d.text((sx, ly0 + 56), st["value"], font=font(True, 44), fill=RED)
        d.text((sx, ly0 + 102), st["label"], font=font(True, 12), fill=GREY)

    # ---- Map strip (260-392) ----
    mx0, my0, mx1, my1 = 16, 260, 1008, 392
    d.rectangle([mx0, my0, mx1, my1], fill=PANEL)
    d.text((mx0 + 16, my0 + 8), "WHERE THE NEWS HAPPENED — 26 NOV · ALL TIMES UTC",
           font=font(True, 19), fill=NAVY)
    # dotted world map: 64 cols x 32 rows, spacing 9 x 3.2, centred
    ox, oy = 224, 292
    dot_r = 1
    for row, spans in MAP_RANGES.items():
        for (c0, c1) in spans:
            for c in range(c0, c1 + 1):
                x, y = ox + c * 9, oy + row * 3.2
                if mx0 + 4 <= x <= mx1 - 4 and my0 + 30 <= y <= my1 - 4:
                    d.ellipse([x - dot_r, y - dot_r, x + dot_r, y + dot_r], fill=NAVY)
    for card in data["cards"]:
        col, row = card["pin"]
        x, y = ox + col * 9, oy + row * 3.2
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=WHITE)
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=RED)
        num = str(card["n"])
        nf = font(True, 8)
        nw = d.textlength(num, font=nf)
        d.text((x - nw / 2, y - 4), num, font=nf, fill=WHITE)

    # ---- Story grid (400-840): 2 cols x 7 rows, card 492x56, gap 8 ----
    gx0, gy0 = 16, 400
    cw_, ch_, gap = 492, 56, 8
    for i, card in enumerate(data["cards"]):
        r, c = divmod(i, 2)
        x0 = gx0 + c * (cw_ + gap)
        y0 = gy0 + r * (ch_ + gap)
        x1, y1 = x0 + cw_, y0 + ch_
        d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=(210, 210, 210))
        d.rectangle([x0, y0, x0 + 6, y1], fill=card["color"])
        kf = font(True, 12)
        kick = card["glyph"] + " " + card["region"]
        d.text((x0 + 14, y0 + 4), fit(kick, kf, 380, d), font=kf, fill=card["color"])
        dcf = font(True, 11)
        dc = " " + card["date"] + " "
        dcw = d.textlength(dc, font=dcf)
        d.rectangle([x1 - 8 - dcw, y0 + 4, x1 - 8, y0 + 4 + 16], fill=RED)
        d.text((x1 - 8 - dcw, y0 + 5), dc, font=dcf, fill=WHITE)
        d.text((x0 + 14, y0 + 19), fit(card["headline"], font(True, 17), cw_ - 28, d),
               font=font(True, 17), fill=NAVY)
        d.text((x0 + 14, y0 + 38), fit(card["body"], font(False, 14), cw_ - 28, d),
               font=font(False, 14), fill=GREY)

    # ---- Briefs ticker (848-952) ----
    tx0, ty0, tx1, ty1 = 16, 848, 1008, 952
    d.rectangle([tx0, ty0, tx1, ty1], fill=CHARCOAL)
    joined = " • ".join(data["briefs"])
    lab = "ALSO TODAY: "
    full_w = tx1 - tx0 - 32
    band_h = ty1 - ty0
    chosen = None
    for size in (13, 12, 11, 10):
        fnt = font(False, size)
        lw = d.textlength(lab, font=font(True, size))
        words = joined.split()
        lines, cur = [], ""
        first = True
        for w in words:
            trial = (cur + " " + w).strip()
            lim = full_w - lw if first else full_w
            if d.textlength(trial, font=fnt) <= lim:
                cur = trial
            else:
                lines.append(cur)
                cur = w
                first = False
        if cur:
            lines.append(cur)
        if len(lines) * (size + 3) <= band_h:
            chosen = (size, lines, lw)
            break
    assert chosen is not None, "ticker does not fit even at 10px"
    size, lines, lw = chosen
    # sanity: every brief must appear in the wrapped lines
    assert all(b in " ".join(lines) for b in data["briefs"]), "ticker dropped a brief"
    lh = size + 3
    total_h = len(lines) * lh
    y = ty0 + (ty1 - ty0 - total_h) // 2
    d.text((tx0 + 16, y), lab, font=font(True, size), fill=GOLD)
    if lines:
        d.text((tx0 + 16 + lw, y), lines[0], font=font(False, size), fill=WHITE)
    for i, ln in enumerate(lines[1:], start=1):
        d.text((tx0 + 16, y + i * lh), ln, font=font(False, size), fill=WHITE)

    # ---- Footer (960-1024) ----
    fx0, fy0, fx1, fy1 = 16, 960, 1008, 1024
    d.rectangle([fx0, fy0, fx1, fy1], fill=CHARCOAL)
    ff = font(False, 14)
    d.text((fx0 + 16, fy0 + 8), data["footer"]["date_check"], font=ff, fill=LIGHTGREY)
    rt = "THE WORLD TODAY — 26 NOV 2026"
    rw = d.textlength(rt, font=ff)
    d.text((fx1 - 16 - rw, fy0 + 8), rt, font=ff, fill=LIGHTGREY)
    d.text((fx0 + 16, fy0 + 32), data["footer"]["counts"], font=ff, fill=GOLD)

    out = os.path.join(HERE, "entry.png")
    img.convert("P", palette=Image.ADAPTIVE, colors=256).save(out, "PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
