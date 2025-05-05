#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the redis image
# Author: Radosław Kolba
# e-mail: radoslaw.kolba@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

REDIS_DOWNLOAD_URL="http://download.redis.io/redis-stable.tar.gz"
curl -o redis-stable.tar.gz ${REDIS_DOWNLOAD_URL}
tar xzf redis-stable.tar.gz
VERSION=$(grep "VERSION " redis-stable/src/version.h | awk '{print $3}')
VERSION=${VERSION:1:-1}

sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1

rm -rf redis-stable.tar.gz
rm -rf redis-stable/

echo "Finished setting up the Redis Sentinel $VERSION image"