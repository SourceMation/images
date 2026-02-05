FROM sourcemation/debian-13-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="nginx-mainline" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="BSD-2-Clause License" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Nginx Mainline on Debian 13 Slim Container" \
      description="Provides Nginx Mainline on Debian 13 Slim Container" \
      version="1.29.5" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Nginx Mainline on Debian 13 Slim Container" \
      io.k8s.description="Provides Nginx Mainline on Debian 13 Slim Container" \
      io.openshift.tags="nginx debian-13-slim"

ENV NGINX_VERSION="1.29.5"
ENV PKG_RELEASE="1~trixie"
ENV NJS_VERSION="0.9.5"
ENV NJS_RELEASE="1~trixie"
ENV DYNPKG_RELEASE="1~trixie"

RUN set -xeu; \
    groupadd --system --gid 101 nginx ;\
    useradd --system --gid nginx --no-create-home --home /nonexistent --comment "nginx user" --shell /bin/false --uid 101 nginx ;\
    apt-get update ;\
    apt-get install --no-install-recommends --no-install-suggests -y gnupg ca-certificates ;\
    NGINX_GPGKEYS="573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 8540A6F18833A80E9C1653A42FD21310B49F6B46 9E9BE90EACBCDE69FE9B204CBCDCD8A38D88A2B3" ;\
    NGINX_GPGKEY_PATH=/etc/apt/keyrings/nginx-archive-keyring.gpg ;\
    export GNUPGHOME="$(mktemp -d)" ;\
    gpg --keyserver keyserver.ubuntu.com --keyserver-options timeout=10 --recv-keys $NGINX_GPGKEYS; \
    gpg --export $NGINX_GPGKEYS > "$NGINX_GPGKEY_PATH" ; \
    rm -rf "$GNUPGHOME"; \
    apt-get remove --purge --auto-remove -y gnupg && rm -rf /var/lib/apt/lists/* ;\
    nginxPackages=" \
        nginx=${NGINX_VERSION}-${PKG_RELEASE} \
        nginx-module-xslt=${NGINX_VERSION}-${DYNPKG_RELEASE} \
        nginx-module-geoip=${NGINX_VERSION}-${DYNPKG_RELEASE} \
        nginx-module-image-filter=${NGINX_VERSION}-${DYNPKG_RELEASE} \
        nginx-module-njs=${NGINX_VERSION}+${NJS_VERSION}-${NJS_RELEASE} \
    " ; \
    # Original Nginx rebuild the packages for not supported architectures. But they are doing it the wrong way IMO. \
    # Instead of creating a builder sub image, they are using a temp directory to build the packages... \
    # It complicates a lot of things. So if in the future we would also support other architectures, do it simpler and cleaner way. \
    echo "deb [signed-by=$NGINX_GPGKEY_PATH] https://nginx.org/packages/mainline/debian/ trixie nginx" >> /etc/apt/sources.list.d/nginx.list; \
    apt-get update; \
    apt-get install --no-install-recommends --no-install-suggests -y \
                        $nginxPackages \
                        gettext-base \
                        curl ;\
    apt-get remove --purge --auto-remove -y; \
    rm -rf /var/lib/apt/lists/* ; \
## forward request and error logs to docker log collector \
    ln -sf /dev/stdout /var/log/nginx/access.log ;\
    ln -sf /dev/stderr /var/log/nginx/error.log ;\
# create a docker-entrypoint.d directory
    mkdir /docker-entrypoint.d ;

COPY docker-entrypoint.sh /
COPY 10-listen-on-ipv6-by-default.sh /docker-entrypoint.d
COPY 15-local-resolvers.envsh /docker-entrypoint.d
COPY 20-envsubst-on-templates.sh /docker-entrypoint.d
COPY 30-tune-worker-processes.sh /docker-entrypoint.d
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 80

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
