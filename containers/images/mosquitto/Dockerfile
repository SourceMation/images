FROM sourcemation/rocky-9:latest

ARG TARGETARCH

LABEL name="mosquitto" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="Eclipse Public License 2.0 and Eclipse Distribution License 1.0" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Mosquitto from EPEL on EL9 Container" \
      description="Provides Mosquitto" \
      version="2.0.18" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Mosquitto on EL9 Container" \
      io.k8s.description="Provides Mosquitto on Rocky Linux 9 Container" \
      io.openshift.tags="mosquitto rockylinux"


ENV APP_VERSION="2.0.18" \
    APP_NAME="mosquitto"

# Install required system packages and dependencies
RUN dnf install -y epel-release && \
    dnf install -y mosquitto && \
    dnf update -y &&  dnf clean all

# prepare the image before starting the mosquito normally done by systemd service

RUN mkdir -m 740 -p /var/log/mosquitto && chown mosquitto:mosquitto /var/log/mosquitto && \
    mkdir -m 740 -p /run/mosquitto && chown mosquitto:mosquitto /run/mosquitto && \
    mkdir -m 740 -p /mosquitto/log && chown mosquitto:mosquitto /mosquitto/log && \
    mkdir -m 740 -p /mosquitto/data && chown mosquitto:mosquitto /mosquitto/data

VOLUME ["/mosquitto/data", "/mosquitto/log"]

COPY docker-entrypoint.sh /docker-entrypoint.sh
USER mosquitto
EXPOSE 1883
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/sbin/mosquitto", "-c", "/etc/mosquitto/mosquitto.conf"]
