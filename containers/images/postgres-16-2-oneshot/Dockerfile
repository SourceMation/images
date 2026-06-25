FROM sourcemation/debian-13-slim:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="postgres-16-2-oneshot" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="PostgreSQL 16.2 on Debian 13 Slim Container" \
      description="Provides PostgreSQL 16.2 on Debian 13 Slim Container" \
      version="16.2.1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="PostgreSQL 16.2 on Debian 13 Slim Container" \
      io.k8s.description="Provides PostgreSQL 16.2 on Debian 13 Slim Container" \
      io.openshift.tags="postgresql debian-13-slim oneshot"

# Setup the environment variables
ENV LANG en_US.utf8
ENV PG_MAJOR="16"
ENV PATH="$PATH:/usr/lib/postgresql/$PG_MAJOR/bin"
ENV PGDATA /var/lib/postgresql/data
ENV PG_VERSION="16.2-1.pgdg130+1"
ENV GOSU_VERSION 1.17

# explicitly set user/group IDs
RUN set -eux; \
    groupadd -r postgres --gid=999; \
    useradd -r -g postgres --uid=999 --home-dir=/var/lib/postgresql --shell=/bin/bash postgres; \
    install --verbose --directory --owner postgres --group postgres --mode 1777 /var/lib/postgresql

RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends gnupg less ; \
    rm -rf /var/lib/apt/lists/*

# grab gosu for easy step-down from root
# https://github.com/tianon/gosu/releases
RUN set -eux; \
    savedAptMark="$(apt-mark showmanual)"; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates wget; \
    rm -rf /var/lib/apt/lists/*; \
    dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
    wget --progress=dot:giga -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
    wget --progress=dot:giga -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
    GNUPGHOME="$(mktemp -d)"; export GNUPGHOME; \
    gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
    gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
    apt-mark auto '.*' > /dev/null; \
    [ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    chmod +x /usr/local/bin/gosu; \
    gosu --version; \
    gosu nobody true

# make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
RUN set -eux; \
    if [ -f /etc/dpkg/dpkg.cfg.d/docker ]; then \
            grep -q '/usr/share/locale' /etc/dpkg/dpkg.cfg.d/docker; \
            sed -ri '/\/usr\/share\/locale/d' /etc/dpkg/dpkg.cfg.d/docker; \
    fi; \
    if grep -q '/usr/share/locale' /etc/dpkg/dpkg.cfg.d/docker; then \
        echo "Failed to remove locale exclusion from /etc/dpkg/dpkg.cfg.d/docker"; \
        exit 1; \
    fi; \
    apt-get update; apt-get install -y --no-install-recommends locales; rm -rf /var/lib/apt/lists/*; \
    echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen; \
    locale-gen; \
    locale -a | grep 'en_US.utf8'

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            libnss-wrapper \
            xz-utils \
            zstd \
    ; \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /docker-entrypoint-initdb.d

RUN set -ex; \
    key='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8'; \
    GNUPGHOME="$(mktemp -d)"; export GNUPGHOME; \
    mkdir -p /usr/local/share/keyrings/; \
    gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$key"; \
    gpg --batch --export --armor "$key" > /usr/local/share/keyrings/postgres.gpg.asc; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME"


RUN set -ex; \
    export PYTHONDONTWRITEBYTECODE=1; \
    echo 'deb http://deb.debian.org/debian bookworm main' > /etc/apt/sources.list.d/bookworm.list; \
    echo 'Acquire::https::apt-archive.postgresql.org::Verify-Peer "false";' > /etc/apt/apt.conf.d/99postgresql-cert; \
    \
    aptRepo="[ signed-by=/usr/local/share/keyrings/postgres.gpg.asc ] https://apt-archive.postgresql.org/pub/repos/apt/ trixie-pgdg-archive main $PG_MAJOR"; \
    echo "deb $aptRepo" > /etc/apt/sources.list.d/pgdg.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends postgresql-common; \
    sed -ri 's/#(create_main_cluster) .*$/\1 = false/' /etc/postgresql-common/createcluster.conf; \
    apt-get install -y --no-install-recommends --allow-downgrades \
            "postgresql-$PG_MAJOR=$PG_VERSION" \
            "postgresql-client-$PG_MAJOR=$PG_VERSION" \
    ; \
    \
    rm -rf /var/lib/apt/lists/*; \
    \
    if [ -n "$tempDir" ]; then \
            apt-get purge -y --auto-remove; \
            rm -rf "$tempDir" /etc/apt/sources.list.d/temp.list; \
    fi; \
    \
    find /usr -name '*.pyc' -type f -exec bash -c 'for pyc; do dpkg -S "$pyc" &> /dev/null || rm -vf "$pyc"; done' -- '{}' +; \
    \
    postgres --version

# make the sample config easier to munge (and "correct by default")
RUN set -eux; \
    dpkg-divert --add --rename --divert "/usr/share/postgresql/postgresql.conf.sample.dpkg" "/usr/share/postgresql/$PG_MAJOR/postgresql.conf.sample"; \
    cp -v /usr/share/postgresql/postgresql.conf.sample.dpkg /usr/share/postgresql/postgresql.conf.sample; \
    ln -sv ../postgresql.conf.sample "/usr/share/postgresql/$PG_MAJOR/"; \
    sed -ri "s!^#?(listen_addresses)\s*=\s*\S+.*!\1 = '*'!" /usr/share/postgresql/postgresql.conf.sample; \
    grep -F "listen_addresses = '*'" /usr/share/postgresql/postgresql.conf.sample

RUN install --verbose --directory --owner postgres --group postgres --mode 3777 /var/run/postgresql \
    && install --verbose --directory --owner postgres --group postgres --mode 1777 "$PGDATA"

COPY docker-entrypoint.sh docker-ensure-initdb.sh /usr/local/bin/
RUN ln -sT docker-ensure-initdb.sh /usr/local/bin/docker-enforce-initdb.sh
ENTRYPOINT ["docker-entrypoint.sh"]

STOPSIGNAL SIGINT
VOLUME /var/lib/postgresql/data
EXPOSE 5432
CMD ["postgres"]