#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the python 3.14 image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

APP="python3-14"

# Updating repository metadata and downloading the latest available version
# of the application
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --refs --tags https://github.com/python/cpython.git | grep  -o 'v3.14.[0-9]*$'| tr -d 'v' | sort --version-sort --reverse | head -1)
# Exit with an error if the returned version contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

# Now get the SHA256 sum
SHA256_SUM=$(curl -s "https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tar.xz" | sha256sum | awk '{print $1}')


# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/PYTHON_VERSION=\"[^\"]*\"/PYTHON_VERSION=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/PYTHON_SHA256=\"[^\"]*\"/PYTHON_SHA256=\"$SHA256_SUM\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
