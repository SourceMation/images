#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the JDK 17 image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="JDK 17"

echo "Checking the latest version of $APP"

JAVA_VERSION=$(git ls-remote --refs --tags https://github.com/adoptium/temurin17-binaries.git | grep -v beta | grep -o  'jdk-17[.+0-9]*' | sort --version-sort -r | head -1)

# Exit with an error if the returned version contains anything other
# than digits and dots
echo "Checking the latest version of $APP against the regex"
echo "$JAVA_VERSION" | grep -q 'jdk-17[.+0-9]*' || exit 1

echo "Latest version of $APP is $JAVA_VERSION"

# We are using version as the label and also as docker tag docker tag cannot
# contain +

VERSION_WITH_PLUS_REPLACED=${JAVA_VERSION//+/-}

sed -i "s/version=\"[^\"]*\"/version=\"$VERSION_WITH_PLUS_REPLACED\"/" Dockerfile || exit 1
sed -i "s/JAVA_VERSION=\"[^\"]*\"/JAVA_VERSION=\"$JAVA_VERSION\"/" Dockerfile || exit 1


echo "Init script completed successfully"
