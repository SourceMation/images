FROM sourcemation/debian-13-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="mysql" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="MySQL Community Server on Debian 13 Slim Container" \
      description="Provides MySQL Community Server on Debian 13 Slim Container" \
      version="8.4.7" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="MySQL Community Server on Debian 13 Slim Container" \
      io.k8s.description="Provides MySQL Community Server on Debian 13 Slim Container" \
      io.openshift.tags="mysql debian-13-slim"

ENV LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    MYSQL_ALLOW_EMPTY_PASSWORD="no" \
    MYSQL_RANDOM_ROOT_PASSWORD="no" \
    MYSQL_INITDB_SKIP_TZINFO="no"

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
        gnupg \
    && curl -fsSL https://repo.mysql.com/RPM-GPG-KEY-mysql-2023 | gpg --dearmor -o /etc/apt/keyrings/mysql-keyring.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/mysql-keyring.gpg trusted=yes] http://repo.mysql.com/apt/debian/ trixie mysql-8.4-lts" > /etc/apt/sources.list.d/mysql.list \
    && printf "Package: *\nPin: release o=MySQL\nPin-Priority: 999" > /etc/apt/preferences.d/mysql \
    && apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        --no-install-suggests \
        mysql-community-server \
        mysql-community-client \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/archives/* \
        /var/log/* \
        /tmp/* \
        /var/tmp/* \
        /var/lib/mysql/* \
    && mkdir -p /var/run/mysqld /var/lib/mysql /var/log/mysql /docker-entrypoint-initdb.d \
    && chown -R mysql:mysql /var/run/mysqld /var/lib/mysql /var/log/mysql /docker-entrypoint-initdb.d \
    && chmod 1777 /var/run/mysqld

COPY docker.cnf /etc/mysql/conf.d/10-docker.cnf
COPY docker-entrypoint.sh /usr/local/bin/

USER mysql
EXPOSE 3306
VOLUME ["/var/lib/mysql"]
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["mysqld"]