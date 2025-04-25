FROM docker.io/sourcemation/debian-12-slim:latest as builder

ARG TARGETARCH

ARG REDIS_SENTINEL_VERSION="stable"

RUN apt-get update && apt-get install -y sudo tzdata make curl build-essential libc6-dev bash libssl-dev

WORKDIR /tmp

RUN VERSION=$(echo ${REDIS_SENTINEL_VERSION} | sed -e "s/^v//g"); \
    case "${VERSION}" in \
       latest | stable) REDIS_DOWNLOAD_URL="http://download.redis.io/redis-stable.tar.gz" && VERSION="stable";; \
       *) REDIS_DOWNLOAD_URL="http://download.redis.io/releases/redis-${VERSION}.tar.gz";; \
    esac; \
    \
    curl -fL -Lo redis-${VERSION}.tar.gz ${REDIS_DOWNLOAD_URL}; \
    tar xvzf redis-${VERSION}.tar.gz; \
    \
    arch="$(uname -m)"; \
    extraJemallocConfigureFlags="--with-lg-page=16"; \
    if [ "$arch" = "aarch64" ] || [ "$arch" = "arm64" ]; then \
      sed -ri 's!cd jemalloc && ./configure !&'"$extraJemallocConfigureFlags"' !' /tmp/redis-${VERSION}/deps/Makefile; \
    fi; \
    export BUILD_TLS=yes; \
    make -C redis-${VERSION} all; \
    make -C redis-${VERSION} install

FROM docker.io/sourcemation/debian-12-slim:latest

ARG TARGETARCH

ENV SENTINEL_PORT=26379

LABEL name="redis-sentinel" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Redis Sentinel on Debian Container" \
      description="Provides Redis Sentinel on Debian 12 Container" \
      version="1.0.0" \
      io.k8s.display-name="Redis Sentinel on Debian Container" \
      io.k8s.description="Provides Redis Sentinel on Debian 12 Container" \
      io.openshift.tags="redis sentinel debian"

COPY --from=builder /usr/local/bin/redis-cli /usr/local/bin/redis-cli
COPY --from=builder /usr/local/bin/redis-sentinel /usr/local/bin/redis-sentinel

RUN apt-get update && apt-get upgrade -y

RUN groupadd -r -g 998 redis && useradd -r -g redis -u 998 redis && \
    apt-get update && apt-get install -y bash libssl3

COPY sentinel.conf /etc/redis/sentinel.conf

COPY entrypoint.sh /usr/bin/entrypoint.sh

COPY healthcheck.sh /usr/bin/healthcheck.sh

RUN chown -R 998:0 /etc/redis && \
    chmod -R g+rw /etc/redis && \
    mkdir /sentinel-data && \
    chown -R 998:0 /sentinel-data && \
    chmod -R g+rw /sentinel-data && \
    chmod -R g+rw /var/run

VOLUME ["/sentinel-data"]

WORKDIR /sentinel-data

EXPOSE ${SENTINEL_PORT}

USER 998

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
