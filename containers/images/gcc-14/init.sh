#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the GCC 14
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="gcc"

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --tags https://github.com/gcc-mirror/gcc.git  | grep -o 'gcc-14[.0-9]*$' | sort --version-sort --reverse | tr -d 'gc-' | head -n 1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1
echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/GCC_VERSION=\"[^\"]*\"/GCC_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
