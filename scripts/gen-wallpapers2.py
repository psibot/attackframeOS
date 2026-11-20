#!/usr/bin/env python3
"""AttackFrame wallpaper pack, volume 2: 20 abstract neon designs (16:9).
Run after gen-wallpapers.py (it appends to assets/wallpapers/names.tsv)."""
import importlib.util
import math
import random
from pathlib import Path

_spec = importlib.util.spec_from_file_location("wp1", Path(__file__).with_name("gen-wallpapers.py"))
wp1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(wp1)
W, H, svg, t, brackets, wordmark = wp1.W, wp1.H, wp1.svg, wp1.t, wp1.brackets, wp1.wordmark
VOID, PANEL, CYAN, MAG, YEL, TEXT, DIM, VIOLET = (wp1.VOID, wp1.PANEL, wp1.CYAN, wp1.MAG, wp1.YEL,
                                                   wp1.TEXT, wp1.DIM, wp1.VIOLET)
ORANGE, TEAL = "#ff7a2b", "#00ffb3"


def lin(id_, stops, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rad(id_, stops, cx="50%", cy="50%", r="50%"):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def mark(x=60, y=H - 50, color=CYAN, anchor="start"):
    return t(x, y, "ATTACK//FRAME", 15, color, .8, anchor, 'letter-spacing="6" font-weight="700"')


def stars(r, n, ymax=H, op=(.2, .9)):
    return "".join(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, ymax):.0f}" r="{r.uniform(.5, 1.8):.1f}" '
                   f'fill="{TEXT}" opacity="{r.uniform(*op):.2f}"/>' for _ in range(n))


