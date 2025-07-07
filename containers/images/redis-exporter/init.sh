#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the redis image
# Author: Radosław Kolba
# e-mail: radoslaw.kolba@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

REDIS_EXPORTER_GIT="https://github.com/oliver006/redis_exporter.git"
VERSION=$(git ls-remote --refs --tags $REDIS_EXPORTER_GIT | grep -o 'v.*' | sort --version-sort --reverse | head -1)

sed -i "s/REDIS_EXPORTER_VERSION=\"[^\"]*\"/REDIS_EXPORTER_VERSION=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/version=\"[^\"]*\"/version=\"${VERSION:1}\"/" Dockerfile || exit 1

echo "Finished setting up the Redis Exporter ${VERSION:1} image"

