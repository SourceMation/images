#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the postgres-exporter docker init.sh
# Author: Radosław Kolba
# e-mail: radoslaw.kolba@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="postgres_exporter"

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --refs --tags https://github.com/prometheus-community/postgres_exporter.git | grep  -o 'v[0-9]*.[0-9]*.[0-9]*$'| tr -d 'v' | sort --version-sort --reverse | head -1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

# Replacing the version number in the Dockerfile
sed -i "s/PGEXPORTER_VER=\"[^\"]*\"/PGEXPORTER_VER=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"