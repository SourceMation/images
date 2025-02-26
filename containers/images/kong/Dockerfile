FROM rockylinux/rockylinux:9

COPY kong-x86_64.rpm /tmp/kong.rpm

LABEL name="kong" \
      vendor="SourceMation" \
      url="https://sourcemation.com"\
      licenses="Apache-2.0" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Kong Gateway on EL9 Container" \
      description="Provides Kong Gateway Community Edition on Rocky Linux 9 Container" \
      version="3.7.1" \
      io.k8s.display-name="Kong Gateway on EL9 Container" \
      io.k8s.description="Provides Kong Gateway Community Edition on Rocky Linux 9 Container" \
      io.openshift.tags="kong gateway rockylinux"

RUN set -ex; \
    yum install -y /tmp/kong.rpm \
    && rm /tmp/kong.rpm \
    && chown kong:0 /usr/local/bin/kong \
    && chown -R kong:0 /usr/local/kong \
    && ln -s /usr/local/openresty/luajit/bin/luajit /usr/local/bin/luajit \
    && ln -s /usr/local/openresty/luajit/bin/luajit /usr/local/bin/lua \
    && ln -s /usr/local/openresty/nginx/sbin/nginx /usr/local/bin/nginx \
    && kong version

COPY docker-entrypoint.sh /docker-entrypoint.sh

USER kong

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 8000 8443 8001 8444 8002 8445 8003 8446 8004 8447

STOPSIGNAL SIGQUIT


CMD ["kong", "start"]
