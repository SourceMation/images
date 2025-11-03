FROM sourcemation/debian-13-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="mariadb" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="mariadb on Debian 13 Slim Container" \
      description="Provides mariadb on Debian 13 Slim Container" \
      version="12.0.2" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="mariadb on Debian 13 Slim Container" \
      io.k8s.description="Provides mariadb on Debian 13 Slim Container" \
      io.openshift.tags="mariadb debian-13-slim"

ENV LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    MARIADB_ALLOW_EMPTY_PASSWORD="no" \
    MARIADB_RANDOM_ROOT_PASSWORD="no" \
    MARIADB_INITDB_SKIP_TZINFO="no"

RUN useradd -r -d /var/lib/mysql -s /bin/bash mysql

RUN apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        --no-install-suggests \
        curl \
        ca-certificates \
        gosu \
        pwgen \
        tzdata \
        zlib1g \
    && curl -o /etc/apt/keyrings/mariadb-keyring.pgp 'https://mariadb.org/mariadb_release_signing_key.pgp' \
    && echo "deb [signed-by=/etc/apt/keyrings/mariadb-keyring.pgp] https://deb.mariadb.org/12.0/debian trixie main" > /etc/apt/sources.list.d/mariadb.list \
    && printf "Package: *\nPin: release o=MariaDB\nPin-Priority: 999" > /etc/apt/preferences.d/mariadb \
    && apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        --no-install-suggests \
        mariadb-server \
        mariadb-client \
        mariadb-backup \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/archives/* \
        /var/log/* \
        /tmp/* \
        /var/tmp/* \
        /var/lib/mysql/* \
    && sed -Ei 's/^(bind-address\s)/#&/' /etc/mysql/mariadb.conf.d/50-server.cnf \
    && mkdir -p /var/run/mysqld /var/lib/mysql /var/log/mysql /docker-entrypoint-initdb.d \
    && chown -R mysql:mysql /var/run/mysqld /var/lib/mysql /var/log/mysql /docker-entrypoint-initdb.d \
    && chmod 1777 /var/run/mysqld

COPY docker.cnf /etc/mysql/mariadb.conf.d/10-docker.cnf
COPY docker-entrypoint.sh /usr/local/bin/

USER mysql
EXPOSE 3306
VOLUME ["/var/lib/mysql"]
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["mariadbd"]