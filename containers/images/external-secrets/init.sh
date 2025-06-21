#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the external-secrets image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="external-secrets"

echo "Checking the latest available version of the $APP"
# note there is old and wrong tag v.0.3.6 thats version grep looks like this,
# we also do not want any release candidates
VERSION=$(git ls-remote --tags https://github.com/external-secrets/external-secrets.git | grep -v  '\-rc' | grep -o 'v[0-9].*[.0-9]*$' | sort --version-sort --reverse | head -1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^v[0-9.]+$ ]] && exit 1
echo "VERSION = $VERSION"

echo "Downloading the $APP $VERSION source code"
[ -d "external-secrets" ] && rm -rf external-secrets
set -x
git clone --depth 1 --branch "$VERSION" https://github.com/external-secrets/external-secrets.git
set +x

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
