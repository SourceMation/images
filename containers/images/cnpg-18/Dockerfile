# Copyright The CloudNativePG Contributors
# Copyright Sourcemation
# License: Apache License 2.0

FROM sourcemation/postgres-18

ARG BUILD_DATE
ARG TARGETARCH

# Do not split the description, otherwise we will see a blank space in the labels
LABEL name="cnpg-18" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="PostgreSQL 18 for CNPG on Debian 13 Slim Container" \
      description="Provides PostgreSQL 18 for CNPG on Debian Slim Container" \
      version="18.1.1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="PostgreSQL 18 for CNPG on Debian 13 Slim Container" \
      io.k8s.description="Provides PostgreSQL 18 for CPNG on Debian 13 Slim Container" \
      io.openshift.tags="postgresql debian-13-slim cnpg"

# Install additional extensions
RUN set -xeu; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            "postgresql-${PG_MAJOR}-pgaudit" \
            "postgresql-${PG_MAJOR}-pgvector" \
            "postgresql-${PG_MAJOR}-pg-failover-slots" \
    ; \
    rm -rf /tmp/* ; \
    rm -rf /var/lib/apt/lists/* /var/cache/* /var/log/*

# Barman is install from pip, it will break system packages
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV BARMAN_VERSION="3.17.0"

# Install barman-cloud
RUN set -xeu; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            # We require build-essential and python3-dev to build lz4 on arm64 since there isn't a pre-compiled wheel available
            build-essential python3-dev \
            python3-pip \
            python3-psycopg2 \
            python3-setuptools \
    ; \
    # pip3 install --break-system-packages --upgrade pip; \
    pip3 install --no-cache-dir "barman[cloud,azure,snappy,google,zstandard,lz4]==${BARMAN_VERSION}" ;\
    apt-get remove -y --purge --autoremove build-essential python3-dev; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    rm -rf /var/lib/apt/lists/* /var/cache/* /var/log/* ;

# enable optional pl locale for postgres create cluster
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    sed -i -e 's/# pl_PL/pl_PL/g' -e 's/# en_US/en_US/g' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8

# Change the uid of postgres to 26
RUN usermod -u 26 postgres
USER 26
