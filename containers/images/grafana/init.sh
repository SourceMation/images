#!/bin/bash
set -euo pipefail
APP=grafana

echo "Checking the latest available version of the $APP"
version=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/grafana/grafana/releases/latest | sed 's/.*\///')
VERSION=${version#v}
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

BASE_ARCH=$(uname -m)
if [ "$BASE_ARCH" == "x86_64" ]; then
    ARCH="amd64"
elif [ "$BASE_ARCH" == "aarch64" ]; then
    ARCH="arm64"
else
    echo "Unsupported architecture $BASE_ARCH ..." >&2
    exit 1
fi

rm -rf grafana grafana.tar.gz

echo "Download binaries for $APP version $VERSION for architecture $ARCH"
curl https://dl.grafana.com/oss/release/grafana-$VERSION.linux-$ARCH.tar.gz -sLo grafana.tar.gz

mkdir grafana
tar -xzf grafana.tar.gz -C grafana --strip-components=1

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/" Dockerfile