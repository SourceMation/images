#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2024-04-10
# -----------------------------------

set -eu

echo "-> Preparing rabbitmq variables"
RABBITMQ_VER_SRC="https://api.github.com/repos/rabbitmq/rabbitmq-server/releases/latest"
RABBITMQ_VERSION=$(curl -s ${RABBITMQ_VER_SRC} |grep -o '"tag_name": "[^"]*'|cut -d'"' -f4 |sed 's/v//')

if [[ ! "$RABBITMQ_VERSION" =~ ^4\. ]]; then
    echo "Version 4 is no more! Check the EOL status at https://endoflife.date/rabbitmq"
    exit 1
fi

sed -i "s#^ARG RABBITMQ_VERSION=.*#ARG RABBITMQ_VERSION=${RABBITMQ_VERSION}#" Dockerfile || exit 1
sed -i "s/version=\"[^\"]*\"/version=\"$RABBITMQ_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$RABBITMQ_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$RABBITMQ_VERSION\"/" README.md || exit 1
