#!/usr/bin/env bash

# License: MIT
# Rewritten build script made by:
# Alex Baranowski <aleksander.baranowski@yahoo.pl>
#
# Original script written by:
# - Jarosław Mazurkiewicz <jaroslaw.mazurkiewicz@linuxpolska.pl>
# - Kamil Halat <kh@euro-linux.com>
# - Marek Janosz <marek.janosz@linuxpolska.pl>
# - Radosław Kolba <radoslaw.kolba@linuxpolska.pl>

# Be more strict with errors
set -euo pipefail

# Global vars

BASE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
BASE_ARCH=$(arch)

# Functions

print_help(){
    echo "Usage: $0 <container-name>"
    echo "Try to build a container with the given name and saves it to local with same name"
    exit 1
}

# Print colorized info
print_info(){
    echo -e "\e[1;32m$*\e[0m"
}

print_fail(){
    echo -e "\e[1;31m[FAIL] $*\e[0m"
    exit 1
}

check_command_available(){
    if hash "$1" 2>/dev/null; then
        print_info "[OK] Command $1 is available"
    else
        print_fail "Command $1 is not available. Please install it"
    fi
}

check_file_exists(){
    if [ -f "$1" ]; then
        print_info "[OK] File $1 exists"
    else
        print_fail "File $1 does not exist"
    fi
}

login_to_dockerhub(){
    print_info "Logging in to Dockerhub"
    docker login --username "$DOCKER_USER" --password "$DOCKER_PASS" docker.io
    print_info "Login to Dockerhub done"
}

login_to_quayio(){
    print_info "Logging in to Quay.io"
    docker login --username "$QUAY_USER" --password "$QUAY_PASS" quay.io
    print_info "Login to Quay.io done"
}

prepare_build(){
    if [ -f "$BASE/$container_dir/init.sh" ]; then
        pushd "$BASE/$container_dir"
        print_info "Running init.sh - preparing the build"
        ./init.sh
        print_info "init.sh done"
        popd
    else
        print_info "No init.sh found in at $BASE/$container_dir/init.sh"
    fi
}

read_configs(){
    pushd "$container_dir"
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
        # shellcheck disable=SC1091
        . ./conf.sh
    fi

    DOCKER_TAG_NAME="${image_name}"
    IMAGE_VERSION="${image_version}"
    print_info "DOCKER_TAG_NAME $DOCKER_TAG_NAME"
    print_info "IMAGE_VERSION $IMAGE_VERSION"
    export DOCKER_TAG_NAME IMAGE_VERSION
    popd
}

