#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the redis docker image
# Author: Jarosław Mazurkiewicz
# e-mail: jaroslaw.mazurkiewicz@linuxpolska.pl
# ---------------------------------------------------

# Test image:
# sudo dnf install redis -y && sudo systemctl disable --now redis
# docker run -d -p 6379:6379 -e PERSISTENCE_ENABLED=true -e REDIS_PASSWORD=mypass123 IMAGE_ID
# redis-cli -h 127.0.0.1 -p 6379 -a mypass123
# 127.0.0.1:6379> set testkey "It Works!"
# 127.0.0.1:6379> get testkey

APP="redis"
ARCH="$(arch)"
IMG=$(head -1 Dockerfile | awk '{print $2}')

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP app"
VERSION=$(docker run --rm ${IMG} /bin/bash -c \
	"dnf module enable redis:7 -y &>/dev/null; dnf check-update --refresh > /dev/null; dnf info --available ${APP}.${ARCH} | grep Version | awk '{print \$3}'")

# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Building the $APP $VERSION image"
