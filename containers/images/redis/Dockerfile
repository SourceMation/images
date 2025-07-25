FROM docker.io/sourcemation/debian-12-slim:latest as builder

ARG TARGETARCH

ARG REDIS_VERSION="stable"

RUN apt-get update && apt-get install -y sudo tzdata make curl build-essential libc6-dev bash libssl-dev

WORKDIR /tmp

RUN VERSION=$(echo ${REDIS_VERSION} | sed -e "s/^v//g"); \
    case "${VERSION}" in \
       latest | stable) REDIS_DOWNLOAD_URL="https://download.redis.io/redis-stable.tar.gz" && VERSION="stable";; \
       *) REDIS_DOWNLOAD_URL="https://download.redis.io/releases/redis-${VERSION}.tar.gz";; \
    esac; \
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

LABEL name="redis" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Redis on Debian Container" \
      description="Provides Redis on Debian 12 Container" \
      version="8.0.3" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Redis on Debian Container" \
      io.k8s.description="Provides Redis on Debian 12 Container" \
      io.openshift.tags="redis debian"


ARG TARGETARCH

ENV REDIS_PORT=6379

COPY --from=builder /usr/local/bin/redis-server /usr/local/bin/redis-server
COPY --from=builder /usr/local/bin/redis-cli /usr/local/bin/redis-cli

RUN apt-get update && apt-get upgrade -y

RUN groupadd -r -g 1000 redis && useradd -r -g redis -u 1000 redis && \
    apt-get update && apt-get install -y bash libssl3

COPY redis.conf /etc/redis/redis.conf

COPY entrypoint.sh setupMasterSlave.sh healthcheck.sh /usr/bin/

RUN chown -R 1000:0 /etc/redis && \
    chmod -R g+rw /etc/redis && \
    mkdir /data && \
    chown -R 1000:0 /data && \
    chmod -R g+rw /data && \
    mkdir /node-conf && \
    chown -R 1000:0 /node-conf && \
    chmod -R g+rw /node-conf && \
    chmod -R g+rw /var/run

VOLUME ["/data"]
VOLUME ["/node-conf"]

WORKDIR /data

EXPOSE ${REDIS_PORT}

USER 1000

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
