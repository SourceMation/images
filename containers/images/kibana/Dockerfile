FROM sourcemation/debian-12-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Kibana on Debian 12 Slim Container"

LABEL name="kibana" \
      vendor="SourceMation" \
      url="https://sourcemation.com" \
      source="https://github.com/SourceMation/images/issues" \
      licenses="Elastic-License-2.0" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="..." \
      io.k8s.display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="kibana debian-12-slim"

ENV KIBANA_HOME=/usr/share/kibana

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends libnss3 libfontconfig1 libasound2; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 1000 kibana; \
    useradd --uid 1000 --gid 1000 --shell /bin/bash -d ${KIBANA_HOME} --create-home kibana

COPY --chown=kibana:kibana kibana/ ${KIBANA_HOME}/

RUN ln -s ${KIBANA_HOME}/bin/kibana /usr/local/bin/kibana

WORKDIR ${KIBANA_HOME}

USER kibana

EXPOSE 5601

VOLUME [ "/usr/share/kibana/data" ]

CMD ["bin/kibana"]