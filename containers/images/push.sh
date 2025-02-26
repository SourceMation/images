#!/usr/bin/env bash
#
# Author: Alex Baranowski <ab@euro-linux.com>
#         Kamil Halat <kh@euro-linux.com>
#         Radosław Kolba <rk@euro-linux.com>
#         Jarosław Mazurkiewicz <jaroslaw.mazurkiewicz@linuxpolska.pl>
#         Marek Janosz <marek.janosz@linuxpolska.pl>

BASE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
BASE_ARCH=$(arch)

config_directory="$(echo $1 | sed 's#arm64-##')"
name="$(basename "$config_directory")"

# Dev mode is active if any second argument is added to this script
# In this mode logging into Docker Hub and deploying images are deactivated
[[ $# -eq 2 ]] && dev_mode=$2

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

    DOCKER_TAG_RELEASE="$image_version"
    if grep -sq 'eurolinux-' <<< "$image_name"; then
        echo "Image name ${image_name} contains 'eurolinux-' the docker_tag_name won't have eurolinux-9- prefix!"
        DOCKER_TAG_NAME="${image_name}"
    else
        DOCKER_TAG_NAME="eurolinux-9-${image_name}"
    fi
    echo "DOCKER_TAG_NAME $DOCKER_TAG_NAME"
}

docker_push(){
    [ -n "$dev_mode" ] && return
    # Login to dockerhub
    docker login --username=$DOCKERHUB_CREDS_USR --password=$DOCKERHUB_CREDS_PSW docker.io
    # Login to quay.io
    docker login --username=$QUAYIO_CREDS_USR --password=$QUAYIO_CREDS_PSW quay.io
    # Docker push
    if hash podman; then
        # to support multiarch
        # https://stackoverflow.com/questions/74816159/how-can-i-pull-push-the-docker-image-for-all-os-arch-into-dockerhub
        if [ "$BASE_ARCH" == "x86_64" ];then
            latest_arch="amd64"
        elif [ "$BASE_ARCH" == "aarch64" ]; then
            latest_arch="arm64"
        fi
        docker push docker.io/eurolinux/${DOCKER_TAG_NAME}:latest-${latest_arch} docker://docker.io/eurolinux/${DOCKER_TAG_NAME}:latest-${latest_arch}
        docker push docker.io/eurolinux/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch} docker://docker.io/eurolinux/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch}
        docker push quay.io/eurolinux/${DOCKER_TAG_NAME}:latest-${latest_arch}
        docker push quay.io/eurolinux/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch}
        if [ "$BASE_ARCH" == "x86_64" ];then
           docker manifest rm docker.io/eurolinux/${DOCKER_TAG_NAME}:latest || true
           docker manifest rm quay.io/eurolinux/${DOCKER_TAG_NAME}:latest || true
           docker manifest create docker.io/eurolinux/${DOCKER_TAG_NAME}:latest --amend docker.io/eurolinux/${DOCKER_TAG_NAME}:latest-amd64
           docker manifest push docker.io/eurolinux/${DOCKER_TAG_NAME}:latest docker://docker.io/eurolinux/${DOCKER_TAG_NAME}:latest
           # reuse the docker.ioa manifest
           # docker manifest create quay.io/eurolinux/${DOCKER_TAG_NAME}:latest --amend quay.io/eurolinux/${DOCKER_TAG_NAME}:latest-arm64 --amend quay.io/eurolinux/${DOCKER_TAG_NAME}:latest-amd64
           docker manifest push docker.io/eurolinux/${DOCKER_TAG_NAME}:latest quay.io/eurolinux/${DOCKER_TAG_NAME}:latest
        fi
    else
        # EL 7 && EL8 uses docker
        docker push eurolinux/${DOCKER_TAG_NAME}:latest
        docker push eurolinux/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}
        docker push quay.io/eurolinux/${DOCKER_TAG_NAME}:latest
        docker push quay.io/eurolinux/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}
    fi
    docker logout docker.io
    docker logout quay.io

    echo "Update docker tag for this and remote repository"
}

set -eo pipefail
echo "$name"

cd $name
read_configs
docker_push
cd ..

if hash podman; then
    podman system reset -f || true
fi
exit 0
