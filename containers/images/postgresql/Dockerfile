FROM rockylinux/rockylinux:9

LABEL name="postgresql" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="PostgreSQL on EL9 Container" \
      description="Provides PostgreSQL on Rocky Linux 9 Container" \
      version="14.17" \
      io.k8s.display-name="PostgreSQL on EL9 Container" \
      io.k8s.description="Provides PostgreSQL on Rocky Linux 9 Container" \
      io.openshift.tags="postgresql rockylinux"

# 70 is the standard uid/gid for "postgres"
RUN set -eux; \
    groupadd -g 26 postgres; \
    useradd -u 26 -g postgres -p postgres -s /bin/sh -d /var/lib/postgresql -c "PostgreSQL Server" postgres; \
    mkdir -p /var/lib/postgresql/pg-data; \
    chown -R postgres:postgres /var/lib/postgresql; \
    dnf update -y && dnf install -y glibc-langpack-en glibc-langpack-pl

# make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
ENV LANG=pl_PL.utf8 \
    PG_MAJOR=14 \
    PG_VERSION="14.17" \
    LC_ALL=pl_PL.utf8 \
    PATH="$PATH:/usr/pgsql-14/bin" \
    PGDATA="/var/lib/postgresql/pg-data" 

ENV APP_VERSION="14.17" \
    APP_NAME="postgresql"

RUN mkdir /docker-entrypoint-initdb.d

RUN set -eux; \
    dnf -qy module disable postgresql; \
    dnf update -y; \
    dnf install -y --nogpgcheck https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm; \
    dnf install -y --nogpgcheck postgresql14-server && \
    dnf clean all

COPY requirements.txt /

# Install pgaudit
RUN set -xe; \
	yum install --nogpgcheck -y \
		pgaudit16_14 \
		postgresql14-contrib \
	; \
	rm -fr /tmp/* ; \
	rm -rf /var/lib/apt/lists/*;

# Install barman-cloud
RUN set -xe; \
	yum install --nogpgcheck -y \
		python3-pip \
		python3-psycopg2 \
		python3-setuptools \
	; \
	pip3 install --upgrade pip; \
	pip3 install --no-deps -r requirements.txt; \
	rm -rf /var/lib/apt/lists/*;

# make the sample config easier to munge (and "correct by default")
RUN set -eux; \
    cp -v /usr/pgsql-14/share/postgresql.conf.sample /usr/pgsql-14/share/postgresql.conf.sample.orig; \
    sed -ri "s!^#?(listen_addresses)\s*=\s*\S+.*!\1 = '*'!" /usr/pgsql-14/share/postgresql.conf.sample; \
    grep -F "listen_addresses = '*'" /usr/pgsql-14/share/postgresql.conf.sample;

RUN mkdir -p /var/run/postgresql && chown -R postgres:postgres /var/run/postgresql && chmod 3777 /var/run/postgresql

VOLUME /var/lib/postgresql

# this 777 will be replaced by 700 at runtime (allows semi-arbitrary "--user" values)

RUN mkdir -p "$PGDATA"; \
    chown -R postgres:postgres "$PGDATA"; \
    chmod 1777 "$PGDATA"

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod 777 /usr/local/bin/docker-entrypoint.sh; \
    ln -s /usr/local/bin/docker-entrypoint.sh /
USER 26

ENTRYPOINT ["docker-entrypoint.sh"]

# We set the default STOPSIGNAL to SIGINT, which corresponds to what PostgreSQL
# calls "Fast Shutdown mode" wherein new connections are disallowed and any
# in-progress transactions are aborted, allowing PostgreSQL to stop cleanly and
# flush tables to disk, which is the best compromise available to avoid data
# corruption.
#
# Users who know their applications do not keep open long-lived idle connections
# may way to use a value of SIGTERM instead, which corresponds to "Smart
# Shutdown mode" in which any existing sessions are allowed to finish and the
# server stops when all sessions are terminated.
#
# See https://www.postgresql.org/docs/12/server-shutdown.html for more details
# about available PostgreSQL server shutdown signals.
#
# See also https://www.postgresql.org/docs/12/server-start.html for further
# justification of this as the default value, namely that the example (and
# shipped) systemd service files use the "Fast Shutdown mode" for service
# termination.
#
STOPSIGNAL SIGINT
#
# An additional setting that is recommended for all users regardless of this
# value is the runtime "--stop-timeout" (or your orchestrator/runtime's
# equivalent) for controlling how long to wait between sending the defined
# STOPSIGNAL and sending SIGKILL (which is likely to cause data corruption).
#
# The default in most runtimes (such as Docker) is 10 seconds, and the
# documentation at https://www.postgresql.org/docs/12/server-start.html notes
# that even 90 seconds may not be long enough in many instances.
EXPOSE 5432

CMD ["postgres"]
