#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the Tomcat 9 image
# ---------------------------------------------------

set -euo pipefail

APP="Tomcat 9"

echo "Checking the latest version of $APP"

# Get latest 9.0.x version from Apache
TOMCAT_VERSION=$(curl -fsSL https://downloads.apache.org/tomcat/tomcat-9/ | grep -o 'v9\.0\.[0-9]*' | sort -V | tail -1 | cut -c2-)

if [ -z "${TOMCAT_VERSION:-}" ]; then
  echo "Failed to determine latest Tomcat 9.0.x version" >&2
  exit 1
fi

echo "Latest version of $APP is $TOMCAT_VERSION"

# Fetch corresponding SHA512 checksum for this version
TOMCAT_SHA512=$(curl -fsSL "https://downloads.apache.org/tomcat/tomcat-9/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz.sha512" | awk '{print $1}')

if [ -z "${TOMCAT_SHA512:-}" ]; then
  echo "Failed to determine SHA512 checksum for Tomcat version ${TOMCAT_VERSION}" >&2
  exit 1
fi

# Update Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$TOMCAT_VERSION\"/" Dockerfile || exit 1
sed -i "s/ENV TOMCAT_VERSION=[0-9.]*[a-z]*/ENV TOMCAT_VERSION=$TOMCAT_VERSION/" Dockerfile || exit 1
sed -i "s/ENV TOMCAT_SHA512=.*/ENV TOMCAT_SHA512=$TOMCAT_SHA512/" Dockerfile || exit 1

echo "Init script completed successfully"
