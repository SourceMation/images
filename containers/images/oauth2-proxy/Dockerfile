FROM sourcemation/golang-1.25:latest AS builder

ARG TARGETARCH
ARG OAUTH2_PROXY_VERSION="v7.14.2"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

# Download source
RUN curl -L "https://github.com/oauth2-proxy/oauth2-proxy/archive/${OAUTH2_PROXY_VERSION}.tar.gz" -o oauth2-proxy.tar.gz && \
    tar -xzf oauth2-proxy.tar.gz --strip-components=1 && \
    rm oauth2-proxy.tar.gz

# Build
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build -ldflags "-s -w -X main.VERSION=${OAUTH2_PROXY_VERSION}" -o oauth2-proxy .

FROM sourcemation/debian-13-slim:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="oauth2-proxy" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="MIT" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="OAuth2 Proxy on Debian 13 Slim Container" \
      description="Provides oauth2-proxy on Debian 13 Slim Container" \
      version="v7.14.2" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="OAuth2 Proxy on Debian 13 Slim Container" \
      io.k8s.description="Provides oauth2-proxy on Debian 13 Slim Container" \
      io.openshift.tags="oauth2-proxy debian-13"

ENV OAUTH2_PROXY_VERSION="v7.14.2"

RUN apt-get update && apt-get install --no-install-recommends -y ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy binary from builder
COPY --from=builder /app/oauth2-proxy /usr/local/bin/oauth2-proxy

RUN chmod +x /usr/local/bin/oauth2-proxy && \
    groupadd -g 1001 oauth2-proxy && \
    useradd -u 1001 -g oauth2-proxy -m oauth2-proxy

USER 1001
WORKDIR /home/oauth2-proxy/

ENTRYPOINT [ "oauth2-proxy" ]
CMD [ "--help" ]
