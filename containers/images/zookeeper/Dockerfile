FROM sourcemation/jre-21:latest

ARG BUILD_DATE
ARG TARGETARCH
ARG ZOOKEEPER_VERSION=3.9.4

LABEL name="zookeeper" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Apache ZooKeeper on Debian 12 Slim Container" \
      description="Provides Apache ZooKeeper on Debian 12 Slim Container" \
      version="3.9.4" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Apache ZooKeeper on Debian 12 Slim Container" \
      io.k8s.description="Provides Apache ZooKeeper on Debian 12 Slim Container" \
      io.openshift.tags="zookeeper debian-12-slim"

ENV DEBIAN_FRONTEND=noninteractive \
    ZK_HOME=/opt/zookeeper \
    ZK_USER=zookeeper \
    ZK_DATA_DIR=/var/lib/zookeeper/data \
    ZK_DATA_LOG_DIR=/var/lib/zookeeper/logs \
    ZK_CONF_DIR=/opt/zookeeper/conf \
    ZK_LOG_DIR=/var/log/zookeeper
ENV PATH=$PATH:$ZK_HOME/bin

RUN useradd -r -d $ZK_HOME -s /bin/bash $ZK_USER \
    && mkdir -p $ZK_HOME $ZK_DATA_DIR $ZK_DATA_LOG_DIR $ZK_LOG_DIR $ZK_CONF_DIR \
    && chown -R $ZK_USER:$ZK_USER $ZK_HOME $ZK_DATA_DIR $ZK_DATA_LOG_DIR $ZK_LOG_DIR $ZK_CONF_DIR

WORKDIR /tmp
RUN /bin/bash -c set -o pipefail \
    && apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        --no-install-suggests \
        curl \
        ca-certificates \
        netcat-traditional \
        openssl \
    && curl -fsSL -O "https://downloads.apache.org/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz" \
    && curl -fsSL -O "https://downloads.apache.org/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz.sha512" \
    && sha512sum -c apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz.sha512 \
    && tar -xzf apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz \
    && mv apache-zookeeper-${ZOOKEEPER_VERSION}-bin/* $ZK_HOME/ \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/archives/* \
        /var/log/* \
        /tmp/* \
        /var/tmp/* \
        $ZK_HOME/docs \
        $ZK_HOME/*.md

COPY --chown=$ZK_USER:$ZK_USER zoo.cfg $ZK_CONF_DIR/
COPY docker-entrypoint.sh /usr/local/bin/

WORKDIR $ZK_HOME
USER $ZK_USER
EXPOSE 2181 2888 3888 8080
VOLUME ["$ZK_DATA_DIR", "$ZK_DATA_LOG_DIR", "$ZK_LOG_DIR"]
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["zkServer.sh"]