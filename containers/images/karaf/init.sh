#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for Apache Karaf
# ---------------------------------------------------

set -euo pipefail

APP="karaf"

# Fetch the latest version from Apache Karaf CDN
VERSION=$(curl -s https://dlcdn.apache.org/karaf/ | grep -o 'href="4\.[0-9.]*/"' | sed 's/href="//;s/\/"//' | sort --version-sort --reverse | head -n 1)

# Exit with an error if the returned version contains anything other than digits and dots
if [[ ! $VERSION =~ ^[0-9.]+$ ]]; then
    echo "Could not find a valid Karaf 4 version on dlcdn.apache.org, falling back to git tags"
    VERSION=$(git ls-remote --refs --tags https://github.com/apache/karaf.git | \
      grep -o 'karaf-4\.[0-9][0-9]*\.[0-9][0-9]*$' | \
      sed 's/karaf-//g' | \
      sort -V | \
      tail -n 1)
fi

echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/KARAF_VERSION=.*/KARAF_VERSION=$VERSION/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
