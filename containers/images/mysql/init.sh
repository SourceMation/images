#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-12
# -----------------------------------

set -eu

echo "-> Preparing mysql variables"
APP="mysql"
VERSION=$(curl -s https://repo.mysql.com/apt/debian/dists/trixie/mysql-8.4-lts/binary-amd64/Packages.gz \
    |   gunzip \
    |   grep -A2 'Package: mysql-server' \
    |   grep Version \
    |   sed -E 's/Version: ([0-9]+\.[0-9]+\.[0-9]+).*/\1/')

# Exit if the version variable contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1