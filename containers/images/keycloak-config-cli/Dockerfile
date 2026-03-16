FROM sourcemation/jdk-21:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Keycloak Config CLI on Debian 13 Slim Container"

LABEL name="keycloak-config-cli" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      source="https://github.com/Sourcemation/images/issues" \
      licenses="Apache-2.0" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="6.4.1" \
      io.k8s.display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="keycloak-config-cli jdk-21 debian-13-slim"

ENV CLI_HOME=/opt/keycloak-config-cli

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 1001 cli; \
    useradd --uid 1001 --gid 1001 --shell /bin/bash -d ${CLI_HOME} --create-home cli

WORKDIR ${CLI_HOME}

COPY --chown=cli:cli keycloak-config-cli/ ${CLI_HOME}

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

USER cli

ENTRYPOINT ["entrypoint.sh"]

CMD ["java", "-jar", "/opt/keycloak-config-cli/keycloak-config-cli.jar"]