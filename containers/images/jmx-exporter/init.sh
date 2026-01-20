#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the jmx-exporter image
# ---------------------------------------------------

APP="jmx-exporter"

# Updating repository metadata and downloading the latest available version
# of the application using git ls-remote
echo "Checking the latest available version of the $APP"
TAG=$(git ls-remote --refs --tags https://github.com/prometheus/jmx_exporter.git | cut -d/ -f3 | grep -v parent | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort --version-sort --reverse | head -n 1)

# Exit with an error if the returned tag is empty
[[ -z "$TAG" ]] && exit 1

echo "TAG = $TAG"
VERSION=$TAG

echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/JMX_EXPORTER_VERSION=\"[^\"]*\"/JMX_EXPORTER_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"

