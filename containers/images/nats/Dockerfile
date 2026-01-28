FROM sourcemation/golang-1.25:latest AS builder

ARG TARGETARCH
ARG NATS_VERSION="v2.12.4"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch ${NATS_VERSION} https://github.com/nats-io/nats-server.git .

# Build
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build -v -ldflags "-s -w -X github.com/nats-io/nats-server/v2/server.gitCommit=$(git rev-parse --short HEAD)" -o nats-server .

FROM sourcemation/debian-13-slim:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="nats" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="NATS Server on Debian 13 Slim Container" \
      description="Provides NATS Server on Debian 13 Slim Container" \
      version="v2.12.4" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="NATS Server on Debian 13 Slim Container" \
      io.k8s.description="Provides NATS Server on Debian 13 Slim Container" \
      io.openshift.tags="nats nats-server debian-13"

ENV NATS_VERSION="v2.12.4"

COPY --from=builder /app/nats-server /bin/nats-server
COPY nats-server.conf /etc/nats/nats-server.conf

# Expose ports
# 4222: NATS client
# 8222: HTTP management
# 6222: Clustering
EXPOSE 4222 8222 6222

ENTRYPOINT ["/bin/nats-server"]
CMD ["-c", "/etc/nats/nats-server.conf"]
