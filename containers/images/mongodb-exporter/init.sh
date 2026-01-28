#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the mongodb-exporter image
# ---------------------------------------------------

APP="mongodb-exporter"

# Updating repository metadata and downloading the latest available version
# of the application using git ls-remote
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --refs --tags https://github.com/percona/mongodb_exporter.git | grep -o 'v[0-9.]*$' | sort --version-sort --reverse | head -n 1)

# Exit with an error if the returned version is empty or invalid
[[ ! $VERSION =~ ^v[0-9.]+$ ]] && exit 1

echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/MONGODB_EXPORTER_VERSION=\"[^\"]*\"/MONGODB_EXPORTER_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"

