#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for Hugo SSG
# Author: Michal Niezborala (based on script by Alex Baranowski)
# e-mail: michal.niezborala@linuxpolska.pl
# ---------------------------------------------------

APP="hugo"
DART_SASS="dart-sass"

# Updating repository metadata and downloading latest versions
echo "Checking the latest available version of $DART_SASS"
DART_SASS_VERSION=$(git ls-remote --refs --tags https://github.com/sass/dart-sass.git | grep  -o 'refs/tags/[0-9]*[.0-9]*[.0-9]*$' | sort --version-sort --reverse | tr -d 'refs/tags/' | head -n 1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $DART_SASS_VERSION =~ ^[0-9.]+$ ]] && exit 1
echo "DART_SASS_VERSION = $DART_SASS_VERSION"

echo "Checking the latest available version of $APP"
HUGO_VERSION=$(git ls-remote --refs --tags https://github.com/gohugoio/hugo.git | grep  -o 'refs/tags/v[0-9]*[.0-9]*[.0-9]*$' | sort --version-sort --reverse | tr -d 'refs/tags/v' | head -n 1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $DART_SASS_VERSION =~ ^[0-9.]+$ ]] && exit 1
echo "HUGO_VERSION = $HUGO_VERSION"

# Replacing versions in Dockerfile
sed -i "s/DART_SASS_VERSION=.*/DART_SASS_VERSION=$DART_SASS_VERSION/" Dockerfile || exit 1

sed -i "s/version=\"[^\"]*\"/version=\"$HUGO_VERSION\"/" Dockerfile || exit 1
sed -i "s/HUGO_VERSION=.*/HUGO_VERSION=$HUGO_VERSION/" Dockerfile || exit 1

echo "Finished setting up the $APP $HUGO_VERSION image (with supporting $DART_SASS $DART_SASS_VERSION)"
