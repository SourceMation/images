#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2024-04-11
# -----------------------------------

set -eu

SPATH=$(pwd)

APP_NAME="cluster-operator"

echo "-> Preparing rabbitmq-cluster-operator variables"
CLUSTER_OPERATOR_VER_URL="https://api.github.com/repos/rabbitmq/cluster-operator/releases/latest"
CLUSTER_OPERATOR_VERSION=$(curl -s ${CLUSTER_OPERATOR_VER_URL} |grep -o '"tag_name": "[^"]*'|cut -d'"' -f4 |sed 's/v//')
CLUSTER_OPERATOR_SRC="https://github.com/rabbitmq/cluster-operator/archive/refs/tags/v${CLUSTER_OPERATOR_VERSION}.tar.gz"

curl -sL -o $APP_NAME.tar.gz $CLUSTER_OPERATOR_SRC
rm -rf $APP_NAME
mkdir $APP_NAME && tar -xf "$APP_NAME.tar.gz" -C $APP_NAME --strip-components=1

pushd $APP_NAME
cp -R go.mod go.sum main.go api controllers internal pkg $SPATH
popd

sed -i "s/version=\"[^\"]*\"/version=\"$CLUSTER_OPERATOR_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$CLUSTER_OPERATOR_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$CLUSTER_OPERATOR_VERSION\"/" README.md || exit 1
