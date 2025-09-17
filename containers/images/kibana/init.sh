#!/bin/bash
set -euo pipefail
APP=kibana

echo "Checking the latest available version of the $APP"
version=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/elastic/kibana/releases/latest | sed 's/.*\///')
VERSION=${version#v}
# Exit if the version variable contains anything other than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

BASE_ARCH=$(uname -m)
if [ "$BASE_ARCH" == "x86_64" ]; then
    ARCH="x86_64"
elif [ "$BASE_ARCH" == "aarch64" ]; then
    ARCH="aarch64"
else
    echo "Unsupported architecture $BASE_ARCH ..." >&2
    exit 1
fi

rm -rf kibana kibana-*.tar.gz

echo "Download binaries for $APP version $VERSION for architecture $ARCH"
curl https://artifacts.elastic.co/downloads/kibana/kibana-$VERSION-linux-$ARCH.tar.gz -sLo kibana.tar.gz

mkdir kibana
tar -xzf kibana.tar.gz -C kibana --strip-components=1

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/" Dockerfile