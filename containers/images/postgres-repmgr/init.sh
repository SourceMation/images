#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the postgres-exporter docker init.sh
# Author: Radosław Kolba
# e-mail: radoslaw.kolba@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="postgres_repmgr"

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --refs --tags https://github.com/EnterpriseDB/repmgr.git | grep  -o 'v[0-9]*.[0-9]*.[0-9]*$'| tr -d 'v' | sort --version-sort --reverse | head -1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

# Replacing the version number in the Dockerfile
sed -i "s/REPMGR_VER=\"[^\"]*\"/REPMGR_VER=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"