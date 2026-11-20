#!/usr/bin/env bash
# Runs inside the archlinux container started by build.sh.
set -euo pipefail

AF=/af
WORK=/tmp/af
PROFILE=$WORK/profile
log() { printf '\e[1;36m[AF]\e[0m %s\n' "$*"; }
warn() { printf '\e[1;35m[AF:warn]\e[0m %s\n' "$*"; }

# ---------------------------------------------------------------- toolchain
log "Installing build toolchain"
sed -i 's/^#ParallelDownloads.*/ParallelDownloads = 8/' /etc/pacman.conf
pacman -Syu --noconfirm --needed archiso librsvg ttf-jetbrains-mono-nerd noto-fonts curl

# ---------------------------------------------------------------- BlackArch
log "Bootstrapping the BlackArch repository (strap.sh)"
curl -fsSL -o /tmp/strap.sh https://blackarch.org/strap.sh
sum=$(sha1sum /tmp/strap.sh | cut -d' ' -f1)
log "strap.sh sha1: $sum  (compare with https://blackarch.org/downloads.html)"
if [[ -n "${STRAP_SHA1:-}" && "$sum" != "$STRAP_SHA1" ]]; then
  echo "strap.sh checksum mismatch (expected $STRAP_SHA1)" >&2; exit 1
fi
bash /tmp/strap.sh
pacman -Sy --noconfirm

# ---------------------------------------------------------------- profile
log "Assembling archiso profile from releng + AttackFrame overlay"
rm -rf "$WORK"; mkdir -p "$WORK"
cp -r /usr/share/archiso/configs/releng "$PROFILE"
cp -rT "$AF/profile/airootfs" "$PROFILE/airootfs"

# pacman.conf used by pacstrap: add BlackArch after the official repos
cat >> "$PROFILE/pacman.conf" <<'EOF'

[blackarch]
Include = /etc/pacman.d/blackarch-mirrorlist
EOF
# ...and the same config on the live system, so `pacman -S <tool>` works there too
# (the pacman package then installs its stock file as pacman.conf.pacnew)
install -Dm644 "$PROFILE/pacman.conf" "$PROFILE/airootfs/etc/pacman.conf"

# Some packages (certipy, cewl, evil-winrm, whatweb, ...) fetch gems / pip build
# deps in their install scriptlets. releng's resolv.conf is a symlink into
# systemd-resolved, which isn't running inside pacstrap's chroot, so give the
# build a real file; attackframe-firstboot restores the symlink on the live system.
rm -f "$PROFILE/airootfs/etc/resolv.conf"
cp -L /etc/resolv.conf "$PROFILE/airootfs/etc/resolv.conf"