# 01 aurora — flowing neon ribbons
def aurora():
    r = random.Random(101)
    body = [stars(r, 160)]
    for k in range(9):
        c = [CYAN, TEAL, MAG, VIOLET][k % 4]
        amp, ph, base = r.uniform(60, 160), r.uniform(0, 6), H * .35 + k * 28
        pts = [(x, base + amp * math.sin(x / 260 + ph) + 30 * math.sin(x / 90 + ph * 2)) for x in range(-20, W + 40, 20)]
        d = "M" + " L".join(f"{x},{y:.1f}" for x, y in pts)
        body.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{r.uniform(10, 34):.0f}" opacity=".16" filter="url(#bigglow)"/>')
        body.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2" opacity=".75" filter="url(#softglow)"/>')
    body.append(mark())
    svg("aurora", "".join(body), bg="#03040c")


# 02 tunnel — receding neon frames
def tunnel():
    body = []
    cx, cy = W / 2, H / 2
    for k in range(34, 0, -1):
        s = (k / 34) ** 2.2
        w, h = W * 1.1 * s, H * 1.1 * s
        c = MAG if k % 3 == 0 else CYAN
        body.append(f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" '
                    f'stroke="{c}" stroke-width="{.6 + 3 * s:.2f}" opacity="{.25 + .7 * s:.2f}"' +
                    (' filter="url(#softglow)"' if k % 3 == 0 else "") + "/>")
    for fx, fy in [(0, 0), (W, 0), (0, H), (W, H)]:
        body.append(f'<line x1="{fx}" y1="{fy}" x2="{cx}" y2="{cy}" stroke="{CYAN}" stroke-width="1.5" opacity=".35"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="{TEXT}" filter="url(#bigglow)"/>')
    body.append(mark(W / 2, H - 50, CYAN, "middle"))
    svg("tunnel", "".join(body), bg="#030308")


# 03 neon ocean — sun over scanline waves
def neon_ocean():
    r = random.Random(103)
    hz = H * .58
    defs = (lin("sky2", [(0, "#06031a", 1), (1, "#4a0b4f", 1)]) + lin("sun2", [(0, YEL, 1), (1, ORANGE, 1)]) +
            f'<clipPath id="sc"><circle cx="{W / 2}" cy="{hz}" r="260"/></clipPath>')
    body = [f'<rect width="{W}" height="{hz}" fill="url(#sky2)"/>', stars(r, 120, hz * .8)]
    bars = "".join(f'<rect x="{W / 2 - 270}" y="{hz - 120 + k * 22}" width="540" height="{3 + k * 1.6:.1f}" fill="#2a0636"/>' for k in range(7))
    body.append(f'<g clip-path="url(#sc)" filter="url(#bigglow)"><rect x="{W / 2 - 270}" y="{hz - 270}" width="540" height="270" fill="url(#sun2)"/>{bars}</g>')
    body.append(f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="#05030c"/>')
    for k in range(48):
        y = hz + 4 + (k ** 1.55) * 1.6
        if y > H:
            break
        wdt = 540 * (1 - k / 60) * r.uniform(.6, 1.1)
        body.append(f'<line x1="{W / 2 - wdt / 2:.0f}" y1="{y:.0f}" x2="{W / 2 + wdt / 2:.0f}" y2="{y:.0f}" stroke="{ORANGE}" '
                    f'stroke-width="{1 + k / 20:.1f}" opacity="{max(.1, .8 - k / 50):.2f}"/>')
        for _ in range(3):
            x = r.uniform(0, W)
            body.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + r.uniform(30, 160):.0f}" y2="{y:.0f}" stroke="{CYAN}" stroke-width="1" opacity=".35"/>')
    body.append(wordmark(W / 2, 150, 70))
    svg("neon-ocean", "".join(body), extra_defs=defs)


# 04 iso grid — isometric tiles, some lit
def iso_grid():
    r = random.Random(104)
    body, s = [], 60
    for i in range(-20, 40):
        for j in range(-5, 40):
            x, y = (i - j) * s + W / 2, (i + j) * s / 2 - 200
            if not (-80 < x < W + 80 and -80 < y < H + 80):
                continue
            p = f"{x},{y} {x + s},{y + s / 2} {x},{y + s} {x - s},{y + s / 2}"
            if r.random() < .07:
                c = r.choice([CYAN, MAG, YEL])
                hgt = r.uniform(20, 120)
                body.append(f'<polygon points="{x - s},{y + s / 2} {x},{y + s} {x},{y + s - hgt} {x - s},{y + s / 2 - hgt}" fill="{c}" opacity=".18"/>'
                            f'<polygon points="{x},{y + s} {x + s},{y + s / 2} {x + s},{y + s / 2 - hgt} {x},{y + s - hgt}" fill="{c}" opacity=".10"/>'
                            f'<polygon points="{x},{y - hgt} {x + s},{y + s / 2 - hgt} {x},{y + s - hgt} {x - s},{y + s / 2 - hgt}" '
                            f'fill="{c}" fill-opacity=".35" stroke="{c}" stroke-width="2" filter="url(#softglow)"/>')
            else:
                body.append(f'<polygon points="{p}" fill="none" stroke="{CYAN}" stroke-width="1" opacity=".18"/>')
    body.append(mark())
    svg("iso-grid", "".join(body), bg="#04060c")


# 05 warp — radial star streaks
def warp():
    r = random.Random(105)
    cx, cy = W / 2, H / 2
    body = []
    for _ in range(700):
        a = r.uniform(0, 2 * math.pi)
        d0 = r.uniform(40, 900); L = d0 * r.uniform(.08, .35)
        c = r.choice([CYAN, CYAN, TEXT, MAG, VIOLET])
        body.append(f'<line x1="{cx + d0 * math.cos(a):.0f}" y1="{cy + d0 * math.sin(a):.0f}" '
                    f'x2="{cx + (d0 + L) * math.cos(a):.0f}" y2="{cy + (d0 + L) * math.sin(a):.0f}" '
                    f'stroke="{c}" stroke-width="{.6 + d0 / 500:.1f}" stroke-linecap="round" opacity="{min(.95, .15 + d0 / 900):.2f}"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="60" fill="{CYAN}" opacity=".25" filter="url(#bigglow)"/>')
    body.append(mark(W / 2, H - 50, CYAN, "middle"))
    svg("warp", "".join(body), bg="#020309")


# 06 bokeh — soft neon light orbs
def bokeh():
    r = random.Random(106)
    defs = '<filter id="blur12"><feGaussianBlur stdDeviation="12"/></filter><filter id="blur4"><feGaussianBlur stdDeviation="3"/></filter>'
    body = []
    for _ in range(90):
        rr = r.uniform(20, 120); c = r.choice([CYAN, MAG, VIOLET, YEL, TEAL])
        body.append(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, H):.0f}" r="{rr:.0f}" fill="{c}" '
                    f'opacity="{r.uniform(.05, .22):.2f}" filter="url(#{"blur12" if rr > 60 else "blur4"})"/>')
    body.append(wordmark(W / 2, H / 2 + 20, 84))
    svg("bokeh", "".join(body), bg="#06040e", extra_defs=defs, scan=False)


