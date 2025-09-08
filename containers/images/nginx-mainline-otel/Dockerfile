FROM sourcemation/nginx-mainline:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="nginx-mainline" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="BSD-2-Clause License" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Nginx Mainline on Debian 12 Slim Container with OTEL" \
      description="Provides Nginx Mainline on Debian 12 Slim Container with OTEL" \
      version="1.29.1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Nginx mainline on Debian 12 Slim Container with OTEL" \
      io.k8s.description="Provides Nginx Mainline on Debian 12 Slim Container with OTEL" \
      io.openshift.tags="nginx debian-12-slim otel"

ENV NGINX_VERSION="1.29.1"
ENV PKG_RELEASE="1~bookworm"
ENV OTEL_VERSION="0.1.2"

RUN set -xeu; \
    nginxPackages=" \
        nginx-module-otel=${NGINX_VERSION}+${OTEL_VERSION}-${PKG_RELEASE} \
    " ; \
    apt-get update; \
    apt-get install --no-install-recommends --no-install-suggests -y $nginxPackages; \
    apt-get remove --purge --auto-remove -y; \
    rm -rf /var/lib/apt/lists/*
