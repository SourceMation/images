FROM sourcemation/golang-1.24:latest AS builder

ARG TARGETARCH

ARG EXPORTER_URL="https://github.com/oliver006/redis_exporter/releases/download"

ARG REDIS_EXPORTER_VERSION="v1.74.0"

WORKDIR /tmp

RUN apt-get update && apt-get install -y curl ca-certificates git; \
    git clone --branch ${REDIS_EXPORTER_VERSION} https://github.com/oliver006/redis_exporter.git && \
    cd redis_exporter && \
    BUILD_DATE=$(date +%F-%T) CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o /redis_exporter \
    -ldflags  "-s -w -extldflags \"-static\" -X main.BuildVersion=${REDIS_EXPORTER_VERSION} -X main.BuildDate=$BUILD_DATE"

# Smoke test
RUN /redis_exporter -version

FROM scratch

LABEL name="redis-exporter" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Redis Exporter" \
      description="Provides Redis Exporter" \
      version="1.74.0" \
      io.k8s.display-name="Redis Exporter" \
      io.k8s.description="Provides Redis Exporter" \
      io.openshift.tags="redis exporter"

# Not root user -> keep UID/GID in sync with oliver006 image

USER 59000:59000

COPY --from=builder /etc/ssl/certs /etc/ssl/certs
COPY --from=builder /redis_exporter /redis_exporter

EXPOSE 9121

ENTRYPOINT ["/redis_exporter"]
