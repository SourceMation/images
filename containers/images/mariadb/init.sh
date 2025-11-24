#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-09
# -----------------------------------

set -eu

echo "-> Preparing mariadb variables"
APP="mariadb"
VERSION=$(curl -s https://api.github.com/repos/MariaDB/server/releases/latest |grep tag_name |awk -F'-' '{print $2}' |sed 's/",//')

# Exit if the version variable contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
