FROM sourcemation/nginx-mainline:latest


LABEL name="nginx-mainline" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="BSD-2-Clause License" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Nginx Mainline on Debian 12 Slim Container with OTEL" \
      description="Provides Nginx Mainline on Debian 12 Slim Container with OTEL" \
      version="1.29.0" \
      io.k8s.display-name="Nginx mainline on Debian 12 Slim Container with OTEL" \
      io.k8s.description="Provides Nginx Mainline on Debian 12 Slim Container with OTEL" \
      io.openshift.tags="nginx debian-12-slim otel"

ENV NGINX_VERSION="1.29.0"
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
