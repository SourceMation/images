FROM docker.io/sourcemation/debian-12-slim:latest as builder

ARG TARGETARCH

ARG EXPORTER_URL="https://github.com/oliver006/redis_exporter/releases/download"

ARG REDIS_EXPORTER_VERSION="v1.70.0"

WORKDIR /tmp

RUN apt-get update && apt-get install -y curl ca-certificates; \
    curl -fL -Lo redis_exporter-${REDIS_EXPORTER_VERSION}.linux-$TARGETARCH.tar.gz \
    ${EXPORTER_URL}/${REDIS_EXPORTER_VERSION}/redis_exporter-${REDIS_EXPORTER_VERSION}.linux-$TARGETARCH.tar.gz; \
    tar -xvzf redis_exporter-${REDIS_EXPORTER_VERSION}.linux-$TARGETARCH.tar.gz; \
    mv redis_exporter-${REDIS_EXPORTER_VERSION}.linux-$TARGETARCH redis_exporter

FROM scratch

ARG TARGETARCH

LABEL name="redis-exporter" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Redis Exporter on Debian Container" \
      description="Provides Redis Exporter on Debian 12 Container" \
      version="1.70.0" \
      io.k8s.display-name="Redis Exporter on Debian Container" \
      io.k8s.description="Provides Redis Exporter on Debian 12 Container" \
      io.openshift.tags="redis exporter debian"

COPY --from=builder /etc/ssl/certs /etc/ssl/certs
COPY --from=builder /tmp/redis_exporter/redis_exporter /usr/local/bin/redis_exporter

EXPOSE 9121

ENTRYPOINT ["/usr/local/bin/redis_exporter"]