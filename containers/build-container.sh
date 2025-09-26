#!/usr/bin/env bash

# License: MIT
# Rewritten build script made by:
# Alex Baranowski <aleksander.baranowski@yahoo.pl>
#
# Original script written by:
# - Jarosław Mazurkiewicz <jaroslaw.mazurkiewicz@linuxpolska.pl>
# - Kamil Halat <kh@euro-linux.com>
# - Marek Janosz <marek.janosz@linuxpolska.pl>
# - Radosław Kolba <rk@euro-linux.com>

# Be more strict with errors
set -euo pipefail
arch(){ uname -m; }

# Global vars

BASE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Source the lib.sh
. "${BASE}/lib.sh"

BASE_ARCH=$(arch)
# create unique name
CONTAINER_NAME="container-$(date +%s)"

# set to false in the check variables if push_readme is set to true, and everything else is false
BUILD_CONTAINER="true"

# This way we can set entrypoint on invocation
ENTRYPOINT_CMD="${ENTRYPOINT_CMD:-}"


# Functions

print_help(){
    echo "Usage: $0 <container-name>"
    echo "Try to build a container with the given name and saves it to local with same name"
    exit 1
}

check_variables_set_build_container(){
    print_info "TEST_IMAGE is set ${TEST_IMAGE}"
    print_info "PUSH_IMAGE is set ${PUSH_IMAGE}"
    print_info "PUSH_README is set ${PUSH_README}"
    # It's nasty :)
    if [[ "$TEST_IMAGE" == "false" && "$PUSH_IMAGE" == "false" && "$PUSH_README" == "true" ]]; then
        BUILD_CONTAINER="false"
    fi
}


