#!/usr/bin/env python3
"""news-23 b162 front-page-dense: THE WORLD TODAY, Monday 23 November 2026.
Draws a 1024x1024 front page summarising 23 Nov 2026 world news (31 stories).
PIL only; run: python3 draw.py  -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (14, 42, 74)
NAVY2 = (20, 58, 96)
GOLD = (201, 162, 39)
GOLD_LT = (232, 196, 90)
RED = (179, 38, 30)
RED_LT = (246, 226, 224)
TEAL = (16, 74, 74)
GREY = (90, 88, 80)
LINE = (180, 175, 160)
WHITE = (255, 255, 255)
GREEN = (28, 110, 60)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, text, f):
    return d.textlength(text, font=f)


def fit(d, text, fpath, size, max_w, min_size=8):
    """Largest font size (<=size) that fits max_w, else truncated with ellipsis."""
    s = size
    while s > min_size:
        f = font(fpath, s)
        if tw(d, text, f) <= max_w:
            return f, text
        s -= 1
    f = font(fpath, min_size)
    t = text
    while t and tw(d, t + "\u2026", f) > max_w:
        t = t[:-1]
    return f, t + "\u2026"


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, text, fill, fg=WHITE):
    f = font(SANS_B, 9)
    w_ = int(tw(d, text, f)) + 10
    d.rounded_rectangle([x, y, x + w_, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), text, font=f, fill=fg)
    return w_


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    CW = W - 2 * M  # 976

    # ---------- masthead ----------
    y = 10
    f_title = font(SERIF_B, 46)
    d.text((M, y), "THE WORLD TODAY", font=f_title, fill=INK)
    f_date = font(SANS_B, 15)
    dt = "MONDAY 23 NOVEMBER 2026"
    d.text((W - M - tw(d, dt, f_date), y + 16), dt, font=f_date, fill=NAVY)
    y = 66
    d.line([(M, y), (W - M, y)], fill=INK, width=3)
    y = 72
    f_kick = font(SANS_B, 12)
    kick = "AI ROUT HITS ASIA  \u00b7  GUTERRES: REGULATE AI BEFORE IT'S TOO LATE  \u00b7  US LEAD OVER CHINA AT RECORD LOW"
    f_kick2, kick2 = fit(d, kick, SANS_B, 12, CW)
    d.text((M, y), kick2, font=f_kick2, fill=RED)
    y = 92

    # ---------- number strip ----------
    strip = [
        ("-3.3%", "KOSPI FALLS"),
        ("5.3", "US-CHINA GAP"),
        ("11,762", "EBOLA CASES, DRC"),
        ("10T won", "SEOUL RESCUE FUND"),
        ("2%", "BILLIONAIRE TAX"),
        ("$450M", "SKUBAL TO METS"),
        ("165", "MISSILES / WEEK"),
        ("12,000", "MANCHESTER CLEARED"),
        ("264 kg", "EXPLOSIVES, LEBANON"),
        ("$107.3B", "ANTHROPIC IPO"),
    ]
    d.rectangle([M, y, W - M, y + 62], outline=LINE, width=1)
    col_w = CW / 5
    for i, (val, lab) in enumerate(strip):
        cx = M + (i % 5) * col_w
        cy = y + (i // 5) * 31
        fv, _ = fit(d, val, SANS_B, 19, col_w - 12)
        d.text((cx + 8, cy + 2), val, font=fv, fill=NAVY)
        fl, _ = fit(d, lab, SANS_B, 9, col_w - 12)
        d.text((cx + 8, cy + 19), lab, font=fl, fill=GREY)
        if i % 5 < 4:
            d.line([(cx + col_w, cy + 3), (cx + col_w, cy + 28)], fill=LINE, width=1)
    y = 162

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC", 7), ("AMERICAS", 8), ("MIDDLE EAST", 6),
               ("EUROPE", 5), ("AFRICA", 3), ("WORLD", 2)]
    f_reg = font(SANS_B, 11)
    x = M
    d.text((x, y), "REGIONS:", font=f_reg, fill=INK)
    x += tw(d, "REGIONS:  ", f_reg)
    for name, n in regions:
        t = "%s %d" % (name, n)
        d.text((x, y), t, font=f_reg, fill=NAVY)
        x += tw(d, t + "   \u00b7   ", f_reg)
    d.text((W - M - tw(d, "31 STORIES", f_reg), y), "31 STORIES", font=f_reg, fill=RED)
    y = 186

    # ---------- black strip: TOP STORIES ----------
    d.rectangle([M, y, W - M, y + 22], fill=INK)
    d.text((M + 8, y + 4), "THE DAY'S TOP STORIES", font=font(SANS_B, 12), fill=WHITE)
    y = 212

    # ---------- hero scenes ----------
    hero_w = 317
    gap = (CW - 3 * hero_w) // 2  # 12
    scene_h = 132
    heroes = [
        dict(head="AI ROUT HITS ASIA",
             body="Kospi sinks 3.3% to 4,708.54, shedding 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
             src="REUTERS", scene="kospi"),
        dict(head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
             body="150 delegates at the Bridgetown summit back a risk framework \u2014 a blueprint, not a treaty.",
             src="AP", scene="guterres"),
        dict(head="US LEAD OVER CHINA AT RECORD LOW",
             body="Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India 3rd at 40.5.",
             src="BLOOMBERG", scene="power"),
    ]
    hx = M
    for h in heroes:
        # scene
        d.rectangle([hx, y, hx + hero_w, y + scene_h], fill=NAVY)
        if h["scene"] == "kospi":
            # skyline
            import random
            rnd = random.Random(7)
            bx = hx + 6
            while bx < hx + hero_w - 20:
                bw = rnd.randint(18, 30)
                bh = rnd.randint(34, 78)
                d.rectangle([bx, y + scene_h - bh, bx + bw, y + scene_h],
                            fill=(24, 68, 110))
                for wx in range(bx + 4, bx + bw - 3, 7):
                    for wy in range(y + scene_h - bh + 5, y + scene_h - 4, 9):
                        if rnd.random() < 0.55:
                            d.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD_LT)
                bx += bw + 3
            # falling chart line
            pts = [(hx + 10, y + 34), (hx + 80, y + 52), (hx + 150, y + 44),
                   (hx + 220, y + 78), (hx + 300, y + 96)]
            d.line(pts, fill=(255, 122, 26), width=4)
            f_big = font(SANS_B, 30)
            d.text((hx + 12, y + 8), "-3.3%", font=f_big, fill=GOLD_LT)
            # caption band
            d.rectangle([hx, y + scene_h - 18, hx + hero_w, y + scene_h], fill=NAVY2)
            f_cap = font(SANS_B, 10)
            d.text((hx + 8, y + scene_h - 15),
                   "KOSPI 4,708.54 \u00b7 -161 PTS", font=f_cap, fill=WHITE)
        elif h["scene"] == "guterres":
            d.rectangle([hx, y, hx + hero_w, y + scene_h], fill=TEAL)
            # globe
            cx, cy, r = hx + hero_w - 62, y + 62, 44
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 110, 180),
                      outline=GOLD, width=2)
            d.ellipse([cx - r + 12, cy - r + 14, cx - r + 34, cy - r + 34], fill=(70, 160, 90))
            d.ellipse([cx + 4, cy + 2, cx + 30, cy + 26], fill=(70, 160, 90))
            d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=WHITE, width=2)
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=WHITE, width=2)
            f_g = font(SANS_B, 15)
            d.text((hx + 10, y + 12), "150 DELEGATES", font=f_g, fill=GOLD_LT)
            d.text((hx + 10, y + 32), "BRIDGETOWN", font=f_g, fill=WHITE)
            d.text((hx + 10, y + 52), "SUMMIT", font=f_g, fill=WHITE)
            # small flags row
            for i, c in enumerate([(200, 60, 60), (60, 120, 200), (60, 160, 90),
                                   (220, 180, 40)]):
                fx = hx + 12 + i * 26
                d.rectangle([fx, y + 96, fx + 20, y + 110], fill=c, outline=WHITE)
                d.line([(fx, y + 96), (fx, y + 114)], fill=WHITE, width=2)
        else:  # power bars
            d.text((hx + 10, y + 8), "ASIA POWER INDEX 2026", font=font(SANS_B, 11),
                   fill=GOLD_LT)
            bars = [("US", 78.9), ("CHINA", 73.6), ("INDIA", 40.5)]
            by = y + 30
            for name, val in bars:
                d.text((hx + 10, by), name, font=font(SANS_B, 11), fill=WHITE)
                bw = int(180 * val / 80.0)
                d.rectangle([hx + 66, by + 1, hx + 66 + bw, by + 13], fill=GOLD)
                d.text((hx + 66 + bw + 6, by), "%.1f" % val, font=font(SANS_B, 11),
                       fill=WHITE)
                by += 26
            f_gap = font(SANS_B, 10)
            d.text((hx + 10, by + 2), "GAP 5.3 \u2014 NARROWEST SINCE 2018",
                   font=f_gap, fill=GOLD_LT)
        # headline below scene (clear gap from strip/scene)
        hy = y + scene_h + 8
        fh, head = fit(d, h["head"], SANS_B, 14, hero_w)
        d.text((hx, hy), head, font=fh, fill=INK)
        # body, up to 2 lines
        fb = font(SANS, 11)
        lines = wrap(d, h["body"], fb, hero_w)[:2]
        by = hy + 20
        for ln in lines:
            d.text((hx, by), ln, font=fb, fill=(40, 40, 40))
            by += 14
        # source + chip
        sy = by + 4
        fs = font(SANS, 10)
        d.text((hx, sy + 1), h["src"], font=fs, fill=GREY)
        chip(d, hx + tw(d, h["src"], fs) + 8, sy, "REPORTED", NAVY)
        hx += hero_w + gap
    y = 212 + scene_h + 8 + 20 + 28 + 4 + 16  # ~ 452

    # ---------- black bar: MORE OF THE DAY ----------
    d.rectangle([M, y, W - M, y + 22], fill=INK)
    d.text((M + 8, y + 4), "MORE OF THE DAY", font=font(SANS_B, 12), fill=WHITE)
    y += 28

    # ---------- 10 cards: 2 cols x 5 rows ----------
    cards = [
        ("BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief presses chipmaker over China sales.", "REPORTED"),
        ("FBI PROBES NCIC POLICE-DATABASE HACK", "Agents investigate breach of law-enforcement system.", "REPORTED"),
        ("TRUMP: IRAN STRIKES MAY RESUME", "President says action could resume in the New Year.", "REPORTED"),
        ("NASDAQ FUTURES JUMP 3%", "Holiday-week rally lifts US tech futures.", "REPORTED"),
        ("SKUBAL SIGNS $450M METS DEAL", "Two-time Cy Young winner, nine years \u2014 a pitcher record.", "REPORTED"),
        ("TOM JACKSON DIES AT 75", "Former NFL linebacker and broadcaster passes away.", "REPORTED"),
        ("STATES SUE SPACEX OVER AI SAFETY", "Attorneys general challenge AI safety claims.", "REPORTED"),
        ("ANTHROPIC IPO AT $107.3B", "Shares priced at $83; debut close $97.17.", "REPORTED"),
        ("POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE", "Warsaw says Kh-101s entered its skies.", "CLAIM"),
        ("INTEL WARNS OF RUSSIAN NUCLEAR SATELLITE", "US intelligence flags orbital weapon risk.", "CLAIM"),
    ]
    card_w = (CW - 12) // 2
    card_h = 40
    for i, (head, body, tag) in enumerate(cards):
        cx = M + (i % 2) * (card_w + 12)
        cy = y + (i // 2) * (card_h + 2)
        d.rectangle([cx, cy, cx + card_w, cy + card_h - 2], outline=LINE, width=1)
        # chip first (right side), headline fits remaining width
        tag_fill = NAVY if tag == "REPORTED" else RED
        f_chip = font(SANS_B, 9)
        chip_w = int(tw(d, tag, f_chip)) + 10
        fh, head_f = fit(d, head, SANS_B, 12, card_w - chip_w - 24)
        d.text((cx + 8, cy + 4), head_f, font=fh, fill=INK)
        d.rounded_rectangle([cx + card_w - chip_w - 6, cy + 4,
                             cx + card_w - 6, cy + 18], radius=3, fill=tag_fill)
        d.text((cx + card_w - chip_w - 1, cy + 6), tag, font=f_chip, fill=WHITE)
        fb2, body_f = fit(d, body, SANS, 10, card_w - 16)
        d.text((cx + 8, cy + 21), body_f, font=fb2, fill=(60, 60, 60))
    y += 5 * (card_h + 2) + 6  # ~ 684

    # ---------- map + ALSO ----------
    d.text((M, y), "AROUND THE WORLD", font=font(SANS_B, 12), fill=INK)
    d.text((M + 520, y), "ALSO ON MONDAY", font=font(SANS_B, 12), fill=INK)
    y += 18
    map_x, map_y, map_w, map_h = M, y, 496, 176
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=LINE, width=1,
                fill=(226, 232, 238))
    # rough continent blobs
    d.polygon([(map_x + 30, map_y + 30), (map_x + 120, map_y + 18),
               (map_x + 150, map_y + 60), (map_x + 110, map_y + 110),
               (map_x + 60, map_y + 120), (map_x + 28, map_y + 80)],
              fill=(170, 190, 170))  # Americas
    d.polygon([(map_x + 250, map_y + 26), (map_x + 460, map_y + 16),
               (map_x + 470, map_y + 70), (map_x + 400, map_y + 96),
               (map_x + 300, map_y + 90), (map_x + 250, map_y + 60)],
              fill=(170, 190, 170))  # Eurasia
    d.polygon([(map_x + 250, map_y + 96), (map_x + 310, map_y + 92),
               (map_x + 320, map_y + 140), (map_x + 280, map_y + 158),
               (map_x + 252, map_y + 130)], fill=(170, 190, 170))  # Africa
    pins = [
        (1, 400, 60, "Seoul"), (2, 120, 108, "Bridgetown"), (3, 96, 44, "Washington"),
        (4, 288, 52, "Paris"), (5, 258, 48, "London"), (6, 270, 26, "Manchester"),
        (7, 336, 50, "Kyiv"), (8, 314, 70, "Antalya"), (9, 326, 94, "Gaza"),
        (10, 350, 80, "Beirut"), (11, 376, 94, "Bahrain"), (12, 280, 124, "Khartoum"),
        (13, 296, 148, "Kinshasa"),
    ]
    f_pin = font(SANS_B, 9)
    for num, px, py, _name in pins:
        d.ellipse([map_x + px - 8, map_y + py - 8, map_x + px + 8, map_y + py + 8],
                  fill=RED, outline=WHITE, width=1)
        t = str(num)
        d.text((map_x + px - tw(d, t, f_pin) / 2, map_y + py - 6), t, font=f_pin,
               fill=WHITE)
    # legend: 3 rows under map (inside map box bottom is crowded; put below map)
    ly = map_y + map_h + 4
    f_leg = font(SANS, 9)
    leg = ["1 Seoul  2 Bridgetown  3 Washington  4 Paris  5 London  6 Manchester",
           "7 Kyiv  8 Antalya  9 Gaza  10 Beirut  11 Bahrain  12 Khartoum  13 Kinshasa"]
    for ln in leg:
        d.text((map_x, ly), ln, font=f_leg, fill=GREY)
        ly += 12

    # ALSO list, 2 cols x 9 rows
    also = [
        "Paris: 100+ back 2% billionaire tax",
        "Manchester: 12,000 cleared",
        "Zelenskyy: 165 Russian missiles in a week",
        "COP31: the day after Antalya pact rejected",
        "Israel unity talks resume",
        "Gaza: two killed in Israeli strike",
        "West Bank settler attacks",
        "Iran war: no deal in sight",
        "Lebanon seizes 264 kg explosives",
        "Bahrain: Iranian strike hits plant, 2 hurt",
        "Benghazi: UN demands port probe [CLAIM]",
        "Sudan: drones downed over Khartoum [CLAIM]",
        "DRC: fighting traps Ebola teams",
        "Bangladesh: Hasina jailed if she returns",
        "Seoul minister quits over AI exam chaos",
        "SK Telecom falls 7.3%",
        "China eases margin rules to 80%",
        "Seoul readies 10T-won stabilisation fund",
    ]
    ax = M + 520
    col2_w = 232
    f_also = font(SANS, 10)
    for i, item in enumerate(also):
        col = i // 9
        row = i % 9
        ix = ax + col * (col2_w + 8)
        iy = y + row * 20
        # red [CLAIM] suffix handling: draw claim in red
        if item.endswith("[CLAIM]"):
            base = item[:-8].rstrip()
            fb_, base_f = fit(d, base, SANS, 10, col2_w - 44)
            d.text((ix, iy), "\u2022 " + base_f, font=fb_, fill=INK)
            d.text((ix + tw(d, "\u2022 " + base_f, fb_), iy), " [CLAIM]",
                   font=font(SANS_B, 10), fill=RED)
        else:
            fa, item_f = fit(d, item, SANS, 10, col2_w)
            d.text((ix, iy), "\u2022 " + item_f, font=fa, fill=INK)
    y = map_y + map_h + 4 + 2 * 12 + 8  # ~ 902

    # ---------- DATE CHECK red box ----------
    d.rectangle([M, y, W - M, y + 84], outline=RED, width=2, fill=RED_LT)
    d.text((M + 8, y + 5), "DATE CHECK \u2014 LEFT OUT (NOT 23 NOVEMBER)",
           font=font(SANS_B, 11), fill=RED)
    f_dc = font(SANS, 10)
    left = ["Democrats reach 258 (22 Nov)", "Sparta II fire (22 Nov)",
            "El Chapo Isidro captured (22 Nov)", "EU\u2013Indonesia pact (21 Nov)",
            "Nigeria boat (21 Nov)", "ICJ Myanmar ruling (19 Nov)"]
    notyet = ["Dymer search continues (14 missing)", "4 House races uncalled",
              "COP32 venue not set", "WHO evacuating trapped Ebola staff"]
    dy = y + 20
    for i, item in enumerate(left):
        col = i // 3
        row = i % 3
        d.text((M + 8 + col * 330, dy + row * 13), "\u2022 " + item, font=f_dc,
               fill=INK)
    d.text((M + 668, dy), "NOT YET:", font=font(SANS_B, 10), fill=RED)
    for i, item in enumerate(notyet):
        d.text((M + 668, dy + 12 + i * 12), "\u2022 " + item, font=f_dc, fill=INK)
    y += 92

    # ---------- footer ----------
    f_f = font(SANS, 9)
    d.line([(M, y), (W - M, y)], fill=LINE, width=1)
    d.text((M, y + 4), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 wires  |  REPORTED = confirmed by wires  \u00b7  CLAIM = one side's claim",
           font=f_f, fill=GREY)
    d.text((M, y + 16), "THE WORLD TODAY \u00b7 Monday 23 November 2026 \u00b7 31 stories \u00b7 6 regions",
           font=font(SANS_B, 9), fill=INK)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
