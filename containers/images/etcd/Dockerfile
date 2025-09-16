FROM docker.io/sourcemation/debian-12-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="etcd on Debian 12 Slim Container"
ARG COPYFROM

LABEL name="etcd" \
  vendor="SourceMation" \
  url="https://sourcemation.com"\
  source="https://github.com/SourceMation/images/issues"\
  licenses="Apache-2.0" \
  created="${BUILD_DATE}" \
  architecture="${TARGETARCH}" \
  summary="${LONGNAME}" \
  description="Provides ${LONGNAME}" \
  version="..." \
  io.k8s.display-name="${LONGNAME}" \
  io.k8s.description="Provides ${LONGNAME}" \
  io.openshift.tags="etcd debian-12-slim"

# RUN update
RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*;

# INSTAL OR COPY --from=builder /builder/path /path
COPY $COPYFROM/etcd $COPYFROM/etcdctl $COPYFROM/etcdutl /usr/local/bin/

# END INSTALL
USER       nobody
WORKDIR    /var/lib/etcd/
EXPOSE     2379 2380
CMD        [ "/usr/local/bin/etcd" ]
