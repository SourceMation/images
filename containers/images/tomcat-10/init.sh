#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the Tomcat 10 image
# ---------------------------------------------------

set -euo pipefail

APP="Tomcat 10"

echo "Checking the latest version of $APP"

# Get latest 10.1.x version from Apache
TOMCAT_VERSION=$(curl -s https://downloads.apache.org/tomcat/tomcat-10/ | grep -o 'v10\.1\.[0-9]*' | sort -V | tail -1 | cut -c2-)

if [[ -z "${TOMCAT_VERSION:-}" ]]; then
    echo "Error: Failed to determine latest Tomcat 10.1.x version." >&2
    exit 1
fi

echo "Latest version of $APP is $TOMCAT_VERSION"

# Fetch corresponding SHA512 checksum for this Tomcat version
TOMCAT_BASE_URL="https://downloads.apache.org/tomcat/tomcat-10"
TOMCAT_TAR_SHA512_URL="${TOMCAT_BASE_URL}/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz.sha512"
TOMCAT_SHA512=$(curl -fsSL "${TOMCAT_TAR_SHA512_URL}" | awk '{print $1}')

if [[ -z "${TOMCAT_SHA512:-}" ]]; then
    echo "Error: Failed to retrieve SHA512 checksum from ${TOMCAT_TAR_SHA512_URL}." >&2
    exit 1
fi

# Update Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$TOMCAT_VERSION\"/" Dockerfile || exit 1
sed -i "s/ENV TOMCAT_VERSION=[0-9.]*/ENV TOMCAT_VERSION=$TOMCAT_VERSION/" Dockerfile || exit 1
sed -i "s/ENV TOMCAT_SHA512=[^[:space:]]*/ENV TOMCAT_SHA512=$TOMCAT_SHA512/" Dockerfile || exit 1

echo "Init script completed successfully"
