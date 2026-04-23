#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the ActiveMQ 6
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

APP="activemq"

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP"

VERSION=$(curl -s https://dlcdn.apache.org/activemq/ | grep -o 'href="6\.[0-9.]*/"' | sed 's/href="//;s/\/"//' | sort --version-sort --reverse | head -n 1)
# Exit with an error if the returned version contains anything other
# than digits and dots
if [[ ! $VERSION =~ ^[0-9.]+$ ]]; then
    echo "Could not find a valid ActiveMQ 6 version on dlcdn.apache.org, falling back to 6.2.4"
    VERSION="6.2.4"
fi
echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/ACTIVEMQ_VERSION=.*/ACTIVEMQ_VERSION=$VERSION/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
