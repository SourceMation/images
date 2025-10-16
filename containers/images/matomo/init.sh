#!/bin/bash
set -euo pipefail
APP=matomo

echo "Checking the latest available version of the $APP"
API_URL="https://api.matomo.org/1.0/getLatestVersion/"
VERSION=$(curl -sL "${API_URL}")
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

rm -rf matomo matomo.zip *.html

echo "Download files for $APP version $VERSION"
curl https://builds.matomo.org/matomo-${VERSION}.zip -sLo matomo.zip

unzip -q matomo.zip

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/" Dockerfile