FROM docker.io/sourcemation/golang-1.24 AS builder

ARG TARGETARCH
ARG VERSION=v2.18.0

ADD https://github.com/kubernetes/kube-state-metrics/archive/refs/tags/${VERSION}.tar.gz .

ENV GOARCH=${TARGETARCH}

RUN set -eu && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install --no-install-recommends ca-certificates && \
    tar -xzf ${VERSION}.tar.gz -C src --strip 1 && \
    cd src && \
    make build-local && \
    mv kube-state-metrics ../bin/

FROM sourcemation/debian-13-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="kube-state-metrics on Debian 13 Slim Container"

LABEL name="kube-state-metrics" \
  vendor="Sourcemation" \
  url="https://sourcemation.com"\
  source="https://github.com/Sourcemation/images/issues"\
  licenses="Apache-2.0" \
  created="${BUILD_DATE}" \
  architecture="${TARGETARCH}" \
  summary="${LONGNAME}" \
  description="Provides ${LONGNAME}" \
  version="2.18.0" \
  io.k8s.display-name="${LONGNAME}" \
  io.k8s.description="Provides ${LONGNAME}" \
  io.openshift.tags="kube-state-metrics debian-13-slim"

# RUN update and setup user
RUN set -e && \
    apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# INSTAL OR COPY --from=builder /builder/path /path
COPY --from=builder /go/bin/kube-state-metrics      /usr/local/bin/
COPY --from=builder /go/src/LICENSE                 /

# END INSTALL
USER       nobody
EXPOSE     8080 8081
ENTRYPOINT ["kube-state-metrics", "--port=8080", "--telemetry-port=8081"]
