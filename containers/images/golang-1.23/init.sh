#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the golang 1.23 image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

APP="golang-1.23"

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --tags https://github.com/golang/go.git | grep  -o 'go1.23[.0-9]*$' | sort --version-sort --reverse | tr -d 'go' | head -n 1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1
echo "VERSION = $VERSION"
# create the url
MY_ARCH=$(uname -m)
if [ "$MY_ARCH" == "x86_64" ]; then
    MY_ARCH="amd64"
elif [ "$MY_ARCH" == "aarch64" ]; then
    MY_ARCH="arm64"
fi
URL="https://dl.google.com/go/go$VERSION.linux-$MY_ARCH.tar.gz"

# Now get the SHA256 sum
SHA256_SUM=$(curl -s $URL | sha256sum | awk '{print $1}')


# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/GOLANG_VERSION=\"[^\"]*\"/GOLANG_VERSION=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/GO_SHA256=\"[^\"]*\"/GO_SHA256=\"$SHA256_SUM\"/" Dockerfile || exit 1
sed -i "s#GO_URL=\"[^\"]*\"#GO_URL=\"$URL\"#" Dockerfile || exit 1


echo "Finished setting up the $APP $VERSION image"
