#!/usr/bin/env bash

set -eou pipefail


mkdir -p common-scripts
curl -L https://raw.githubusercontent.com/apache/kafka/3.8.0/docker/docker_official_images/3.7.0/jvm/resources/common-scripts/bash-config -o common-scripts/bash-config
curl -L https://raw.githubusercontent.com/apache/kafka/3.8.0/docker/docker_official_images/3.7.0/jvm/resources/common-scripts/configure -o common-scripts/configure
curl -L https://raw.githubusercontent.com/apache/kafka/3.8.0/docker/docker_official_images/3.7.0/jvm/resources/common-scripts/configureDefaults -o common-scripts/configureDefaults
curl -L https://raw.githubusercontent.com/apache/kafka/3.8.0/docker/docker_official_images/3.7.0/jvm/resources/common-scripts/run -o common-scripts/run

curl -LO https://raw.githubusercontent.com/apache/kafka/trunk/docker/docker_official_images/3.7.0/jvm/jsa_launch
curl -LO https://raw.githubusercontent.com/apache/kafka/3.8.0/docker/docker_official_images/3.7.0/jvm/launch
chmod +x common-scripts/configureDefaults common-scripts/configure common-scripts/run jsa_launch launch
