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
container_dir="auto_containers/images/$name"
config_file="auto_containers/images/$name/conf.sh"

# Dev mode is active if any second argument is added to this script
# In this mode logging into Docker Hub and deploying images are deactivated
[[ $# -eq 2 ]] && dev_mode=$2

prepare_build(){
    # Run init.sh if script exists
    [ -f "$BASE/$config_directory/init.sh" ] && (cd "$BASE/$config_directory" && ./init.sh) || echo "There is no init.sh.."
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

    DOCKER_TAG_RELEASE="$image_version"
    if grep -sq 'eurolinux-' <<< "$image_name"; then
        echo "Image name ${image_name} contains 'eurolinux-' the docker_tag_name won't have eurolinux-9- prefix!"
        DOCKER_TAG_NAME="${image_name}"
    else
        DOCKER_TAG_NAME="eurolinux-9-${image_name}"
    fi
    echo "DOCKER_TAG_NAME $DOCKER_TAG_NAME"
}

docker_check(){
    curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin
    set +e
    grype dir:./ --fail-on medium || touch ../warning.status && grype dir:./ -o template -t ../html.tmpl > grype_${image_name:12:-3}.html
    set -e
}

docker_build(){

    if [ -z "$dev_mode" ]; then
        # Login to dockerhub
        docker login --username=$DOCKERHUB_CREDS_USR --password=$DOCKERHUB_CREDS_PSW docker.io
        # Login to quay.io
        docker login --username=$QUAYIO_CREDS_USR --password=$QUAYIO_CREDS_PSW quay.io
    fi
    echo "Using pre-created Dockerfiles"
    # Prepare build dir
    mkdir /tmp/docker-build-push/ || sudo rm -rf /tmp/docker-build-push/*


    # Docker build
    if hash podman; then
        # to support multiarch
        # https://stackoverflow.com/questions/74816159/how-can-i-pull-push-the-docker-image-for-all-os-arch-into-dockerhub
        if [ "$BASE_ARCH" == "x86_64" ];then
            latest_arch="amd64"
        elif [ "$BASE_ARCH" == "aarch64" ]; then
            latest_arch="arm64"
        fi
        podman build \
            --tag docker.io/eurolinux/${DOCKER_TAG_NAME}:latest-${latest_arch} \
            --tag docker.io/eurolinux/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch} \
            --tag quay.io/eurolinux/${DOCKER_TAG_NAME}:latest-${latest_arch} \
            --tag quay.io/eurolinux/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch} \
            --iidfile /tmp/docker-build-push/iidfile \
            --platform="linux/$latest_arch" \
            --file "./Dockerfile" --no-cache ./
    else
        # EL 7 && EL8 uses docker
        docker buildx build \
            --tag eurolinux/${DOCKER_TAG_NAME}:latest \
            --tag eurolinux/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE} \
            --tag quay.io/eurolinux/${DOCKER_TAG_NAME}:latest \
            --tag quay.io/eurolinux/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE} \
            --iidfile /tmp/docker-build-push/iidfile \
            --platform="linux/$latest_arch" \
            --metadata-file /tmp/docker-build-push/metadata-file \
            --file "./Dockerfile" --no-cache --output type=docker ./
    fi

    if [ -z "$dev_mode" ]; then
        docker logout docker.io
        docker logout quay.io
    fi
}

docker_test(){
    [ -f "$BASE/$config_directory/test.sh" ] || return 0
    # Exporting vars to allow script to use them outside of push.sh
    export latest_arch
    export DOCKER_TAG_NAME
    cd "$BASE/$config_directory"
    ./test.sh
}

docker_save(){
    [ "$IMG_TYPE" == "tar" ] || return 0

    if hash podman; then
        podman save > $DOCKER_TAG_NAME.tar quay.io/eurolinux/${DOCKER_TAG_NAME}:latest
    else
        docker save > $DOCKER_TAG_NAME.tar quay.io/eurolinux/${DOCKER_TAG_NAME}:latest
    fi
    cp -f "$DOCKER_TAG_NAME.tar" /containers
}


set -eo pipefail
echo "$name"

cd $name
prepare_build
read_configs
docker_check
docker_build
docker_test
docker_save
cd ..

exit 0