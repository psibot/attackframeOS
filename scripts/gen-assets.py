#!/usr/bin/env python3
"""Generate AttackFrame OS artwork as SVG: wallpaper, boot splash, app/category icons.
Original artwork — neon HUD / retro-grid style. Run: python3 scripts/gen-assets.py"""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
(OUT / "icons").mkdir(parents=True, exist_ok=True)

VOID, PANEL, CYAN, MAG, YEL, TEXT, DIM = "#05070d", "#0b0f1a", "#00f0ff", "#ff2bd6", "#f5ff3b", "#c8f7ff", "#3a4660"
FONT = "'JetBrainsMono Nerd Font','JetBrains Mono','DejaVu Sans Mono',monospace"
rnd = random.Random(0xAF)

GLOW = f"""
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="softglow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>"""


def grid(w, h, horizon, vx, color, n_h=18, spread=6.0, stroke=1.4):
    out = []
    for i in range(-int(n_h * 1.6), int(n_h * 1.6) + 1):  # verticals converging to (vx, horizon)
        x = vx + i * (w / n_h) * spread / 2
        op = max(0.12, 0.85 - abs(i) / (n_h * 1.6))
        out.append(f'<line x1="{vx}" y1="{horizon}" x2="{x:.1f}" y2="{h}" stroke="{color}" stroke-width="{stroke}" opacity="{op:.2f}"/>')
    k, y = 1, horizon
    while y < h:  # horizontals, spacing grows toward viewer
        y = horizon + (k ** 2) * 2.6
        op = min(0.9, 0.15 + k / 22)
        out.append(f'<line x1="0" y1="{y:.1f}" x2="{w}" y2="{y:.1f}" stroke="{color}" stroke-width="{stroke}" opacity="{op:.2f}"/>')
        k += 1
    return "\n".join(out)


def skyline(w, base, max_h, count):
    out, x = [], 0
    while x < w:
        bw = rnd.randint(18, 70)
        bh = rnd.randint(30, max_h) * (1.0 - 0.55 * (1 - abs(x - w / 2) / (w / 2)) ** 2.5)  # lower near the sun
        out.append(f'<rect x="{x}" y="{base - bh:.0f}" width="{bw}" height="{bh:.0f}" fill="{VOID}"/>')
        for _ in range(int(bh * bw / 900)):
            wx, wy = x + rnd.randint(3, max(4, bw - 5)), base - rnd.uniform(6, bh - 4)
            c = rnd.choice([CYAN, CYAN, MAG, YEL])
            out.append(f'<rect x="{wx}" y="{wy:.0f}" width="2" height="2" fill="{c}" opacity="{rnd.uniform(.35, .9):.2f}"/>')
        if bh > max_h * 0.75 and rnd.random() < 0.5:  # antenna beacons
            out.append(f'<rect x="{x + bw // 2}" y="{base - bh - 22:.0f}" width="1.5" height="22" fill="{VOID}"/>'
                       f'<circle cx="{x + bw // 2 + .75}" cy="{base - bh - 23:.0f}" r="2" fill="{MAG}" filter="url(#softglow)"/>')
        x += bw + rnd.randint(0, 6)
    return "\n".join(out)


def hex_column(x, y, rows, size=11):
    lines = []
    for r in range(rows):
        words = " ".join(f"{rnd.randint(0, 0xFFFF):04x}" for _ in range(4))
        op = 0.18 + 0.5 * rnd.random()
        lines.append(f'<text x="{x}" y="{y + r * (size + 6)}" font-size="{size}" fill="{CYAN}" opacity="{op:.2f}">{0x7f3a00 + r * 16:06x}  {words}</text>')
    return "\n".join(lines)


