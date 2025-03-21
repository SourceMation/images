#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the postgresql-17 cnpg image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

# First we have to find the newest version of the PostgreSQL available for us.
IMG_NAME=sourcemation/debian-12-slim

# Unique container name
container_name="temp-$(date +%s)"
cp ../postgres-17/prepare-container-to-get-version.sh .
docker run -d --name $container_name $IMG_NAME sleep 180
docker cp prepare-container-to-get-version.sh $container_name:/prepare-container-to-get-version.sh
docker exec $container_name /prepare-container-to-get-version.sh
version=$(docker exec $container_name cat /version)
docker rm -f $container_name
echo "Found version: $version"

# Extract versions :)
upstream_version=$(echo "$version" | cut -d '-' -f 1)
debian_revision=$(echo "$version" | cut -d '-' -f 2 | cut -d '.' -f 1)
version_label="${upstream_version}.${debian_revision}"

sed -i "s/version=\"[^\"]*\"/version=\"$version_label\"/" Dockerfile || exit 1

# Our images are based on the official Docker so we we need same entrypoint and ensure-initdb scripts.
rm -f requirements.txt
wget https://github.com/cloudnative-pg/postgres-containers/raw/refs/heads/main/Debian/17/bookworm/requirements.txt
