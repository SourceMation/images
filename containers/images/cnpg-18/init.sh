#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the postgresql-18 cnpg image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

# First we have to find the newest version of the PostgreSQL available for us.
IMG_NAME=sourcemation/debian-13-slim

# Unique container name
container_name="temp-$(date +%s)"
cp ../postgres-18/prepare-container-to-get-version.sh .
docker run --rm -d --name $container_name $IMG_NAME sleep 120
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

# Get the barman version from the docker-bake.hcl file
curl https://raw.githubusercontent.com/cloudnative-pg/postgres-containers/refs/heads/main/docker-bake.hcl | grep barmanVersion  | awk '{print $3}' > barman_version
barman_version=$(cat barman_version | head -1 | tr -d '"')

# Check if version is in format XX.ZZ.YY only digits and dots

if ! echo "$barman_version" | grep -Eq '^[0-9]+(\.[0-9]+){2}$'; then
    echo "Error: barman_version is not in the correct format (XX.ZZ.YY)"
    echo "The value is: $barman_version"
    exit 1
fi
# Set barman version in Dockerfile 
sed -i "s/ENV BARMAN_VERSION=\"[^\"]*\"/ENV BARMAN_VERSION=\"$barman_version\"/" Dockerfile || exit 1
