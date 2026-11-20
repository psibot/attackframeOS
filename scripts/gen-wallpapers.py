#!/usr/bin/env python3
"""Generate the AttackFrame wallpaper pack (10 original SVG designs, 16:9).
Run: python3 scripts/gen-wallpapers.py   ->  assets/wallpapers/af-*.svg
Render: scripts/render-wallpapers.sh     ->  assets/wallpapers/png/af-*.png (3840x2160)"""
import math
import random
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "wallpapers"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080
VOID, PANEL, CYAN, MAG, YEL, TEXT, DIM = "#05070d", "#0b0f1a", "#00f0ff", "#ff2bd6", "#f5ff3b", "#c8f7ff", "#3a4660"
VIOLET = "#7a2bff"
FONT = "'JetBrainsMono Nerd Font','JetBrains Mono','DejaVu Sans Mono',monospace"

DEFS = """
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="softglow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="bigglow" x="-30%" y="-30%" width="160%" height="160%">
  <feGaussianBlur stdDeviation="18" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="1" fill="#000" opacity=".35"/>
</pattern>
<radialGradient id="vignette" cx="50%" cy="50%" r="75%">
  <stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".75"/>
</radialGradient>"""


def svg(name, body, bg=VOID, extra_defs="", scan=True):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="{FONT}">\n<defs>{DEFS}{extra_defs}</defs>\n'
           f'<rect width="{W}" height="{H}" fill="{bg}"/>\n{body}\n'
           + (f'<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".5"/>\n' if scan else "")
           + f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>\n</svg>\n')
    (OUT / f"af-{name}.svg").write_text(doc)


def t(x, y, s, size=14, fill=TEXT, op=1.0, anchor="start", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" opacity="{op:.2f}" '
            f'text-anchor="{anchor}" xml:space="preserve" {extra}>{escape(s)}</text>')