build_container(){
    pushd "$container_dir"
    print_info "Building container $DOCKER_TAG_NAME"
    mkdir /tmp/docker-build-push/ || sudo rm -rf /tmp/docker-build-push/*
    if [ "$BASE_ARCH" == "x86_64" ]; then
        latest_arch="amd64"
    elif [ "$BASE_ARCH" == "aarch64" ]; then
        latest_arch="arm64"
    else
        print_fail "Unsupported architecture $BASE_ARCH ..."
    fi
    # get epoch time
    epoch_time=$(date +%s)
    DOCKER_TAG_RELEASE="${IMAGE_VERSION}-${epoch_time}"

    docker buildx build \
        --tag "sourcemation/${DOCKER_TAG_NAME}:latest-${latest_arch}" \
        --tag "sourcemation/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch}" \
        --tag "quay.io/sourcemation/${DOCKER_TAG_NAME}:latest-${latest_arch}" \
        --tag "quay.io/sourcemation/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch}" \
        --iidfile /tmp/docker-build-push/iidfile \
        --platform="linux/$latest_arch" \
        --file "./Dockerfile" --no-cache ./
    print_info "Build done"
    popd
}

test_container(){
    set -x
    CONTAINER_FULL_NAME="sourcemation/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch}"
    CONTAINER_STARTUP_TIMEOUT=10

    if [ -f "tests/test_${DOCKER_TAG_NAME}.py" ]; then
      CONTAINER_TEST_FILES="test_linux.py test_${DOCKER_TAG_NAME}.py"
    else
      CONTAINER_TEST_FILES="test_linux.py"
    fi

    CONTAINER_RUN_PARAMETERS=""
    CONTAINER_RUN_COMMAND="/bin/bash"
    case ${DOCKER_TAG_NAME} in
        "postgresql")
            CONTAINER_RUN_COMMAND=""
            CONTAINER_RUN_PARAMETERS="-e POSTGRES_HOST_AUTH_METHOD=trust"
            ;;
        "redis")
            CONTAINER_RUN_COMMAND=""
            ;;
        "rabbitmq")
            CONTAINER_RUN_COMMAND=""
            ;;
        *)
            :
            ;;
    esac

    print_info "Running Docker Container from Image: ${CONTAINER_FULL_NAME}"
    # shellcheck disable=SC2086
    docker run -d -it --name my_container ${CONTAINER_RUN_PARAMETERS} ${CONTAINER_FULL_NAME} ${CONTAINER_RUN_COMMAND}

    print_info "Waiting for the container to fully boot..."
    sleep ""${CONTAINER_STARTUP_TIMEOUT}

    if [ "$(docker inspect -f '{{.State.Running}}' my_container)" != 'true' ]; then
        print_fail "Timeout of ${CONTAINER_STARTUP_TIMEOUT} seconds reached when waiting for my_container to start - aborting."
    fi

    print_info 'Copying PyTest Scripts to Docker Container'
    docker cp tests my_container:/tmp

    print_info 'Installing Python and PyTest in the Container'
    docker exec -u 0 my_container dnf install -y python3-pip
    docker exec -u 0 my_container pip3 install pytest requests psycopg2-binary redis pymongo pika

    print_info 'Executing PyTest Scripts'
    docker exec -u 0 my_container /bin/bash -c "cd /tmp/tests && python3 -m pytest -vv ${CONTAINER_TEST_FILES}" || print_fail "PyTest execution failed"

    docker stop my_container
    docker rm my_container
    set +x
}

push_container_image(){
        # to support multiarch
        # https://stackoverflow.com/questions/74816159/how-can-i-pull-push-the-docker-image-for-all-os-arch-into-dockerhub
        if [ "$BASE_ARCH" == "x86_64" ];then
            latest_arch="amd64"
        elif [ "$BASE_ARCH" == "aarch64" ]; then
            latest_arch="arm64"
        fi
        docker push "sourcemation/${DOCKER_TAG_NAME}:latest-${latest_arch}"
        docker push "sourcemation/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch}"
        docker push "quay.io/sourcemation/${DOCKER_TAG_NAME}:latest-${latest_arch}"
        docker push "quay.io/sourcemation/${DOCKER_TAG_NAME}:${DOCKER_TAG_NAME}-${DOCKER_TAG_RELEASE}-${latest_arch}"
        # Note in the future must start with aarch64 and other builds then push
        # x86_64. We do not have podman farm or similar solution
        if [ "$BASE_ARCH" == "x86_64" ];then
            docker manifest rm "docker.io/sourcemation/${DOCKER_TAG_NAME}:latest" || true
            docker manifest create "docker.io/sourcemation/${DOCKER_TAG_NAME}:latest" --amend "docker.io/sourcemation/${DOCKER_TAG_NAME}:latest-amd64"
            docker manifest push "docker.io/sourcemation/${DOCKER_TAG_NAME}:latest"
            docker manifest rm "quay.io/sourcemation/${DOCKER_TAG_NAME}:latest" || true
            docker manifest create "quay.io/sourcemation/${DOCKER_TAG_NAME}:latest" --amend "quay.io/sourcemation/${DOCKER_TAG_NAME}:latest-amd64"
            docker manifest push "quay.io/sourcemation/${DOCKER_TAG_NAME}:latest"
        fi
}

push_readme(){

    # preapre the binary
    if [ "$BASE_ARCH" == "x86_64" ];then
        bin_arch="amd64"
    elif [ "$BASE_ARCH" == "aarch64" ]; then
        bin_arch="arm64"
    fi
    binary_url="https://github.com/christian-korneck/docker-pushrm/releases/download/v1.9.0/docker-pushrm_linux_${bin_arch}"
    mkdir -p ~/.docker/cli-plugins
    curl -L  "${binary_url}" -o ~/.docker/cli-plugins/docker-pushrm
    chmod +x ~/.docker/cli-plugins/docker-pushrm

    # push the README.md
    pushd "$container_dir"
    print_info "Pushing README.md to dockerhub"
    docker pushrm "docker.io/sourcemation/${DOCKER_TAG_NAME}"

    print_info "Pushing README.md to quay.io"
    docker pushrm "quay.io/sourcemation/${DOCKER_TAG_NAME}"

    popd
}


cleanup(){
        docker logout docker.io
        docker logout quay.io
}
# main


if [ $# -ne 1 ]; then
    print_help
else
        container_name=$1
fi

container_dir="images/$container_name"
container_file="$container_dir/Dockerfile"
set -euo pipefail


# Build the container
print_info "Build information for container $container_name"
print_info "-> Container directory: $container_dir"

print_info "Checking prerequisites"
check_command_available "docker"
check_file_exists "$container_file"
check_file_exists "$container_dir/README.md"
[ "$PUSH_IMAGE" != "true" ] || login_to_quayio
[ "$PUSH_IMAGE" != "true" ] || login_to_dockerhub
prepare_build # Run init.sh if it exists
read_configs
build_container
[ "$TEST_IMAGE" != "true" ] || test_container
[ "$PUSH_IMAGE" != "true" ] || push_container_image
[ "$PUSH_IMAGE" != "true" ] || push_readme
cleanup
