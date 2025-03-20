#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the postgresql-17 image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

# First we have to find the newest version of the PostgreSQL avaialble for us.
IMG_NAME=sourcemation/debian-12-slim


docker rm -f temp || true
docker run -d --name temp $IMG_NAME sleep infinity
docker cp prepare-continer-to-get-version.sh temp:/prepare-continer-to-get-version.sh
docker exec temp /prepare-continer-to-get-version.sh
version=$(docker exec temp cat /version)
docker stop temp
echo "Found version: $version"

# Extract versions :)
upstream_version=$(echo "$version" | cut -d '-' -f 1)
debian_revision=$(echo "$version" | cut -d '-' -f 2 | cut -d '.' -f 1)
version_label="${upstream_version}.${debian_revision}"
# Just rename for clarity
package_version="$version"

sed -i "s/version=\"[^\"]*\"/version=\"$version_label\"/" Dockerfile || exit 1
sed -i "s/PG_VERSION=\"[^\"]*\"/PG_VERSION=\"$package_version\"/" Dockerfile || exit 1

# Our images are based on the official Docker so we we need same entrypoint and ensure-initdb scripts.
rm -f docker-entrypoint.sh docker-ensure-initdb.sh
wget https://raw.githubusercontent.com/docker-library/postgres/refs/heads/master/17/bookworm/docker-entrypoint.sh
wget https://raw.githubusercontent.com/docker-library/postgres/refs/heads/master/17/bookworm/docker-ensure-initdb.sh
chmod +x docker-entrypoint.sh docker-ensure-initdb.sh
