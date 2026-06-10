#!/usr/bin/env bash
set -euo pipefail

SPATH=$(pwd)
APP_NAME="kyvernopre"

echo "-> Checking latest version of Kyverno"
VERSION_URL="https://api.github.com/repos/kyverno/kyverno/releases/latest"
# Fetch latest version and strip 'v' prefix
KYVERNO_VERSION=$(curl -sL ${VERSION_URL} | grep -o '"tag_name": "[^"]*' | cut -d'"' -f4 | sed 's/v//')

[[ ! $KYVERNO_VERSION =~ ^[0-9.]+$ ]] && exit 1

SRC_TAR="https://github.com/kyverno/kyverno/archive/refs/tags/v${KYVERNO_VERSION}.tar.gz"

echo "-> Downloading source v${KYVERNO_VERSION}"
curl -sL -o $APP_NAME.tar.gz $SRC_TAR
mkdir -p $APP_NAME && tar -xf "$APP_NAME.tar.gz" -C $APP_NAME --strip-components=1

pushd $APP_NAME
for item in go.mod go.sum cmd pkg api internal ext; do
  if [ -e "$item" ]; then
    cp -R "$item" "$SPATH/"
  fi
done
mkdir -p "$SPATH/internal" "$SPATH/ext"
popd

rm -rf $APP_NAME.tar.gz $APP_NAME

sed -i "s/version=\"[^\"]*\"/version=\"$KYVERNO_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$KYVERNO_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$KYVERNO_VERSION\"/" README.md || exit 1
