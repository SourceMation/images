#!/usr/bin/bash
# ---------------------------------------------------
# Automated build process for the promethues image
# Author: Paweł Piasek
# e-mail: pawel.piasek@linuxpolska.pl
# ---------------------------------------------------

set -euxo pipefail
APP=prometheus
# Get latest version
echo "Checking the latest available version of the $APP"
version=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/prometheus/prometheus/releases/latest | sed 's/.*\///')
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
curl https://github.com/prometheus/prometheus/releases/download/${version}/prometheus-$VERSION.linux-$ARCH.tar.gz -sLo - | tar -xz --strip 1

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/" Dockerfile

