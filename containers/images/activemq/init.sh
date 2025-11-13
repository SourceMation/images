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

# After dec 25 2025 we have to make this fail so it's clear that the newer version 6.2 was released

current_date=$(date +%s)
cutoff_date=$(date -d "2025-12-25" +%s)
if [ "$current_date" -gt "$cutoff_date" ]; then
    echo "Error: ActiveMQ 6.2 should have arrive you must init.sh again to update to the newer version."
    exit 1
fi



VERSION=$(git ls-remote --refs --tags https://github.com/apache/activemq.git | grep  -o 'activemq-6.[.0-9]*$'| grep -v 'activemq-6.2' | sort --version-sort --reverse | tr -d 'activemq-' | head -n 1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1
echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/ACTIVEMQ_VERSION=.*/ACTIVEMQ_VERSION=$VERSION/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
