#!/bin/bash
set -euo pipefail
APP=wordpress

echo "Checking the latest available version of the $APP"
API_URL="https://api.wordpress.org/core/version-check/1.7/"
VERSION=$(curl -sL "${API_URL}" | grep -o '"version":"[0-9.]*"' | head -n 1 | awk -F '"' '{print $4}')
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

rm -rf wordpress wordpress.tar.gz

echo "Download binaries for $APP version $VERSION"
curl https://wordpress.org/latest.tar.gz -sLo wordpress.tar.gz

tar -xzf wordpress.tar.gz

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/" Dockerfile