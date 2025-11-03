#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the nginx-mainline-otel image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

# First we have to find the newest version of the Nginx mainline available for us.
IMG_NAME=sourcemation/debian-13-slim

# Unique container name
container_name="temp-$(date +%s)"

docker run -d --name $container_name $IMG_NAME sleep 180
docker cp prepare-container-to-get-version.sh $container_name:/prepare-container-to-get-version.sh
docker exec $container_name /prepare-container-to-get-version.sh
main_package_version=$(docker exec $container_name cat /version)
otel_version=$(docker exec $container_name cat /otel_version)
docker rm -f $container_name
echo "Found version: $main_package_version"

## Extract versions :)
NGINX_VERSION=$(echo "$main_package_version" | cut -d '-' -f 1) # NGINX_VERSION
PKG_RELEASE=$(echo "$main_package_version" | cut -d '-' -f 2 | cut -d '.' -f 1) # PKG_RELEASE
OTEL_VERSION=$(echo "$otel_version" | cut -d '-' -f 1 | cut -d '+' -f 2) # OTEL_VERSION

echo "Found versions:
NGINX_VERSION: $NGINX_VERSION
PKG_RELEASE: $PKG_RELEASE
OTEL_VERSION: $OTEL_VERSION
"

sed -i "s/version=\"[^\"]*\"/version=\"$NGINX_VERSION\"/" Dockerfile || exit 1
sed -i "s/NGINX_VERSION=\"[^\"]*\"/NGINX_VERSION=\"$NGINX_VERSION\"/" Dockerfile || exit 1
sed -i "s/PKG_RELEASE=\"[^\"]*\"/PKG_RELEASE=\"$PKG_RELEASE\"/" Dockerfile || exit 1
sed -i "s/OTEL_VERSION=\"[^\"]*\"/OTEL_VERSION=\"$OTEL_VERSION\"/" Dockerfile || exit 1

echo "init.sh finished"