build_container(){
    # That's nasty too
    UNSUPPORTED_IMAGES="mysql-aarch64 "
    if [[ " $UNSUPPORTED_IMAGES " == *" $IMAGE_NAME-$BASE_ARCH "* ]]; then
        print_info "Architecture $BASE_ARCH is not supported for $IMAGE_NAME image!"
        exit 0
    fi
    
    pushd "$container_dir"
    print_info "Building container $IMAGE_NAME"
    mkdir /tmp/docker-build-push/ || sudo rm -rf /tmp/docker-build-push/*
    if [ "$BASE_ARCH" == "x86_64" ]; then
        latest_arch="amd64"
    elif [ "$BASE_ARCH" == "aarch64" ]; then
        latest_arch="arm64"
    else
        print_fail "Unsupported architecture $BASE_ARCH ..."
    fi

    current_time=$(date +%s)
    midnight=$(date -d "tomorrow 00:00:00" +%s)
    if (( midnight - current_time < 1800 )); then
        print_fail "Less than 30 minutes to midnight, refusing to build to avoid tag issues."
    fi

    # This might be problematic when the date switches to the next day!
    B_DATE=$(date +%Y%m%d)

    DOCKER_TAG_LATEST="${IMAGE_NAME}:latest-${latest_arch}${DOCKER_TAG_SUFFIX}"
    DOCKER_TAG_VERSION="${IMAGE_NAME}:${IMAGE_VERSION}${DOCKER_TAG_SUFFIX}"
    DOCKER_TAG_BUILD_VER_NO_ARCH="${IMAGE_NAME}:${IMAGE_VERSION}-${B_DATE}${DOCKER_TAG_SUFFIX}"
    DOCKER_TAG_BUILD="${IMAGE_NAME}:${IMAGE_VERSION}-${B_DATE}${DOCKER_TAG_SUFFIX}-${latest_arch}"

    docker buildx build \
        --tag "sourcemation/$DOCKER_TAG_LATEST" \
        --tag "sourcemation/$DOCKER_TAG_VERSION" \
        --tag "sourcemation/$DOCKER_TAG_BUILD" \
        --tag "quay.io/sourcemation/$DOCKER_TAG_LATEST" \
        --tag "quay.io/sourcemation/$DOCKER_TAG_VERSION" \
        --tag "quay.io/sourcemation/$DOCKER_TAG_BUILD" \
        --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
        --iidfile /tmp/docker-build-push/iidfile \
        --platform="linux/$latest_arch" \
        --file "./Dockerfile" --no-cache ./

    print_info "Build done"
    popd
}

test_container(){
    print_info "Testing container $IMAGE_NAME"
    set -x
    CONTAINER_FULL_NAME="sourcemation/$DOCKER_TAG_BUILD"
    # THIS can be set in the conf.sh file
    CONTAINER_STARTUP_TIMEOUT=${CONTAINER_STARTUP_TIMEOUT:-10}
    # default test
    CONTAINER_TEST_FILES="test_linux.py"
    # Extra tests
    if [ -f "tests/test_${IMAGE_NAME}.py" ]; then
        CONTAINER_TEST_FILES+=" test_${IMAGE_NAME}.py"
    fi

    if [ "${DOCKER_TAG_SUFFIX}" != "" ] && [ -f "tests/test_${IMAGE_NAME}${DOCKER_TAG_SUFFIX}.py" ]; then
            CONTAINER_TEST_FILES+=" test_${IMAGE_NAME}${DOCKER_TAG_SUFFIX}.py"
    fi

    # Python do not like the modules with '.' in the name so we have to fix it
    if [[ "${IMAGE_NAME}" =~ python-3. ]]; then
        CONTAINER_TEST_FILES+=" test_python.py"
    fi
    # same for golang
    if [[ "${IMAGE_NAME}" =~ golang-1 ]]; then
        CONTAINER_TEST_FILES+=" test_golang.py"
    fi
    # cnpg tests should also contain postgresql tests
    if [[ "${IMAGE_NAME}" =~ cnpg ]]; then
        CONTAINER_TEST_FILES+=" test_postgresql.py"
    fi

    CONTAINER_RUN_PARAMETERS=""
    # We should use CONTAINER_RUN_COMMAND only if it's not defined in conf.sh file that why there is no :-
    CONTAINER_RUN_COMMAND=${CONTAINER_RUN_COMMAND-"/bin/bash"}
    case ${IMAGE_NAME} in
        "alertmanager")
            CONTAINER_RUN_COMMAND=""
            ;;
        "apache-activemq")
            CONTAINER_RUN_COMMAND=""
            ;;
        "apache")
            CONTAINER_RUN_COMMAND=""
            CONTAINER_RUN_PARAMETERS="-p 8080:8080"
            ;;
        "apicast")
            CONTAINER_RUN_COMMAND="apicast start --dev"
            CONTAINER_RUN_PARAMETERS="--ulimit nofile=64000:64000 --ulimit nproc=64000:64000 -p 8080:8080"
            ;;
        "camel-k")
            CONTAINER_RUN_COMMAND=""
            ;;
        "camel-karavan")
            CONTAINER_RUN_COMMAND=""
            CONTAINER_RUN_PARAMETERS="-v /var/run/docker.sock:/var/run/docker.sock"
            ;;
        cnpg-*)
            CONTAINER_RUN_COMMAND=""
            CONTAINER_RUN_PARAMETERS="-e POSTGRES_HOST_AUTH_METHOD=trust"
            ;;
        "elasticsearch")
            CONTAINER_RUN_COMMAND="-E discovery.type=single-node -E xpack.security.enabled=false -E xpack.security.http.ssl.enabled=false"
            ;;
        "etcd")
            CONTAINER_RUN_COMMAND=""
            ;;
        "external-dns")
            ENTRYPOINT_CMD=--entrypoint=""
            ;;
        "grafana")
            CONTAINER_RUN_COMMAND=""
            ;;
        "helidon")
            CONTAINER_RUN_COMMAND=""
            ;;
        "hugo")
            CONTAINER_RUN_COMMAND=""
            ENTRYPOINT_CMD=--entrypoint="/bin/bash"
            ;;
        "kafka")
            CONTAINER_RUN_COMMAND=""
            ;;
        "kibana")
            CONTAINER_RUN_COMMAND=""
            ;;
        "kong")
            CONTAINER_RUN_COMMAND=""
            ;;
        "manageiq")
            CONTAINER_RUN_COMMAND=""
            ;;
        "metrics-server")
            ENTRYPOINT_CMD=--entrypoint=""
           ;;
        "micronaut")
            CONTAINER_RUN_COMMAND=""
            ;;
        "minio")
            CONTAINER_RUN_COMMAND="server /data --console-address :9001"
            ;;
        "mosquitto")
            CONTAINER_RUN_COMMAND=""
            ;;
        nginx*)
            CONTAINER_RUN_COMMAND=""
            ;;
        "node_exporter")
            CONTAINER_RUN_COMMAND=""
            ;;
        "openldap")
            CONTAINER_RUN_COMMAND=""
            CONTAINER_RUN_PARAMETERS="-e LDAP_ADMIN_PASSWORD=admin -e LDAP_DOMAIN=mycompany.com -e LDAP_ORGANISATION=my-company"
            ;;
        "postgresql")
            CONTAINER_RUN_COMMAND=""
            CONTAINER_RUN_PARAMETERS="-e POSTGRES_HOST_AUTH_METHOD=trust"
            ;;
        "pgpool")
            CONTAINER_RUN_COMMAND=""
            CONTAINER_RUN_PARAMETERS="-e PGPOOL_PARAMS_BACKEND_HOSTNAME0='test_hostname'"
            ;;
        postgres-*)
            CONTAINER_RUN_COMMAND=""
            CONTAINER_RUN_PARAMETERS="-e POSTGRES_HOST_AUTH_METHOD=trust"
            ;;
        "prometheus")
            CONTAINER_RUN_COMMAND="--storage.tsdb.path=/prometheus --config.file=/etc/prometheus/prometheus.yml --web.enable-lifecycle"
            ;;
        "prometheus-operator")
            CONTAINER_RUN_COMMAND=""
            ;;
        "redis")
            CONTAINER_RUN_COMMAND=""
            ;;
        "redis-sentinel")
            CONTAINER_RUN_COMMAND=""
            ;;
        "rabbitmq")
            CONTAINER_RUN_COMMAND=""
            ;;
        "rabbitmq-4")
            CONTAINER_RUN_COMMAND=""
            ;;
        "rabbitmq-4-management")
            CONTAINER_RUN_COMMAND=""
            ;;
        "quarkus")
            CONTAINER_RUN_COMMAND=""
            ;;
        "servicemix")
            CONTAINER_RUN_COMMAND=""
            ;;
        *)
            :
            ;;
    esac

    print_info "Running Docker Container from Image: ${CONTAINER_FULL_NAME}"
    if [ "${IMAGE_NAME}" == "kong" ]; then
        docker network create kong-net
        docker run -d --name kong-database --network=kong-net -p 5432:5432 -e "POSTGRES_USER=kong" -e "POSTGRES_DB=kong" -e "POSTGRES_PASSWORD=kongpass" postgres:13
        docker run --rm --network=kong-net -e "KONG_DATABASE=postgres" -e "KONG_PG_HOST=kong-database" -e "KONG_PG_PASSWORD=kongpass" -e "KONG_PASSWORD=test" "${CONTAINER_FULL_NAME}" kong migrations bootstrap

        docker run -d --name "$CONTAINER_NAME" \
            --network=kong-net \
            -e "KONG_DATABASE=postgres" \
            -e "KONG_PG_HOST=kong-database" \
            -e "KONG_PG_USER=kong" \
            -e "KONG_PG_PASSWORD=kongpass" \
            -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
            -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
            -e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
            -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
            -e "KONG_ADMIN_LISTEN=0.0.0.0:8001" \
            -e "KONG_ADMIN_GUI_URL=http://localhost:8002" \
            -e KONG_LICENSE_DATA \
            -p 8000:8000 \
            -p 8443:8443 \
            -p 8001:8001 \
            -p 8444:8444 \
            -p 8002:8002 \
            -p 8445:8445 \
            -p 8003:8003 \
            -p 8004:8004 \
            "${CONTAINER_FULL_NAME}"
    elif [ "${IMAGE_NAME}" == "postgres-repmgr" ]; then
        docker network create postgres-repmgr-net
        
        docker run -d --network postgres-repmgr-net --name "${CONTAINER_NAME}" \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=mysecretpassword \
        -e REPMGR_ROLE=primary \
        -e REPMGR_USER=repmgr \
        -e REPMGR_PASSWORD=repmgrpass \
        -e REPMGR_DB=repmgr \
        -e NODE_ID=1 \
        -e NODE_NAME="${CONTAINER_NAME}" \
        "${CONTAINER_FULL_NAME}"

        sleep 15

        docker run -d --network postgres-repmgr-net --name "${CONTAINER_NAME}-standby" \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=mysecretpassword \
        -e REPMGR_ROLE=standby \
        -e REPMGR_USER=repmgr \
        -e REPMGR_PASSWORD=repmgrpass \
        -e REPMGR_DB=repmgr \
        -e REPMGR_UPSTREAM_NAME="${CONTAINER_NAME}" \
        -e NODE_ID=2 \
        -e NODE_NAME="${CONTAINER_NAME}-standby" \
        "${CONTAINER_FULL_NAME}"
    else
        print_info "Running Docker Container from Image: ${CONTAINER_FULL_NAME}"
        # shellcheck disable=SC2086
        docker run -d -it --name "$CONTAINER_NAME" ${CONTAINER_RUN_PARAMETERS} ${ENTRYPOINT_CMD} "${CONTAINER_FULL_NAME}" ${CONTAINER_RUN_COMMAND}

    fi


    print_info "Waiting for the container to fully boot..."
    sleep ${CONTAINER_STARTUP_TIMEOUT}

    if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME")" != 'true' ]; then
        print_fail "Timeout of ${CONTAINER_STARTUP_TIMEOUT} seconds reached when waiting for $CONTAINER_NAME to start - aborting."
    fi

    print_info 'Copying PyTest Scripts to Docker Container'
    docker cp tests "$CONTAINER_NAME:/tmp"

    print_info 'Installing Python and PyTest in the Container'
    docker exec -u 0 "$CONTAINER_NAME" dnf install -y python3-pip procps iproute || docker exec -u 0 "$CONTAINER_NAME" microdnf install -y python3-pip procps iproute || docker exec -u 0 "$CONTAINER_NAME" bash -c 'apt-get update && apt-get install -y python3-pip procps iproute2'
    docker exec -u 0 "$CONTAINER_NAME" pip3 install pytest requests psycopg2-binary redis pymongo pika || docker exec -u 0 "$CONTAINER_NAME" pip3 install pytest requests psycopg2-binary redis pymongo pika --break-system-packages

    print_info 'Executing PyTest Scripts'
    docker exec -u 0 "$CONTAINER_NAME" /bin/bash -c "cd /tmp/tests && python3 -m pytest -vv ${CONTAINER_TEST_FILES}" || print_fail "PyTest execution failed"

    docker stop "$CONTAINER_NAME"
    docker rm "$CONTAINER_NAME"
    if [ "${IMAGE_NAME}" == "kong" ]; then
        docker stop kong-database
        docker rm kong-database
        docker network rm kong-net
    elif [ "${IMAGE_NAME}" == "postgres-repmgr" ]; then
        docker stop "${CONTAINER_NAME}-standby"
        docker rm "${CONTAINER_NAME}-standby"
        docker network rm postgres-repmgr-net
    fi
    set +x
}

push_container_image(){
    set -x
    # to support multiarch
    # https://stackoverflow.com/questions/74816159/how-can-i-pull-push-the-docker-image-for-all-os-arch-into-dockerhub
    # latest_arch is set in the build_container function
    docker push "sourcemation/$DOCKER_TAG_LATEST"
    #    docker push "sourcemation/$DOCKER_TAG_VERSION"
    docker push "sourcemation/$DOCKER_TAG_BUILD"
    docker push "quay.io/sourcemation/$DOCKER_TAG_LATEST"
    #    docker push "quay.io/sourcemation/$DOCKER_TAG_VERSION"
    docker push "quay.io/sourcemation/$DOCKER_TAG_BUILD"

    # The TAG_BUILD should be always connected to TAG_VERSION

    # Note the x86_64 MUST BE the first build
    if [ "$BASE_ARCH" == "x86_64" ]; then
        echo "Removing the latest tag for to setup multiarch - x86_64 must be the first build"
        for container_registry in "docker.io" "quay.io"; do
            echo "Removing latest manifest for ${container_registry} with amd64 ${container_registry} and $DOCKER_TAG_VERSION"
            docker manifest rm "${container_registry}/sourcemation/$DOCKER_TAG_VERSION" || true
            echo "Creating latest manifest for ${container_registry} with amd64 ${container_registry} and $DOCKER_TAG_VERSION"
            docker manifest create "${container_registry}/sourcemation/$DOCKER_TAG_VERSION" --amend "${container_registry}/sourcemation/$DOCKER_TAG_BUILD"
        done
    elif [ "$BASE_ARCH" == "aarch64" ]; then
        echo "Creating arm64 manifest for $DOCKER_TAG_VERSION"
        # This may look stupid, I get that, but the thing is that in the
        # previous pipeline, we had a single host that was pushing the
        # manifests, so the x86_64 manifest was present before the arm64, and
        # had host had the x86_64 image saved.
        #        docker pull "sourcemation/$DOCKER_TAG_VERSION" || true
        for container_registry in "docker.io" "quay.io"; do
            echo "Creating latest manifest for ${container_registry} with arm64 and amd64"
            docker manifest create "${container_registry}/sourcemation/$DOCKER_TAG_VERSION" --amend "${container_registry}/sourcemation/$DOCKER_TAG_BUILD" --amend "$(echo ${container_registry}/sourcemation/"$DOCKER_TAG_BUILD" | sed 's/-arm64/-amd64/g' )"
        done
    fi
    docker manifest push "docker.io/sourcemation/$DOCKER_TAG_VERSION"
    docker manifest push "quay.io/sourcemation/$DOCKER_TAG_VERSION"

    # DOCKER_TAG_BUILD_VER_NO_ARCH - it's useful for the HELM charts

    if [ "$BASE_ARCH" == "x86_64" ]; then
        for container_registry in "docker.io" "quay.io"; do
            # there is no need to remove the tag as it should be always unique
            echo "Creating latest manifest for ${container_registry} with amd64 ${container_registry} and $DOCKER_TAG_BUILD_VER_NO_ARCH"
            docker manifest create "${container_registry}/sourcemation/$DOCKER_TAG_BUILD_VER_NO_ARCH" --amend "${container_registry}/sourcemation/$DOCKER_TAG_BUILD"
        done
    elif [ "$BASE_ARCH" == "aarch64" ]; then
        echo "Creating arm64 manifest for $DOCKER_TAG_BUILD_VER_NO_ARCH"
        # This may look stupid, I get that, but the thing is that in the
        # previous pipeline, we had a single host that was pushing the
        # manifests, so the x86_64 manifest was present before the arm64, and
        # had host had the x86_64 image saved.
        #        docker pull "sourcemation/$DOCKER_TAG_VERSION" || true
        for container_registry in "docker.io" "quay.io"; do
            echo "Creating $DOCKER_TAG_BUILD_VER_NO_ARCH manifest for ${container_registry} with arm64 and amd64"
            docker manifest create "${container_registry}/sourcemation/$DOCKER_TAG_BUILD_VER_NO_ARCH" --amend "${container_registry}/sourcemation/$DOCKER_TAG_BUILD" --amend "$(echo ${container_registry}/sourcemation/"$DOCKER_TAG_BUILD" | sed 's/-arm64/-amd64/g' )"
        done
    fi

    docker manifest push "docker.io/sourcemation/$DOCKER_TAG_BUILD_VER_NO_ARCH"
    docker manifest push "quay.io/sourcemation/$DOCKER_TAG_BUILD_VER_NO_ARCH"



    # The latest tag is special case, do absolutely nothing if there is suffix
    if [ "$DOCKER_TAG_SUFFIX" != "" ]; then
        return 0
    fi

    # Note the x86_64 MUST BE the first build
    if [ "$BASE_ARCH" == "x86_64" ]; then
        echo "Removing the latest tag for to setup multiarch - x86_64 must be the first build"
        for container_registry in "docker.io" "quay.io"; do
            echo "Removing latest manifest for ${container_registry} with amd64"
            docker manifest rm "${container_registry}/sourcemation/${IMAGE_NAME}:latest" || true
            echo "Creating latest manifest for ${container_registry}"
            docker manifest create "${container_registry}/sourcemation/${IMAGE_NAME}:latest" --amend "${container_registry}/sourcemation/${IMAGE_NAME}:latest-${latest_arch}"
        done
    elif [ "$BASE_ARCH" == "aarch64" ]; then
        echo "Creating arm64 manifest"
        # This may look stupid, I get that, but the thing is that in the
        # previous pipeline, we had a single host that was pushing the
        # manifests, so the x86_64 manifest was present before the arm64, and
        # had host had the x86_64 image saved.
        docker pull "sourcemation/${IMAGE_NAME}:latest-amd64"
        for container_registry in "docker.io" "quay.io"; do
            echo "Creating latest manifest for ${container_registry} with arm64 and amd64"
            docker manifest create "${container_registry}/sourcemation/${IMAGE_NAME}:latest" --amend "${container_registry}/sourcemation/${IMAGE_NAME}:latest-${latest_arch}" --amend "${container_registry}/sourcemation/${IMAGE_NAME}:latest-amd64"
        done
    fi
    docker manifest push "docker.io/sourcemation/${IMAGE_NAME}:latest"
    docker manifest push "quay.io/sourcemation/${IMAGE_NAME}:latest"
}

push_readme(){

    # We do not push readme for suffixes
    if [ "$DOCKER_TAG_SUFFIX" != "" ]; then
        return 0
    fi

    # preapre the binary
    if [ "$BASE_ARCH" == "x86_64" ];then
        bin_arch="amd64"
    else
        # README.md is the same for all images; we do not need to push it for
        # each architecture, it's eating precious compute time/cloud credits
        return 0
    fi
    binary_url="https://github.com/christian-korneck/docker-pushrm/releases/download/v1.9.0/docker-pushrm_linux_${bin_arch}"
    mkdir -p ~/.docker/cli-plugins
    curl -L  "${binary_url}" -o ~/.docker/cli-plugins/docker-pushrm
    chmod +x ~/.docker/cli-plugins/docker-pushrm

    # push the README.md
    pushd "$container_dir"
    print_info "Pushing README.md to dockerhub"
    docker pushrm "docker.io/sourcemation/${IMAGE_NAME}"

    print_info "Pushing README.md to quay.io"
    docker pushrm "quay.io/sourcemation/${IMAGE_NAME}"

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
check_variables_set_build_container
check_command_available "docker"
check_file_exists "$container_file"
check_file_exists "$container_dir/README.md"
[[ "$PUSH_README" != "true" && "$PUSH_IMAGE" != "true" ]] || login_to_quayio
[[ "$PUSH_README" != "true" && "$PUSH_IMAGE" != "true" ]] || login_to_dockerhub
[ "$BUILD_CONTAINER" != "true" ] || prepare_build # Run init.sh if it exists
read_configs # This is always needed
[ "$BUILD_CONTAINER" != "true" ] || build_container
[ "$TEST_IMAGE" != "true" ] || test_container
[ "$PUSH_IMAGE" != "true" ] || push_container_image
[[ "$PUSH_README" != "true" && "$PUSH_IMAGE" != "true" ]] || push_readme
cleanup

