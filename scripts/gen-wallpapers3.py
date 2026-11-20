#!/usr/bin/env python3
"""AttackFrame wallpaper pack, volume 3: 20 original designs (16:9).
Moods: glowing grid worlds, 90s cyber-collage, neon megacity. All artwork is original.
Run after gen-wallpapers.py / gen-wallpapers2.py (appends to assets/wallpapers/names.tsv)."""
import importlib.util
import math
import random
from pathlib import Path


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


wp1 = _load("wp1", "gen-wallpapers.py")
wp2 = _load("wp2", "gen-wallpapers2.py")
W, H, svg, t, brackets, wordmark = wp1.W, wp1.H, wp1.svg, wp1.t, wp1.brackets, wp1.wordmark
lin, rad, mark, stars = wp2.lin, wp2.rad, wp2.mark, wp2.stars
VOID, CYAN, MAG, YEL, TEXT, DIM, VIOLET = wp1.VOID, wp1.CYAN, wp1.MAG, wp1.YEL, wp1.TEXT, wp1.DIM, wp1.VIOLET
ORANGE, TEAL = wp2.ORANGE, wp2.TEAL
RED, CYBY = "#ff2a3d", "#fcee0a"   # signal red, warning yellow


def floor_grid(hz, color, n_long=40, n_lat=22, op=.55, spread=4.0, sw=1.4):
    """Perspective floor: lines converge to (W/2, hz)."""
    cx, out = W / 2, []
    for i in range(-n_long, n_long + 1):
        x_near = cx + i * (W * spread / n_long / 2)
        out.append(f'<line x1="{cx + i * 6:.1f}" y1="{hz}" x2="{x_near:.1f}" y2="{H}" stroke="{color}" stroke-width="{sw}" opacity="{op}"/>')
    for k in range(1, n_lat + 1):
        y = hz + (H - hz) * (k / n_lat) ** 2.2
        out.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}" stroke="{color}" stroke-width="{sw}" opacity="{op * (.35 + .65 * k / n_lat):.2f}"/>')
    return "".join(out)


def proj(u, d, hz, k=None):
    """Floor point (u sideways, d depth >= 1) -> screen. d=1 is the bottom edge."""
    k = k or (H - hz)
    return W / 2 + u * k * 1.6 / d, hz + k / d


