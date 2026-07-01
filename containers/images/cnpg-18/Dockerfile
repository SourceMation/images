# Copyright The CloudNativePG Contributors
# Copyright Sourcemation
# License: Apache License 2.0

FROM sourcemation/debian-13-slim:latest

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
      version="18.4.1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="PostgreSQL 18 for CNPG on Debian 13 Slim Container" \
      io.k8s.description="Provides PostgreSQL 18 for CPNG on Debian 13 Slim Container" \
      io.openshift.tags="postgresql debian-13-slim cnpg"

ENV PG_MAJOR="18"
ENV PG_VERSION="18.4-1.pgdg13+1"
ENV PATH=$PATH:/usr/lib/postgresql/$PG_MAJOR/bin
ENV BARMAN_VERSION="3.19.1"
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Install PostgreSQL 18 minimal, standard extensions, and system packages (including Barman)
RUN set -xeu; \
    apt-get update; \
    apt-get install -y --no-install-recommends postgresql-common ca-certificates gnupg; \
    /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y -c "${PG_MAJOR}"; \
    apt-get install -y --no-install-recommends -o Dpkg::::="--force-confdef" -o Dpkg::::="--force-confold" postgresql-common; \
    sed -ri 's/#(create_main_cluster) .*$/\1 = false/' /etc/postgresql-common/createcluster.conf; \
    apt-get install -y --no-install-recommends \
      libsasl2-modules libldap-common \
      -o Dpkg::::="--force-confdef" -o Dpkg::::="--force-confold" "postgresql-${PG_MAJOR}=${PG_VERSION}*"; \
    # Install standard extensions (including JIT package required for version 18+)
    apt-get install -y --no-install-recommends \
      "postgresql-${PG_MAJOR}-pgaudit" \
      "postgresql-${PG_MAJOR}-pgvector" \
      "postgresql-${PG_MAJOR}-pg-failover-slots" \
      "postgresql-${PG_MAJOR}-jit" \
      locales-all; \
    # Install Barman cloud dependencies and Barman
    apt-get install -y --no-install-recommends \
      build-essential python3-dev \
      python3-pip \
      python3-psycopg2 \
      python3-setuptools; \
    pip3 install --no-cache-dir "barman[cloud,azure,snappy,google,zstandard,lz4]==${BARMAN_VERSION}"; \
    python3 -c "import sysconfig, compileall; compileall.compile_dir(sysconfig.get_path('stdlib'), quiet=1); compileall.compile_dir(sysconfig.get_path('purelib'), quiet=1); compileall.compile_dir(sysconfig.get_path('platlib'), quiet=1)"; \
    # Clean up build dependencies and apt caches
    apt-get remove -y --purge --autoremove build-essential python3-dev; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    rm -rf /var/lib/apt/lists/* /var/cache/* /var/log/* /tmp/*

# enable optional pl locale for postgres create cluster
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    sed -i -e 's/# pl_PL/pl_PL/g' -e 's/# en_US/en_US/g' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8

# Change the uid of postgres to 26 and set default user
RUN usermod -u 26 postgres
USER 26
