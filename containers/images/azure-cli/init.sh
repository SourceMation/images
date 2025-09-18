#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-18
# -----------------------------------

set -eu

echo "-> Preparing azure-cli variables"
VERSION=$(curl -s https://api.github.com/repos/Azure/azure-cli/releases/latest |grep tag_name |awk -F'-' '{print $3}' |sed 's/",//')

# Exit if the version variable contains anything other
# than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
