FROM sourcemation/debian-12-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Cassandra on Debian 12 Slim Container"

LABEL name="cassandra" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      source="https://github.com/Sourcemation/images/issues" \
      licenses="Apache-2.0" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="5.0.6" \
      io.k8s.display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="cassandra debian-12-slim"

ENV CASSANDRA_HOME=/opt/cassandra
ENV PATH="${CASSANDRA_HOME}/bin:${PATH}"

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless gosu procps; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 999 cassandra; \
    useradd --uid 999 --gid 999 --shell /bin/bash -d ${CASSANDRA_HOME} --create-home cassandra

COPY --chown=cassandra:cassandra cassandra/ ${CASSANDRA_HOME}/

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN mkdir -p /var/lib/cassandra /var/log/cassandra; \
    chown -R cassandra:cassandra /var/lib/cassandra /var/log/cassandra

WORKDIR ${CASSANDRA_HOME}

EXPOSE 7000 9042

VOLUME /var/lib/cassandra

ENTRYPOINT ["entrypoint.sh"]

CMD ["cassandra", "-f"]