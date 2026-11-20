#!/usr/bin/env bash
# Render assets/wallpapers/*.svg to 3840x2160 PNGs inside an Arch container
# (needs librsvg + JetBrains Mono Nerd font, which the host may not have).
set -euo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
python3 "$HERE/scripts/gen-wallpapers.py"
python3 "$HERE/scripts/gen-wallpapers2.py"
python3 "$HERE/scripts/gen-wallpapers3.py"
python3 "$HERE/scripts/gen-icon-themes.py"
mkdir -p "$HERE/.cache/pacman-user"
podman run --rm -v "$HERE:/af:Z" -v "$HERE/.cache/pacman-user:/var/cache/pacman/pkg:Z" \
  docker.io/archlinux/archlinux bash -c '
    pacman -Sy --noconfirm --needed librsvg ttf-jetbrains-mono-nerd >/dev/null
    mkdir -p /af/assets/wallpapers/png
    for f in /af/assets/wallpapers/af-*.svg; do
      n=$(basename "$f" .svg); echo "render $n"
      rsvg-convert -w 3840 -h 2160 "$f" -o "/af/assets/wallpapers/png/$n.png"
    done
    for f in /af/assets/icon-themes/preview-*.svg; do rsvg-convert "$f" -o "${f%.svg}.png"; done'
echo "PNGs in $HERE/assets/wallpapers/png"
