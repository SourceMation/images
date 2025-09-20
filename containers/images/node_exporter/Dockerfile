FROM docker.io/sourcemation/debian-12-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Node_Exporter on Debian 12 Slim Container"

LABEL name="node_exporter" \
  vendor="SourceMation" \
  url="https://sourcemation.com"\
  source="https://github.com/SourceMation/images/issues"\
  licenses="Apache-2.0" \
  created="${BUILD_DATE}" \
  architecture="${TARGETARCH}" \
  summary="${LONGNAME}" \
  description="Provides ${LONGNAME}" \
  version="1.9.1" \
  io.k8s.display-name="${LONGNAME}" \
  io.k8s.description="Provides ${LONGNAME}" \
  io.openshift.tags="node_exporter debian-12-slim"

# RUN update and setup user
RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*

# COPY
COPY tmpdir/node_exporter           /usr/local/bin/
COPY tmpdir/LICENSE tmpdir/NOTICE   /LICENSE

# END INSTALL
USER       nobody
EXPOSE     9100
ENTRYPOINT [ "/usr/local/bin/node_exporter" ]

