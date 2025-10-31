#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-08
# -----------------------------------

set -eu

echo "-> Preparing git variables"
APP="git"
VERSION=$(curl -s "https://packages.debian.org/trixie/git" | grep -o 'Package: git ([^-]*' | grep -o '[0-9.]*$')

# Exit if the version variable contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1