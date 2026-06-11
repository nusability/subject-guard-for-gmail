#!/usr/bin/env bash
# Build the Gmail Subject Guard extension zip.
#
#   ./build.sh                 generate i18n.js + icons, then package dist zip
#   ./build.sh --screenshots   also regenerate the localized store screenshots
#
# The zip contains only what ships (everything under src/), with manifest.json
# at the archive root — ready to upload to the Chrome Web Store.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

DO_STORE=0
[ "${1:-}" = "--screenshots" ] && DO_STORE=1

echo "==> Generating src/i18n.js from tools/translations.json"
python3 tools/build_i18n.py

echo "==> Generating icons"
python3 tools/make_icons.py

echo "==> Generating localized store listing pages"
python3 tools/make_listings.py

if [ "$DO_STORE" = 1 ]; then
  echo "==> Generating localized store screenshots"
  python3 tools/make_screenshot.py
fi

# Catch syntax errors before shipping, if node is available.
if command -v node >/dev/null 2>&1; then
  echo "==> Syntax-checking scripts"
  node --check src/i18n.js
  node --check src/content.js
fi

VERSION="$(python3 -c "import json; print(json.load(open('src/manifest.json'))['version'])")"
NAME="gmail-subject-guard-v${VERSION}.zip"

mkdir -p dist
rm -f "dist/$NAME"
echo "==> Packaging dist/$NAME"
# Zip from inside src/ so paths are relative to the extension root.
( cd src && zip -r -X "../dist/$NAME" . -x '*/.DS_Store' '.*' >/dev/null )

echo "==> Done"
unzip -l "dist/$NAME"
