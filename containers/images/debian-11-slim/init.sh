#!/usr/bin/env bash

# Author: Alex Baranowski
# License: MIT
#
# Description: This script is used to build rootfs.tar.gz for the debian-11-slim image
# Allowing us to reproduce the image without having to rely on the dockerhub image

set -euo pipefail
BASEDIR="$(dirname $(readlink -f "$0"))"

[ -d debuerreotype ] && sudo rm -rf "$BASEDIR/debuerreotype" && sudo rm -f "$BASEDIR/rootfs.tar.gz"
git clone https://github.com/debuerreotype/debuerreotype.git

pushd debuerreotype
./docker-run.sh sh -euxc "debuerreotype-init rootfs bullseye $(date); debuerreotype-minimizing-config rootfs; debuerreotype-debian-sources-list rootfs bullseye; debuerreotype-slimify rootfs; debuerreotype-tar rootfs rootfs.tar.gz"
mv -f rootfs.tar.gz "$BASEDIR"
popd
sudo rm -rf "$BASEDIR/debuerreotype"
