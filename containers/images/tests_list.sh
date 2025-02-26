#!/usr/bin/env bash
#
# Author: Marek Janosz <marek.janosz@linuxpolska.pl>

set -eou pipefail

test_ports(){
    # Test exposed port(s)
    port_exposed=$(grep "EXPOSE " Dockerfile |egrep -o "[0-9-]*")
    
    if [ ! -z "$port_exposed" ]; then
        docker_ports=""
        for expose in $port_exposed
        do
            docker_ports="$docker_ports -p $expose:$expose "
        done
        
        if hash podman; then
            docker run -dit --rm $docker_ports --name $DOCKER_TAG_NAME-test eurolinux/${DOCKER_TAG_NAME}:latest-${latest_arch}
        else
            docker run -dit --rm $docker_ports --name $DOCKER_TAG_NAME-test eurolinux/${DOCKER_TAG_NAME}:latest
        fi

        sleep 5

        for expose in $port_exposed
        do
            echo "Testing port $expose"
            nc 127.0.0.1 $expose -vz
            echo "Port $expose OK"
        done
        docker stop $DOCKER_TAG_NAME-test
    else
        echo "Skipping port test"
    fi
}

test_user(){
    # Test user
    image_user=$(grep "USER " Dockerfile | grep -o "[a-z-]*"| tr -d '[:space:]')
    
    if [ ! -z "$image_user" ]; then
        if hash podman; then
            docker run -dit --rm --name $DOCKER_TAG_NAME-test eurolinux/${DOCKER_TAG_NAME}:latest-${latest_arch}
        else
            docker run -dit --rm --name $DOCKER_TAG_NAME-test eurolinux/${DOCKER_TAG_NAME}:latest
        fi

        container_user=$(docker exec -it $DOCKER_TAG_NAME-test whoami | tr -d '[:space:]')
        if [ "$container_user" == "$image_user" ]; then
            echo "Container USER OK"
            docker stop $DOCKER_TAG_NAME-test
        else
            echo "The USER of the container and the image are different!"
            docker stop $DOCKER_TAG_NAME-test
            exit 1
        fi
    else
        echo "Skipping user test"
    fi
}
