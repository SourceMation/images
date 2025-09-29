#!/bin/bash
set -euo pipefail
APP=keycloak-config-cli

echo "Checking the latest available version of the $APP"
RELEASE_JSON=$(curl -sL "https://api.github.com/repos/adorsys/keycloak-config-cli/releases/latest")
version=$(echo "$RELEASE_JSON" | grep '"tag_name":' | awk -F '"' '{print $4}')
VERSION=${version#v}
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

DOWNLOAD_URLS=$(echo "$RELEASE_JSON" | grep '"browser_download_url":' | grep '\.jar"' | awk -F '"' '{print $4}' | tr -d '\r')

rm -rf keycloak-config-cli
mkdir -p keycloak-config-cli

echo "Download .jar for $APP version $VERSION"
for url in $DOWNLOAD_URLS; do
    echo "Downloading ${url##*/}..."
    curl -sL "$url" -o "keycloak-config-cli/${url##*/}"
done

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/" Dockerfile