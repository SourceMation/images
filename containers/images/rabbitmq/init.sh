#!/usr/bin/env bash
# ----------------------------------------------------
# Automated build process for the RabbitMQ Docker image
# Author: Jarosław Mazurkiewicz
# e-mail: jaroslaw.mazurkiewicz@linuxpolska.pl
# ----------------------------------------------------
APP="rabbitmq-server"
IMG=$(head -1 Dockerfile | awk '{print $2}')
SPATH=$(dirname "$0")

echo "Checking the latest available version of the ${APP} app"
# Updating repository metadata and downloading the latest available version of the
# application, including adding the RabbitMQ repository
# For testing on Podman run with the --privileged flag
VERSION=$(docker run --privileged -v $SPATH/rabbitmq.repo:/etc/yum.repos.d/rabbitmq.repo --rm ${IMG} /bin/bash -c \
          "dnf check-update --refresh &> /dev/null; dnf info --available ${APP} | grep '^Version' | awk '{print \$3}'")

echo "Found the latest version of the ${APP}: $VERSION"
# Exit with an error if the returned version contains anything other than digits and dots
if [[ ! $VERSION =~ ^[0-9.]+$ ]]; then
    echo "Error: The version number contains invalid characters"
    exit 1
fi


# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Building the $APP $VERSION image"
