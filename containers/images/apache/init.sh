#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the apache docker init.sh
# Author: Radosław Kolba
# e-mail: radoslaw.kolba@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="apache"
URL="https://httpd.apache.org/download.cgi"

# Fetch the HTML content and process it to find the latest version
LATEST_VERSION=$(curl -s "$URL" | \
  grep -o 'httpd-[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.tar\.gz' | \
  sed 's/httpd-//g' | \
  sed 's/\.tar\.gz//g' | \
  sort -V | \
  tail -n 1)

# Replacing the version number in the Dockerfile
sed -i "s/APACHE_VER=\"[^\"]*\"/APACHE_VER=\"$LATEST_VERSION\"/g" Dockerfile || exit 1
sed -i "s/version=\"[^\"]*\"/version=\"$LATEST_VERSION\"/g" Dockerfile || exit 1

echo "Finished setting up the $APP $LATEST_VERSION image"
