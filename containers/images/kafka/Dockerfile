FROM sourcemation/rocky-9:latest AS jsa-builder

# UPDATE init.sh to include new scripts
ENV kafka_url=https://downloads.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz

COPY jsa_launch /etc/kafka/docker/jsa_launch

# Apache Software Foundation dev keys: https://downloads.apache.org/kafka/KEYS
ADD KEYS /

RUN dnf install -y --setopt=install_weak_deps=0 --setopt=tsflags=nodocs gpg hostname procps-ng java-21-openjdk-headless && dnf clean all && \
    gpg --import KEYS &&\
    mkdir opt/kafka &&\
    curl -L -o kafka.tgz "$kafka_url"; curl -L -o kafka.tgz.asc "$kafka_url".asc ;\
    gpg --verify kafka.tgz.asc kafka.tgz &&\
    tar xfz kafka.tgz -C /opt/kafka --strip-components 1

# Generate jsa files using dynamic CDS for kafka server start command and kafka storage format command
RUN /etc/kafka/docker/jsa_launch

FROM sourcemation/rocky-9:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="kafka" \
      vendor="Sourcemation" \
      url="https://sourcemation.com"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Apache Kafka on EL9 Container" \
      description="Provides Apache Kafka on Rocky Linux 9 Container" \
      version="3.9.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Apache Kafka on EL9 Container" \
      io.k8s.description="Provides Apache Kafka on Rocky Linux 9 Container" \
      io.openshift.tags="kafka rockylinux"

RUN dnf install -y --setopt=install_weak_deps=0 --setopt=tsflags=nodocs hostname java-21-openjdk-headless procps-ng && dnf clean all

RUN mkdir /opt/kafka

COPY --from=jsa-builder kafka.tgz /

RUN tar xfz kafka.tgz -C /opt/kafka --strip-components 1 && \
    mkdir -p /var/lib/kafka/data /etc/kafka/secrets && \
    mkdir -p /etc/kafka/docker /usr/logs /mnt/shared/config &&\
    useradd appuser &&\
    chown appuser:appuser -R /usr/logs /opt/kafka /mnt/shared/config &&\
    chown appuser:root -R /var/lib/kafka /etc/kafka/secrets /etc/kafka &&\
    chmod -R ug+w /etc/kafka /var/lib/kafka /etc/kafka/secrets && \
    cp /opt/kafka/config/log4j.properties /etc/kafka/docker/log4j.properties && \
    cp /opt/kafka/config/tools-log4j.properties /etc/kafka/docker/tools-log4j.properties &&\
    cp /opt/kafka/config/kraft/server.properties /etc/kafka/docker/server.properties &&\
    rm kafka.tgz

# TODO - Add the kafka.jsa file
COPY --from=jsa-builder kafka.jsa /opt/kafka/kafka.jsa
COPY --from=jsa-builder storage.jsa /opt/kafka/storage.jsa
COPY --chown=appuser:appuser common-scripts/ /etc/kafka/docker
COPY --chown=appuser:appuser launch /etc/kafka/docker/launch
EXPOSE 9092

VOLUME ["/var/lib/kafka/data", "/mnt/shared/config", "/etc/kafka/secrets"]

RUN version=$(/opt/kafka/bin/kafka-topics.sh --version | grep -oP "\d+\.\d+\.\d+" | head -1) && \
    echo "kafka: $version" >> /var/tmp/sourcemation.yml

USER appuser

WORKDIR /opt/kafka/bin

CMD ["/etc/kafka/docker/run"]
