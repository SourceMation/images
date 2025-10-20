#!/bin/bash
set -euo pipefail
APP=ghost

echo "Checking the latest available version of the $APP"
VERSION=$(curl -sL -o /dev/null -w '%{url_effective}' https://github.com/TryGhost/Ghost/releases/latest | sed 's/.*\///')
VERSION=${VERSION#v}
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/" Dockerfile
sed -i "s/ARG GHOST_VERSION.*/ARG GHOST_VERSION=${VERSION}/" Dockerfile