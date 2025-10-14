#!/bin/bash
set -euo pipefail
APP=phpmyadmin

echo "Checking the latest available version of the $APP"
API_URL="https://www.phpmyadmin.net/home_page/version.json"
VERSION=$(curl -sL "${API_URL}" | awk -F'"' '/"version":/ {print $4; exit}')
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

rm -rf phpmyadmin* phpMyAdmin-* phpmyadmin.tar.gz

echo "Download files for $APP version $VERSION"
curl https://files.phpmyadmin.net/phpMyAdmin/${VERSION}/phpMyAdmin-${VERSION}-all-languages.tar.gz -sLo phpmyadmin.tar.gz

tar -xzf phpmyadmin.tar.gz
mv phpMyAdmin-*-all-languages phpmyadmin

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/" Dockerfile