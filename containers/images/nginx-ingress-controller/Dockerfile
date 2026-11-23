FROM sourcemation/golang-1.26:latest AS builder

ARG TARGETARCH
ARG INGRESS_NGINX_VERSION="controller-v1.15.1"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/*

# Download source
RUN curl -L "https://github.com/kubernetes/ingress-nginx/archive/refs/tags/${INGRESS_NGINX_VERSION}.tar.gz" -o ingress-nginx.tar.gz && \
    tar -xzf ingress-nginx.tar.gz --strip-components=1 && \
    rm ingress-nginx.tar.gz

# Build binaries
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build \
    -ldflags "-s -w -X k8s.io/ingress-nginx/version.RELEASE=${INGRESS_NGINX_VERSION} -X k8s.io/ingress-nginx/version.REPO=https://github.com/kubernetes/ingress-nginx" \
    -o nginx-ingress-controller ./cmd/nginx && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build -ldflags "-s -w" -o dbg ./cmd/dbg && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build -ldflags "-s -w" -o wait-shutdown ./cmd/waitshutdown

# Add load_module directives and lua paths to nginx.tmpl for dynamic modules
RUN sed -i '/pid {{ .PID }};/a \
load_module /usr/lib/nginx/modules/ndk_http_module.so;\
load_module /usr/lib/nginx/modules/ngx_http_lua_module.so;\
load_module /usr/lib/nginx/modules/ngx_stream_module.so;\
load_module /usr/lib/nginx/modules/ngx_stream_lua_module.so;\
load_module /usr/lib/nginx/modules/ngx_http_headers_more_filter_module.so;' rootfs/etc/nginx/template/nginx.tmpl && \
    sed -i 's|lua_package_path "/etc/nginx/lua/?.lua;;";|lua_package_path "/etc/nginx/lua/?.lua;/usr/local/lib/lua/?.lua;/usr/local/lib/lua/?/init.lua;;";\n    lua_package_cpath "/usr/local/lib/lua/5.1/?.so;/usr/local/lib/lua/?.so;;";|' rootfs/etc/nginx/template/nginx.tmpl && \
    sed -i 's|lua_package_path "/etc/nginx/lua/?.lua;/etc/nginx/lua/vendor/?.lua;;";|lua_package_path "/etc/nginx/lua/?.lua;/usr/local/lib/lua/?.lua;/usr/local/lib/lua/?/init.lua;;";\n    lua_package_cpath "/usr/local/lib/lua/5.1/?.so;/usr/local/lib/lua/?.so;;";|' rootfs/etc/nginx/template/nginx.tmpl

FROM sourcemation/debian-13-slim:latest AS module-builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpcre2-dev zlib1g-dev libssl-dev libluajit-5.1-dev curl ca-certificates libnginx-mod-http-lua libnginx-mod-stream git && \
    curl -sL https://nginx.org/download/nginx-1.26.3.tar.gz | tar -xz && \
    curl -sL https://github.com/openresty/stream-lua-nginx-module/archive/v0.0.16.tar.gz | tar -xz && \
    curl -sL https://github.com/vision5/ngx_devel_kit/archive/v0.3.3.tar.gz | tar -xz && \
    cd nginx-1.26.3 && \
    export LUAJIT_LIB=/usr/lib/x86_64-linux-gnu && \
    export LUAJIT_INC=/usr/include/luajit-2.1 && \
    ./configure --with-compat --with-stream --with-stream_ssl_module --with-http_ssl_module \
        --add-dynamic-module=../stream-lua-nginx-module-0.0.16 --add-dynamic-module=../ngx_devel_kit-0.3.3 && \
    make modules && \
    cd / && \
    git clone --depth 1 https://github.com/openresty/lua-cjson.git /tmp/lua-cjson && \
    cd /tmp/lua-cjson && make LUA_INCLUDE_DIR=/usr/include/luajit-2.1 && \
    cd / && \
    git clone --depth 1 https://github.com/openresty/lua-resty-balancer.git /tmp/lua-resty-balancer && \
    cd /tmp/lua-resty-balancer && make LUA_INCLUDE_DIR=/usr/include/luajit-2.1 && \
    gcc -shared -o /usr/local/lib/libmimalloc.so -x c /dev/null

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
      version="v1.15.1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="NGINX Ingress Controller on Debian 13 Slim Container" \
      io.k8s.description="Provides NGINX Ingress Controller on Debian 13 Slim Container" \
      io.openshift.tags="nginx-ingress-controller debian-13"

ENV INGRESS_NGINX_VERSION="controller-v1.15.1"

# Install nginx, lua and other dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    nginx \
    libnginx-mod-http-lua \
    libnginx-mod-stream \
    libnginx-mod-http-headers-more-filter \
    lua-resty-core \
    lua-resty-lrucache \
    ca-certificates \
    libcap2-bin \
    dumb-init \
    curl \
    diffutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy compiled stream lua module, libmimalloc dummy, and native libraries
COPY --from=module-builder /nginx-1.26.3/objs/ngx_stream_lua_module.so /usr/lib/nginx/modules/ngx_stream_lua_module.so
COPY --from=module-builder /usr/local/lib/libmimalloc.so /usr/local/lib/libmimalloc.so
COPY --from=registry.k8s.io/ingress-nginx/controller:v1.15.1 /usr/local/lib/lua /usr/local/lib/lua
COPY --from=module-builder /tmp/lua-cjson/cjson.so /usr/local/lib/lua/5.1/cjson.so
COPY --from=module-builder /tmp/lua-resty-balancer/librestychash.so /usr/local/lib/lua/librestychash.so

# Copy binaries, default nginx.conf and templates from builder
COPY --from=builder /app/nginx-ingress-controller /usr/local/bin/nginx-ingress-controller
COPY --from=builder /app/dbg /usr/local/bin/dbg
COPY --from=builder /app/wait-shutdown /usr/local/bin/wait-shutdown
COPY --from=builder /app/rootfs/etc/nginx/template /etc/nginx/template
COPY --from=builder /app/rootfs/etc/nginx/lua /etc/nginx/lua
COPY --from=builder /app/rootfs/etc/nginx/nginx.conf /etc/nginx/nginx.conf

# Symlinks for upstream compatibility and log forwarding
RUN ln -sf /usr/local/bin/nginx-ingress-controller /nginx-ingress-controller && \
    ln -sf /usr/local/bin/dbg /dbg && \
    ln -sf /usr/local/bin/wait-shutdown /wait-shutdown && \
    ln -sf /usr/sbin/nginx /usr/bin/nginx && \
    mkdir -p /usr/local/nginx/sbin && \
    ln -sf /usr/sbin/nginx /usr/local/nginx/sbin/nginx && \
    ln -sf /usr/local/lib/lua/5.1/cjson.so /usr/local/lib/lua/cjson.so && \
    mkdir -p /usr/local/lib/lua/cjson && \
    ln -sf /usr/local/lib/lua/5.1/cjson.so /usr/local/lib/lua/cjson/safe.so

# Setup user and required writable directories
RUN groupadd -g 1001 www-data-ingress && \
    useradd -u 1001 -g www-data-ingress -m www-data-ingress && \
    mkdir -p /etc/ingress-controller/ssl \
             /etc/ingress-controller/auth \
             /etc/ingress-controller/geoip \
             /etc/ingress-controller/telemetry \
             /var/log/nginx \
             /tmp/nginx \
             /var/lib/nginx \
             /etc/nginx \
             /tmp/coredump && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    chown -R 1001:1001 /etc/ingress-controller /etc/nginx /var/log/nginx /tmp/nginx /var/lib/nginx /home/www-data-ingress /tmp/coredump && \
    chmod -R 777 /etc/ingress-controller /tmp/nginx /var/log/nginx /var/lib/nginx /etc/nginx /tmp/coredump

# Allow nginx to bind to privileged ports
RUN setcap 'cap_net_bind_service=+ep' /usr/sbin/nginx && \
    setcap 'cap_net_bind_service=+ep' /usr/local/bin/nginx-ingress-controller

USER 1001
WORKDIR /home/www-data-ingress/

ENTRYPOINT [ "/usr/bin/dumb-init", "--", "nginx-ingress-controller" ]
CMD [ "--help" ]
