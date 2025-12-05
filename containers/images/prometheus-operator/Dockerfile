FROM docker.io/sourcemation/golang-1.24 AS builder

ARG TARGETARCH
ARG VERSION=v0.87.0

ADD https://github.com/prometheus-operator/prometheus-operator/archive/refs/tags/${VERSION}.tar.gz .

ENV GOARCH=${TARGETARCH}

RUN << EOF
set -eu
apt-get update
apt-get -y upgrade
apt-get -y install ca-certificates
tar -xzf ${VERSION}.tar.gz -C src --strip 1
cd src
go mod download -x 
go mod verify
make operator
mv operator ../bin/
EOF

FROM docker.io/sourcemation/debian-13-slim:latest

ARG TARGETARCH="amd64"
ARG BUILD_DATE
ARG LONGNAME="Prometheus Operator on Debian 13 Slim Container"

LABEL name="prometheus-operator" \
  vendor="Sourcemation" \
  url="https://sourcemation.com"\
  source="https://github.com/Sourcemation/images/issues"\
  licenses="Apache-2.0" \
  created="${BUILD_DATE}" \
  architecture="${TARGETARCH}" \
  summary="${LONGNAME}" \
  description="Provides ${LONGNAME}" \
  version="0.87.0" \
  io.k8s.display-name="${LONGNAME}" \
  io.k8s.description="Provides ${LONGNAME}" \
  io.openshift.tags="prometheus-operator debian-13-slim"

# RUN update and setup user
RUN set -e; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*

# INSTAL OR COPY --from=builder /builder/path /path
COPY --from=builder /go/bin/operator                /usr/local/bin/
COPY --from=builder /go/src/LICENSE /go/src/NOTICE  /

# END INSTALL
USER       nobody
ENTRYPOINT [ "/usr/local/bin/operator" ]
