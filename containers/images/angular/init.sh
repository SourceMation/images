#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the angular image
# ---------------------------------------------------

APP="@angular/cli"

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP"
VERSION=$(npm show $APP version) || exit 1
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1
echo "VERSION = $VERSION"

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/@angular\/cli@[0-9.]*/@angular\/cli@$VERSION/" Dockerfile || exit 1

echo "Finished setting up the angular $VERSION image"