def brackets(m, L, color, sw=2):
    p = [f"M{m},{m + L} V{m} H{m + L}", f"M{W - m - L},{m} H{W - m} V{m + L}",
         f"M{m},{H - m - L} V{H - m} H{m + L}", f"M{W - m - L},{H - m} H{W - m} V{H - m - L}"]
    return "".join(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>' for d in p)


def tag(x, y, label, color=CYAN, anchor="start"):
    """Small HUD caption, e.g. bottom-left corner text."""
    return t(x, y, label, 13, color, .75, anchor, 'letter-spacing="3"')


def wordmark(cx, cy, size=96, sub=None):
    out = [t(cx + 4, cy, "ATTACK//FRAME", size, MAG, .55, "middle", 'font-weight="800" letter-spacing="10"'),
           t(cx - 3, cy, "ATTACK//FRAME", size, CYAN, .55, "middle", 'font-weight="800" letter-spacing="10"'),
           t(cx, cy, "ATTACK//FRAME", size, TEXT, 1, "middle", 'font-weight="800" letter-spacing="10" filter="url(#glow)"')]
    if sub:
        out.append(t(cx, cy + size * .5, sub, size * .17, CYAN, .85, "middle", f'letter-spacing="{size * .07:.0f}"'))
    return "".join(out)


# ------------------------------------------------------------------ 01 neon rain
def neon_rain():
    r = random.Random(1)
    glyphs = "0123456789ABCDEF<>/\\|=+*#$%{}[]:;"
    body, step, size = [], 20, 18
    for col in range(W // step + 1):
        x = col * step + r.uniform(-2, 2)
        head = r.uniform(-200, H + 300)
        length = r.randint(10, 42)
        color = MAG if r.random() < .14 else CYAN
        for k in range(length):
            y = head - k * (size + 2)
            if not -20 < y < H + 20:
                continue
            op = max(.05, 1 - k / length) * (.9 if k else 1)
            fill = TEXT if k == 0 else color
            body.append(t(x, y, r.choice(glyphs), size, fill, op * r.uniform(.6, 1),
                          extra='filter="url(#softglow)"' if k == 0 else ""))
    body.append(f'<rect x="{W / 2 - 520}" y="{H / 2 - 110}" width="1040" height="200" fill="{VOID}" opacity=".78"/>')
    body.append(wordmark(W / 2, H / 2 + 20, 92, "DATA STREAM // LIVE"))
    body.append(brackets(28, 70, CYAN))
    body.append(tag(40, H - 40, "STREAM 0x7F3A // PACKETS INBOUND"))
    svg("neon-rain", "\n".join(body), bg="#03060b")


# ------------------------------------------------------------------ 02 circuit
def circuit():
    r = random.Random(2)
    g = 40
    body = []
    cx, cy, cw, ch = W / 2, H / 2, 360, 220
    for i in range(170):
        # start on the chip edge or a random grid point, walk outward with 45° bends
        if i < 70:
            side = r.choice("nsew")
            if side in "ns":
                x, y = cx - cw / 2 + r.randint(1, cw // 20 - 1) * 20, cy + (ch / 2 if side == "s" else -ch / 2)
                dx, dy = 0, (1 if side == "s" else -1)
            else:
                x, y = cx + (cw / 2 if side == "e" else -cw / 2), cy - ch / 2 + r.randint(1, ch // 20 - 1) * 20
                dx, dy = (1 if side == "e" else -1), 0
        else:
            x, y = r.randint(0, W // g) * g, r.randint(0, H // g) * g
            if abs(x - cx) < cw / 2 + 40 and abs(y - cy) < ch / 2 + 40:
                continue
            dx, dy = r.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        pts = [(x, y)]
        for _ in range(r.randint(2, 6)):
            n = r.randint(2, 9) * g / 2
            x, y = x + dx * n, y + dy * n
            pts.append((x, y))
            if r.random() < .6:  # 45° turn
                if dx == 0:
                    dx = r.choice([-1, 1]); dy = dy
                    x, y = x + dx * g / 2, y + dy * g / 2
                    pts.append((x, y)); dy = 0
                else:
                    dy = r.choice([-1, 1])
                    x, y = x + dx * g / 2, y + dy * g / 2
                    pts.append((x, y)); dx = 0
        hot = r.random() < .12
        color = MAG if hot else CYAN
        d = "M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts)
        body.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{2.2 if hot else 1.6}" '
                    f'opacity="{.95 if hot else r.uniform(.25, .55):.2f}" stroke-linejoin="round"'
                    + (' filter="url(#softglow)"' if hot else "") + "/>")
        ex, ey = pts[-1]
        body.append(f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{4.5 if hot else 3.5}" fill="{VOID}" stroke="{color}" stroke-width="2"/>')
    # chip
    body.append(f'<rect x="{cx - cw / 2}" y="{cy - ch / 2}" width="{cw}" height="{ch}" rx="10" fill="{PANEL}" '
                f'stroke="{CYAN}" stroke-width="3" filter="url(#glow)"/>')
    for k in range(1, cw // 20):
        for yy in (cy - ch / 2 - 10, cy + ch / 2):
            body.append(f'<rect x="{cx - cw / 2 + k * 20 - 3}" y="{yy}" width="6" height="10" fill="{CYAN}" opacity=".8"/>')
    for k in range(1, ch // 20):
        for xx in (cx - cw / 2 - 10, cx + cw / 2):
            body.append(f'<rect x="{xx}" y="{cy - ch / 2 + k * 20 - 3}" width="10" height="6" fill="{CYAN}" opacity=".8"/>')
    body.append(t(cx, cy - 10, "AF//CORE", 54, TEXT, 1, "middle", 'font-weight="800" letter-spacing="6" filter="url(#softglow)"'))
    body.append(t(cx, cy + 40, "0x7F3A  ·  OFFENSIVE SoC", 16, MAG, .9, "middle", 'letter-spacing="4"'))
    body.append(brackets(28, 70, CYAN))
    body.append(tag(40, H - 40, "BUS 0x7F // SILICON ARSENAL"))
    svg("circuit", "\n".join(body), bg="#04070c")


# ------------------------------------------------------------------ 03 hex hive
def hexhive():
    r = random.Random(3)
    s = 46  # hex radius
    hw, vh = math.sqrt(3) * s, 1.5 * s
    codes = ["RC", "WB", "EX", "CR", "WL", "SN", "AD", "RE", "FR", "PV"]
    body = []
    for row in range(-1, int(H / vh) + 2):
        for col in range(-1, int(W / hw) + 2):
            x = col * hw + (hw / 2 if row % 2 else 0)
            y = row * vh
            dist = math.hypot((x - W / 2) / W, (y - H / 2) / H)
            pts = " ".join(f"{x + (s - 3) * math.cos(math.radians(60 * k + 30)):.1f},"
                           f"{y + (s - 3) * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
            lit = r.random() < max(.03, .5 - dist * 1.4)
            color = MAG if r.random() < .3 else CYAN
            if lit:
                body.append(f'<polygon points="{pts}" fill="{color}" fill-opacity="{r.uniform(.06, .22):.2f}" '
                            f'stroke="{color}" stroke-width="2" filter="url(#softglow)"/>')
                if r.random() < .45:
                    body.append(t(x, y + 6, r.choice(codes), 17, color, .95, "middle", 'font-weight="700"'))
            else:
                body.append(f'<polygon points="{pts}" fill="none" stroke="{DIM}" stroke-width="1.2" opacity="{max(.15, .6 - dist):.2f}"/>')
    # central hex emblem
    R = 170
    pts = " ".join(f"{W / 2 + R * math.cos(math.radians(60 * k + 30)):.1f},{H / 2 + R * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
    body.append(f'<polygon points="{pts}" fill="{VOID}" stroke="{CYAN}" stroke-width="5" filter="url(#glow)"/>')
    body.append(f'<path d="M{W / 2 - 50},{H / 2 + 70} L{W / 2 - 5},{H / 2 - 70} M{W / 2 + 5},{H / 2 + 70} L{W / 2 + 50},{H / 2 - 70}" '
                f'stroke="{MAG}" stroke-width="16" stroke-linecap="round" filter="url(#glow)"/>')
    body.append(t(W / 2, H / 2 + R + 60, "THE HIVE // 10 CELLS ARMED", 20, CYAN, .9, "middle", 'letter-spacing="6"'))
    svg("hexhive", "\n".join(body), bg="#05060c")


# ------------------------------------------------------------------ 04 glitch
def glitch():
    r = random.Random(4)
    clips, body = [], []
    # background noise bars
    for _ in range(90):
        y = r.uniform(0, H); h = r.uniform(1, 7)
        x = r.uniform(-200, W); w = r.uniform(80, 900)
        body.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.1f}" '
                    f'fill="{r.choice([CYAN, MAG, VIOLET, DIM])}" opacity="{r.uniform(.05, .35):.2f}"/>')
    # sliced title: each slice shifted horizontally
    y0, size = H / 2 + 60, 190
    ys = sorted(r.uniform(y0 - size, y0 + 30) for _ in range(9))
    bands = list(zip([y0 - size - 20] + ys, ys + [y0 + 50]))
    for i, (a, b) in enumerate(bands):
        clips.append(f'<clipPath id="sl{i}"><rect x="0" y="{a:.1f}" width="{W}" height="{b - a:.1f}"/></clipPath>')
        dx = r.choice([0, 0, r.uniform(-60, 60)])
        g = (t(W / 2 + dx + 9, y0, "ATTACK//FRAME", size, MAG, .85, "middle", 'font-weight="900"')
             + t(W / 2 + dx - 9, y0, "ATTACK//FRAME", size, CYAN, .85, "middle", 'font-weight="900"')
             + t(W / 2 + dx, y0, "ATTACK//FRAME", size, TEXT, 1, "middle", 'font-weight="900"'))
        body.append(f'<g clip-path="url(#sl{i})">{g}</g>')
    body.append(f'<rect x="0" y="{y0 - size * .45:.0f}" width="{W}" height="6" fill="{YEL}" opacity=".85" filter="url(#softglow)"/>')
    body.append(t(W / 2, y0 + 110, "SIGNAL CORRUPTED // OPERATOR IN CONTROL", 26, YEL, .9, "middle", 'letter-spacing="10"'))
    body.append(t(60, 90, "ERR 0x7F3A :: framebuffer desync", 18, MAG, .8))
    body.append(t(W - 60, H - 60, "▌▌▌ REC ●", 20, MAG, .9, "end", 'letter-spacing="4"'))
    svg("glitch", "\n".join(body), bg="#07040e", extra_defs="".join(clips))


# ------------------------------------------------------------------ 05 rain city
def rain_city():
    r = random.Random(5)
    body = []
    base = H * .72
    grad = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05040f"/>'
            f'<stop offset=".7" stop-color="#2a0a3d"/><stop offset="1" stop-color="{MAG}" stop-opacity=".5"/></linearGradient>'
            '<linearGradient id="wet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".95"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{base}" fill="url(#sky)"/>')

    def layer(max_h, shade, win_p, signs):
        out, x = [], -20
        while x < W:
            bw = r.randint(50, 150); bh = r.randint(int(max_h * .35), max_h)
            out.append(f'<rect x="{x}" y="{base - bh}" width="{bw}" height="{bh}" fill="{shade}"/>')
            for wy in range(int(base - bh + 12), int(base - 8), 14):
                for wx in range(x + 8, x + bw - 8, 12):
                    if r.random() < win_p:
                        out.append(f'<rect x="{wx}" y="{wy}" width="5" height="7" fill="{r.choice([CYAN, YEL, TEXT, MAG])}" opacity="{r.uniform(.3, .85):.2f}"/>')
            if signs and r.random() < .3 and bh > 200:
                word = r.choice(["ROOT", "0DAY", "SHELL", "PWN", "NODE7", "TCP/445"])
                c = r.choice([MAG, CYAN, YEL])
                sx, sy = x + bw / 2 - 16, base - bh + 30
                out.append(f'<rect x="{sx}" y="{sy}" width="32" height="{len(word) * 30 + 16}" rx="4" fill="{VOID}" stroke="{c}" stroke-width="2.5" filter="url(#softglow)"/>')
                for k, ch_ in enumerate(word):
                    out.append(t(sx + 16, sy + 34 + k * 30, ch_, 24, c, 1, "middle", 'font-weight="800" filter="url(#softglow)"'))
            x += bw + r.randint(-10, 10)
        return out

    city = layer(380, "#0d0a1c", .05, False) + layer(560, "#06050d", .09, True)
    body += city
    # wet street reflection
    body.append(f'<g transform="translate(0,{2 * base}) scale(1,-1)" opacity=".35">{"".join(city)}</g>')
    body.append(f'<rect y="{base}" width="{W}" height="{H - base}" fill="url(#wet)"/>')
    body.append(f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" stroke="{MAG}" stroke-width="2" opacity=".7" filter="url(#softglow)"/>')
    # rain
    for _ in range(900):
        x, y, L = r.uniform(-100, W), r.uniform(-50, H), r.uniform(14, 40)
        body.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - L * .25:.0f}" y2="{y + L:.0f}" stroke="{TEXT}" '
                    f'stroke-width="1" opacity="{r.uniform(.08, .3):.2f}"/>')
    body.append(t(60, 100, "ATTACK//FRAME", 40, TEXT, .95, "start", 'font-weight="800" letter-spacing="8" filter="url(#softglow)"'))
    body.append(t(62, 130, "NIGHT SHIFT // SECTOR 7", 15, CYAN, .9, "start", 'letter-spacing="5"'))
    svg("rain-city", "\n".join(body), extra_defs=grad)


# ------------------------------------------------------------------ 06 terminal
def terminal():
    r = random.Random(6)
    body = []
    # faded background log
    for k in range(60):
        line = " ".join(f"{r.randint(0, 255):02x}" for _ in range(r.randint(8, 40)))
        body.append(t(20, 20 + k * 18, line, 13, DIM, .35))
    x0, y0, w, h = 300, 170, 1320, 740
    body.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="14" fill="{PANEL}" fill-opacity=".94" stroke="{CYAN}" stroke-width="2.5" filter="url(#glow)"/>')
    body.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="46" rx="14" fill="#0f1626"/>')
    for i, c in enumerate([MAG, YEL, CYAN]):
        body.append(f'<circle cx="{x0 + 28 + i * 26}" cy="{y0 + 23}" r="7" fill="{c}"/>')
    body.append(t(x0 + w / 2, y0 + 29, "ghost@attackframe: ~/ops", 16, CYAN, .95, "middle"))
    P = [(CYAN, "┌─[ghost@attackframe]─[~/ops]─[tgt 10.10.11.5]"), (MAG, "└──╼ ▶ portscan -sV 10.10.11.5"),
         (DIM, ""), (TEXT, "PORT      STATE  SERVICE        VERSION"),
         (TEXT, "22/tcp    open   ssh            OpenSSH 9.x"),
         (TEXT, "53/tcp    open   domain         DNS"),
         (TEXT, "88/tcp    open   kerberos-sec"),
         (YEL,  "445/tcp   open   microsoft-ds   SMB signing: disabled"),
         (TEXT, "5985/tcp  open   wsman          WinRM"),
         (DIM, ""), (CYAN, "┌─[ghost@attackframe]─[~/ops]─[tgt 10.10.11.5]"),
         (MAG, "└──╼ ▶ loot --summary"),
         (TEXT, "[+] creds ....... 3 harvested"), (TEXT, "[+] hashes ...... 12 cracked / 40"),
         (YEL,  "[!] path to DA .. FOUND (4 hops)"), (DIM, ""),
         (CYAN, "┌─[ghost@attackframe]─[~/ops]─[tgt 10.10.11.5]"), (MAG, "└──╼ ▶ ")]
    for i, (c, s) in enumerate(P):
        body.append(t(x0 + 36, y0 + 96 + i * 34, s, 24, c, 1))
    body.append(f'<rect x="{x0 + 132}" y="{y0 + 96 + (len(P) - 1) * 34 - 22}" width="14" height="28" fill="{MAG}" filter="url(#softglow)"/>')
    body.append(t(W / 2, 110, "ATTACK//FRAME", 44, TEXT, .95, "middle", 'font-weight="800" letter-spacing="12" filter="url(#softglow)"'))
    body.append(tag(40, H - 40, "SESSION 0x7F3A // AUTHORIZED ENGAGEMENTS ONLY"))
    svg("terminal", "\n".join(body), bg="#04060a")


# ------------------------------------------------------------------ 07 radar
def radar():
    r = random.Random(7)
    cx, cy, R = W / 2, H / 2, 470
    grad = (f'<radialGradient id="sweep" cx="{cx}" cy="{cy}" r="{R}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".35"/></radialGradient>'
            f'<linearGradient id="wedge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{CYAN}" stop-opacity=".45"/></linearGradient>')
    body = []
    for k in range(1, 6):
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{R * k / 5}" fill="none" stroke="{CYAN}" stroke-width="{2.5 if k == 5 else 1.2}" opacity="{.25 + k * .1:.2f}"/>')
    for a in range(0, 360, 2):
        L = 22 if a % 30 == 0 else (12 if a % 10 == 0 else 6)
        x1, y1 = cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))
        x2, y2 = cx + (R + L) * math.cos(math.radians(a)), cy + (R + L) * math.sin(math.radians(a))
        body.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{CYAN}" stroke-width="1.5" opacity=".7"/>')
        if a % 30 == 0:
            tx, ty = cx + (R + 48) * math.cos(math.radians(a - 90)), cy + (R + 48) * math.sin(math.radians(a - 90)) + 5
            body.append(t(tx, ty, f"{a:03d}", 14, CYAN, .8, "middle"))
    body.append(f'<line x1="{cx - R}" y1="{cy}" x2="{cx + R}" y2="{cy}" stroke="{CYAN}" opacity=".3"/>'
                f'<line x1="{cx}" y1="{cy - R}" x2="{cx}" y2="{cy + R}" stroke="{CYAN}" opacity=".3"/>')
    # sweep wedge (60°) ending at -35°
    a1, a2 = math.radians(-95), math.radians(-35)
    body.append(f'<path d="M{cx},{cy} L{cx + R * math.cos(a1):.1f},{cy + R * math.sin(a1):.1f} '
                f'A{R},{R} 0 0 1 {cx + R * math.cos(a2):.1f},{cy + R * math.sin(a2):.1f} Z" fill="url(#sweep)"/>')
    body.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + R * math.cos(a2):.1f}" y2="{cy + R * math.sin(a2):.1f}" '
                f'stroke="{CYAN}" stroke-width="3" filter="url(#softglow)"/>')
    hosts = ["10.10.11.5 :445", "10.10.11.12 :80", "10.10.11.20 :88", "10.10.11.31 :22", "10.10.11.44 :3389",
             "10.10.11.50 :5985", "10.10.11.61 :443", "10.10.11.77 :1433"]
    for i, hst in enumerate(hosts):
        a = math.radians(r.uniform(0, 360)); d = r.uniform(.2, .92) * R
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        c = MAG if i == 0 else (YEL if i < 3 else CYAN)
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{9 if i == 0 else 6}" fill="{c}" filter="url(#glow)"/>')
        if i == 0:
            body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="26" fill="none" stroke="{MAG}" stroke-width="2"/>'
                        f'<path d="M{x - 40:.1f},{y:.1f} h20 M{x + 20:.1f},{y:.1f} h20 M{x:.1f},{y - 40:.1f} v20 M{x:.1f},{y + 20:.1f} v20" stroke="{MAG}" stroke-width="2"/>')
        body.append(t(x + 16, y - 12, hst, 15, c, .95))
    # side panels
    body.append(t(70, 120, "ATTACK//FRAME", 34, TEXT, .95, "start", 'font-weight="800" letter-spacing="6" filter="url(#softglow)"'))
    body.append(t(72, 150, "TARGET ACQUISITION", 14, CYAN, .9, "start", 'letter-spacing="5"'))
    for i, s in enumerate(["SUBNET   10.10.11.0/24", "HOSTS    8 LIVE", "LOCK     10.10.11.5", "SVC      SMB / KERBEROS"]):
        body.append(t(72, 210 + i * 28, s, 15, MAG if "LOCK" in s else TEXT, .85))
    body.append(brackets(28, 70, CYAN))
    svg("radar", "\n".join(body), bg="#030a0c", extra_defs=grad)


# ------------------------------------------------------------------ 08 wireframe peaks
def wireframe_peaks():
    r = random.Random(8)
    hz = H * .55
    grad = ('<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05030d"/>'
            f'<stop offset="1" stop-color="#2b0738"/></linearGradient>'
            f'<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{YEL}"/>'
            f'<stop offset="1" stop-color="{MAG}"/></linearGradient>'
            f'<clipPath id="sunclip"><circle cx="{W / 2}" cy="{hz - 40}" r="230"/></clipPath>')
    body = [f'<rect width="{W}" height="{hz + 2}" fill="url(#dusk)"/>']
    for _ in range(220):
        body.append(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, hz * .9):.0f}" r="{r.uniform(.6, 1.8):.1f}" fill="{TEXT}" opacity="{r.uniform(.2, .9):.2f}"/>')
    # striped sun
    stripes = "".join(f'<rect x="{W / 2 - 240}" y="{hz - 40 + k * 26 - 30}" width="480" height="{4 + k * 2.2}" fill="#05030d"/>' for k in range(9))
    body.append(f'<g clip-path="url(#sunclip)" filter="url(#bigglow)"><rect x="{W / 2 - 240}" y="{hz - 280}" width="480" height="480" fill="url(#sun)"/>{stripes}</g>')

    # perspective terrain: rows far→near, height noise rises toward the sides
    cols, rows = 72, 34

    def height(u, v):
        side = abs(u - .5) * 2
        n = (math.sin(u * 23 + v * 3) + math.sin(u * 51 - v * 7) * .5 + r.uniform(-.25, .25))
        return max(0, side ** 1.6 * (1.4 + n) * 230)

    grid = []
    for j in range(rows):
        v = j / (rows - 1)
        depth = .03 + v ** 2.2  # 0 at horizon -> 1 near
        y_base = hz + depth * (H - hz) * 1.05
        row = []
        for i in range(cols):
            u = i / (cols - 1)
            x = W / 2 + (u - .5) * W * (0.25 + 2.6 * depth)
            row.append((x, y_base - height(u, v) * (0.15 + depth)))
        grid.append(row)
    for j, row in enumerate(grid):  # fill to hide farther lines, then stroke
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in row) + f" L{row[-1][0]:.0f},{H} L{row[0][0]:.0f},{H} Z"
        body.append(f'<path d="{d}" fill="#06030c" opacity=".55"/>')
        body.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in row)}" fill="none" stroke="{MAG}" '
                    f'stroke-width="{.8 + j / rows * 1.6:.2f}" opacity="{.35 + j / rows * .6:.2f}"/>')
    for i in range(0, cols, 2):
        pts = " ".join(f"{grid[j][i][0]:.1f},{grid[j][i][1]:.1f}" for j in range(rows))
        body.append(f'<polyline points="{pts}" fill="none" stroke="{VIOLET}" stroke-width="1" opacity=".45"/>')
    body.append(f'<line x1="0" y1="{hz}" x2="{W}" y2="{hz}" stroke="{CYAN}" stroke-width="2" opacity=".8" filter="url(#softglow)"/>')
    body.append(wordmark(W / 2, 170, 80, "OUTRUN THE BLUE TEAM"))
    svg("wireframe-peaks", "\n".join(body), extra_defs=grad)


