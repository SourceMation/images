#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-29
# -----------------------------------

set -eu

SPATH=$(pwd)

APP_NAME="default-credential-updater"

echo "-> Preparing rabbitmq-default-credential-updater"
CREDENTIAL_UPDATER_VER_URL="https://api.github.com/repos/rabbitmq/default-user-credential-updater/releases/latest"
CREDENTIAL_UPDATER_VERSION=$(curl -sL ${CREDENTIAL_UPDATER_VER_URL} |grep -o '"tag_name": "[^"]*'|cut -d'"' -f4 |sed 's/v//')
CREDENTIAL_UPDATER_SRC="https://github.com/rabbitmq/default-user-credential-updater/archive/refs/tags/v${CREDENTIAL_UPDATER_VERSION}.tar.gz"

curl -sL -o $APP_NAME.tar.gz $CREDENTIAL_UPDATER_SRC
mkdir $APP_NAME && tar -xf "$APP_NAME.tar.gz" -C $APP_NAME --strip-components=1

sed -i "s/version=\"[^\"]*\"/version=\"$CREDENTIAL_UPDATER_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$CREDENTIAL_UPDATER_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$CREDENTIAL_UPDATER_VERSION\"/" README.md || exit 1
