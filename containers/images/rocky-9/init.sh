#!/usr/bin/env bash

# Author: Alex Baranowski
# License: MIT
# Description: This script is used create a base rootfs for a container.

# TODO: We can change rocky from EuroLinux to sourcemation rocky after first build

set -euo pipefail

cleanup() {
    docker rm -f podman_build
}
trap cleanup EXIT

docker run --name podman_build -d --privileged -v /dev/shm:/dev/shm -it -v $(pwd):/tmp/code eurolinux/rocky-9:latest
docker exec podman_build /bin/bash -c "cd /tmp/code && ./mk-image-podman.sh"
docker cp podman_build:/tmp/base-image.tar.gz .
