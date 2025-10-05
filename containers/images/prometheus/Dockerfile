FROM docker.io/sourcemation/debian-12-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Prometheus on Debian 12 Slim Container"

LABEL name="prometheus" \
  vendor="SourceMation" \
  url="https://sourcemation.com"\
  source="https://github.com/SourceMation/images/issues"\
  licenses="Apache-2.0" \
  created="${BUILD_DATE}" \
  architecture="${TARGETARCH}" \
  summary="${LONGNAME}" \
  description="Provides ${LONGNAME}" \
  version="3.6.0" \
  io.k8s.display-name="${LONGNAME}" \
  io.k8s.description="Provides ${LONGNAME}" \
  io.openshift.tags="prometheus debian-12-slim"

# RUN update and setup user
RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*

# INSTAL OR COPY --from=builder /builder/path /path
COPY prometheus       /bin/prometheus
COPY promtool         /bin/promtool
COPY prometheus.yml   /etc/prometheus/prometheus.yml
COPY LICENSE          /LICENSE
COPY NOTICE           /NOTICE

WORKDIR /prometheus
RUN chown -R nobody:nogroup /etc/prometheus /prometheus && chmod g+w /prometheus

# END INSTALL
USER       nobody
EXPOSE     9090
VOLUME     [ "/prometheus" ]
ENTRYPOINT [ "/bin/prometheus" ]
CMD        [ "--config.file=/etc/prometheus/prometheus.yml", \
             "--storage.tsdb.path=/prometheus" ]
