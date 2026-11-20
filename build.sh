#!/usr/bin/env bash
# AttackFrame OS — ISO build entry point.
# Runs the archiso build inside a privileged Arch Linux container, so it works
# from any Linux host that has Docker or Podman.
#
#   ./build.sh                 # core toolset (curated, ~6-8 GB ISO)
#   TOOLSET=categories ./build.sh   # core + whole BlackArch categories in BA_GROUPS
#   TOOLSET=full ./build.sh         # every BlackArch package (very large, expect conflicts)
#
# Output: ./out/attackframe-<date>-x86_64.iso
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLSET="${TOOLSET:-core}"
BA_GROUPS="${BA_GROUPS:-blackarch-recon blackarch-webapp blackarch-exploitation blackarch-cracker blackarch-wireless}"
# Prefer a Docker daemon we can actually talk to, else Podman (rootless is fine;
# if pacstrap's mounts are refused there, run this script with sudo).
if [[ -z "${ENGINE:-}" ]]; then
  if command -v docker >/dev/null && docker info >/dev/null 2>&1; then ENGINE=docker
  elif command -v podman >/dev/null; then ENGINE=podman
  else echo "docker or podman is required" >&2; exit 1; fi
fi

case "$TOOLSET" in core|categories|full) ;; *) echo "TOOLSET must be core|categories|full" >&2; exit 1;; esac

mkdir -p "$HERE/out" "$HERE/.cache/pacman"
echo ">> AttackFrame build  toolset=$TOOLSET  engine=$ENGINE"

exec "$ENGINE" run --rm --privileged \
  -v "$HERE":/af \
  -v "$HERE/.cache/pacman":/var/cache/pacman/pkg \
  -e TOOLSET="$TOOLSET" -e BA_GROUPS="$BA_GROUPS" -e STRAP_SHA1="${STRAP_SHA1:-}" \
  -e HOST_UID="${SUDO_UID:-$(id -u)}" -e HOST_GID="${SUDO_GID:-$(id -g)}" \
  docker.io/archlinux/archlinux:latest \
  bash /af/scripts/build-in-container.sh
