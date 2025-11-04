FROM sourcemation/rabbitmq-4:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="rabbitmq-4-management" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="MPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="RabbitMQ-4-Management Debian 12-slim" \
      description="Provides RabbitMQ-4-Management on Debian 12-slim" \
      version="4.1.4" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="RabbitMQ-4-Management on Debian 12-slim Container" \
      io.k8s.description="Provides RabbitMQ-4-Management Debian 12-slim Container" \
      io.openshift.tags="rabbitmq-4-management debian-12-slim"

RUN set -eux \
	&& gosu rabbitmq rabbitmq-plugins enable --offline rabbitmq_management \
# make sure the metrics collector is re-enabled (disabled in the base image for Prometheus-style metrics by default)
	&& rm -f /etc/rabbitmq/conf.d/20-management_agent.disable_metrics_collector.conf \
# grab "rabbitmqadmin" from inside the "rabbitmq_management-X.Y.Z" plugin folder
# see https://github.com/docker-library/rabbitmq/issues/207
	&& cp /plugins/rabbitmq_management-*/priv/www/cli/rabbitmqadmin /usr/local/bin/rabbitmqadmin \
	&& [ -s /usr/local/bin/rabbitmqadmin ] \
	&& chmod +x /usr/local/bin/rabbitmqadmin \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends python3 \
	&& rm -rf /var/lib/apt/lists/* \
	&& rabbitmqadmin --version

ENV APP_NAME="rabbitmq-4-management" \
    APP_VERSION="4.1.4"

EXPOSE 15671 15672
