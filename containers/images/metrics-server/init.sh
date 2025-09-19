#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-19
# -----------------------------------

set -eu

echo "-> Preparing metrics-server variables"
VERSION_SRC="https://api.github.com/repos/kubernetes-sigs/metrics-server/releases/latest"
VERSION=$(curl -s ${VERSION_SRC} |grep -o '"tag_name": "[^"]*'|cut -d'"' -f4 |sed 's/v//')

sed -i "s#^ARG VERSION=.*#ARG VERSION=${VERSION}#" Dockerfile || exit 1
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
