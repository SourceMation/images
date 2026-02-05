FROM sourcemation/golang-1.24 AS builder

ARG VERSION=0.8.1
ARG TARGETOS=linux
ARG TARGETARCH
ARG CGO_ENABLED=0

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        --no-install-suggests \
        git \
        ca-certificates \
        openssl \
        tzdata

WORKDIR /workspace

RUN git clone --depth 1 --branch v${VERSION} https://github.com/kubernetes-sigs/metrics-server.git /workspace \
    && CGO_ENABLED=${CGO_ENABLED} GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
        go build -a \
        -installsuffix cgo \
        -ldflags="-s -w -X sigs.k8s.io/metrics-server/pkg/version.gitVersion=${VERSION}" \
        -o metrics-server \
        ./cmd/metrics-server

FROM sourcemation/debian-13-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="metrics-server" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Metrics Server on Debian 13 Slim Container" \
      description="Provides Metrics Server on Debian 13 Slim Container" \
      version="0.8.1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Metrics Server on Debian 13 Slim Container" \
      io.k8s.description="Provides Metrics Server on Debian 13 Slim Container" \
      io.openshift.tags="metrics-server debian-13-slim"

ENV DEBIAN_FRONTEND=noninteractive

COPY --from=builder /workspace/metrics-server /usr/local/bin/metrics-server

RUN apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        --no-install-suggests \
        ca-certificates \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/archives/* \
        /var/log/* \
        /tmp/* \
        /var/tmp/*

RUN useradd --shell /bin/bash -m metrics-server \
    && chmod +x /usr/local/bin/metrics-server \
    && chown metrics-server:metrics-server /usr/local/bin/metrics-server /usr/local/share/ca-certificates

USER metrics-server
EXPOSE 8443
ENTRYPOINT ["metrics-server"]
CMD [ \
    "--cert-dir=/usr/local/share/ca-certificates", \
    "--secure-port=8443", \
    "--kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname", \
    "--kubelet-use-node-status-port", \
    "--metric-resolution=15s" \
]