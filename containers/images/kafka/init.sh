#!/usr/bin/env bash

set -eou pipefail

echo "-> Preparing kafka variables"
KAFKA_VERSION=$(curl -sL https://downloads.apache.org/kafka/ | grep -oP '\d+\.\d+\.\d+' | sort -V | tail -1)

echo "Latest version of Kafka is $KAFKA_VERSION"

# Updating the version in Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$KAFKA_VERSION\"/" Dockerfile || exit 1
sed -i "s#ENV kafka_url=.*#ENV kafka_url=https://downloads.apache.org/kafka/$KAFKA_VERSION/kafka_2.13-$KAFKA_VERSION.tgz#" Dockerfile || exit 1

# Updating the version in README.md
sed -i "s/Apache Kafka [0-9.]*)/Apache Kafka $KAFKA_VERSION)/" README.md || exit 1
sed -i "s#blob/[0-9.]*/LICENSE-binary#blob/$KAFKA_VERSION/LICENSE-binary#" README.md || exit 1

# Download latest KEYS
curl -L https://downloads.apache.org/kafka/KEYS -o KEYS

mkdir -p common-scripts
curl -L https://raw.githubusercontent.com/apache/kafka/$KAFKA_VERSION/docker/docker_official_images/3.7.0/jvm/resources/common-scripts/bash-config -o common-scripts/bash-config
curl -L https://raw.githubusercontent.com/apache/kafka/$KAFKA_VERSION/docker/docker_official_images/3.7.0/jvm/resources/common-scripts/configure -o common-scripts/configure
curl -L https://raw.githubusercontent.com/apache/kafka/$KAFKA_VERSION/docker/docker_official_images/3.7.0/jvm/resources/common-scripts/configureDefaults -o common-scripts/configureDefaults
curl -L https://raw.githubusercontent.com/apache/kafka/$KAFKA_VERSION/docker/docker_official_images/3.7.0/jvm/resources/common-scripts/run -o common-scripts/run

curl -LO https://raw.githubusercontent.com/apache/kafka/$KAFKA_VERSION/docker/docker_official_images/3.7.0/jvm/jsa_launch
curl -LO https://raw.githubusercontent.com/apache/kafka/$KAFKA_VERSION/docker/docker_official_images/3.7.0/jvm/launch

# Fix paths in jsa_launch for Kafka 4.x
sed -i 's/config\/kraft\//config\//g' jsa_launch
sed -i 's/opt\/kafka/\/opt\/kafka/g' jsa_launch

# Set KRaft defaults in configureDefaults
sed -i '/"CLUSTER_ID"]="5L6g3nShT-eMCtK--X86sw"/a \  ["KAFKA_PROCESS_ROLES"]="broker,controller"\n  ["KAFKA_NODE_ID"]="1"\n  ["KAFKA_CONTROLLER_QUORUM_VOTERS"]="1@localhost:9093"\n  ["KAFKA_CONTROLLER_LISTENER_NAMES"]="CONTROLLER"\n  ["KAFKA_LISTENERS"]="PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093"\n  ["KAFKA_ADVERTISED_LISTENERS"]="PLAINTEXT://localhost:9092"\n  ["KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR"]="1"\n  ["KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR"]="1"\n  ["KAFKA_TRANSACTION_STATE_LOG_MIN_ISR"]="1"' common-scripts/configureDefaults

chmod +x common-scripts/configureDefaults common-scripts/configure common-scripts/run jsa_launch launch