# 07 equalizer — audio bars with reflection
def equalizer():
    r = random.Random(107)
    defs = lin("bar", [(0, MAG, 1), (.5, VIOLET, 1), (1, CYAN, 1)])
    body, n, base = [], 96, H * .66
    for i in range(n):
        x = 40 + i * (W - 80) / n
        h = (math.sin(i / 7) * .5 + .6) * r.uniform(.4, 1) * 420
        body.append(f'<rect x="{x:.1f}" y="{base - h:.0f}" width="{(W - 80) / n - 5:.1f}" height="{h:.0f}" fill="url(#bar)" rx="2" filter="url(#softglow)"/>')
        body.append(f'<rect x="{x:.1f}" y="{base + 6}" width="{(W - 80) / n - 5:.1f}" height="{h * .35:.0f}" fill="url(#bar)" opacity=".15" rx="2"/>')
    body.append(f'<line x1="40" y1="{base + 3}" x2="{W - 40}" y2="{base + 3}" stroke="{CYAN}" stroke-width="2" opacity=".8"/>')
    body.append(t(60, 110, "ATTACK//FRAME", 40, TEXT, .95, "start", 'font-weight="800" letter-spacing="8" filter="url(#softglow)"'))
    body.append(t(62, 140, "FREQUENCY // 7F3A HZ", 14, CYAN, .85, "start", 'letter-spacing="5"'))
    svg("equalizer", "".join(body), bg="#05040b", extra_defs=defs)


# 08 contours — topographic lines
def contours():
    r = random.Random(108)
    peaks = [(r.uniform(200, W - 200), r.uniform(150, H - 150), r.uniform(.6, 1.2)) for _ in range(4)]
    body = []
    for pi_, (px, py, sc) in enumerate(peaks):
        ph = r.uniform(0, 6)
        for k in range(1, 22):
            rad_ = k * 26 * sc
            pts = []
            for a in range(0, 361, 6):
                ang = math.radians(a)
                wob = 1 + .18 * math.sin(3 * ang + ph + k * .3) + .08 * math.sin(7 * ang - ph)
                pts.append(f"{px + rad_ * wob * math.cos(ang):.1f},{py + rad_ * wob * .7 * math.sin(ang):.1f}")
            c = MAG if k % 5 == 0 else CYAN
            body.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="{1.8 if k % 5 == 0 else 1}" '
                        f'opacity="{.7 if k % 5 == 0 else .3}"/>')
        body.append(t(px + 10, py + 5, f"▲ {r.randint(1200, 4800)}", 14, YEL, .9))
    body.append(brackets(28, 70, DIM))
    body.append(mark())
    svg("contours", "".join(body), bg="#04070b")


# 09 low poly — triangle mesh
def low_poly():
    r = random.Random(109)
    cols, rows = 22, 13
    pts = [[(c * W / (cols - 1) + (r.uniform(-30, 30) if 0 < c < cols - 1 else 0),
             rr * H / (rows - 1) + (r.uniform(-30, 30) if 0 < rr < rows - 1 else 0)) for c in range(cols)] for rr in range(rows)]
    body = []
    for j in range(rows - 1):
        for i in range(cols - 1):
            a, b, c, d = pts[j][i], pts[j][i + 1], pts[j + 1][i], pts[j + 1][i + 1]
            for tri in ((a, b, c), (b, d, c)):
                mx = sum(p[0] for p in tri) / 3 / W; my = sum(p[1] for p in tri) / 3 / H
                light = .15 + .55 * (1 - math.hypot(mx - .3, my - .3)) * r.uniform(.7, 1)
                col = MAG if mx > .6 and r.random() < .5 else (VIOLET if r.random() < .5 else "#132a4a")
                body.append(f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in tri)}" fill="{col}" '
                            f'fill-opacity="{max(.05, light * .6):.2f}" stroke="{CYAN}" stroke-width=".8" stroke-opacity=".35"/>')
    body.append(wordmark(W / 2, H / 2 + 20, 84))
    svg("low-poly", "".join(body), bg="#05060e", scan=False)


