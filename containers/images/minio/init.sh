#!/usr/bin/bash
# ---------------------------------------------------
# Automated build process for the minio image
# Author: Paweł Piasek
# e-mail: pawel.piasek@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail
APP=minio
# Get latest version
echo "Checking the latest available version of the $APP"
version=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/$APP/$APP/releases/latest | sed 's/.*\///')
VERSION=$version
## Exit if the version variable contains anything other than digits and dots
#[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/;s/^ARG VERSION.*/ARG VERSION=$version/;" Dockerfile

