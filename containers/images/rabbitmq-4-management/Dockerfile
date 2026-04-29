FROM sourcemation/rabbitmq-4:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="rabbitmq-4-management" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="MPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="RabbitMQ-4-Management Debian 13-slim" \
      description="Provides RabbitMQ-4-Management on Debian 13-slim" \
      version="4.3.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="RabbitMQ-4-Management on Debian 13-slim Container" \
      io.k8s.description="Provides RabbitMQ-4-Management Debian 13-slim Container" \
      io.openshift.tags="rabbitmq-4-management debian-13-slim"

RUN set -eux; \
    gosu rabbitmq rabbitmq-plugins enable --offline rabbitmq_management; \
# make sure the metrics collector is re-enabled (disabled in the base image for Prometheus-style metrics by default)
    rm -f /etc/rabbitmq/conf.d/20-management_agent.disable_metrics_collector.conf; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl; \
    arch="$(dpkg --print-architecture)"; \
    case "$arch" in \
        'amd64') url='https://github.com/rabbitmq/rabbitmqadmin-ng/releases/download/v2.29.0/rabbitmqadmin-2.29.0-x86_64-unknown-linux-gnu' ;; \
        'arm64') url='https://github.com/rabbitmq/rabbitmqadmin-ng/releases/download/v2.29.0/rabbitmqadmin-2.29.0-aarch64-unknown-linux-gnu' ;; \
        *) echo "[INFO] rabbitmqadmin is not available on $arch (yet?)"; exit 0 ;; \
    esac; \
    curl -fsL "$url" -o /usr/local/bin/rabbitmqadmin; \
    chmod +x /usr/local/bin/rabbitmqadmin; \
    [ -s /usr/local/bin/rabbitmqadmin ]; \
    rm -rf /var/lib/apt/lists/*; \
    rabbitmqadmin --help
ENV APP_NAME="rabbitmq-4-management" \
    APP_VERSION="4.3.0"

EXPOSE 15671 15672
