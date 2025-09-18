FROM sourcemation/debian-12-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Elasticsearch on Debian 12 Slim Container"

LABEL name="elasticsearch" \
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
      io.openshift.tags="elasticsearch debian-12-slim"

ENV ELASTICSEARCH_HOME=/usr/share/elasticsearch

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 1000 elasticsearch; \
    useradd --uid 1000 --gid 1000 --shell /bin/bash -d ${ELASTICSEARCH_HOME}--create-home elasticsearch; \
    mkdir -p ${ELASTICSEARCH_HOME}/data ${ELASTICSEARCH_HOME}/logs; \
    chown -R elasticsearch:elasticsearch ${ELASTICSEARCH_HOME} 

COPY --chown=elasticsearch:elasticsearch elasticsearch/ ${ELASTICSEARCH_HOME}/

WORKDIR ${ELASTICSEARCH_HOME}

USER elasticsearch

EXPOSE 9200 9300

VOLUME [ "/usr/share/elasticsearch/data", "/usr/share/elasticsearch/logs" ]

ENTRYPOINT ["bin/elasticsearch"]