# 10 ringworld — planet with rings
def ringworld():
    r = random.Random(110)
    defs = (rad("planet", [(0, "#3b1a6b", 1), (.7, "#140a2a", 1), (1, "#05030d", 1)], "35%", "35%", "70%") +
            f'<clipPath id="front"><rect x="0" y="{H / 2 + 10}" width="{W}" height="{H}"/></clipPath>')
    cx, cy, R = W * .62, H * .52, 240
    rings = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{R + 60 + k * 18}" ry="{(R + 60 + k * 18) * .22:.0f}" fill="none" '
                    f'stroke="{[CYAN, MAG, VIOLET][k % 3]}" stroke-width="{r.uniform(2, 6):.1f}" opacity="{r.uniform(.3, .8):.2f}"/>'
                    for k in range(9))
    body = [stars(r, 260),
            f'<g transform="rotate(-14 {cx} {cy})">{rings}</g>',
            f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#planet)" stroke="{CYAN}" stroke-width="2" filter="url(#glow)"/>',
            f'<g transform="rotate(-14 {cx} {cy})" clip-path="url(#front)">{rings}</g>',
            t(120, H / 2 - 20, "ATTACK//FRAME", 54, TEXT, .95, "start", 'font-weight="800" letter-spacing="10" filter="url(#softglow)"'),
            t(124, H / 2 + 20, "ORBITAL STATION 7F3A", 16, CYAN, .85, "start", 'letter-spacing="7"')]
    svg("ringworld", "".join(body), bg="#03030a", extra_defs=defs)


