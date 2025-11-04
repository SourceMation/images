FROM sourcemation/postgres-18

ARG BUILD_DATE
ARG TARGETARCH

ENV REPMGR_VER="5.5.0"
ENV BINARY_URL="https://github.com/EnterpriseDB/repmgr/archive/v${REPMGR_VER}.tar.gz"

LABEL name="postgres-repmgr" \
  vendor="Linux Polska" \
  url="https://sourcemation.com"\
  source="https://github.com/Sourcemation/images/issues"\
  licenses="GPLv2" \
  created="$BUILD_DATE" \
  architecture="$TARGETARCH" \
  summary="Postgresql-repmgr on Debian 13 Slim Container" \
  description="Provides postgres-repmgr on Debian 13 Slim Container" \
  version="5.5.0" \
  io.k8s.display-name="Postgresql-repmgr on Debian 13 Slim Container" \
  io.k8s.description="Provides postgres-repmgr on Debian 13 Slim Container" \
  io.openshift.tags="postgres repmgr debian"


RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      build-essential \
      ca-certificates \
      flex \
      libcurl4 \
      libcurl4-openssl-dev \
      libedit-dev \
      libjson-c-dev \
      libkrb5-dev \
      liblz4-dev  \
      libnuma-dev \
      libpam0g-dev \ 
      libpq-dev \
      libreadline-dev \
      libselinux1-dev \
      libxml2-dev \
      libxslt1-dev \
      libzstd-dev \
      postgresql-server-dev-all \
      tar \
      wget \
      zlib1g-dev ; \
    \
    wget --progress=dot:giga -O /tmp/postgres-repmgr.tar.gz ${BINARY_URL}; \
    mkdir /tmp/repmgr;\
    tar --extract \
        --file=/tmp/postgres-repmgr.tar.gz \
        --directory="/tmp/repmgr" \
        --strip-components=1 \
        --no-same-owner; \
    \
    cd /tmp/repmgr && ./configure && make LDFLAGS="-L /usr/lib/postgresql/18/lib" USE_PGXS=1 install; \
    cd /; \
    apt-get purge -y --auto-remove \
      ca-certificates \
      wget \
      build-essential \
      libpq-dev \
      libxslt1-dev \
      libxml2-dev \
      libedit-dev \
      postgresql-server-dev-all \
      flex \
      libselinux1-dev libzstd-dev liblz4-dev libpam0g-dev libkrb5-dev zlib1g-dev libreadline-dev; \
    \
    rm -f /tmp/postgres-repmgr.tar.gz;\
    rm -rf /tmp/repmgr; \
    rm -rf /var/lib/apt/lists/*;

# END INSTALL
COPY entrypoint.sh /entrypoint.sh
RUN mkdir -p /etc/repmgr && chown -R postgres:postgres /etc/repmgr

USER postgres

ENTRYPOINT ["/entrypoint.sh"]

CMD ["postgres"]
