#!/usr/bin/env bash

apt-get update
apt-get install ca-certificates gpg -y

key_path=/etc/apt/keyrings/nginx-archive-keyring.gpg; \
keys='573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 8540A6F18833A80E9C1653A42FD21310B49F6B46 9E9BE90EACBCDE69FE9B204CBCDCD8A38D88A2B38'
# we want the keys variable to split on spaces :) do not quote it
# shellcheck disable=SC2086
gpg --batch --keyserver keyserver.ubuntu.com --recv-keys $keys
# shellcheck disable=SC2086
gpg --export $keys > "$key_path"

aptRepo="deb [signed-by=$key_path] https://nginx.org/packages/debian/ trixie nginx"
# Add the repository to apt sources.list.d
echo "$aptRepo" > /etc/apt/sources.list.d/nginx-stable.list
apt update
# Main Nginx package version
apt-cache madison nginx | awk '{print $3}' | head -n 1 > /version
# Otel version
apt-cache madison nginx-module-otel | awk '{print $3}' | head -n 1 > /otel_version
