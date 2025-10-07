#!/bin/bash
set -euo pipefail
APP=cassandra

echo "Checking the latest available version of the $APP"
VERSION=$(curl -sL https://cassandra.apache.org/download/ \
    | grep -o 'apache-cassandra-[0-9.]*-bin.tar.gz' \
    | sort -V \
    | tail -n 1 \
    | sed -E 's/apache-cassandra-|-bin.tar.gz//g')
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1


rm -rf cassandra cassandra.tar.gz

echo "Download binaries for $APP version $VERSION"
curl https://dlcdn.apache.org/cassandra/${VERSION}/apache-cassandra-${VERSION}-bin.tar.gz -sLo cassandra.tar.gz

mkdir cassandra
tar -xzf cassandra.tar.gz -C cassandra --strip-components=1

echo "Setup version in $APP Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/" Dockerfile