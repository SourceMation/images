FROM sourcemation/debian-12-slim:latest AS builder

ARG PGPOOL_VER=""

ENV PGPOOL_INSTALL_DIR /opt/pgpool-II
ENV PGPOOL_CONF_VOLUME /config

# Install packages
RUN set -eux \
    && apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        tar \
    && apt-get install -y \
        bison \
        flex \
        file \
        gcc \
        g++ \
        libbsd-dev \
        libpq-dev \
        make \
        patch \
        libssl-dev

COPY fix_compile_error.patch /tmp/pgpool/
COPY entrypoint.sh ${PGPOOL_INSTALL_DIR}/bin/
COPY start.sh ${PGPOOL_INSTALL_DIR}/bin/

# Install Pgpool-II
RUN set -eux \
    && wget -O /tmp/pgpool.tar.gz "https://pgpool.net/mediawiki/images/pgpool-II-${PGPOOL_VER}.tar.gz" \
    && tar -zxf /tmp/pgpool.tar.gz -C /tmp/pgpool --strip-components 1 \
    && cd /tmp/pgpool \
    && patch -p1 < fix_compile_error.patch \
    && ./configure \
        --prefix=${PGPOOL_INSTALL_DIR} \
        --with-openssl \
    && make -j "$(nproc)" \
    && make install


FROM sourcemation/postgres-17

ARG BUILD_DATE
ARG TARGETARCH

ARG PGPOOL_VER=""
ENV PGPOOL_INSTALL_DIR "/opt/pgpool-II"
ENV PGPOOL_CONF_VOLUME "/config"

LABEL name="pgpool" \
  vendor="Linux Polska" \
  url="https://sourcemation.com"\
  source="https://github.com/SourceMation/images/issues"\
  licenses="GPLv2" \
  created="$BUILD_DATE" \
  architecture="$TARGETARCH" \
  summary="Pgpool-II on Debian 12 Slim Container" \
  description="Provides pgpool-II on Debian 12 Slim Container" \
  version="$PGPOOL_VER" \
  io.k8s.display-name="Pgpool-II on Debian 12 Slim Container" \
  io.k8s.description="Provides pgpool-II on Debian 12 Slim Container" \
  io.openshift.tags="pgpool debian"

# Copy install directory
COPY --from=builder $PGPOOL_INSTALL_DIR $PGPOOL_INSTALL_DIR
RUN mkdir /var/run/pgpool \
    && chown -R postgres:postgres /var/run/pgpool ${PGPOOL_INSTALL_DIR}

# END INSTALL
USER postgres

ENTRYPOINT ["/opt/pgpool-II/bin/entrypoint.sh"]
CMD ["/opt/pgpool-II/bin/start.sh"]

EXPOSE 9999