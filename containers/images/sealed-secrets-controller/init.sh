#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the sealed-secrets-controller
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="sealed-secrets-controller"

echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --refs --tags https://github.com/bitnami-labs/sealed-secrets.git | grep -v helm |grep -o 'v[.0-9]*$' | sort --version-sort --reverse | head -1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^v[0-9.]+$ ]] && exit 1
echo "VERSION = $VERSION"

echo "Downloading the $APP $VERSION source code"
[ -d "sealed-secrets" ] && rm -rf sealed-secrets
set -x
git clone --depth 1 --branch "$VERSION" https://github.com/bitnami-labs/sealed-secrets.git
set +x

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
