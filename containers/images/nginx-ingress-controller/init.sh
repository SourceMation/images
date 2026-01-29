#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the nginx-ingress-controller image
# ---------------------------------------------------

APP="nginx-ingress-controller"

# Updating repository metadata and downloading the latest available version
# of the application using git ls-remote
echo "Checking the latest available version of the $APP"
TAG=$(git ls-remote --refs --tags https://github.com/kubernetes/ingress-nginx.git | grep -o 'controller-v[0-9.]*$' | sort --version-sort --reverse | head -n 1)

# Exit with an error if the returned tag is empty
[[ -z "$TAG" ]] && exit 1

echo "TAG = $TAG"

# Extract version (e.g., controller-v1.11.0 -> v1.11.0)
VERSION=${TAG#controller-}

echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/INGRESS_NGINX_VERSION=\"[^\"]*\"/INGRESS_NGINX_VERSION=\"$TAG\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"

