FROM sourcemation/rocky-9:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="mosquitto" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="Eclipse Public License 2.0 and Eclipse Distribution License 1.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Mosquitto from EPEL on EL9 Container" \
      description="Provides Mosquitto" \
      version="2.0.22" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Mosquitto on EL9 Container" \
      io.k8s.description="Provides Mosquitto on Rocky Linux 9 Container" \
      io.openshift.tags="mosquitto rockylinux"


ENV APP_VERSION="2.0.22" \
    APP_NAME="mosquitto"

# Install required system packages and dependencies
RUN dnf install -y epel-release && \
    dnf install -y mosquitto && \
    dnf update -y &&  dnf clean all

# prepare the image before starting the mosquito normally done by systemd service
# IMPORTANT NOTE: because we are not using systemd - we have to manually create
# the mosquitto user and directories. Also the new version uses systemd-sysusers to create user.
# BUT DO NOT USE THE systemd-sysusers as it create the uid/gid 999 and we want
# to use 993 so the rolling update is seamless.

RUN groupadd --system --gid 993 mosquitto && \
    useradd --system --uid 993 --gid 993 --home-dir /etc/mosquitto --shell /sbin/nologin --comment "Mosquitto Broker" mosquitto && \
    mkdir -m 740 -p /var/log/mosquitto && chown mosquitto:mosquitto /var/log/mosquitto && \
    mkdir -m 740 -p /run/mosquitto && chown mosquitto:mosquitto /run/mosquitto && \
    mkdir -m 740 -p /mosquitto/log && chown mosquitto:mosquitto /mosquitto/log && \
    mkdir -m 740 -p /mosquitto/data && chown mosquitto:mosquitto /mosquitto/data

VOLUME ["/mosquitto/data", "/mosquitto/log"]

COPY docker-entrypoint.sh /docker-entrypoint.sh
USER mosquitto
EXPOSE 1883
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/sbin/mosquitto", "-c", "/etc/mosquitto/mosquitto.conf"]
