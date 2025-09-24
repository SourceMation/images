#!/bin/bash
set -euo pipefail
APP=openldap

echo "Checking the latest available version of the $APP"
DOWNLOAD_URL="https://www.openldap.org/software/download/OpenLDAP/openldap-release/"
VERSION=$(curl -sL ${DOWNLOAD_URL} | grep -o 'openldap-[0-9.]*\.tgz' | sort -V | tail -n 1 | sed -E 's/openldap-|\.tgz//g')
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1


echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"${VERSION}\" \\\\/" Dockerfile
sed -i "s/ARG VERSION=.*/ARG VERSION=${VERSION}/" Dockerfile