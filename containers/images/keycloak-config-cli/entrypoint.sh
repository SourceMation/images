#!/bin/bash
set -e

if [ -z "${KEYCLOAK_MAJOR_VERSION}" ]; then
    JAR=$(ls -v "${CLI_HOME}" | tail -n 1)
else
    VERSION=$(ls -v | grep -o "${KEYCLOAK_MAJOR_VERSION}\.[0-9][0-9]*\.[0-9][0-9]*" | sort -V | tail -n 1)
    if [ -z "${VERSION}" ]; then
        JAR=$(ls -v "${CLI_HOME}" | tail -n 1)
    else
        JAR="keycloak-config-cli-${VERSION}.jar"
    fi
fi

ln -s "${CLI_HOME}/${JAR}" "${CLI_HOME}/keycloak-config-cli.jar"
chown -h cli:cli "${CLI_HOME}/keycloak-config-cli.jar"
echo "Using keycloak-config-cli version: ${JAR}"

exec "$@"