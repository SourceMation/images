#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for Apache Karaf
# ---------------------------------------------------

set -euo pipefail

APP="karaf"

# Fetch the latest version from Apache Karaf GitHub releases
VERSION=$(git ls-remote --refs --tags https://github.com/apache/karaf.git | \
  grep -o 'karaf-[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*$' | \
  sed 's/karaf-//g' | \
  sort -V | \
  tail -n 1)

# Exit with an error if the returned version contains anything other than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/KARAF_VERSION=.*/KARAF_VERSION=$VERSION/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