# ------------------------------------------------------------------ grid worlds
def grid_arena():
    hz = 470
    defs = lin("asky", [(0, "#02040a", 1), (1, "#06243a", 1)]) + lin("afl", [(0, "#03121c", 1), (1, "#000", 1)])
    body = [f'<rect width="{W}" height="{hz}" fill="url(#asky)"/>', f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="url(#afl)"/>',
            floor_grid(hz, CYAN, op=.4),
            f'<rect y="{hz - 3}" width="{W}" height="6" fill="{CYAN}" opacity=".9" filter="url(#bigglow)"/>']
    for path, col in [([(-2.6, 1.2), (-2.6, 3), (-.6, 3), (-.6, 9), (.4, 9), (.4, 30)], CYAN),
                      ([(2.8, 1.1), (2.8, 2.2), (1.2, 2.2), (1.2, 6), (2.4, 6), (2.4, 14), (.9, 14), (.9, 40)], ORANGE)]:
        pts, top = [], []
        for (u0, d0), (u1, d1) in zip(path, path[1:]):
            for s in range(13):
                u, d = u0 + (u1 - u0) * s / 12, d0 + (d1 - d0) * s / 12
                x, y = proj(u, d, hz)
                pts.append((x, y)); top.append((x, y - 70 / d))
        wall = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts + top[::-1])
        body.append(f'<polygon points="{wall}" fill="{col}" opacity=".22"/>')
        body.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in top)}" fill="none" stroke="{col}" stroke-width="3" filter="url(#glow)"/>')
        body.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="2" opacity=".8"/>')
        hx, hy = top[0]
        body.append(f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="10" fill="#fff" filter="url(#bigglow)"/>')
    body.append(t(W / 2, 200, "ATTACK//FRAME", 64, TEXT, .95, "middle", 'font-weight="300" letter-spacing="34" filter="url(#glow)"'))
    body.append(t(W / 2, 245, "E N T E R   T H E   G R I D", 16, CYAN, .8, "middle", 'letter-spacing="6"'))
    svg("grid-arena", "".join(body), extra_defs=defs)


def light_ribbons():
    r = random.Random(302)
    body = [f'<rect width="{W}" height="{H}" fill="#02060c"/>']
    for x in range(0, W + 1, 48):
        body.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{CYAN}" stroke-width="1" opacity=".09"/>')
    for y in range(0, H + 1, 48):
        body.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{CYAN}" stroke-width="1" opacity=".09"/>')
    for col in [CYAN, ORANGE, CYAN, MAG, ORANGE, TEAL]:
        x, y = r.randrange(4, W // 48 - 4) * 48, r.randrange(3, H // 48 - 3) * 48
        dx, dy = r.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        pts = [(x, y)]
        for _ in range(r.randint(7, 12)):
            n = r.randint(3, 14)
            x = min(max(x + dx * 48 * n, 48), W - 48); y = min(max(y + dy * 48 * n, 48), H - 48)
            pts.append((x, y))
            dx, dy = (dy, dx) if r.random() < .5 else (-dy, -dx)
        p = " ".join(f"{a},{b}" for a, b in pts)
        body.append(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="16" opacity=".18" filter="url(#bigglow)"/>')
        body.append(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="miter" filter="url(#softglow)"/>')
        body.append(f'<circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="9" fill="#fff" filter="url(#glow)"/>')
    body.append(mark())
    svg("light-ribbons", "".join(body), scan=False)


def monolith():
    r = random.Random(303)
    hz = 640
    defs = rad("mglow", [(0, CYAN, .5), (1, CYAN, 0)], "50%", "60%", "45%")
    body = [f'<rect width="{W}" height="{H}" fill="#010308"/>', f'<rect width="{W}" height="{H}" fill="url(#mglow)"/>',
            stars(r, 120, hz), floor_grid(hz, CYAN, op=.35, spread=6)]
    cx = W / 2
    body.append(f'<rect x="{cx - 4}" y="0" width="8" height="{hz - 420}" fill="{CYAN}" opacity=".5" filter="url(#bigglow)"/>')
    body.append(f'<polygon points="{cx - 90},{hz} {cx - 70},{hz - 430} {cx + 70},{hz - 430} {cx + 90},{hz}" fill="#030a12" stroke="{CYAN}" stroke-width="3" filter="url(#glow)"/>')
    for k in range(1, 18):
        y = hz - k * 24
        body.append(f'<line x1="{cx - 88 + k * 1.1:.1f}" y1="{y}" x2="{cx + 88 - k * 1.1:.1f}" y2="{y}" stroke="{CYAN}" stroke-width="1" opacity="{.15 + .03 * k:.2f}"/>')
    body.append(f'<line x1="{cx}" y1="{hz - 430}" x2="{cx}" y2="{hz}" stroke="{TEXT}" stroke-width="1.5" opacity=".6"/>')
    body.append(f'<ellipse cx="{cx}" cy="{hz + 6}" rx="260" ry="26" fill="none" stroke="{CYAN}" stroke-width="2" opacity=".7" filter="url(#glow)"/>')
    for _ in range(90):
        x, y = cx + r.gauss(0, 160), r.uniform(80, hz)
        body.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="3" height="3" fill="{CYAN}" opacity="{r.uniform(.2, .9):.2f}"/>')
    body.append(mark(W / 2, H - 40, CYAN, "middle"))
    svg("monolith", "".join(body), extra_defs=defs)


def halo_disc():
    cx, cy = W / 2, H / 2
    defs = rad("hd", [(0, "#0a2a3a", 1), (1, "#010306", 1)], "50%", "50%", "70%")
    body = [f'<rect width="{W}" height="{H}" fill="url(#hd)"/>']
    for R, sw, op, dash in [(380, 3, .35, "2 10"), (330, 16, .9, ""), (300, 2, .7, "60 14"), (250, 6, .5, "180 30 20 30"),
                            (205, 2, .6, "4 6"), (160, 10, .35, ""), (120, 2, .8, "40 20")]:
        d = f'stroke-dasharray="{dash}"' if dash else ""
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{CYAN}" stroke-width="{sw}" opacity="{op}" {d} filter="url(#glow)"/>')
    for k in range(24):
        a = math.radians(k * 15)
        body.append(f'<line x1="{cx + 340 * math.cos(a):.1f}" y1="{cy + 340 * math.sin(a):.1f}" x2="{cx + 372 * math.cos(a):.1f}" '
                    f'y2="{cy + 372 * math.sin(a):.1f}" stroke="{TEXT}" stroke-width="3" opacity=".8"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="330" fill="none" stroke="#fff" stroke-width="3" opacity=".9"/>')
    body.append(f'<path d="M{cx - 380},{cy} H{cx - 900} M{cx + 380},{cy} H{cx + 900}" stroke="{CYAN}" stroke-width="1.5" opacity=".5"/>')
    body.append(t(cx, cy + 14, "ATTACK//FRAME", 40, TEXT, .95, "middle", 'font-weight="300" letter-spacing="12" filter="url(#softglow)"'))
    svg("halo-disc", "".join(body), extra_defs=defs)


def circuit_horizon():
    r = random.Random(305)
    hz = 700
    defs = lin("chs", [(0, "#020308", 1), (1, "#1a0630", 1)])
    body = [f'<rect width="{W}" height="{hz}" fill="url(#chs)"/>', f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="#020107"/>']
    for _ in range(70):
        x, y = r.uniform(40, W - 40), hz
        pts = [(x, y)]
        for _ in range(r.randint(3, 7)):
            y -= r.uniform(30, 140)
            pts.append((x, y))
            if r.random() < .6:
                x += r.choice([-1, 1]) * r.uniform(20, 90); y -= r.uniform(10, 50)
                pts.append((x, y))
        col = r.choice([MAG, MAG, VIOLET, CYAN])
        body.append(f'<polyline points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="2" opacity=".7" filter="url(#softglow)"/>')
        body.append(f'<circle cx="{pts[-1][0]:.0f}" cy="{pts[-1][1]:.0f}" r="4" fill="none" stroke="{col}" stroke-width="2"/>')
        # reflection
        body.append(f'<polyline points="{" ".join(f"{a:.0f},{2 * hz - b:.0f}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="2" opacity=".12"/>')
    body.append(f'<rect y="{hz - 2}" width="{W}" height="4" fill="{MAG}" filter="url(#bigglow)"/>')
    body.append(wordmark(W / 2, hz + 190, 72))
    svg("circuit-horizon", "".join(body), extra_defs=defs)


def cube_sea():
    r = random.Random(306)
    body = [f'<rect width="{W}" height="{H}" fill="#03040c"/>']
    s = 34
    cells = [(i, j) for j in range(-2, 72) for i in range(-30, 72)]
    cells.sort(key=lambda c: c[0] + c[1])
    for i, j in cells:
        x, y = W / 2 + (i - j) * s, -380 + (i + j) * s / 2
        if not (-60 < x < W + 60 and -60 < y < H + 120):
            continue
        h = max(0, 40 * math.sin(i * .35) * math.cos(j * .3) + r.uniform(0, 30))
        hot = r.random() < .04
        top = f"{x},{y - h} {x + s},{y + s / 2 - h} {x},{y + s - h} {x - s},{y + s / 2 - h}"
        body.append(f'<polygon points="{x - s},{y + s / 2 - h} {x},{y + s - h} {x},{y + s} {x - s},{y + s / 2}" fill="#06101c"/>')
        body.append(f'<polygon points="{x},{y + s - h} {x + s},{y + s / 2 - h} {x + s},{y + s / 2} {x},{y + s}" fill="#040a14"/>')
        body.append(f'<polygon points="{top}" fill="{MAG if hot else "#08182a"}" stroke="{MAG if hot else CYAN}" stroke-width="1" '
                    f'opacity="{.95 if hot else .9}" {"filter=\"url(#glow)\"" if hot else ""}/>')
    body.append(mark())
    svg("cube-sea", "".join(body))


# ------------------------------------------------------------------ 90s cyber-collage
def wire_cube(cx, cy, s, a, col, sw=2):
    pts = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    def p(v):
        x, y, z = v
        x, z = x * math.cos(a) - z * math.sin(a), x * math.sin(a) + z * math.cos(a)
        y, z = y * math.cos(a * .7) - z * math.sin(a * .7), y * math.sin(a * .7) + z * math.cos(a * .7)
        f = 4 / (4 + z)
        return cx + x * s * f, cy + y * s * f
    P = [p(v) for v in pts]
    edges = [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]
    return "".join(f'<line x1="{P[a_][0]:.1f}" y1="{P[a_][1]:.1f}" x2="{P[b][0]:.1f}" y2="{P[b][1]:.1f}" stroke="{col}" stroke-width="{sw}"/>' for a_, b in edges)


def wire_sphere(cx, cy, R, col, n=9, sw=1.5, op=.8):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}"/>']
    for k in range(1, n):
        f = math.cos(math.pi * k / n)
        out.append(f'<ellipse cx="{cx}" cy="{cy + R * f:.1f}" rx="{R * math.sqrt(1 - f * f):.1f}" ry="{R * .18 * math.sqrt(1 - f * f):.1f}" '
                   f'fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{abs(R * f):.1f}" ry="{R}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op * .7:.2f}"/>')
    return "".join(out)


def window(x, y, w, h, title, col):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0a0420" fill-opacity=".55" stroke="{col}" stroke-width="2"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="26" fill="{col}" opacity=".85"/>'
            + t(x + 10, y + 18, title, 13, "#05030c", 1, "start", 'font-weight="700" letter-spacing="2"')
            + "".join(f'<rect x="{x + w - 22 - 20 * k}" y="{y + 6}" width="14" height="14" fill="none" stroke="#05030c" stroke-width="2"/>' for k in range(3)))


def cyber_collage():
    r = random.Random(307)
    defs = lin("cc", [(0, "#2a0a4a", 1), (.5, "#0a1640", 1), (1, "#003a3a", 1)], 1, 1)
    body = [f'<rect width="{W}" height="{H}" fill="url(#cc)"/>']
    for _ in range(140):
        x, y = r.uniform(0, W), r.uniform(0, H)
        body.append(t(x, y, r.choice("+×·○□△"), r.randint(10, 26), r.choice([CYAN, MAG, YEL, TEXT]), r.uniform(.2, .6)))
    body.append(wire_sphere(1450, 330, 230, CYAN, op=.65))
    body.append(f'<g filter="url(#softglow)">{wire_cube(380, 300, 140, .6, MAG, 3)}{wire_cube(1640, 850, 90, 1.1, YEL, 2)}{wire_cube(820, 860, 60, .3, CYAN, 2)}</g>')
    body.append(window(160, 560, 520, 300, "SYS.MONITOR", CYAN))
    for k in range(9):
        body.append(f'<rect x="{190 + k * 52}" y="{820 - (k * 37 % 200) - 40}" width="34" height="{(k * 37 % 200) + 40}" fill="{MAG}" opacity=".7"/>')
    body.append(window(1080, 600, 440, 220, "DIAL-UP://NODE", MAG))
    for k in range(6):
        body.append(t(1100, 660 + k * 26, "".join(r.choice("0123456789ABCDEF") for _ in range(32)), 15, TEXT, .8))
    body.append(window(760, 180, 400, 160, "README.TXT", YEL))
    body.append(t(780, 250, "welcome, operator.", 22, TEXT, .95))
    body.append(t(780, 290, "the frame is open.", 22, CYAN, .95))
    body.append(t(W / 2, 1010, "ATTACK//FRAME", 72, TEXT, .95, "middle", 'font-weight="800" font-style="italic" letter-spacing="8" filter="url(#glow)"'))
    svg("cyber-collage", "".join(body), extra_defs=defs)


def data_spires():
    r = random.Random(308)
    hz = 380
    defs = lin("dsk", [(0, "#000", 1), (1, "#140630", 1)])
    body = [f'<rect width="{W}" height="{H}" fill="url(#dsk)"/>', stars(r, 140, hz)]
    towers = []
    for i in range(-14, 15):
        for d in (9, 6, 4, 2.6, 1.8):
            if r.random() < .55:
                towers.append((i + r.uniform(-.3, .3), d, r.uniform(.6, 2.4)))
    towers.sort(key=lambda tw: -tw[1])
    for u, d, hgt in towers:
        x, y = W / 2 + u * 260 / d, hz + 700 / d
        w, h = 110 / d, hgt * 900 / d
        col = r.choice([CYAN, CYAN, MAG, TEAL])
        body.append(f'<rect x="{x - w / 2:.1f}" y="{y - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#04030c" stroke="{col}" stroke-width="1" opacity=".95"/>')
        fs = max(5, 14 / d * 2)
        cols = max(1, int(w / fs))
        for cidx in range(cols):
            col_x = x - w / 2 + (cidx + .5) * w / cols
            ys = y - h + fs
            while ys < y:
                if r.random() < .55:
                    body.append(f'<rect x="{col_x - fs * .25:.1f}" y="{ys - fs * .6:.1f}" width="{fs * .5:.1f}" height="{fs * .5:.1f}" fill="{col}" opacity="{r.uniform(.25, .9):.2f}"/>')
                ys += fs
        body.append(f'<rect x="{x - w / 2:.1f}" y="{y - h - 2:.1f}" width="{w:.1f}" height="3" fill="{col}" filter="url(#glow)"/>')
    body.append(f'<rect y="{hz + 700 / 1.8}" width="{W}" height="{H}" fill="#04030c"/>')
    body.append(floor_grid(hz + 700 / 1.8, MAG, n_lat=8, op=.4))
    body.append(mark(W / 2, H - 40, CYAN, "middle"))
    svg("data-spires", "".join(body), extra_defs=defs)


def crt_dream():
    r = random.Random(309)
    defs = (rad("crt", [(0, "#0d2a3a", 1), (1, "#02060a", 1)], "50%", "50%", "65%")
            + '<clipPath id="scr"><rect x="230" y="120" width="1460" height="840" rx="70"/></clipPath>')
    body = [f'<rect width="{W}" height="{H}" fill="#0c0a10"/>',
            f'<rect x="200" y="90" width="1520" height="900" rx="90" fill="#16131c" stroke="#2c2735" stroke-width="6"/>',
            f'<g clip-path="url(#scr)"><rect x="230" y="120" width="1460" height="840" fill="url(#crt)"/>']
    bars = [CYAN, YEL, TEAL, MAG, RED, VIOLET, TEXT]
    for k, c in enumerate(bars):
        body.append(f'<rect x="{230 + k * 1460 / 7:.1f}" y="790" width="{1460 / 7:.1f}" height="60" fill="{c}" opacity=".55"/>')
    for k in range(6):
        body.append(f'<g filter="url(#softglow)">{wire_cube(960 + (k - 2.5) * 210, 520 + 60 * math.sin(k), 60, k * .5, r.choice([CYAN, MAG, YEL]), 2)}</g>')
    body.append(t(960, 300, "ATTACK//FRAME", 90, TEXT, .95, "middle", 'font-weight="800" letter-spacing="10" filter="url(#glow)"'))
    body.append(t(960, 350, "CONNECT 28800 // CARRIER OK", 18, CYAN, .85, "middle", 'letter-spacing="6"'))
    body.append(f'<rect x="230" y="120" width="1460" height="840" fill="url(#scan)" opacity="1"/></g>')
    body.append(f'<circle cx="1640" cy="955" r="8" fill="{TEAL}" filter="url(#glow)"/>')
    svg("crt-dream", "".join(body), extra_defs=defs, scan=False)


def y2k_chrome():
    defs = (lin("irid", [(0, "#ff9ef0", 1), (.3, "#9ef0ff", 1), (.6, "#c6a6ff", 1), (1, "#7cffd8", 1)], 1, 1)
            + lin("chrome", [(0, "#ffffff", 1), (.45, "#8aa0b8", 1), (.5, "#20283a", 1), (.75, "#c0d8ff", 1), (1, "#ffffff", 1)])
            + rad("dk", [(0, "#000", 0), (1, "#000", .8)], "50%", "50%", "75%"))
    body = [f'<rect width="{W}" height="{H}" fill="url(#irid)"/>', f'<rect width="{W}" height="{H}" fill="#0a0420" opacity=".55"/>']
    for k in range(14):
        body.append(f'<ellipse cx="{W / 2}" cy="{H / 2}" rx="{300 + k * 60}" ry="{90 + k * 22}" fill="none" stroke="#fff" stroke-width="1.2" opacity="{.4 - k * .025:.2f}"/>')
    body.append(wire_sphere(W / 2, H / 2 - 30, 280, "#ffffff", 12, 1.4, .55))
    body.append(f'<text x="{W / 2}" y="{H / 2 + 40}" font-size="150" text-anchor="middle" font-weight="900" font-style="italic" '
                f'letter-spacing="6" fill="url(#chrome)" stroke="#0a0420" stroke-width="3">ATTACK//FRAME</text>')
    body.append(t(W / 2, H / 2 + 110, "MILLENNIUM EDITION", 22, "#fff", .9, "middle", 'letter-spacing="18"'))
    for k, (x, y) in enumerate([(300, 200), (1640, 260), (260, 860), (1600, 880)]):
        body.append(f'<path d="M{x},{y - 40} L{x + 10},{y - 10} L{x + 40},{y} L{x + 10},{y + 10} L{x},{y + 40} L{x - 10},{y + 10} L{x - 40},{y} L{x - 10},{y - 10} Z" fill="#fff" opacity=".85" filter="url(#glow)"/>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#dk)"/>')
    svg("y2k-chrome", "".join(body), extra_defs=defs, scan=False)


def skyline(r, base, n, hmin, hmax):
    pts, x = [f"0,{base}"], 0
    while x < W:
        w, h = r.uniform(40, 130), r.uniform(hmin, hmax)
        pts += [f"{x:.0f},{base - h:.0f}", f"{x + w:.0f},{base - h:.0f}"]
        x += w
    return " ".join(pts + [f"{W},{base}"])


def chroma_city():
    r = random.Random(311)
    base = 860
    sk = skyline(r, base, 0, 120, 520)
    body = [f'<rect width="{W}" height="{H}" fill="#030308"/>']
    for dx, c, op in [(-9, RED, .75), (9, CYAN, .75)]:
        body.append(f'<polygon points="{sk}" transform="translate({dx},0)" fill="none" stroke="{c}" stroke-width="3" opacity="{op}" filter="url(#softglow)"/>')
    body.append(f'<polygon points="{sk}" fill="#060610" stroke="#fff" stroke-width="1.5"/>')
    for _ in range(600):
        x, y = r.uniform(0, W), r.uniform(base - 500, base - 10)
        body.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="3" height="5" fill="{r.choice([YEL, CYAN, TEXT])}" opacity="{r.uniform(.1, .7):.2f}"/>')
    body.append(f'<polygon points="{sk}" fill="none" stroke="none"/>')
    for y in range(0, H, 3):
        if r.random() < .05:
            body.append(f'<rect x="0" y="{y}" width="{W}" height="{r.randint(2, 10)}" fill="{r.choice([RED, CYAN])}" opacity=".12"/>')
    body.append(f'<rect y="{base}" width="{W}" height="{H - base}" fill="#020205"/>')
    for dx, c in [(-6, RED), (6, CYAN), (0, TEXT)]:
        body.append(t(W / 2 + dx, base + 130, "ATTACK//FRAME", 84, c, .9 if c == TEXT else .6, "middle", 'font-weight="800" letter-spacing="14"'))
    svg("chroma-city", "".join(body))


def xerox_zine():
    r = random.Random(312)
    defs = ('<pattern id="ht" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="2.2" fill="#000"/></pattern>'
            '<pattern id="ht2" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="8" cy="8" r="5" fill="#ff2bd6"/></pattern>')
    body = [f'<rect width="{W}" height="{H}" fill="#e9e6dc"/>', f'<rect width="{W}" height="{H}" fill="url(#ht)" opacity=".15"/>']
    for _ in range(9):
        x, y, w, h = r.uniform(-100, W - 200), r.uniform(-100, H - 150), r.uniform(300, 800), r.uniform(150, 400)
        jag = " ".join(f"{x + w * k / 12:.0f},{y + r.uniform(-12, 12):.0f}" for k in range(13))
        jag2 = " ".join(f"{x + w * (12 - k) / 12:.0f},{y + h + r.uniform(-12, 12):.0f}" for k in range(13))
        fill = r.choice(["#111", "url(#ht2)", "#111", "#00e5ff"])
        body.append(f'<polygon points="{jag} {jag2}" fill="{fill}" opacity="{r.uniform(.75, .95):.2f}" transform="rotate({r.uniform(-8, 8):.1f} {x + w / 2:.0f} {y + h / 2:.0f})"/>')
    body.append(f'<rect x="250" y="420" width="1420" height="190" fill="{YEL}" opacity=".85" transform="rotate(-3 960 515)"/>')
    body.append(t(W / 2, 575, "ATTACK//FRAME", 170, "#0a0a0a", 1, "middle", 'font-weight="900" letter-spacing="4" transform="rotate(-3 960 515)"'))
    body.append(t(330, 700, "ISSUE #07 ··· THE FRAME IS OPEN", 30, "#0a0a0a", .9, "start", 'font-weight="700" letter-spacing="6" transform="rotate(-3 960 515)"'))
    for k in range(5):
        body.append(t(1500 - k * 40, 180 + k * 60, "★", 50, MAG, .9))
    svg("xerox-zine", "".join(body), bg="#e9e6dc", extra_defs=defs, scan=False)


# ------------------------------------------------------------------ neon megacity
def yellow_alert():
    r = random.Random(313)
    body = [f'<rect width="{W}" height="{H}" fill="{CYBY}"/>']
    body.append(f'<polygon points="0,0 1180,0 1040,1080 0,1080" fill="#0b0b0f"/>')
    body.append(f'<polygon points="1180,0 1210,0 1070,1080 1040,1080" fill="{RED}"/>')
    for k in range(18):
        body.append(f'<line x1="{60}" y1="{120 + k * 48}" x2="{60 + r.uniform(200, 700):.0f}" y2="{120 + k * 48}" stroke="{TEAL if k % 5 else RED}" stroke-width="2" opacity=".5"/>')
    body.append(t(90, 560, "ATTACK", 210, CYBY, 1, "start", 'font-weight="900" font-style="italic" letter-spacing="-4"'))
    body.append(t(90, 760, "//FRAME", 210, CYBY, 1, "start", 'font-weight="900" font-style="italic" letter-spacing="-4"'))
    body.append(t(96, 830, "OPERATOR INTERFACE  v2.077-AF", 22, TEAL, .9, "start", 'letter-spacing="6"'))
    for k in range(60):
        w = r.choice([2, 3, 5, 8])
        body.append(f'<rect x="{1350 + k * 7}" y="860" width="{w}" height="120" fill="#0b0b0f"/>')
    body.append(t(1350, 1010, "7F3A-0BAD-AF20", 20, "#0b0b0f", 1, "start", 'letter-spacing="6" font-weight="700"'))
    for k in range(5):
        y = 140 + k * 110
        body.append(f'<rect x="1340" y="{y}" width="460" height="74" fill="none" stroke="#0b0b0f" stroke-width="3"/>')
        body.append(f'<rect x="1340" y="{y}" width="{r.uniform(80, 440):.0f}" height="74" fill="#0b0b0f" opacity=".85"/>')
        body.append(t(1352, y + 48, ["NET", "SYS", "MEM", "SIG", "CPU"][k], 26, CYBY, 1, "start", 'font-weight="800" letter-spacing="4"'))
    svg("yellow-alert", "".join(body), bg=CYBY, scan=False)


def megatowers():
    r = random.Random(314)
    defs = lin("mt", [(0, "#0a0418", 1), (.55, "#5a0f2a", 1), (1, "#ff3a4a", 1)])
    body = [f'<rect width="{W}" height="{H}" fill="url(#mt)"/>']
    for layer, (col, op, wmin, wmax) in enumerate([("#2a1430", 1, 120, 220), ("#1a0c22", 1, 160, 300), ("#0c0612", 1, 220, 380)]):
        x = -50
        while x < W:
            w = r.uniform(wmin, wmax); top = r.uniform(40 + layer * 120, 380 + layer * 150)
            body.append(f'<rect x="{x:.0f}" y="{top:.0f}" width="{w:.0f}" height="{H - top:.0f}" fill="{col}"/>')
            for _ in range(int(w * (H - top) / 700)):
                body.append(f'<rect x="{x + r.uniform(4, w - 8):.0f}" y="{r.uniform(top + 6, H):.0f}" width="4" height="2" fill="{r.choice([YEL, ORANGE, TEAL])}" opacity="{r.uniform(.3, .95) * (1 - layer * .2):.2f}"/>')
            if r.random() < .35:
                ax, ay, aw, ah = x + w * .15, top + r.uniform(40, 300), w * .7, r.uniform(80, 200)
                c = r.choice([MAG, TEAL, RED, CYAN])
                body.append(f'<rect x="{ax:.0f}" y="{ay:.0f}" width="{aw:.0f}" height="{ah:.0f}" fill="{c}" opacity=".35"/>')
                body.append(f'<rect x="{ax:.0f}" y="{ay:.0f}" width="{aw:.0f}" height="{ah:.0f}" fill="none" stroke="{c}" stroke-width="4" filter="url(#glow)"/>')
                body.append(f'<circle cx="{ax + aw / 2:.0f}" cy="{ay + ah / 2:.0f}" r="{min(aw, ah) * .28:.0f}" fill="none" stroke="{c}" stroke-width="4" opacity=".9"/>')
            x += w + r.uniform(10, 60)
    for _ in range(14):
        y, x0 = r.uniform(150, 650), r.uniform(0, W)
        body.append(f'<line x1="{x0:.0f}" y1="{y:.0f}" x2="{x0 + r.uniform(80, 260):.0f}" y2="{y - r.uniform(0, 30):.0f}" stroke="{r.choice([RED, "#fff"])}" stroke-width="2" opacity=".7" filter="url(#softglow)"/>')
    body.append(mark(60, H - 50, RED))
    svg("megatowers", "".join(body), extra_defs=defs, scan=False)


def red_chrome():
    r = random.Random(315)
    body = [f'<rect width="{W}" height="{H}" fill="#080203"/>']
    pts = [(x, y) for x in range(-200, W + 400, 260) for y in range(-200, H + 400, 220)]
    pts = [(x + r.uniform(-90, 90), y + r.uniform(-80, 80)) for x, y in pts]
    cols = (W + 600) // 260 + 1
    rows = len(pts) // cols
    for i in range(cols - 1):
        for j in range(rows - 1):
            a, b, c, d = pts[i * rows + j], pts[i * rows + j + 1], pts[(i + 1) * rows + j + 1], pts[(i + 1) * rows + j]
            shade = r.randint(14, 40)
            body.append(f'<polygon points="{a[0]:.0f},{a[1]:.0f} {b[0]:.0f},{b[1]:.0f} {c[0]:.0f},{c[1]:.0f} {d[0]:.0f},{d[1]:.0f}" '
                        f'fill="rgb({shade + 8},{shade // 3},{shade // 3})" stroke="{RED}" stroke-width="{r.choice([1, 1, 2, 3])}" '
                        f'stroke-opacity="{r.uniform(.3, 1):.2f}" filter="url(#softglow)"/>')
    for _ in range(26):
        x, y = r.uniform(0, W), r.uniform(0, H)
        body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(3, 7):.0f}" fill="{r.choice([RED, TEAL])}" filter="url(#glow)"/>')
    body.append(f'<rect x="0" y="{H / 2 - 70}" width="{W}" height="140" fill="#000" opacity=".6"/>')
    body.append(t(W / 2, H / 2 + 26, "ATTACK//FRAME", 76, "#fff", .95, "middle", 'font-weight="800" letter-spacing="24"'))
    body.append(f'<line x1="{W / 2 - 520}" y1="{H / 2 + 50}" x2="{W / 2 + 520}" y2="{H / 2 + 50}" stroke="{RED}" stroke-width="3" filter="url(#glow)"/>')
    svg("red-chrome", "".join(body), bg="#080203")


def rooftop_rain():
    r = random.Random(316)
    defs = lin("rr", [(0, "#06020e", 1), (.7, "#2a0a3a", 1), (1, "#4a1040", 1)])
    body = [f'<rect width="{W}" height="{H}" fill="url(#rr)"/>']
    for _ in range(70):
        body.append(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(450, 820):.0f}" r="{r.uniform(8, 40):.0f}" fill="{r.choice([MAG, CYAN, ORANGE, VIOLET])}" opacity="{r.uniform(.25, .6):.2f}" filter="url(#bigglow)"/>')
    body.append(f'<polygon points="{skyline(r, 820, 0, 60, 330)}" fill="#0a0612" opacity=".85"/>')
    body.append(f'<polygon points="0,{H} 0,860 520,860 560,820 1300,820 1340,860 {W},860 {W},{H}" fill="#020104"/>')
    body.append(f'<rect x="1380" y="560" width="22" height="300" fill="#020104"/><rect x="1300" y="540" width="200" height="34" fill="#020104"/>')
    body.append(f'<rect x="1310" y="548" width="180" height="18" fill="{MAG}" opacity=".8" filter="url(#glow)"/>')
    for _ in range(14):
        x, w = r.uniform(0, W), r.uniform(60, 300)
        body.append(f'<rect x="{x:.0f}" y="{r.uniform(880, 1060):.0f}" width="{w:.0f}" height="3" fill="{r.choice([MAG, CYAN])}" opacity=".35" filter="url(#softglow)"/>')
    for _ in range(900):
        x, y, L = r.uniform(-100, W), r.uniform(-50, H), r.uniform(20, 70)
        body.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - L * .18:.0f}" y2="{y + L:.0f}" stroke="#bcd" stroke-width="1" opacity="{r.uniform(.08, .35):.2f}"/>')
    body.append(mark(60, H - 50, MAG))
    svg("rooftop-rain", "".join(body), extra_defs=defs)


def glyph_row(r, x, y, n, size, col):
    out = []
    for k in range(n):
        gx = x + k * size * 1.2
        for _ in range(3):
            if r.random() < .8:
                ax, ay = gx + r.uniform(0, size * .6), y - r.uniform(size * .3, size)
                out.append(f'<rect x="{ax:.0f}" y="{ay:.0f}" width="{r.choice([size * .15, size * .6]):.0f}" height="{r.choice([size * .15, size * .7]):.0f}" fill="{col}"/>')
    return "".join(out)


def night_market():
    r = random.Random(317)
    defs = lin("nm", [(0, "#05030a", 1), (1, "#12081a", 1)])
    body = [f'<rect width="{W}" height="{H}" fill="url(#nm)"/>']
    for _ in range(60):
        w, h = r.uniform(120, 420), r.uniform(60, 160)
        x, y = r.uniform(-60, W - 60), r.uniform(-20, 900)
        c = r.choice([MAG, CYAN, YEL, TEAL, RED, ORANGE, VIOLET])
        body.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="6" fill="{c}" opacity=".12"/>')
        body.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="6" fill="none" stroke="{c}" stroke-width="3" filter="url(#glow)"/>')
        body.append(f'<g filter="url(#softglow)">{glyph_row(r, x + 14, y + h * .7, int((w - 28) / (h * .5 * 1.2)), h * .5, c)}</g>')
    for _ in range(18):
        x0, x1, y0 = r.uniform(0, W), r.uniform(0, W), r.uniform(0, 400)
        body.append(f'<path d="M{x0:.0f},{y0:.0f} Q{(x0 + x1) / 2:.0f},{y0 + 160:.0f} {x1:.0f},{y0 + r.uniform(-40, 40):.0f}" fill="none" stroke="#000" stroke-width="3" opacity=".8"/>')
    body.append(f'<rect y="900" width="{W}" height="180" fill="#000" opacity=".75"/>')
    body.append(t(W / 2, 1010, "ATTACK//FRAME", 56, TEXT, .95, "middle", 'font-weight="700" letter-spacing="20" filter="url(#softglow)"'))
    svg("night-market", "".join(body), extra_defs=defs)


def datamosh():
    r = random.Random(318)
    defs = lin("dm", [(0, "#ff2a3d", 1), (.5, "#2a0010", 1), (1, "#00ffd0", 1)], 1, 0)
    body = [f'<rect width="{W}" height="{H}" fill="#050206"/>']
    y = 0
    while y < H:
        h = r.choice([4, 8, 16, 30, 60, 90])
        dx = r.choice([0, 0, 0, r.uniform(-260, 260)])
        body.append(f'<rect x="{dx:.0f}" y="{y}" width="{W}" height="{h}" fill="url(#dm)" opacity="{r.uniform(.25, .8):.2f}"/>')
        y += h
    for _ in range(140):
        s = r.choice([16, 32, 64])
        body.append(f'<rect x="{r.randrange(0, W, 16)}" y="{r.randrange(0, H, 16)}" width="{s}" height="{s}" fill="{r.choice([RED, TEAL, "#000", "#fff"])}" opacity="{r.uniform(.1, .6):.2f}"/>')
    for dx, c in [(-14, RED), (14, TEAL)]:
        body.append(t(W / 2 + dx, H / 2 + 40, "ATTACK//FRAME", 140, c, .7, "middle", 'font-weight="900" letter-spacing="6"'))
    body.append(t(W / 2, H / 2 + 40, "ATTACK//FRAME", 140, "#fff", .95, "middle", 'font-weight="900" letter-spacing="6"'))
    for _ in range(12):
        yy = r.uniform(H / 2 - 80, H / 2 + 60)
        body.append(f'<rect x="{r.uniform(300, 1400):.0f}" y="{yy:.0f}" width="{r.uniform(80, 400):.0f}" height="{r.uniform(4, 14):.0f}" fill="#050206"/>')
    svg("datamosh", "".join(body), extra_defs=defs)


def skyway():
    r = random.Random(319)
    defs = lin("sw", [(0, "#01030a", 1), (.5, "#0e1a36", 1), (1, "#2a1a2a", 1)])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sw)"/>', stars(r, 80, 400)]
    body.append(f'<rect y="420" width="{W}" height="300" fill="{ORANGE}" opacity=".18" filter="url(#bigglow)"/>')
    for _ in range(3200):
        x, y = r.uniform(0, W), r.uniform(520, H)
        body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1, 3.2):.1f}" fill="{r.choice([YEL, ORANGE, ORANGE, TEXT, CYAN])}" opacity="{r.uniform(.35, 1):.2f}"/>')
    roads = [(-100, 700, 600, 380, 1300, 760, 2050, 520), (-100, 980, 500, 760, 1500, 1000, 2050, 700),
             (-100, 560, 700, 650, 1200, 420, 2050, 460)]
    for x0, y0, c1x, c1y, c2x, c2y, x1, y1 in roads:
        d = f"M{x0},{y0} C{c1x},{c1y} {c2x},{c2y} {x1},{y1}"
        body.append(f'<path d="{d}" fill="none" stroke="#020409" stroke-width="44"/>')
        body.append(f'<path d="{d}" fill="none" stroke="{CYAN}" stroke-width="2" opacity=".6" transform="translate(0,-22)"/>')
        body.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="3 28" opacity=".9" transform="translate(0,-8)" filter="url(#softglow)"/>')
        body.append(f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="5" stroke-dasharray="3 22" opacity=".9" transform="translate(0,8)" filter="url(#softglow)"/>')
    for x in range(100, W, 260):
        body.append(f'<rect x="{x}" y="{r.uniform(600, 820):.0f}" width="14" height="{H}" fill="#020409"/>')
    body.append(mark(W - 60, 80, CYAN, "end"))
    svg("skyway", "".join(body), extra_defs=defs, scan=False)


def data_wall():
    r = random.Random(320)
    defs = rad("dwg", [(0, "#1a0a30", 1), (1, "#02010a", 1)], "50%", "50%", "70%")
    body = [f'<rect width="{W}" height="{H}" fill="url(#dwg)"/>']
    R = 46
    for row in range(-1, 16):
        for col in range(-1, 26):
            x = col * R * 1.75 + (row % 2) * R * .875
            y = row * R * 1.5
            dist = math.hypot(x - W / 2, y - H / 2)
            hot = dist < 260 and r.random() < .45
            gone = dist < 120 and r.random() < .6
            if gone:
                continue
            pts = " ".join(f"{x + R * math.cos(math.radians(60 * k + 30)):.1f},{y + R * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
            c = MAG if hot else CYAN
            body.append(f'<polygon points="{pts}" fill="{c}" fill-opacity="{.25 if hot else r.uniform(.02, .1):.2f}" stroke="{c}" '
                        f'stroke-width="{2 if hot else 1.2}" stroke-opacity="{.9 if hot else .45}"{" filter=\"url(#glow)\"" if hot else ""}/>')
    body.append(f'<circle cx="{W / 2}" cy="{H / 2}" r="90" fill="#fff" opacity=".25" filter="url(#bigglow)"/>')
    body.append(t(W / 2, H - 60, "ATTACK//FRAME", 30, TEXT, .9, "middle", 'font-weight="700" letter-spacing="16"'))
    svg("data-wall", "".join(body), extra_defs=defs)


WALLPAPERS = [
    ("grid-arena", "Grid Arena", grid_arena), ("light-ribbons", "Light Ribbons", light_ribbons),
    ("monolith", "Monolith", monolith), ("halo-disc", "Halo Disc", halo_disc),
    ("circuit-horizon", "Circuit Horizon", circuit_horizon), ("cube-sea", "Cube Sea", cube_sea),
    ("cyber-collage", "Cyber Collage", cyber_collage), ("data-spires", "Data Spires", data_spires),
    ("crt-dream", "CRT Dream", crt_dream), ("y2k-chrome", "Y2K Chrome", y2k_chrome),
    ("chroma-city", "Chroma City", chroma_city), ("xerox-zine", "Xerox Zine", xerox_zine),
    ("yellow-alert", "Yellow Alert", yellow_alert), ("megatowers", "Megatowers", megatowers),
    ("red-chrome", "Red Chrome", red_chrome), ("rooftop-rain", "Rooftop Rain", rooftop_rain),
    ("night-market", "Night Market", night_market), ("datamosh", "Datamosh", datamosh),
    ("skyway", "Skyway", skyway), ("data-wall", "Data Wall", data_wall),
]

if __name__ == "__main__":
    for _, _, fn in WALLPAPERS:
        fn()
    names = wp1.OUT / "names.tsv"
    existing = names.read_text() if names.exists() else ""
    extra = "".join(f"af-{s}\t{n}\n" for s, n, _ in WALLPAPERS if f"af-{s}\t" not in existing)
    names.write_text(existing + extra)
    print(f"wrote {len(WALLPAPERS)} wallpapers to {wp1.OUT}")
