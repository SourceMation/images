#!/usr/bin/env bash
# ----------------------------------------------------
# Automated build process for the python3 Docker image
# Author: Jarosław Mazurkiewicz
# e-mail: jaroslaw.mazurkiewicz@linuxpolska.pl
# ----------------------------------------------------

APP="python3"
IMG=$(head -1 Dockerfile | awk '{print $2}')

# Updating repository metadata and downloading the latest available version
# of the application:
echo "Checking the latest available version of the app"
VERSION=$(docker run --rm ${IMG} /bin/bash -c \
	"dnf check-update --refresh > /dev/null; dnf info ${APP} | grep Version | awk '{print \$3}'")

# Exit with an error if the returned version contains anything other than digits and dots:
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

# Replacing the version number in the Dockerfile:
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Building the $APP $VERSION image"
