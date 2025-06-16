# This file is a simple library for common functions used in container image
# build scripts. It's imported to the main script using the `source` or `.`
# command :).

# License: MIT
# Author: Alex Baranowski and others


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
    # disable shellcheck as script should set exit on error
    # shellcheck disable=SC2154
    if [ -f "$BASE/$container_dir/init.sh" ]; then
        # shellcheck disable=SC2164
        pushd "$BASE/$container_dir"
        print_info "Running init.sh - preparing the build"
        ./init.sh
        print_info "init.sh done"
        # disable shellcheck as script should set exit on error
        # shellcheck disable=SC2164
        popd
    else
        print_info "No init.sh found in at $BASE/$container_dir/init.sh"
    fi
}


read_configs(){
    # disable shellcheck as script should set exit on error
    # shellcheck disable=SC2164
    pushd "$container_dir"
    if [ -f ./Dockerfile ]; then
        echo "Look into Dockerfile"
        # find the line, then get only value between "..", then  remove "
        # LABEL name="init" -> "init" -> init
        print_info "Trying to get image name from Dockerfile"
        image_name=$(grep "LABEL name=" Dockerfile | grep -o '".*"' | tr -d '"' )
        # version="3.9.18" -> "3.9.18" -> 3.9.18
        print_info "Trying to get image version from Dockerfile"
        image_version=$(grep "  version=" Dockerfile | grep -o '".*"' | tr -d '"')
    else
        print_fail "There is no Dockerfile in this directory!"
    fi
    # so basically set image_name image_version here
    if [ -f ./conf.sh  ]; then
        # shellcheck disable=SC1091
        . ./conf.sh
    fi

    IMAGE_NAME="${image_name}"
    IMAGE_VERSION="${image_version}"

    print_info "Checking if DOCKER_TAG_SUFFIX for multipe tag build is set"
    if [[ ! -v DOCKER_TAG_SUFFIX ]]; then
        print_info "DOCKER_TAG_SUFFIX is not set. Setting DOCKER_TAG_SUFFIX as empty string"
        DOCKER_TAG_SUFFIX=""
    else
        print_info "DOCKER_TAG_SUFFIX is set to $DOCKER_TAG_SUFFIX -> we won't push that latest tag!"
        # Add - in front of docker suffix so it's easier to use when setting tags. That's why there is no '-' in front of it
        DOCKER_TAG_SUFFIX="-${DOCKER_TAG_SUFFIX}"
    fi

    print_info "IMAGE_NAME $IMAGE_NAME"
    print_info "IMAGE_VERSION $IMAGE_VERSION"
    export IMAGE_NAME IMAGE_VERSION
    # disable shellcheck as script should set exit on error
    # shellcheck disable=SC2164
    popd
}
