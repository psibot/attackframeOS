#!/usr/bin/env python3
"""Generate two AttackFrame icon themes (scalable SVG, inherit Papirus-Dark for everything not drawn here).

  AttackFrame-Neon   dark tiles / folders with glowing cyan-magenta glyphs
  AttackFrame-Ghost  minimal monochrome outline glyphs, hex-shaped app badges

Run: python3 scripts/gen-icon-themes.py  ->  assets/icon-themes/<Theme>/
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "assets" / "icon-themes"
VOID, PANEL, CYAN, MAG, YEL, TEXT, DIM, TEAL, VIOLET = ("#05070d", "#0b0f1a", "#00f0ff", "#ff2bd6", "#f5ff3b",
                                                        "#c8f7ff", "#3a4660", "#00ffb3", "#7a2bff")
FONT = "'JetBrainsMono Nerd Font','JetBrains Mono','DejaVu Sans Mono',monospace"

# ---------------------------------------------------------------- glyphs (drawn in a 24x24 box)
G = {
    "home": "M4,12 L12,5 L20,12 M6.5,10 V19 H17.5 V10 M10,19 V14 H14 V19",
    "desktop": "M4,6 H20 V16 H4 Z M9,20 H15 M12,16 V20",
    "documents": "M7,4 H14 L18,8 V20 H7 Z M14,4 V8 H18 M9.5,12 H15.5 M9.5,15 H15.5 M9.5,18 H13",
    "download": "M12,4 V15 M7.5,10.5 L12,15 L16.5,10.5 M5,19 H19",
    "music": "M9,17 V6 L19,4 V15 M9,17 A2.5,2.5 0 1 1 8.99,17 M19,15 A2.5,2.5 0 1 1 18.99,15",
    "pictures": "M4,6 H20 V18 H4 Z M4,15 L9,10.5 L13,14 L15.5,12 L20,16 M15.5,9 A1.4,1.4 0 1 1 15.49,9",
    "videos": "M4,6 H16 V18 H4 Z M16,10 L20,8 V16 L16,14",
    "templates": "M5,5 H11 V11 H5 Z M13,5 H19 V11 H13 Z M5,13 H11 V19 H5 Z M13,13 H19 V19 H13 Z",
    "public": "M8,10 A2.5,2.5 0 1 1 7.99,10 M16,10 A2.5,2.5 0 1 1 15.99,10 M3.5,19 C4,15 12,15 12.5,19 M11.5,19 C12,15 20,15 20.5,19",
    "remote": "M12,4 A8,8 0 1 1 11.99,4 M4,12 H20 M12,4 C8,8 8,16 12,20 M12,4 C16,8 16,16 12,20",
    "network": "M10,4 H14 V8 H10 Z M4,16 H8 V20 H4 Z M16,16 H20 V20 H16 Z M12,8 V12 M6,16 V12 H18 V16",
    "trash": "M5,7 H19 M9,7 V4.5 H15 V7 M7,7 L8,20 H16 L17,7 M10.5,10.5 V16.5 M13.5,10.5 V16.5",
    "trash-full": "M5,7 H19 M9,7 V4.5 H15 V7 M7,7 L8,20 H16 L17,7 M9.5,11 L14.5,16 M14.5,11 L9.5,16",
    "disk": "M4,13 L6.5,6 H17.5 L20,13 V18 H4 Z M4,13 H20 M16.5,15.5 H17.5",
    "usb": "M9,3 H15 V8 H9 Z M7,8 H17 V18 A3,3 0 0 1 14,21 H10 A3,3 0 0 1 7,18 Z M11,5 V6 M13,5 V6",
    "terminal": "M3.5,5 H20.5 V19 H3.5 Z M7,9.5 L10,12 L7,14.5 M12,15 H17",
    "files": "M3.5,7 V18.5 H20.5 V8.5 H11.5 L9.5,6 H3.5 Z M3.5,10.5 H20.5",
    "settings": "M12,8.8 A3.2,3.2 0 1 1 11.99,8.8 M12,3 V5.5 M12,18.5 V21 M3,12 H5.5 M18.5,12 H21 M5.6,5.6 L7.4,7.4 M16.6,16.6 L18.4,18.4 M5.6,18.4 L7.4,16.6 M16.6,7.4 L18.4,5.6",
    "editor": "M5,19 L6,15 L15.5,5.5 L18.5,8.5 L9,18 Z M13.5,7.5 L16.5,10.5 M5,21 H19",
    "browser": "M12,3.5 A8.5,8.5 0 1 1 11.99,3.5 M3.5,12 H20.5 M12,3.5 C8,8 8,16 12,20.5 M12,3.5 C16,8 16,16 12,20.5",
    "monitor": "M3.5,5 H20.5 V17 H3.5 Z M5.5,13 L9,13 L10.5,9 L13,15 L14.5,11 L18.5,11 M9,20.5 H15",
    "calculator": "M6,3.5 H18 V20.5 H6 Z M8.5,6 H15.5 V9 H8.5 Z M9,12.5 H10 M14,12.5 H15 M9,15.5 H10 M14,15.5 H15 M9,18.5 H10 M14,18.5 H15",
    "lock": "M6,11 H18 V20 H6 Z M8.5,11 V8 A3.5,3.5 0 0 1 15.5,8 V11 M12,14.5 V16.5",
    "archive": "M4,5 H20 V9 H4 Z M5.5,9 V19 H18.5 V9 M10,12.5 H14",
}

# icon name -> (context, glyph, accent)
PLACES = {
    "folder": ("folder", None, CYAN), "folder-open": ("folder", None, CYAN),
    "user-home": ("folder", "home", MAG), "folder-home": ("folder", "home", MAG),
    "user-desktop": ("folder", "desktop", CYAN), "folder-desktop": ("folder", "desktop", CYAN),
    "folder-documents": ("folder", "documents", CYAN), "folder-download": ("folder", "download", TEAL),
    "folder-music": ("folder", "music", MAG), "folder-pictures": ("folder", "pictures", YEL),
    "folder-videos": ("folder", "videos", MAG), "folder-templates": ("folder", "templates", CYAN),
    "folder-publicshare": ("folder", "public", TEAL), "folder-remote": ("folder", "remote", VIOLET),
    "network-workgroup": ("tile", "network", CYAN), "user-trash": ("tile", "trash", CYAN),
    "user-trash-full": ("tile", "trash-full", MAG), "drive-harddisk": ("tile", "disk", CYAN),
    "media-removable": ("tile", "usb", YEL),
}
APPS = {
    "utilities-terminal": ("terminal", CYAN), "org.gnome.Terminal": ("terminal", CYAN), "org.gnome.Console": ("terminal", CYAN),
    "system-file-manager": ("files", MAG), "org.gnome.Nautilus": ("files", MAG),
    "preferences-system": ("settings", CYAN), "org.gnome.Settings": ("settings", CYAN),
    "accessories-text-editor": ("editor", YEL), "org.gnome.TextEditor": ("editor", YEL),
    "web-browser": ("browser", TEAL), "org.gnome.SystemMonitor": ("monitor", MAG),
    "utilities-system-monitor": ("monitor", MAG), "accessories-calculator": ("calculator", CYAN),
    "org.gnome.Calculator": ("calculator", CYAN), "system-lock-screen": ("lock", MAG),
    "org.gnome.FileRoller": ("archive", YEL), "package-x-generic": ("archive", YEL),
}
CATS = {"recon": ("RC", MAG), "web": ("WB", CYAN), "exploit": ("EX", MAG), "crack": ("CR", YEL), "wireless": ("WL", CYAN),
        "sniff": ("SN", MAG), "ad": ("AD", CYAN), "reverse": ("RE", YEL), "forensics": ("FR", CYAN), "pivot": ("PV", MAG)}

GLOW = ('<filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.6" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
FOLDER = "M6,16 Q6,12 10,12 H25 L30,18 H54 Q58,18 58,22 V50 Q58,54 54,54 H10 Q6,54 6,50 Z"
FOLDER_TAB = "M6,22 H58"
HEX = " ".join(f"{32 + 27 * c:.2f},{32 + 27 * s:.2f}" for c, s in
               [(0.866, -0.5), (0.866, 0.5), (0, 1), (-0.866, 0.5), (-0.866, -0.5), (0, -1)])


def glyph(name, x, y, size, color, width, glow=False):
    if not name:
        return ""
    s = size / 24
    return (f'<g transform="translate({x},{y}) scale({s:.3f})"{" filter=\"url(#g)\"" if glow else ""}>'
            f'<path d="{G[name]}" fill="none" stroke="{color}" stroke-width="{width / s:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/></g>')


def wrap(inner, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"><defs>{GLOW}{defs}</defs>{inner}</svg>\n'


# ---------------------------------------------------------------- theme 1: Neon
def neon_place(kind, g, accent):
    if kind == "folder":
        return wrap(f'<path d="{FOLDER}" fill="{PANEL}" stroke="{accent}" stroke-width="2.6" filter="url(#g)"/>'
                    f'<path d="{FOLDER_TAB}" stroke="{accent}" stroke-width="1.2" opacity=".55"/>'
                    f'<rect x="10" y="49" width="14" height="2" rx="1" fill="{MAG if accent != MAG else CYAN}"/>'
                    + glyph(g, 21, 26, 22, TEXT, 2.2, True))
    return neon_tile(g, accent)


def neon_tile(g, accent):
    return wrap(f'<rect x="5" y="5" width="54" height="54" rx="13" fill="{PANEL}" stroke="{accent}" stroke-width="2.6" filter="url(#g)"/>'
                f'<path d="M10,10 h8 M10,10 v8" stroke="{MAG if accent != MAG else CYAN}" stroke-width="2" stroke-linecap="round"/>'
                + glyph(g, 16, 16, 32, accent, 2.6, True))


def neon_cat(code, accent):
    return wrap(f'<polygon points="{HEX}" fill="{PANEL}" stroke="{accent}" stroke-width="3" filter="url(#g)"/>'
                f'<text x="32" y="38.5" font-family="{FONT}" font-size="17" font-weight="800" fill="{accent}" '
                f'text-anchor="middle" filter="url(#g)">{code}</text>'
                f'<rect x="24" y="43" width="16" height="2" fill="{YEL}"/>')


# ---------------------------------------------------------------- theme 2: Ghost
def ghost_place(kind, g, accent):
    if kind == "folder":
        return wrap(f'<path d="{FOLDER}" fill="{TEXT}" fill-opacity=".06" stroke="{TEXT}" stroke-width="2.2"/>'
                    f'<path d="{FOLDER_TAB}" stroke="{TEXT}" stroke-width="1" opacity=".35"/>'
                    f'<circle cx="51" cy="47" r="3" fill="{accent}"/>'
                    + glyph(g, 21, 27, 22, TEXT, 2))
    return ghost_tile(g, accent)


def ghost_tile(g, accent):
    return wrap(f'<polygon points="{HEX}" fill="{TEXT}" fill-opacity=".05" stroke="{TEXT}" stroke-width="2" opacity=".9"/>'
                f'<circle cx="32" cy="7.5" r="2.6" fill="{accent}"/>'
                + glyph(g, 18, 18, 28, TEXT, 2.2))


def ghost_cat(code, accent):
    return wrap(f'<polygon points="{HEX}" fill="none" stroke="{TEXT}" stroke-width="2"/>'
                f'<text x="32" y="38" font-family="{FONT}" font-size="16" font-weight="400" fill="{TEXT}" '
                f'text-anchor="middle" letter-spacing="1">{code}</text>'
                f'<circle cx="32" cy="46" r="2.4" fill="{accent}"/>')


def logo(style):
    if style == "neon":
        return wrap(f'<polygon points="{HEX}" fill="{PANEL}" stroke="{CYAN}" stroke-width="3" filter="url(#g)"/>'
                    f'<path d="M23,44 L30,20 M34,44 L41,20" stroke="{MAG}" stroke-width="5" stroke-linecap="round" filter="url(#g)"/>')
    return wrap(f'<polygon points="{HEX}" fill="none" stroke="{TEXT}" stroke-width="2"/>'
                f'<path d="M23,44 L30,20 M34,44 L41,20" stroke="{TEXT}" stroke-width="3" stroke-linecap="round"/>'
                f'<circle cx="32" cy="7.5" r="2.6" fill="{MAG}"/>')


THEMES = {
    "AttackFrame-Neon": ("AttackFrame Neon", "Dark tiles with glowing cyan and magenta glyphs", neon_place, neon_tile, neon_cat, "neon"),
    "AttackFrame-Ghost": ("AttackFrame Ghost", "Minimal monochrome outline icons with neon accent dots", ghost_place, ghost_tile, ghost_cat, "ghost"),
}

INDEX = """[Icon Theme]
Name={name}
Comment={comment}
Inherits=Papirus-Dark,Adwaita,hicolor
Example=folder
Directories=scalable/places,scalable/apps

