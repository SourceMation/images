#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the apache docker init.sh
# Author: Radosław Kolba
# e-mail: radoslaw.kolba@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="keycloak-25"
URL="https://www.keycloak.org/downloads-archive"

# Fetch the HTML content and process it to find the latest version
VERSION=$(curl -s "$URL" | grep -o '25\.[0-9][0-9]*\.[0-9][0-9]*' | sort -V | tail -n 1)
VERSION=${VERSION#v}

rm -rf keycloak keycloak-*.tar.gz

echo "Download binaries for $APP version $VERSION"

curl https://github.com/keycloak/keycloak/releases/download/$VERSION/keycloak-$VERSION.tar.gz -sLo keycloak.tar.gz

mkdir keycloak
tar -xzf keycloak.tar.gz -C keycloak --strip-components=1

echo "Setup version in $APP Dockerfile"

# Replacing the version number in the Dockerfile
sed -i "s/KEYCLOAK_VER=\"[^\"]*\"/KEYCLOAK_VER=\"$VERSION\"/g" Dockerfile || exit 1
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/g" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
