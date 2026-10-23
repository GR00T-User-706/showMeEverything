#!/data/data/com.termux/files/usr/bin/bash
# SME_SIGNATURE=gr00t-user-706
# Build and reinstall the showMeEverything Termux package from this checkout.
set -Eeuo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log()  { printf '%b[INFO]%b %s\n' "$BLUE" "$NC" "$*"; }
ok()   { printf '%b[ OK ]%b %s\n' "$GREEN" "$NC" "$*"; }
die()  { printf '%b[FAIL]%b %s\n' "$RED" "$NC" "$*" >&2; exit 1; }

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
MANIFEST="$SCRIPT_DIR/showmeeverything-termux.yaml"

# Build and validate first. A failed build must not remove the working install.
[[ -n "${PREFIX:-}" && -d "$PREFIX" ]] || die 'Termux was not detected (PREFIX is unset or invalid).'
[[ -f "$MANIFEST" && -r "$MANIFEST" ]] || die "Termux package manifest is missing or unreadable: $MANIFEST"
command -v termux-create-package >/dev/null 2>&1 || die 'termux-create-package is not installed.'
command -v apt >/dev/null 2>&1 || die 'apt was not found; this script is for Termux.'
command -v dpkg-deb >/dev/null 2>&1 || die 'dpkg-deb is required to validate the built package.'

# Read package metadata from the YAML control block without requiring yq.
PACKAGE="$(awk '/^control:[[:space:]]*$/ { in_control=1; next } in_control && /^[^[:space:]]/ { exit } in_control && /^[[:space:]]+Package:[[:space:]]*/ { sub(/^[[:space:]]+Package:[[:space:]]*/, ""); print; exit }' "$MANIFEST")"
VERSION="$(awk '/^control:[[:space:]]*$/ { in_control=1; next } in_control && /^[^[:space:]]/ { exit } in_control && /^[[:space:]]+Version:[[:space:]]*/ { sub(/^[[:space:]]+Version:[[:space:]]*/, ""); print; exit }' "$MANIFEST")"
ARCH="$(awk '/^control:[[:space:]]*$/ { in_control=1; next } in_control && /^[^[:space:]]/ { exit } in_control && /^[[:space:]]+Architecture:[[:space:]]*/ { sub(/^[[:space:]]+Architecture:[[:space:]]*/, ""); print; exit }' "$MANIFEST")"

[[ -n "$PACKAGE" && -n "$VERSION" && -n "$ARCH" ]] || die 'Could not read Package, Version, and Architecture from the YAML control block.'

DEB_NAME="${PACKAGE}_${VERSION}_${ARCH}.deb"
DEB_PATH="$SCRIPT_DIR/$DEB_NAME"

printf '\n%bshowMeEverything Termux Package Updater%b\n' "$GREEN" "$NC"
printf 'Repository: %s\nManifest:   %s\nPackage:    %s\nVersion:    %s\n\n' "$SCRIPT_DIR" "$MANIFEST" "$PACKAGE" "$VERSION"

log 'Building the package from the YAML manifest...'
cd "$SCRIPT_DIR"
termux-create-package "$MANIFEST"
[[ -s "$DEB_PATH" ]] || die "Build completed, but expected package was not created: $DEB_PATH"

BUILT_PACKAGE="$(dpkg-deb -f "$DEB_PATH" Package 2>/dev/null)" || die 'The generated .deb is invalid or unreadable.'
BUILT_VERSION="$(dpkg-deb -f "$DEB_PATH" Version 2>/dev/null)" || die 'Could not read the generated package version.'
BUILT_ARCH="$(dpkg-deb -f "$DEB_PATH" Architecture 2>/dev/null)" || die 'Could not read the generated package architecture.'
[[ "$BUILT_PACKAGE" == "$PACKAGE" ]] || die "Package identity mismatch: expected '$PACKAGE', got '$BUILT_PACKAGE'."
[[ "$BUILT_VERSION" == "$VERSION" ]] || die "Package version mismatch: expected '$VERSION', got '$BUILT_VERSION'."
[[ "$BUILT_ARCH" == "$ARCH" ]] || die "Package architecture mismatch: expected '$ARCH', got '$BUILT_ARCH'."
ok "Built and validated $DEB_NAME"

if dpkg-query -W -f='${Status}' "$PACKAGE" 2>/dev/null | grep -q '^install ok installed$'; then
    log "Removing installed package $PACKAGE..."
    apt remove -y "$PACKAGE"
    ok 'Previous package removed.'
else
    log "Package $PACKAGE is not currently installed; skipping removal."
fi

log "Installing $DEB_NAME..."
apt install -y "./$DEB_NAME"

log 'Verifying installed package version...'
INSTALLED_VERSION="$(dpkg-query -W -f='${Version}' "$PACKAGE" 2>/dev/null)" || die 'Package installation did not leave an installed package record.'
[[ "$INSTALLED_VERSION" == "$VERSION" ]] || die "Installed version mismatch: expected '$VERSION', got '$INSTALLED_VERSION'."
command -v smecli >/dev/null 2>&1 || die 'Package installed, but the smecli command is not on PATH.'
smecli --help >/dev/null 2>&1 || die 'Package installed, but the smecli help check failed.'

printf '\n%bUpdate complete.%b\n' "$GREEN" "$NC"
printf 'Package: %s\nVersion: %s\nCommand: %s\nArtifact: %s\n' "$PACKAGE" "$INSTALLED_VERSION" "$(command -v smecli)" "$DEB_PATH"
