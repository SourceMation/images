FROM sourcemation/golang-1.25:latest AS builder

ARG TARGETARCH
ARG INGRESS_NGINX_VERSION="controller-v1.14.3"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/*

# Download source
# We use git clone because the tarball might not have everything or we might want git info
# But curl tarball is faster and deterministic with tags.
RUN curl -L "https://github.com/kubernetes/ingress-nginx/archive/refs/tags/${INGRESS_NGINX_VERSION}.tar.gz" -o ingress-nginx.tar.gz && \
    tar -xzf ingress-nginx.tar.gz --strip-components=1 && \
    rm ingress-nginx.tar.gz

# Build
# We set the version.RELEASE to the tag
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build \
    -ldflags "-s -w -X k8s.io/ingress-nginx/version.RELEASE=${INGRESS_NGINX_VERSION} -X k8s.io/ingress-nginx/version.REPO=https://github.com/kubernetes/ingress-nginx" \
    -o nginx-ingress-controller ./cmd/nginx

FROM sourcemation/debian-13-slim:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="nginx-ingress-controller" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="NGINX Ingress Controller on Debian 13 Slim Container" \
      description="Provides NGINX Ingress Controller on Debian 13 Slim Container" \
      version="v1.14.3" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="NGINX Ingress Controller on Debian 13 Slim Container" \
      io.k8s.description="Provides NGINX Ingress Controller on Debian 13 Slim Container" \
      io.openshift.tags="nginx-ingress-controller debian-13"

ENV INGRESS_NGINX_VERSION="controller-v1.14.3"

# Install nginx and other dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    nginx \
    ca-certificates \
    libcap2-bin \
    dumb-init && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy binary from builder
COPY --from=builder /app/nginx-ingress-controller /usr/local/bin/nginx-ingress-controller

RUN chmod +x /usr/local/bin/nginx-ingress-controller && \
    groupadd -g 1001 www-data-ingress && \
    useradd -u 1001 -g www-data-ingress -m www-data-ingress

# Allow nginx to bind to privileged ports (if needed) and other perms
RUN setcap 'cap_net_bind_service=+ep' /usr/sbin/nginx && \
    setcap 'cap_net_bind_service=+ep' /usr/local/bin/nginx-ingress-controller

USER 1001
WORKDIR /home/www-data-ingress/

ENTRYPOINT [ "/usr/bin/dumb-init", "--", "nginx-ingress-controller" ]
CMD [ "--help" ]
