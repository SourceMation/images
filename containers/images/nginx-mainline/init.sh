#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the nginx-mainline image
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
dyn_package_version=$(docker exec $container_name cat /dyn_version)
njs_package_version=$(docker exec $container_name cat /njs_version)
docker rm -f $container_name
echo "Found version: $main_package_version"

## Extract versions :)
NGINX_VERSION=$(echo "$main_package_version" | cut -d '-' -f 1)
PKG_RELEASE=$(echo "$main_package_version" | cut -d '-' -f 2 | cut -d '.' -f 1)
NJS_RELEASE=$(echo "$njs_package_version" | cut -d '-' -f 2)
NJS_VERSION=$(echo "$njs_package_version" | cut -d '-' -f 1 | cut -d '+' -f 2) 
DYNPKG_RELEASE=$(echo "$dyn_package_version" | cut -d '-' -f 2 | cut -d '.' -f 1)

echo "Found versions:
NGINX_VERSION: $NGINX_VERSION
PKG_RELEASE: $PKG_RELEASE
NJS_VERSION: $NJS_VERSION
NJS_RELEASE: $NJS_RELEASE
DYNPKG_RELEASE: $DYNPKG_RELEASE
"

sed -i "s/version=\"[^\"]*\"/version=\"$NGINX_VERSION\"/" Dockerfile || exit 1
sed -i "s/NGINX_VERSION=\"[^\"]*\"/NGINX_VERSION=\"$NGINX_VERSION\"/" Dockerfile || exit 1
sed -i "s/PKG_RELEASE=\"[^\"]*\"/PKG_RELEASE=\"$PKG_RELEASE\"/" Dockerfile || exit 1
sed -i "s/NJS_VERSION=\"[^\"]*\"/NJS_VERSION=\"$NJS_VERSION\"/" Dockerfile || exit 1
sed -i "s/NJS_RELEASE=\"[^\"]*\"/NJS_RELEASE=\"$NJS_RELEASE\"/" Dockerfile || exit 1
sed -i "s/DYNPKG_RELEASE=\"[^\"]*\"/DYNPKG_RELEASE=\"$DYNPKG_RELEASE\"/" Dockerfile || exit 1

# Download the entrypoints, configs etc to sync with official
echo "-> Removing old entrypoints and configs"
rm -fv 10-listen-on-ipv6-by-default.sh 15-local-resolvers.envsh 20-envsubst-on-templates.sh 30-tune-worker-processes.sh docker-entrypoint.sh
echo "-> Downloading new entrypoints and configs"
wget https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/mainline/debian/10-listen-on-ipv6-by-default.sh
wget https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/mainline/debian/15-local-resolvers.envsh
wget https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/mainline/debian/20-envsubst-on-templates.sh
wget https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/mainline/debian/30-tune-worker-processes.sh
wget https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/mainline/debian/docker-entrypoint.sh
chmod +x 10-listen-on-ipv6-by-default.sh 15-local-resolvers.envsh 20-envsubst-on-templates.sh 30-tune-worker-processes.sh docker-entrypoint.sh


echo "init.sh finished"
