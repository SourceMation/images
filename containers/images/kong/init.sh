#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the redis docker image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

APP="kong"
ARCH="$(arch)"
IMG=$(head -1 Dockerfile | awk '{print $2}')

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP app"
VERSION=$(docker run --rm ${IMG} /bin/bash -c \
	"curl -1sLf 'https://packages.konghq.com/public/gateway-39/config.rpm.txt?distro=el&codename=9' > /etc/yum.repos.d/kong-gateway-39.repo; dnf check-update --refresh -y > /dev/null; dnf info --available ${APP}.${ARCH} | grep Version | awk '{print \$3}'")

# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Building the $APP $VERSION image"
