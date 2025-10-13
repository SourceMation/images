#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-10-13
# -----------------------------------

set -eu

echo "-> Preparing memcached variables"
VERSION=$(curl -s "https://github.com/memcached/memcached/tags.atom" \
        | grep -oP '<title>\K[^<]+' \
        | sed -n '2p')

# Exit if the version variable contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

echo $VERSION

sed -i "s#^ARG VERSION=.*#ARG VERSION=${VERSION}#" Dockerfile || exit 1
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
