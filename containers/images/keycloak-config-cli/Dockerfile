FROM sourcemation/jdk-21:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Keycloak Config CLI on Debian 12 Slim Container"

LABEL name="keycloak-config-cli" \
      vendor="SourceMation" \
      url="https://sourcemation.com" \
      source="https://github.com/SourceMation/images/issues" \
      licenses="Apache-2.0" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="6.4.0" \
      io.k8s.display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="keycloak-config-cli jdk-21 debian-12-slim"

ENV CLI_HOME=/opt/keycloak-config-cli

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 1001 cli; \
    useradd --uid 1001 --gid 1001 --shell /bin/bash -d ${CLI_HOME} --create-home cli

WORKDIR ${CLI_HOME}

COPY --chown=cli:cli keycloak-config-cli/ ${CLI_HOME}

RUN set -ex; \
    LATEST_JAR=$(ls -v "${CLI_HOME}" | tail -n 1); \
    ln -s "${CLI_HOME}/${LATEST_JAR}" "${CLI_HOME}/keycloak-config-cli.jar"; \
    chown -h cli:cli "${CLI_HOME}/keycloak-config-cli.jar"

USER cli

ENTRYPOINT ["java", "-jar", "/opt/keycloak-config-cli/keycloak-config-cli.jar"]