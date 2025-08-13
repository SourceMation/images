#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the ManageIQ build using preexisting containers
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="manageiq"

# Find the newest version
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --refs --tags https://github.com/ManageIQ/manageiq-pods.git | awk '{print $2}'  | grep -Po '\w+-\d+' | sort -r | head -1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[[:alnum:]_-]+[[:digit:]]+$  ]] && { echo "Invalid version format: $VERSION"; exit 1; }


echo "Finished setting up the $APP $VERSION image"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/IMAGE_REF=[^\"]*/IMAGE_REF=$VERSION/" Dockerfile || exit 1

rm -rf manageiq
git clone https://github.com/ManageIQ/manageiq.git manageiq
cd manageiq
git checkout "$VERSION"
