FROM sourcemation/jdk-21:latest

ARG BUILD_DATE
ARG TARGETARCH
ARG KEYCLOAK_VER="26.3.5"
ENV KEYCLOAK_HOME=/opt/keycloak

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 1000 keycloak; \
    useradd --uid 1000 --gid 1000 --shell /bin/bash -d ${KEYCLOAK_HOME} --create-home keycloak

COPY --chown=keycloak:keycloak keycloak/ ${KEYCLOAK_HOME}/
COPY entrypoint.sh $KEYCLOAK_HOME/bin/entrypoint.sh

LABEL name="keycloak" \
  vendor="Linux Polska" \
  url="https://sourcemation.com"\
  source="https://github.com/SourceMation/images/issues"\
  licenses="Apache-2.0" \
  created="$BUILD_DATE" \
  architecture="$TARGETARCH" \
  summary="Keycloak on Debian 12 Slim Container" \
  description="Provides Keycloak on Debian 12 Slim Container" \
  version="26.3.5" \
  io.k8s.display-name="Keycloak on Debian 12 Slim Container" \
  io.k8s.description="Provides Keycloak on Debian 12 Slim Container" \
  io.openshift.tags="keycloak debian"

USER keycloak
WORKDIR ${KEYCLOAK_HOME}

EXPOSE 8080 8443 9000
VOLUME [ "$KEYCLOAK_HOME/data" ]
ENTRYPOINT [ "bin/entrypoint.sh" ]
CMD [ "bin/kc.sh", "start-dev" ]