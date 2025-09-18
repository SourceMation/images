#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-18
# -----------------------------------

set -eu

echo "-> Preparing zookeeper variables"
VERSION=$(curl -SsL https://downloads.apache.org/zookeeper/current \
    |   egrep "apache-zookeeper-.*bin.tar.gz"\
    |   head -1 \
    |   awk -F'-' '{print $3}')

# Exit if the version variable contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s#^ARG ZOOKEEPER_VERSION=.*#ARG ZOOKEEPER_VERSION=${VERSION}#" Dockerfile || exit 1