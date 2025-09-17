#!/usr/bin/bash
# ---------------------------------------------------
# Automated build process for the etcd image
# Author: Paweł Piasek
# e-mail: pawel.piasek@linuxpolska.pl
# ---------------------------------------------------

set -euxo pipefail
APP=etcd
# Get latest version
echo "Checking the latest available version of the $APP"
version=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/$APP-io/$APP/releases/latest | sed 's/.*\///')
VERSION=${version#v}
# Exit if the version variable contains anything other than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

BASE_ARCH=$(uname -m)
if [ "$BASE_ARCH" == "x86_64" ]; then
    ARCH="amd64"
elif [ "$BASE_ARCH" == "aarch64" ]; then
    ARCH="arm64"
else
    echo"Unsupported architecture $BASE_ARCH ..." >&2
fi

echo "Download binaries for $APP"
dir=$APP-$version-linux-$ARCH
curl https://github.com/$APP-io/$APP/releases/download/${version}/$dir.tar.gz -sLo - | tar -xz

echo "Setup version and COPYFROM ARG in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/;s/^ARG COPYFROM.*/ARG COPYFROM=$dir/" Dockerfile