# 11 dawn skyline — cyan twilight city
def dawn_skyline():
    r = random.Random(111)
    base = H * .78
    defs = lin("dawn", [(0, "#020814", 1), (.75, "#0a3a4a", 1), (1, TEAL, .6)])
    body = [f'<rect width="{W}" height="{base}" fill="url(#dawn)"/>', stars(r, 90, H * .4)]
    for layer, (mx, shade, win) in enumerate([(300, "#071622", .02), (480, "#040b12", .06)]):
        x = -10
        while x < W:
            bw = r.randint(40, 130); bh = r.randint(int(mx * .3), mx)
            body.append(f'<rect x="{x}" y="{base - bh}" width="{bw}" height="{bh}" fill="{shade}"/>')
            if layer and r.random() < .25:
                body.append(f'<rect x="{x}" y="{base - bh}" width="{bw}" height="3" fill="{CYAN}" opacity=".9" filter="url(#softglow)"/>')
            for wy in range(int(base - bh + 10), int(base - 6), 16):
                for wx in range(x + 6, x + bw - 6, 11):
                    if r.random() < win:
                        body.append(f'<rect x="{wx}" y="{wy}" width="4" height="6" fill="{r.choice([CYAN, TEAL, TEXT])}" opacity=".7"/>')
            x += bw + r.randint(0, 8)
    body.append(f'<rect y="{base}" width="{W}" height="{H - base}" fill="#020509"/>')
    body.append(f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" stroke="{TEAL}" stroke-width="2" filter="url(#softglow)"/>')
    body.append(t(W / 2, base + 120, "ATTACK//FRAME", 40, TEXT, .9, "middle", 'font-weight="800" letter-spacing="14" filter="url(#softglow)"'))
    svg("dawn-skyline", "".join(body), extra_defs=defs)


# 12 colonnade — vapor pillars over a grid floor
def colonnade():
    r = random.Random(112)
    hz = H * .62
    defs = lin("vap", [(0, "#1a0630", 1), (1, "#ff2bd6", .55)]) + lin("pil", [(0, TEXT, .9), (1, VIOLET, .5)], 1, 0)
    body = [f'<rect width="{W}" height="{hz}" fill="url(#vap)"/>', stars(r, 80, hz * .7),
            f'<circle cx="{W / 2}" cy="{hz - 180}" r="150" fill="{CYAN}" opacity=".35" filter="url(#bigglow)"/>',
            f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="#07030f"/>']
    for k in range(-30, 31):
        body.append(f'<line x1="{W / 2}" y1="{hz}" x2="{W / 2 + k * 90}" y2="{H}" stroke="{MAG}" stroke-width="1.2" opacity=".5"/>')
    for k in range(1, 30):
        y = hz + k * k * 0.9
        if y < H:
            body.append(f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" stroke="{MAG}" stroke-width="1.2" opacity="{min(.8, .2 + k / 25):.2f}"/>')
    for side in (-1, 1):
        for k in range(4):
            sc = 1 - k * .2
            x = W / 2 + side * (360 + k * 140) * (1 if k == 0 else .9)
            w, h = 70 * sc, 460 * sc
            y = hz + 40 * sc - h
            body.append(f'<rect x="{x - w / 2:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="url(#pil)" opacity="{.9 - k * .15:.2f}"/>')
            body.append(f'<rect x="{x - w * .7:.0f}" y="{y - 18 * sc:.0f}" width="{w * 1.4:.0f}" height="{18 * sc:.0f}" fill="{TEXT}" opacity=".85"/>')
            body.append(f'<rect x="{x - w * .7:.0f}" y="{y + h:.0f}" width="{w * 1.4:.0f}" height="{14 * sc:.0f}" fill="{TEXT}" opacity=".7"/>')
            for f in range(1, 4):
                body.append(f'<line x1="{x - w / 2 + f * w / 4:.0f}" y1="{y:.0f}" x2="{x - w / 2 + f * w / 4:.0f}" y2="{y + h:.0f}" stroke="{VIOLET}" stroke-width="1.5" opacity=".5"/>')
    body.append(wordmark(W / 2, 170, 70))
    svg("colonnade", "".join(body), extra_defs=defs)


# 13 lattice — diagonal lattice with glowing nodes
def lattice():
    r = random.Random(113)
    body, s = [], 80
    for k in range(-H // s - 2, W // s + H // s + 2):
        body.append(f'<line x1="{k * s}" y1="0" x2="{k * s + H}" y2="{H}" stroke="{CYAN}" stroke-width="1" opacity=".18"/>')
        body.append(f'<line x1="{k * s}" y1="0" x2="{k * s - H}" y2="{H}" stroke="{MAG}" stroke-width="1" opacity=".14"/>')
    for i in range(-2, W // s + 3):
        for j in range(0, 2 * H // s + 2):
            x, y = i * s + (s / 2 if j % 2 else 0), j * s / 2
            if r.random() < .08:
                c = r.choice([CYAN, MAG, YEL])
                body.append(f'<circle cx="{x}" cy="{y}" r="{r.uniform(3, 7):.1f}" fill="{c}" filter="url(#glow)"/>')
    body.append(f'<rect x="{W / 2 - 430}" y="{H / 2 - 80}" width="860" height="150" fill="{VOID}" opacity=".85"/>')
    body.append(wordmark(W / 2, H / 2 + 22, 76))
    svg("lattice", "".join(body), bg="#04050b")


# 14 sigil — concentric geometric emblem
def sigil():
    cx, cy = W / 2, H / 2
    body = []
    for k, (R, c, dash) in enumerate([(420, DIM, "2 10"), (360, CYAN, ""), (330, CYAN, "40 12"), (280, MAG, ""),
                                      (240, CYAN, "4 6"), (180, MAG, "60 20"), (120, CYAN, "")]):
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{c}" stroke-width="{3 if not dash else 2}" '
                    f'stroke-dasharray="{dash}" opacity="{.5 + .07 * k:.2f}"' + (' filter="url(#softglow)"' if not dash else "") + "/>")
    for n, R, c in [(3, 330, MAG), (6, 280, CYAN), (8, 360, DIM)]:
        pts = " ".join(f"{cx + R * math.cos(2 * math.pi * i / n - math.pi / 2):.1f},{cy + R * math.sin(2 * math.pi * i / n - math.pi / 2):.1f}" for i in range(n))
        body.append(f'<polygon points="{pts}" fill="none" stroke="{c}" stroke-width="1.6" opacity=".6"/>')
    for a in range(0, 360, 15):
        x, y = cx + 390 * math.cos(math.radians(a)), cy + 390 * math.sin(math.radians(a))
        body.append(f'<rect x="{x - 4:.0f}" y="{y - 4:.0f}" width="8" height="8" fill="{CYAN if a % 45 else MAG}" transform="rotate({a} {x:.0f} {y:.0f})"/>')
    body.append(f'<path d="M{cx - 40},{cy + 60} L{cx - 4},{cy - 60} M{cx + 4},{cy + 60} L{cx + 40},{cy - 60}" stroke="{MAG}" '
                f'stroke-width="14" stroke-linecap="round" filter="url(#glow)"/>')
    body.append(mark(60, H - 50))
    svg("sigil", "".join(body), bg="#04040b")


# 15 light trails — right-angle neon trails on a dark grid
def light_trails():
    r = random.Random(115)
    g = 60
    body = [f'<path d="{"".join(f"M{x},0 V{H} " for x in range(0, W + 1, g))}{"".join(f"M0,{y} H{W} " for y in range(0, H + 1, g))}" '
            f'stroke="{DIM}" stroke-width="1" opacity=".35"/>']
    for c in [CYAN, MAG, YEL, TEAL, CYAN, MAG]:
        x, y = r.randint(0, W // g) * g, r.randint(0, H // g) * g
        dx, dy = r.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        pts = [(x, y)]
        for _ in range(r.randint(6, 12)):
            n = r.randint(2, 10) * g
            x, y = x + dx * n, y + dy * n
            pts.append((x, y))
            dx, dy = (dy, dx) if r.random() < .5 else (-dy, -dx)
        d = "M" + " L".join(f"{px},{py}" for px, py in pts)
        body.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="10" opacity=".25" filter="url(#bigglow)"/>')
        body.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="3" stroke-linejoin="round"/>')
        ex, ey = pts[-1]
        body.append(f'<circle cx="{ex}" cy="{ey}" r="7" fill="{TEXT}" filter="url(#glow)"/>')
    body.append(mark())
    svg("light-trails", "".join(body), bg="#03050a")


# 16 dunes — wireframe sand dunes under a violet sky
def dunes():
    r = random.Random(116)
    defs = lin("dsky", [(0, "#04030c", 1), (1, "#3a0d4a", 1)])
    body = [f'<rect width="{W}" height="{H}" fill="url(#dsky)"/>', stars(r, 200, H * .5),
            f'<circle cx="{W * .75}" cy="{H * .28}" r="70" fill="{TEXT}" opacity=".9" filter="url(#bigglow)"/>']
    for k in range(26):
        y0 = H * .45 + k ** 1.45 * 6
        amp = 30 + k * 4
        ph = k * .7
        pts = [(x, y0 - amp * (math.sin(x / (300 + k * 10) + ph) * .6 + math.sin(x / 130 - ph) * .25)) for x in range(-20, W + 40, 16)]
        d = "M" + " L".join(f"{x},{y:.1f}" for x, y in pts)
        body.append(f'<path d="{d} L{W + 40},{H} L-20,{H} Z" fill="#07040f" opacity=".6"/>')
        body.append(f'<path d="{d}" fill="none" stroke="{ORANGE if k % 6 == 0 else MAG}" stroke-width="{.8 + k / 14:.1f}" opacity="{.3 + k / 40:.2f}"/>')
    body.append(t(W / 2, 160, "ATTACK//FRAME", 56, TEXT, .95, "middle", 'font-weight="800" letter-spacing="14" filter="url(#softglow)"'))
    svg("dunes", "".join(body), extra_defs=defs)


# 17 eclipse — corona glow around a dark disc
def eclipse():
    r = random.Random(117)
    cx, cy = W / 2, H / 2 - 20
    defs = rad("corona", [(0, TEXT, 1), (.45, CYAN, .7), (.7, MAG, .25), (1, MAG, 0)])
    body = [stars(r, 220)]
    for _ in range(140):
        a = r.uniform(0, 2 * math.pi); L = r.uniform(30, 160)
        body.append(f'<line x1="{cx + 210 * math.cos(a):.0f}" y1="{cy + 210 * math.sin(a):.0f}" x2="{cx + (210 + L) * math.cos(a):.0f}" '
                    f'y2="{cy + (210 + L) * math.sin(a):.0f}" stroke="{r.choice([CYAN, MAG, TEXT])}" stroke-width="1.2" opacity=".35"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="330" fill="url(#corona)" opacity=".7"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="212" fill="none" stroke="{TEXT}" stroke-width="5" filter="url(#glow)"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="208" fill="#020208"/>')
    body.append(t(cx, cy + 380, "ATTACK//FRAME", 30, TEXT, .9, "middle", 'font-weight="700" letter-spacing="18"'))
    svg("eclipse", "".join(body), bg="#020207", extra_defs=defs)


# 18 server hall — racks in perspective with status LEDs
def server_hall():
    r = random.Random(118)
    body = []
    vx, vy = W / 2, H * .45
    for side in (-1, 1):
        for k in range(10, -1, -1):
            s = .2 + k * .09
            w, h = 220 * s, 640 * s
            x = vx + side * (130 + k * k * 9) * (1 + k * .05) - (w if side < 0 else 0)
            y = vy - h * .45
            body.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{PANEL}" stroke="{CYAN}" stroke-width="{.6 + s:.1f}" opacity="{.4 + s * .4:.2f}"/>')
            units = int(14 * s) + 6
            for u in range(units):
                uy = y + 10 * s + u * (h - 20 * s) / units
                body.append(f'<rect x="{x + 6 * s:.0f}" y="{uy:.0f}" width="{w - 12 * s:.0f}" height="{(h - 20 * s) / units - 3:.1f}" fill="#0e1424" opacity=".9"/>')
                for led in range(3):
                    if r.random() < .7:
                        c = r.choice([CYAN, CYAN, TEAL, MAG, YEL])
                        body.append(f'<circle cx="{x + (14 + led * 9) * s:.1f}" cy="{uy + 5 * s:.1f}" r="{1.6 * s + .6:.1f}" fill="{c}" filter="url(#softglow)"/>')
    body.append(f'<path d="M0,{H} L{vx - 120},{vy + 160} L{vx + 120},{vy + 160} L{W},{H} Z" fill="#06080f"/>')
    for k in range(1, 18):
        y = vy + 160 + k * k * 1.6
        if y < H:
            body.append(f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" stroke="{CYAN}" stroke-width="1" opacity="{.1 + k / 40:.2f}"/>')
    body.append(t(vx, 90, "ATTACK//FRAME", 40, TEXT, .95, "middle", 'font-weight="800" letter-spacing="12" filter="url(#softglow)"'))
    body.append(t(vx, 120, "HALL 7 // RACK ROW F3A", 14, CYAN, .85, "middle", 'letter-spacing="6"'))
    svg("server-hall", "".join(body), bg="#03050a")


# 19 plasma — soft gradient blobs with grain
def plasma():
    r = random.Random(119)
    defs = ('<filter id="blob" filterUnits="userSpaceOnUse" x="-600" y="-600" width="3120" height="2280"><feGaussianBlur stdDeviation="90"/></filter>'
            '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/>'
            '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .07 0"/></filter>')
    body = []
    for c in [MAG, CYAN, VIOLET, TEAL, MAG, ORANGE]:
        body.append(f'<ellipse cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, H):.0f}" rx="{r.uniform(250, 520):.0f}" ry="{r.uniform(200, 420):.0f}" '
                    f'fill="{c}" opacity="{r.uniform(.35, .6):.2f}" filter="url(#blob)"/>')
    body.append(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')
    body.append(t(W / 2, H / 2 + 20, "ATTACK//FRAME", 72, TEXT, .92, "middle", 'font-weight="200" letter-spacing="26"'))
    svg("plasma", "".join(body), bg="#0a0614", extra_defs=defs, scan=False)


# 20 neon sign — tube lettering on a brick wall
def neon_sign():
    r = random.Random(120)
    defs = ('<pattern id="brick" width="120" height="60" patternUnits="userSpaceOnUse">'
            '<rect width="120" height="60" fill="#0d0a12"/>'
            '<path d="M0,0 H120 M0,30 H120 M60,0 V30 M0,30 V60 M120,30 V60" stroke="#1a1422" stroke-width="4"/></pattern>'
            + rad("spill", [(0, MAG, .35), (1, MAG, 0)], "50%", "45%", "55%"))
    body = [f'<rect width="{W}" height="{H}" fill="url(#brick)"/>', f'<rect width="{W}" height="{H}" fill="url(#spill)"/>']
    for _ in range(40):
        body.append(f'<rect x="{r.uniform(0, W):.0f}" y="{r.uniform(0, H):.0f}" width="{r.uniform(20, 110):.0f}" height="{r.uniform(10, 26):.0f}" fill="#000" opacity="{r.uniform(.1, .3):.2f}"/>')
    tube = 'font-weight="300" letter-spacing="14" fill="none" stroke-linejoin="round"'
    for sw, op in [(22, .18), (10, .4)]:
        body.append(f'<text x="{W / 2}" y="{H / 2 + 30}" font-size="150" text-anchor="middle" {tube} stroke="{MAG}" stroke-width="{sw}" opacity="{op}" filter="url(#bigglow)">ATTACK//FRAME</text>')
    body.append(f'<text x="{W / 2}" y="{H / 2 + 30}" font-size="150" text-anchor="middle" {tube} stroke="#ffd6f6" stroke-width="3.5">ATTACK//FRAME</text>')
    body.append(f'<text x="{W / 2}" y="{H / 2 + 120}" font-size="44" text-anchor="middle" font-weight="300" letter-spacing="20" fill="none" '
                f'stroke="{CYAN}" stroke-width="2.5" filter="url(#glow)">OPEN 24/7</text>')
    for x in (W / 2 - 720, W / 2 + 720):
        body.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H / 2 - 120}" stroke="#2a2433" stroke-width="3"/>')
    svg("neon-sign", "".join(body), extra_defs=defs, scan=False)


WALLPAPERS = [
    ("aurora", "Aurora", aurora), ("tunnel", "Tunnel", tunnel), ("neon-ocean", "Neon Ocean", neon_ocean),
    ("iso-grid", "Iso Grid", iso_grid), ("warp", "Warp", warp), ("bokeh", "Bokeh", bokeh),
    ("equalizer", "Equalizer", equalizer), ("contours", "Contours", contours), ("low-poly", "Low Poly", low_poly),
    ("ringworld", "Ringworld", ringworld), ("dawn-skyline", "Dawn Skyline", dawn_skyline),
    ("colonnade", "Colonnade", colonnade), ("lattice", "Lattice", lattice), ("sigil", "Sigil", sigil),
    ("light-trails", "Light Trails", light_trails), ("dunes", "Dunes", dunes), ("eclipse", "Eclipse", eclipse),
    ("server-hall", "Server Hall", server_hall), ("plasma", "Plasma", plasma), ("neon-sign", "Neon Sign", neon_sign),
]

if __name__ == "__main__":
    for _, _, fn in WALLPAPERS:
        fn()
    names = wp1.OUT / "names.tsv"
    existing = names.read_text() if names.exists() else ""
    extra = "".join(f"af-{s}\t{n}\n" for s, n, _ in WALLPAPERS if f"af-{s}\t" not in existing)
    names.write_text(existing + extra)
    print(f"wrote {len(WALLPAPERS)} wallpapers to {wp1.OUT}")