def brackets(w, h, m, L, color, sw=2):
    p = [f"M{m},{m + L} V{m} H{m + L}", f"M{w - m - L},{m} H{w - m} V{m + L}",
         f"M{m},{h - m - L} V{h - m} H{m + L}", f"M{w - m - L},{h - m} H{w - m} V{h - m - L}"]
    return "".join(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>' for d in p)


def wallpaper():
    W, H, HZ = 1920, 1080, 660
    sun_stripes = "".join(f'<rect x="0" y="{HZ - 140 + i * 24 + i * i * .9:.0f}" width="{W}" height="{3 + i * 1.6:.1f}" fill="black"/>' for i in range(9))
    title = "ATTACK//FRAME"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{GLOW}
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{VOID}"/><stop offset=".45" stop-color="#0a0718"/><stop offset=".61" stop-color="#2a0733"/><stop offset=".612" stop-color="{VOID}"/>
</linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{YEL}"/><stop offset=".55" stop-color="#ff7a59"/><stop offset="1" stop-color="{MAG}"/></linearGradient>
<radialGradient id="haze" cx=".5" cy=".61" r=".5"><stop offset="0" stop-color="{MAG}" stop-opacity=".35"/><stop offset="1" stop-color="{MAG}" stop-opacity="0"/></radialGradient>
<linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VOID}" stop-opacity="0"/><stop offset="1" stop-color="{VOID}" stop-opacity=".55"/></linearGradient>
<mask id="sunmask"><rect width="{W}" height="{H}" fill="white"/>{sun_stripes}</mask>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".35"/></pattern>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<rect width="{W}" height="{H}" fill="url(#haze)"/>
<circle cx="{W / 2}" cy="{HZ - 40}" r="230" fill="url(#sun)" mask="url(#sunmask)" opacity=".92"/>
{skyline(W, HZ, 230, 0)}
<rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="{VOID}"/>
<g filter="url(#softglow)">{grid(W, H, HZ, W / 2, MAG)}</g>
<rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floorfade)"/>
<line x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" stroke="{CYAN}" stroke-width="2.5" filter="url(#glow)"/>

<g font-family="{FONT}" font-weight="800" text-anchor="middle" font-size="128" letter-spacing="14">
  <text x="{W / 2 - 5}" y="300" fill="{CYAN}" opacity=".75">{title}</text>
  <text x="{W / 2 + 5}" y="304" fill="{MAG}" opacity=".75">{title}</text>
  <text x="{W / 2}" y="302" fill="{TEXT}" filter="url(#glow)">{title}</text>
  <rect x="{W / 2 - 520}" y="262" width="300" height="5" fill="{VOID}" opacity=".9"/>
  <rect x="{W / 2 + 180}" y="281" width="220" height="3" fill="{VOID}" opacity=".9"/>
</g>
<text x="{W / 2}" y="352" text-anchor="middle" font-family="{FONT}" font-size="21" letter-spacing="9" fill="{CYAN}" filter="url(#softglow)">OFFENSIVE OPERATIONS PLATFORM  //  BLACKARCH × KALI</text>

<g font-family="{FONT}">
{brackets(W, H, 46, 70, CYAN)}
<text x="70" y="88" font-size="14" fill="{CYAN}" letter-spacing="3">◢ NODE attackframe  //  SESSION 0x7F3A  //  LINK <tspan fill="{YEL}">SECURE</tspan></text>
<text x="70" y="110" font-size="12" fill="{DIM}" letter-spacing="2">uplink ▮▮▮▮▮▮▯▯  ·  operator: ghost  ·  clearance: ROOT</text>
{hex_column(W - 330, 96, 14)}
<g transform="translate(70,{H - 140})" font-size="13" letter-spacing="2">
  <text fill="{MAG}">[ SYS ]</text><text x="80" fill="{TEXT}" opacity=".85">arsenal online · blackarch repo linked · kali layer standby</text>
  <text y="22" fill="{MAG}">[ NET ]</text><text x="80" y="22" fill="{TEXT}" opacity=".85">lan ⇄ vpn ⇄ target routing armed</text>
  <text y="44" fill="{MAG}">[ OPS ]</text><text x="80" y="44" fill="{TEXT}" opacity=".85">authorized engagements only — know your scope</text>
</g>
<g transform="translate({W - 340},{H - 120})">{''.join(f'<rect x="{i * 7}" y="0" width="{rnd.choice([2, 3, 4])}" height="{rnd.choice([26, 34, 40])}" fill="{CYAN}" opacity=".55"/>' for i in range(38))}
<text x="0" y="62" font-size="11" fill="{DIM}" letter-spacing="3">AF-OS // ROLLING // x86_64</text></g>
</g>
<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".5"/>
</svg>"""


def splash():
    W, H, HZ = 640, 480, 300
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{GLOW}
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VOID}"/><stop offset=".62" stop-color="#22062b"/><stop offset=".625" stop-color="{VOID}"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<g opacity=".7">{grid(W, H, HZ, W / 2, MAG, n_h=14, spread=5, stroke=1)}</g>
<line x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" stroke="{CYAN}" stroke-width="1.5" filter="url(#glow)"/>
<g font-family="{FONT}" font-weight="800" text-anchor="middle" font-size="46" letter-spacing="5">
<text x="{W / 2 - 2}" y="120" fill="{CYAN}" opacity=".7">ATTACK//FRAME</text>
<text x="{W / 2 + 2}" y="122" fill="{MAG}" opacity=".7">ATTACK//FRAME</text>
<text x="{W / 2}" y="121" fill="{TEXT}">ATTACK//FRAME</text></g>
<text x="{W / 2}" y="150" text-anchor="middle" font-family="{FONT}" font-size="11" letter-spacing="4" fill="{CYAN}">OFFENSIVE OPERATIONS PLATFORM</text>
{brackets(W, H, 14, 26, CYAN, 1.5)}
</svg>"""


def icon(glyph, accent=MAG):
    pts = "64,8 112,36 112,92 64,120 16,92 16,36"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
<defs>{GLOW}</defs>
<polygon points="{pts}" fill="{PANEL}" stroke="{CYAN}" stroke-width="5" stroke-linejoin="round" filter="url(#softglow)"/>
<polygon points="64,20 102,42 102,86 64,108 26,86 26,42" fill="none" stroke="{CYAN}" stroke-width="1.2" opacity=".35"/>
<text x="64" y="78" text-anchor="middle" font-family="{FONT}" font-weight="800" font-size="34" fill="{accent}" filter="url(#softglow)">{glyph}</text>
<rect x="44" y="94" width="40" height="3" fill="{YEL}" opacity=".8"/>
</svg>"""


def logo():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
<defs>{GLOW}</defs>
<polygon points="64,6 114,35 114,93 64,122 14,93 14,35" fill="{VOID}" stroke="{CYAN}" stroke-width="5" stroke-linejoin="round" filter="url(#softglow)"/>
<g stroke-linecap="square" filter="url(#glow)">
<line x1="40" y1="92" x2="62" y2="36" stroke="{MAG}" stroke-width="10"/>
<line x1="66" y1="92" x2="88" y2="36" stroke="{CYAN}" stroke-width="10"/></g>
<rect x="34" y="100" width="60" height="3" fill="{YEL}"/>
</svg>"""


def gdm_logo():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 80" width="480" height="80">
<defs>{GLOW}</defs>
<g font-family="{FONT}" font-weight="800" text-anchor="middle" font-size="48" letter-spacing="5">
<text x="238" y="52" fill="{CYAN}" opacity=".75">ATTACK//FRAME</text>
<text x="242" y="54" fill="{MAG}" opacity=".75">ATTACK//FRAME</text>
<text x="240" y="53" fill="{TEXT}" filter="url(#softglow)">ATTACK//FRAME</text></g>
<text x="240" y="74" text-anchor="middle" font-family="{FONT}" font-size="10" letter-spacing="5" fill="{CYAN}">OFFENSIVE OPERATIONS PLATFORM</text>
</svg>"""


(OUT / "gdm-logo.svg").write_text(gdm_logo())
(OUT / "wallpaper.svg").write_text(wallpaper())
(OUT / "splash.svg").write_text(splash())
(OUT / "icons" / "attackframe.svg").write_text(logo())
CATS = {"recon": ("RC", MAG), "web": ("WB", CYAN), "exploit": ("EX", MAG), "crack": ("CR", YEL),
        "wireless": ("WF", CYAN), "sniff": ("SN", MAG), "ad": ("AD", YEL), "reverse": ("RE", CYAN),
        "forensics": ("FR", MAG), "pivot": ("PV", YEL)}
for cat, (g, accent) in CATS.items():
    (OUT / "icons" / f"attackframe-{cat}.svg").write_text(icon(g, accent))
print(f"assets written to {OUT}")
