#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the oauth2-proxy image
# ---------------------------------------------------

APP="oauth2-proxy"

# Updating repository metadata and downloading the latest available version
# of the application using git ls-remote (avoiding curl/sed for version discovery)
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --refs --tags https://github.com/oauth2-proxy/oauth2-proxy.git | grep -o 'v[0-9.]*$' | sort --version-sort --reverse | head -n 1)

# Exit with an error if the returned version is empty or invalid
[[ ! $VERSION =~ ^v[0-9.]+$ ]] && exit 1

echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/OAUTH2_PROXY_VERSION=\"[^\"]*\"/OAUTH2_PROXY_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"