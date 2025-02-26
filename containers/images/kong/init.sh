#!/usr/bin/env bash

# TODO in the future find the way to get latest release from Kong 
# Current solution that uses the github release for input won't work as the
# lastest release is for version 2.8.5

curl -Lo kong-x86_64.rpm https://packages.konghq.com/public/gateway-37/rpm/el/9/x86_64/kong-3.7.1.el9.x86_64.rpm 
curl -LO https://raw.githubusercontent.com/Kong/docker-kong/master/docker-entrypoint.sh && chmod +x docker-entrypoint.sh
