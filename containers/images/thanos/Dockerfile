FROM docker.io/sourcemation/debian-13-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Thanos on Debian 13 Slim Container"

LABEL name="thanos" \
  vendor="Sourcemation" \
  url="https://sourcemation.com"\
  source="https://github.com/Sourcemation/images/issues"\
  licenses="Apache-2.0" \
  created="${BUILD_DATE}" \
  architecture="${TARGETARCH}" \
  summary="${LONGNAME}" \
  description="Provides ${LONGNAME}" \
  version="0.40.1" \
  io.k8s.display-name="${LONGNAME}" \
  io.k8s.description="Provides ${LONGNAME}" \
  io.openshift.tags="thanos debian-13-slim"

# RUN update and setup user
RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*

# INSTAL OR COPY --from=builder /builder/path /path
COPY tmpdir/thanos    /usr/local/bin/
COPY tmpdir/LICENSE   /

USER       nobody
ENTRYPOINT [ "/usr/local/bin/thanos" ]