# GNOME uses NetworkManager — drop releng's iwd / networkd units
wants=$PROFILE/airootfs/etc/systemd/system
rm -f "$wants"/multi-user.target.wants/{iwd,systemd-networkd}.service \
      "$wants"/sockets.target.wants/systemd-networkd.socket \
      "$wants"/network-online.target.wants/systemd-networkd-wait-online.service \
      "$wants"/systemd-networkd-wait-online.service.wants/* 2>/dev/null || true
mkdir -p "$wants"/multi-user.target.wants "$wants"/graphical.target.wants
ln -sf /usr/lib/systemd/system/gdm.service "$wants"/display-manager.service
ln -sf /usr/lib/systemd/system/NetworkManager.service "$wants"/multi-user.target.wants/NetworkManager.service
ln -sf /etc/systemd/system/attackframe-firstboot.service "$wants"/multi-user.target.wants/attackframe-firstboot.service
mkdir -p "$wants"/sysinit.target.wants
ln -sf /etc/systemd/system/attackframe-resolv.service "$wants"/sysinit.target.wants/attackframe-resolv.service
ln -sf /usr/lib/systemd/system/graphical.target "$wants"/default.target

# ---------------------------------------------------------------- packages
log "Resolving package list (toolset=$TOOLSET)"
want=$(mktemp)
cat "$PROFILE/packages.x86_64" "$AF/packages/desktop.txt" "$AF/packages/tools-core.txt" > "$want"
case "$TOOLSET" in
  categories) tr ' ' '\n' <<<"$BA_GROUPS" >> "$want" ;;
  full)       echo blackarch >> "$want"; warn "TOOLSET=full: expect a 30-60 GB build and package conflicts" ;;
esac
# Names that no longer exist in any repo are skipped instead of failing the build.
# iwd is replaced by NetworkManager in the live desktop.
final=$(mktemp); found=(); missing=()
while read -r p; do
  p=${p%%#*}; p=${p//[[:space:]]/}
  [[ -z "$p" || "$p" == iwd ]] && continue
  if pacman -Si "$p" &>/dev/null || pacman -Sg "$p" &>/dev/null; then found+=("$p"); else missing+=("$p"); fi
done < "$want"
printf '%s\n' "${found[@]}" | sort -u > "$final"
if ((${#missing[@]})); then warn "Not in any repo, skipped: ${missing[*]}"; fi
cp "$final" "$PROFILE/packages.x86_64"
cp "$final" "$PROFILE/airootfs/usr/share/attackframe/packages.txt"
log "$(wc -l < "$final") packages/groups selected"

# ---------------------------------------------------------------- branding
log "Branding profile + rendering artwork"
# shellcheck disable=SC2016  # $(date ...) must stay literal: profiledef.sh evaluates it
sed -i \
  -e 's/^iso_name=.*/iso_name="attackframe"/' \
  -e 's/^iso_label=.*/iso_label="ATTACKFRAME_$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y%m)"/' \
  -e 's/^iso_publisher=.*/iso_publisher="AttackFrame OS"/' \
  -e 's/^iso_application=.*/iso_application="AttackFrame OS live\/install medium"/' \
  "$PROFILE/profiledef.sh"
{
  echo 'file_permissions+=('
  for f in "$PROFILE"/airootfs/usr/local/bin/*; do echo "  [\"/usr/local/bin/$(basename "$f")\"]=\"0:0:755\""; done
  echo ')'
} >> "$PROFILE/profiledef.sh"

# boot menus: name + larger copy-on-write space so tools can be installed live
for f in "$PROFILE"/syslinux/*.cfg "$PROFILE"/efiboot/loader/entries/*.conf "$PROFILE"/grub/*.cfg; do
  [[ -f "$f" ]] || continue
  sed -i -e 's/Arch Linux install medium/AttackFrame OS live/g' -e 's/Arch Linux/AttackFrame OS/g' \
         -e 's/archisobasedir=%INSTALL_DIR%/& cow_spacesize=4G/' "$f"
done

echo attackframe > "$PROFILE/airootfs/etc/hostname"
install -Dm644 "$AF/assets/gdm-logo.svg" "$PROFILE/airootfs/usr/share/attackframe/gdm-logo.svg"
rsvg-convert -w 3840 -h 2160 "$AF/assets/wallpaper.svg" \
  -o "$PROFILE/airootfs/usr/share/backgrounds/attackframe/attackframe-grid.png"
# wallpaper pack (scripts/gen-wallpapers.py) + GNOME Settings → Appearance entries
bgdir=$PROFILE/airootfs/usr/share/backgrounds/attackframe
xml=$PROFILE/airootfs/usr/share/gnome-background-properties/attackframe.xml
wp() { printf '  <wallpaper deleted="false"><name>%s</name><filename>%s</filename><filename-dark>%s</filename-dark><options>zoom</options><shade_type>solid</shade_type><pcolor>#05070d</pcolor><scolor>#05070d</scolor></wallpaper>\n' "$1" "$2" "$2"; }
{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">'
  echo '<wallpapers>'
  wp "AttackFrame Grid" /usr/share/backgrounds/attackframe/attackframe-grid.png
  while IFS=$'\t' read -r slug name; do
    rsvg-convert -w 3840 -h 2160 "$AF/assets/wallpapers/$slug.svg" -o "$bgdir/$slug.png"
    wp "AttackFrame $name" "/usr/share/backgrounds/attackframe/$slug.png"
  done < "$AF/assets/wallpapers/names.tsv"
  echo '</wallpapers>'
} > "$xml"
rsvg-convert -w 640 -h 480 "$AF/assets/splash.svg" -o "$PROFILE/syslinux/splash.png"
cp "$AF"/assets/icons/*.svg "$PROFILE/airootfs/usr/share/icons/hicolor/scalable/apps/"
cp -r "$AF"/assets/icon-themes/AttackFrame-* "$PROFILE/airootfs/usr/share/icons/"

# ---------------------------------------------------------------- build
log "Running mkarchiso (this takes a while)"
mkarchiso -v -w "$WORK/build" -o "$AF/out" "$PROFILE"
chown -R "${HOST_UID:-0}:${HOST_GID:-0}" "$AF/out" "$AF/.cache" || true
# sanity checks on the finished root filesystem
root=$WORK/build/x86_64/airootfs
[[ -s $root/etc/ca-certificates/extracted/tls-ca-bundle.pem ]] \
  || { warn "CA trust store is EMPTY — HTTPS/pacman/Firefox will fail"; exit 1; }
if ! { [[ -s $root/etc/pacman.d/blackarch-mirrorlist ]] && grep -q '^\[blackarch\]' "$root/etc/pacman.conf"; }; then
  warn "BlackArch repo is not configured on the live system"; exit 1
fi
log "Checks passed: CA store has $(grep -c 'BEGIN CERT' "$root/etc/ca-certificates/extracted/tls-ca-bundle.pem") certs, BlackArch repo configured"
log "Done: $(ls "$AF"/out/*.iso)"
