FROM sourcemation/nginx-stable:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="nginx-stable" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="BSD-2-Clause License" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Nginx Stable on Debian 13 Slim Container with Perl" \
      description="Provides Nginx Stable on Debian 13 Slim Container with Perl" \
      version="1.28.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Nginx stable on Debian 13 Slim Container with Perl" \
      io.k8s.description="Provides Nginx Stable on Debian 13 Slim Container with Perl" \
      io.openshift.tags="nginx debian-13-slim perl"

ENV NGINX_VERSION="1.28.0"
ENV DYNPKG_RELEASE="1~trixie"

RUN set -xeu; \
    nginxPackages=" \
        nginx-module-perl=${NGINX_VERSION}-${DYNPKG_RELEASE} \
    " ; \
    # Original Nginx rebuild the packages for not supported architectures. But they are doing it the wrong way IMO. \
    # Instead of creating a builder sub image, they are using a temp directory to build the packages... \
    # It complicates a lot of things. So if in the future we would also support other architectures, do it simpler and cleaner way. \
    apt-get update; \
    apt-get install --no-install-recommends --no-install-suggests -y \
                        $nginxPackages ;\
    apt-get remove --purge --auto-remove -y; \
    rm -rf /var/lib/apt/lists/*
