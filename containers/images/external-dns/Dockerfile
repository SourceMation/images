FROM sourcemation/golang-1.25 AS builder

ARG VERSION=0.20.0
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

RUN git clone --depth 1 --branch v${VERSION} https://github.com/kubernetes-sigs/external-dns.git /workspace \
    && CGO_ENABLED=${CGO_ENABLED} GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -ldflags="-s -w -X sigs.k8s.io/external-dns/pkg/apis/externaldns.Version=${VERSION}" \
    -o external-dns .


FROM sourcemation/debian-13-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="external-dns" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="external-dns on Debian 13 Slim Container" \
      description="Provides external-dns on Debian 13 Slim Container" \
      version="0.20.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="external-dns on Debian 13 Slim Container" \
      io.k8s.description="Provides external-dns on Debian 13 Slim Container" \
      io.openshift.tags="external-dns debian-13-slim"

ENV DEBIAN_FRONTEND=noninteractive

COPY --from=builder /workspace/external-dns /usr/local/bin/external-dns

RUN useradd --shell /bin/bash -m external-dns \
    && chmod +x /usr/local/bin/external-dns \
    && chown external-dns:external-dns /usr/local/bin/external-dns

RUN apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        --no-install-suggests \
        ca-certificates \
        tzdata \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/archives/* \
        /var/log/* \
        /tmp/* \
        /var/tmp/*

USER external-dns
ENTRYPOINT ["external-dns"]
