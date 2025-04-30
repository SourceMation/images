
#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the redis operator image
# Author: Radosław Kolba
# e-mail: radoslaw.kolba@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

REDIS_OPERATOR_GIT="https://github.com/OT-CONTAINER-KIT/redis-operator.git"
VERSION=$(git ls-remote --tags $REDIS_OPERATOR_GIT | grep -o 'v.*' | sort --version-sort --reverse | head -1)
REDIS_OPERATOR_SRC="https://github.com/OT-CONTAINER-KIT/redis-operator/archive/refs/tags/v${VERSION:1}.tar.gz"

SPATH=$(pwd)
APP_NAME=redis-operator

curl -sL -o $APP_NAME.tar.gz $REDIS_OPERATOR_SRC
mkdir $APP_NAME && tar -xf "$APP_NAME.tar.gz" -C $APP_NAME --strip-components=1

pushd $APP_NAME
cp -R go.mod go.sum api cmd internal mocks pkg $SPATH
popd
rm -rf $APP_NAME.tar.gz $APP_NAME/

sed -i "s/version=\"[^\"]*\"/version=\"${VERSION:1}\"/" Dockerfile || exit 1

echo "Finished setting up the Redis Operator ${VERSION:1} image"