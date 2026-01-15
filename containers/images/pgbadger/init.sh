#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the pgbadger docker init.sh
# ---------------------------------------------------

set -eu

echo "-> Preparing pgbadger variables"
# Get latest tag from github, removing 'v' prefix if present
VERSION=$(curl -s https://api.github.com/repos/darold/pgbadger/tags | grep name | head -n 1 | awk -F'"' '{print $4}' | sed 's/^v//')

# Exit if the version variable contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && echo "Error: Invalid version format: $VERSION" && exit 1

echo "Latest version: $VERSION"

sed -i "s/ARG VERSION=\"[^\"]*\"/ARG VERSION=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
