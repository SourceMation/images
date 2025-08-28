#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the kubectl image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

APP="kubectl"

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP"
VERSION=$(curl -sL https://dl.k8s.io/release/stable.txt) || exit 1
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^v[0-9.]+$ ]] && exit 1
echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/KUBECTL_VERSION=\"[^\"]*\"/KUBECTL_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
