FROM sourcemation/debian-12-slim:latest AS builder

ARG TARGETARCH
ARG VERSION=1.6.39
ARG MEMCACHED_DOWNLOAD_URL=https://memcached.org/files/memcached-${VERSION}.tar.gz
ARG MEMCACHED_DOWNLOAD_SHA1_URL=https://memcached.org/files/memcached-${VERSION}.tar.gz.sha1
ARG CONFIGURE_OPTS="--enable-seccomp --enable-extstore --enable-proxy --enable-sasl --enable-sasl-pwdb --enable-tls"


ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
      --no-install-recommends \
      --no-install-suggests \
      build-essential \
      gcc \
      make \
      perl \
      libc6-dev  \
      libevent-dev \
      libseccomp-dev \
      libio-socket-ssl-perl \
      libsasl2-dev \
      libsasl2-modules \
      libssl-dev \
      ca-certificates \
      curl

WORKDIR /workspace

RUN curl -sSL -o memcached-${VERSION}.tar.gz ${MEMCACHED_DOWNLOAD_URL} \
    && curl -sSL -o memcached-${VERSION}.tar.gz.sha1 ${MEMCACHED_DOWNLOAD_SHA1_URL} \
    && cat memcached-${VERSION}.tar.gz.sha1 |sha1sum -c \
    && tar -xzf memcached-${VERSION}.tar.gz --strip-components=1

RUN ./configure --build=${TARGETARCH}-linux-gnu ${CONFIGURE_OPTS}
RUN make -j"$(nproc)"

FROM sourcemation/debian-12-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="memcached" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="BSD-3-Clause" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Memcached on Debian 12 Slim Container" \
      description="Provides Memcached on Debian 12 Slim Container" \
      version="1.6.39" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Memcached on Debian 12 Slim Container" \
      io.k8s.description="Provides Memcached Server on Debian 12 Slim Container" \
      io.openshift.tags="memcached debian-12-slim"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
      --no-install-recommends \
      --no-install-suggests \
      libevent-dev \
      libsasl2-dev \
      libssl-dev \
      libseccomp-dev \
      libc6 \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/archives/* \
        /var/log/* \
        /tmp/* \
        /var/tmp/*

COPY --from=builder /workspace/memcached /usr/local/bin/
COPY docker-entrypoint.sh /usr/local/bin/

RUN groupadd --system --gid 11211 memcache \
    && useradd --system --gid memcache --uid 11211 memcache \
    && chown memcache:memcache /usr/local/bin/docker-entrypoint.sh

EXPOSE 11211

USER memcache
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["memcached"]