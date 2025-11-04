FROM sourcemation/golang-1.24 AS builder

ARG TARGETARCH
ARG VERSION=RELEASE.2025-10-15T17-29-55Z

ADD https://github.com/minio/minio/archive/refs/tags/${VERSION}.tar.gz .

ENV GOARCH=${TARGETARCH}
ENV GOOS=linux

RUN << EOF
set -eu
apt-get update
apt-get -y upgrade
apt-get -y install ca-certificates git
tar -xzf ${VERSION}.tar.gz -C src --strip 1
cd src
make build
mv minio ../bin/
EOF

FROM sourcemation/debian-13-slim:latest

ARG TARGETARCH="amd64"
ARG BUILD_DATE
ARG LONGNAME="Minio on Debian 13 Slim Container"

LABEL name="minio" \
  vendor="Sourcemation" \
  url="https://sourcemation.com"\
  source="https://github.com/Sourcemation/images/issues"\
  licenses="AGPLv3" \
  created="${BUILD_DATE}" \
  architecture="${TARGETARCH}" \
  summary="${LONGNAME}" \
  description="Provides ${LONGNAME}" \
  version="RELEASE.2025-10-15T17-29-55Z" \
  io.k8s.display-name="${LONGNAME}" \
  io.k8s.description="Provides ${LONGNAME}" \
  io.openshift.tags="minio debian-13-slim"

# RUN update and setup user
RUN set -e; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*; \
    mkdir /data; \
    chown nobody:nogroup /data

# INSTAL OR COPY --from=builder /builder/path /path
COPY --from=builder /go/bin/minio                   /usr/local/bin/
COPY --from=builder /go/src/LICENSE /go/src/NOTICE  /

# END INSTALL
USER       nobody
EXPOSE     9000 9001
VOLUME     ["/data"]
ENTRYPOINT [ "/usr/local/bin/minio" ]