# ------------------------------------------------------------------ 09 attack graph
def attack_graph():
    r = random.Random(9)
    nodes = []
    while len(nodes) < 120:
        p = (r.uniform(60, W - 60), r.uniform(60, H - 60))
        if all(math.dist(p, q) > 85 for q in nodes):
            nodes.append(p)
    body = []
    for i, p in enumerate(nodes):
        near = sorted(range(len(nodes)), key=lambda k: math.dist(p, nodes[k]))[1:4]
        for k in near:
            if k > i:
                body.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{nodes[k][0]:.0f}" y2="{nodes[k][1]:.0f}" stroke="{CYAN}" stroke-width="1.1" opacity=".22"/>')
    for p in nodes:
        body.append(f'<circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="{r.uniform(2.5, 5):.1f}" fill="{CYAN}" opacity="{r.uniform(.35, .8):.2f}"/>')
    # highlighted kill chain, left to right
    chain = [("ENTRY", (180, 760)), ("WEB01", (520, 560)), ("SVC_SQL", (860, 700)),
             ("FS02", (1180, 430)), ("ADM-WS", (1460, 610)), ("DC01", (1720, 300))]
    for (a, pa), (b, pb) in zip(chain, chain[1:]):
        body.append(f'<line x1="{pa[0]}" y1="{pa[1]}" x2="{pb[0]}" y2="{pb[1]}" stroke="{MAG}" stroke-width="4" filter="url(#glow)"/>')
        mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
        ang = math.degrees(math.atan2(pb[1] - pa[1], pb[0] - pa[0]))
        body.append(f'<path d="M-12,-9 L6,0 L-12,9 Z" fill="{MAG}" transform="translate({mx:.0f},{my:.0f}) rotate({ang:.1f})"/>')
    for i, (name, (x, y)) in enumerate(chain):
        last = i == len(chain) - 1
        c = YEL if last else MAG
        body.append(f'<circle cx="{x}" cy="{y}" r="{26 if last else 18}" fill="{VOID}" stroke="{c}" stroke-width="4" filter="url(#glow)"/>')
        body.append(f'<circle cx="{x}" cy="{y}" r="{8 if last else 6}" fill="{c}"/>')
        body.append(t(x, y + (52 if last else 46), name, 18 if last else 16, c, 1, "middle", 'font-weight="700" letter-spacing="2"'))
    body.append(t(1720, 250, "DOMAIN ADMIN", 22, YEL, 1, "middle", 'font-weight="800" letter-spacing="4" filter="url(#softglow)"'))
    body.append(t(70, 110, "ATTACK//FRAME", 36, TEXT, .95, "start", 'font-weight="800" letter-spacing="6" filter="url(#softglow)"'))
    body.append(t(72, 140, "SHORTEST PATH TO DA // 5 HOPS", 14, MAG, .95, "start", 'letter-spacing="5"'))
    body.append(brackets(28, 70, CYAN))
    svg("attack-graph", "\n".join(body), bg="#04050b")


