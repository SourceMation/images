# Copyright The CloudNativePG Contributors
# Copyright SourceMation
# License: Apache License 2.0

FROM sourcemation/postgres-17

# Do not split the description, otherwise we will see a blank space in the labels
LABEL name="cnpg-17" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="PostgreSQL 17 for CNPG on Debian 12 Slim Container" \
      description="Provides PostgreSQL 17 for CNPG on Debian Slim Container" \
      version="17.6.1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="PostgreSQL 17 for CNPG on Debian 12 Slim Container" \
      io.k8s.description="Provides PostgreSQL 17 for CPNG on Debian 12 Slim Container" \
      io.openshift.tags="postgresql debian-12-slim cnpg"

COPY requirements.txt /

# Install additional extensions
RUN set -xeu; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            "postgresql-${PG_MAJOR}-pgaudit" \
            "postgresql-${PG_MAJOR}-pgvector" \
            "postgresql-${PG_MAJOR}-pg-failover-slots" \
    ; \
    rm -fr /tmp/* ; \
    rm -rf /var/lib/apt/lists/*;

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
    pip3 install --break-system-packages --upgrade pip; \
    # TODO: Remove --no-deps once https://github.com/pypa/pip/issues/9644 is solved
    # THIS issue is not resolved for about 4 years so yeah, we need to keep this flag...
    pip3 install --break-system-packages --no-deps -r requirements.txt; \
    apt-get remove -y --purge --autoremove build-essential python3-dev; \
    rm -rf /var/lib/apt/lists/*;

# enable optional pl locale for postgres create cluster
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    sed -i -e 's/# pl_PL/pl_PL/g' -e 's/# en_US/en_US/g' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8

# Change the uid of postgres to 26
RUN usermod -u 26 postgres
USER 26
