FROM sourcemation/postgres-16-2-oneshot:16.2.1

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="cnpg-16-2-oneshot" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="PostgreSQL 16 for CNPG on Debian 13 Slim Container" \
      description="Provides PostgreSQL 16 for CNPG on Debian 13 Slim Container" \
      version="16.2.1" \
      io.k8s.display-name="PostgreSQL 16 for CNPG on Debian 13 Slim Container" \
      io.k8s.description="Provides PostgreSQL 16 for CPNG on Debian 13 Slim Container" \
      io.openshift.tags="postgresql debian-13-slim cnpg"

# Install additional extensions
RUN set -xeu; \
    apt-mark hold postgresql-16; \
    echo 'deb http://deb.debian.org/debian bookworm main' > /etc/apt/sources.list.d/bookworm.list; \
    echo 'Acquire::https::apt-archive.postgresql.org::Verify-Peer "false";' > /etc/apt/apt.conf.d/99postgresql-cert; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            "postgresql-${PG_MAJOR}-pgaudit=16.0-1.pgdg130+1" \
            "postgresql-${PG_MAJOR}-pgvector=0.6.0-1.pgdg130+1" \
            "postgresql-${PG_MAJOR}-pg-failover-slots=1.0.1-2.pgdg130+1" \
    ; \
    rm -fr /tmp/* ; \
    rm -rf /var/lib/apt/lists/*;

ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV BARMAN_VERSION="3.19.1"

# Install barman-cloud
RUN set -xeu; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            build-essential python3-dev \
            python3-pip \
            python3-psycopg2 \
            python3-setuptools \
    ; \
    pip3 install --no-cache-dir "barman[cloud,azure,snappy,google,zstandard,lz4]==${BARMAN_VERSION}" ;\
    apt-get remove -y --purge --autoremove build-essential python3-dev; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    rm -rf /var/lib/apt/lists/* /var/cache/* /var/log/* ;

# enable optional pl locale for postgres create cluster
RUN apt-get update && apt-get install -y locales locales-all && rm -rf /var/lib/apt/lists/*; \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    sed -i -e 's/# pl_PL/pl_PL/g' -e 's/# en_US/en_US/g' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8

# Change the uid of postgres to 26
RUN usermod -u 26 postgres
USER 26
