#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2024-04-10
# -----------------------------------

set -eu

echo "Pulling RabbitMQ 4 image..."
docker pull sourcemation/rabbitmq-4:latest
echo "RabbitMQ 4 image pulled successfully. Checking version from the image..."

RABBITMQ_VERSION=$(docker run --rm sourcemation/rabbitmq-4:latest env | grep APP_VERSION |awk -F'=' '{print $2}' | tr -d '\r')

echo "Version is '$RABBITMQ_VERSION'"

if [[ ! "$RABBITMQ_VERSION" =~ ^4\. ]]; then
    echo "Version 4 is no more! Check the EOL status at https://endoflife.date/rabbitmq"
    exit 1
fi

sed -i "s/version=\"[^\"]*\"/version=\"$RABBITMQ_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$RABBITMQ_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$RABBITMQ_VERSION\"/" README.md || exit 1
