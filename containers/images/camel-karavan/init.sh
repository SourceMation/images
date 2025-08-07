#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the camel-karavan image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="Camel Karavan"

echo "Checking the latest version of $APP"

KARAVAN_VERSION=$(git ls-remote --refs --tags https://github.com/apache/camel-karavan.git |  grep -o  '[.+0-9]*$' | sort --version-sort -r | head -1)

# Exit with an error if the returned version contains anything other
# than digits and dots
echo "Checking the latest version of $APP against the regex"
echo "$KARAVAN_VERSION" | grep -q '[.+0-9]*' || exit 1
echo "Check passed"


echo "Latest version of $APP is $KARAVAN_VERSION"

# We are using version as the label and also as docker tag docker tag cannot
# contain +

VERSION_WITH_PLUS_REPLACED=${KARAVAN_VERSION//+/-}

sed -i "s/version=\"[^\"]*\"/version=\"$VERSION_WITH_PLUS_REPLACED\"/" Dockerfile || exit 1
sed -i "s/KARAVAN_VERSION=\"[^\"]*\"/KARAVAN_VERSION=\"$KARAVAN_VERSION\"/" Dockerfile || exit 1


echo "Init script completed successfully"
