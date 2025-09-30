#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-30
# -----------------------------------

set -eu

SPATH=$(pwd)

APP_NAME="rabbitmq-messaging-topology-operator"

echo "-> Preparing rabbitmq-messaging-topology-operator"
MSG_TOPOLOGY_OPER_VER_URL="https://api.github.com/repos/rabbitmq/messaging-topology-operator/releases/latest"
MSG_TOPOLOGY_OPER_VERSION=$(curl -sL ${MSG_TOPOLOGY_OPER_VER_URL} |grep -o '"tag_name": "[^"]*'|cut -d'"' -f4 |sed 's/v//')
MSG_TOPOLOGY_OPER_SRC="https://github.com/rabbitmq/messaging-topology-operator/archive/refs/tags/v${MSG_TOPOLOGY_OPER_VERSION}.tar.gz"

curl -sL -o $APP_NAME.tar.gz $MSG_TOPOLOGY_OPER_SRC
mkdir $APP_NAME && tar -xf "$APP_NAME.tar.gz" -C $APP_NAME --strip-components=1

sed -i "s/version=\"[^\"]*\"/version=\"$MSG_TOPOLOGY_OPER_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$MSG_TOPOLOGY_OPER_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$MSG_TOPOLOGY_OPER_VERSION\"/" README.md || exit 1
