FROM sourcemation/debian-13-slim:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH
# Version is updated by init.sh
ARG VERSION="13.2"

LABEL name="pgbadger" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="PostgreSQL" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="pgBadger on Debian 13 Slim Container" \
      description="Provides pgBadger on Debian 13 Slim Container" \
      version="13.2" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="pgBadger on Debian 13 Slim Container" \
      io.k8s.description="Provides pgBadger on Debian 13 Slim Container" \
      io.openshift.tags="pgbadger debian-13-slim"

ENV PGBADGER_VERSION="${VERSION}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       wget \
       make \
       perl \
    && rm -rf /var/lib/apt/lists/* \
    && wget --progress=dot:giga -O pgbadger.tar.gz "https://github.com/darold/pgbadger/archive/v${PGBADGER_VERSION}.tar.gz" \
    && tar xzf pgbadger.tar.gz \
    && cd "pgbadger-${PGBADGER_VERSION}" \
    && perl Makefile.PL \
    && make \
    && make install \
    && cd .. \
    && rm -rf "pgbadger-${PGBADGER_VERSION}" pgbadger.tar.gz \
    && apt-get purge -y --auto-remove make wget ca-certificates \
    && apt-get clean

ENTRYPOINT ["pgbadger"]
CMD ["--help"]