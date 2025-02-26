#!/usr/bin/env bash

# This script is login to dockerhub and quay.io then uses
# docker pushrm to push README.md to dockerhub and quay.io
# Author: Alex Baranowski <aleksander.baranowski@linuxpolska.pl>

set -euo pipefail




push_docker_hub(){
    echo "Pushing README.md to dockerhub"
    docker pushrm "docker.io/eurolinux/$DOCKER_TAG_NAME"
}

push_quay_io(){
    echo "Pushing README.md to quay.io"
    docker pushrm "quay.io/eurolinux/$DOCKER_TAG_NAME"
}


read_configs(){
    if [ -f ./Dockerfile ]; then
        echo "Look into Dockerfile"
        # find the line, then get only value between "..", then  remove "
        # LABEL name="init" -> "init" -> init
        image_name=$(grep "LABEL name=" Dockerfile | grep -o '".*"' | tr -d '"' )
        # version="3.9.18" -> "3.9.18" -> 3.9.18
        image_version=$(grep "  version=" Dockerfile | grep -o '".*"' | tr -d '"')
    else
        echo "There is no Dockerfile in this directory!"
        exit 1
    fi
    # so basiclly set image_name image_version here
    if [ -f ./conf.sh  ]; then
        . ./conf.sh
    fi

    if grep -sq 'eurolinux-' <<< "$image_name"; then
        echo "Image name ${image_name} contains 'eurolinux-' the docker_tag_name won't have eurolinux-9- prefix!"
        DOCKER_TAG_NAME="${image_name}"
    else
        export DOCKER_TAG_NAME="eurolinux-9-${image_name}"
    fi
    echo "DOCKER_TAG_NAME $DOCKER_TAG_NAME"
}

set +u
if [ -z "$dev_mode" ]; then
    set -u
    # Login to dockerhub
    docker login --username="$DOCKERHUB_CREDS_USR" --password="$DOCKERHUB_CREDS_PSW" docker.io
    # Login to quay.io
    docker login --username="$QUAYIO_CREDS_USR" --password="$QUAYIO_CREDS_PSW" quay.io
    export APIKEY__QUAY_IO="$QUAY_IO_DOCKER_PUSHRM_TOKEN"
else
    echo "dev_mode is set to true, exiting without pushing README.md and status 1"
    exit 1
fi

config_directory="$(echo "$1" | sed 's#arm64-##')"
name="$(basename "$config_directory")"

echo "Pushing README.md to dockerhub and quay.io for $name"

cd "$name"
read_configs
push_docker_hub
push_quay_io
