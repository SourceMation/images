#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the Tomcat 11 image
# ---------------------------------------------------

set -euo pipefail

APP="Tomcat 11"

echo "Checking the latest version of $APP"

# Get latest 11.0.x version from Apache
TOMCAT_VERSION=$(curl -s https://downloads.apache.org/tomcat/tomcat-11/ | grep -o 'v11\.0\.[0-9]*' | sort -V | tail -1 | cut -c2-)

echo "Latest version of $APP is $TOMCAT_VERSION"

# Update Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$TOMCAT_VERSION\"/" Dockerfile || exit 1
sed -i "s/ENV TOMCAT_VERSION=[0-9.]*/ENV TOMCAT_VERSION=$TOMCAT_VERSION/" Dockerfile || exit 1

echo "Init script completed successfully"
