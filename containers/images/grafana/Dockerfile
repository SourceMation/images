FROM sourcemation/debian-13-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Grafana on Debian 13 Slim Container"

LABEL name="grafana" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      source="https://github.com/Sourcemation/images/issues" \
      licenses="AGPL-3.0" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="12.2.1" \
      io.k8s.display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="grafana debian-13-slim"

ENV GRAFANA_HOME=/usr/share/grafana

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends libfontconfig1; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 1000 grafana; \
    useradd --uid 1000 --gid 1000 --shell /bin/bash -d ${GRAFANA_HOME} --create-home grafana; \
    mkdir -p ${GRAFANA_HOME}/data; \
    chown -R grafana:grafana ${GRAFANA_HOME}/data

COPY --chown=grafana:grafana grafana/ ${GRAFANA_HOME}/

WORKDIR ${GRAFANA_HOME}

USER grafana

EXPOSE 3000

VOLUME [ "/usr/share/grafana/data" ]

ENTRYPOINT ["bin/grafana", "server"]