[scalable/places]
Size=64
MinSize=16
MaxSize=512
Type=Scalable
Context=Places

[scalable/apps]
Size=64
MinSize=16
MaxSize=512
Type=Scalable
Context=Applications
"""


def build():
    previews = {}
    for slug, (name, comment, place, tile, cat, style) in THEMES.items():
        base = ROOT / slug
        (base / "scalable/places").mkdir(parents=True, exist_ok=True)
        (base / "scalable/apps").mkdir(parents=True, exist_ok=True)
        (base / "index.theme").write_text(INDEX.format(name=name, comment=comment))
        icons = {}
        for icon, (kind, g, accent) in PLACES.items():
            icons[f"places/{icon}"] = place(kind, g, accent)
        for icon, (g, accent) in APPS.items():
            icons[f"apps/{icon}"] = tile(g, accent)
        for cat_, (code, accent) in CATS.items():
            icons[f"apps/attackframe-{cat_}"] = cat(code, accent)
        icons["apps/attackframe"] = icons["apps/attackframe-arsenal"] = logo(style)
        for rel, data in icons.items():
            (base / "scalable" / f"{rel}.svg").write_text(data)
        previews[slug] = icons
    return previews


def preview(previews):
    """One preview SVG per theme: a grid of unique icons on a dark card."""
    for slug, icons in previews.items():
        seen, uniq = set(), []
        for rel, data in icons.items():
            if data not in seen:
                seen.add(data); uniq.append((rel.split("/")[1], data))
        cols, cell = 8, 150
        rows = (len(uniq) + cols - 1) // cols
        w, h = cols * cell + 40, rows * cell + 110
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
                 f'<rect width="{w}" height="{h}" fill="{VOID}"/>',
                 f'<text x="24" y="52" font-family="{FONT}" font-size="28" font-weight="800" fill="{TEXT}" letter-spacing="4">'
                 f'{THEMES[slug][0].upper()}</text>']
        for i, (name, data) in enumerate(uniq):
            x, y = 20 + (i % cols) * cell, 80 + (i // cols) * cell
            inner = data.split(">", 1)[1].rsplit("</svg>", 1)[0].replace('id="g"', f'id="g{i}"').replace("url(#g)", f"url(#g{i})")
            parts.append(f'<svg x="{x + 35}" y="{y}" width="80" height="80" viewBox="0 0 64 64">{inner}</svg>')
            label = name.replace("org.gnome.", "").replace("attackframe-", "af-")[:18]
            parts.append(f'<text x="{x + 75}" y="{y + 105}" font-family="{FONT}" font-size="12" fill="{DIM}" text-anchor="middle">{label}</text>')
        parts.append("</svg>")
        (ROOT / f"preview-{slug}.svg").write_text("\n".join(parts))


if __name__ == "__main__":
    pv = build()
    preview(pv)
    print("icon themes:", ", ".join(f"{k} ({len(v)} icons)" for k, v in pv.items()))
