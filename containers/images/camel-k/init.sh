#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the camel-k docker init.sh
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------
# TEMPORARY hack as there is camel-k version v2.7.0 that is pre-release!
exit 0
APP="camel-k"

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --tags https://github.com/apache/camel-k.git | grep -v nightly | grep  -o 'v[.0-9]*$' | tr -d 'v' | sort --version-sort --reverse | head -n 1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1
echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/CAMEL_K_VER=\"[^\"]*\"/CAMEL_K_VER=\"v$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