# ------------------------------------------------------------------ 10 minimal
def minimal():
    grad = ('<radialGradient id="mglow" cx="50%" cy="46%" r="55%"><stop offset="0" stop-color="#14123a"/>'
            '<stop offset="1" stop-color="#05060c"/></radialGradient>'
            '<pattern id="dots" width="32" height="32" patternUnits="userSpaceOnUse">'
            f'<circle cx="16" cy="16" r="1.2" fill="{DIM}"/></pattern>')
    cx, cy = W / 2, H / 2 - 30
    body = [f'<rect width="{W}" height="{H}" fill="url(#mglow)"/>',
            f'<rect width="{W}" height="{H}" fill="url(#dots)" opacity=".55"/>']
    # emblem: hex outline + double slash
    R = 120
    pts = " ".join(f"{cx + R * math.cos(math.radians(60 * k + 30)):.1f},{cy + R * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
    body.append(f'<polygon points="{pts}" fill="none" stroke="{CYAN}" stroke-width="3" filter="url(#glow)"/>')
    body.append(f'<path d="M{cx - 38},{cy + 52} L{cx - 4},{cy - 52} M{cx + 4},{cy + 52} L{cx + 38},{cy - 52}" '
                f'stroke="{MAG}" stroke-width="12" stroke-linecap="round" filter="url(#glow)"/>')
    body.append(t(cx, cy + R + 80, "ATTACKFRAME", 34, TEXT, .95, "middle", 'font-weight="300" letter-spacing="22"'))
    body.append(t(cx, cy + R + 115, "OPERATOR", 13, CYAN, .8, "middle", 'letter-spacing="14"'))
    body.append(f'<line x1="{cx - 160}" y1="{cy + R + 135}" x2="{cx + 160}" y2="{cy + R + 135}" stroke="{MAG}" stroke-width="1.5" opacity=".7"/>')
    body.append(brackets(40, 46, DIM, 1.5))
    svg("minimal", "\n".join(body), extra_defs=grad, scan=False)


WALLPAPERS = [
    ("neon-rain", "Neon Rain", neon_rain), ("circuit", "Circuit Core", circuit), ("hexhive", "Hex Hive", hexhive),
    ("glitch", "Glitch", glitch), ("rain-city", "Rain City", rain_city), ("terminal", "Terminal", terminal),
    ("radar", "Radar Lock", radar), ("wireframe-peaks", "Wireframe Peaks", wireframe_peaks),
    ("attack-graph", "Attack Graph", attack_graph), ("minimal", "Minimal Operator", minimal),
]

if __name__ == "__main__":
    for slug, title, fn in WALLPAPERS:
        fn()
    (OUT / "names.tsv").write_text("".join(f"af-{s}\t{n}\n" for s, n, _ in WALLPAPERS))
    print(f"wrote {len(WALLPAPERS)} wallpapers to {OUT}")
