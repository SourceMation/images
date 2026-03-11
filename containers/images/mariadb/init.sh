#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-09
# -----------------------------------

set -euo pipefail

echo "-> Preparing mariadb variables"
APP="mariadb"
VERSION=$(curl -s https://api.github.com/repos/MariaDB/server/releases/latest | grep '"tag_name":' | sed -E 's/.*"mariadb-([0-9.]+)".*/\1/')
MAJOR_MINOR=$(echo "$VERSION" | cut -d. -f1,2)

# Exit if the version variable contains anything other than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

echo "Updating Dockerfile with version $VERSION and repo $MAJOR_MINOR"
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$VERSION\"/" README.md || exit 1
sed -i "s#blob/[0-9.]*/COPYING#blob/$MAJOR_MINOR/COPYING#" README.md || exit 1
sed -i "s#https://deb.mariadb.org/[0-9.]*/debian#https://deb.mariadb.org/$MAJOR_MINOR/debian#" Dockerfile || exit 1
