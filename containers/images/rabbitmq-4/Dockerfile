FROM sourcemation/erlang-27:latest AS builder

ARG RABBITMQ_VERSION=4.1.4
ARG RABBITMQ_SOURCE_URL="https://github.com/rabbitmq/rabbitmq-server/releases/download/v${RABBITMQ_VERSION}/rabbitmq-server-generic-unix-latest-toolchain-${RABBITMQ_VERSION}.tar.xz"
ARG RABBITMQ_PGP_KEY_ID=0x0A9AF2115F4687BD29803A206B73A36E6026DFCA
ARG RABBITMQ_PATH="/usr/local/src/rabbitmq"

ARG RABBITMQ_DATA_DIR=/var/lib/rabbitmq
ARG RABBITMQ_HOME=/opt/rabbitmq

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      curl \
      gnupg \
      xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsL -o "$RABBITMQ_PATH.tar.xz.asc" "$RABBITMQ_SOURCE_URL.asc" \
    && curl -fsL -o "$RABBITMQ_PATH.tar.xz" "$RABBITMQ_SOURCE_URL" \
    \
    && export GNUPGHOME="$(mktemp -d)" \
    && gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys "$RABBITMQ_PGP_KEY_ID" \
    && gpg --batch --verify "$RABBITMQ_PATH.tar.xz.asc" "$RABBITMQ_PATH.tar.xz" \
    && gpgconf --kill all \
    && rm -rf "$GNUPGHOME" \
    \
    && mkdir -p "$RABBITMQ_HOME" \
	  && tar --extract --file "$RABBITMQ_PATH.tar.xz" --directory "$RABBITMQ_HOME" --strip-components=1 \
	  && rm -rf "$RABBITMQ_PATH"* \
# Do not default SYS_PREFIX to RABBITMQ_HOME, leave it empty
    && grep -qE '^SYS_PREFIX=\$\{RABBITMQ_HOME\}$' "$RABBITMQ_HOME/sbin/rabbitmq-defaults" \
    && sed -i 's/^SYS_PREFIX=.*$/SYS_PREFIX=/' "$RABBITMQ_HOME/sbin/rabbitmq-defaults" \
    && grep -qE '^SYS_PREFIX=$' "$RABBITMQ_HOME/sbin/rabbitmq-defaults"

FROM sourcemation/erlang-27:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="rabbitmq-4" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="MPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="RabbitMQ on Debian 13-slim" \
      description="Provides RabbitMQ on Debian 13-slim" \
      version="4.1.4" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="RabbitMQ on Debian 13-slim Container" \
      io.k8s.description="Provides RabbitMQ Debian 13-slim Container" \
      io.openshift.tags="rabbitmq-4 debian-13-slim"

ENV RABBITMQ_DATA_DIR=/var/lib/rabbitmq
ENV RABBITMQ_HOME=/opt/rabbitmq
ENV PATH=$RABBITMQ_HOME/sbin:$PATH

# Create rabbitmq system user & group, fix permissions & allow root user to connect to the RabbitMQ Erlang VM
RUN groupadd --gid 999 --system rabbitmq \
    && useradd --uid 999 --system --home-dir "$RABBITMQ_DATA_DIR" --gid rabbitmq rabbitmq \
    && mkdir -p "$RABBITMQ_DATA_DIR" /etc/rabbitmq /etc/rabbitmq/conf.d /tmp/rabbitmq-ssl /var/log/rabbitmq \
    && chown -fR rabbitmq:rabbitmq "$RABBITMQ_DATA_DIR" /etc/rabbitmq /etc/rabbitmq/conf.d /tmp/rabbitmq-ssl /var/log/rabbitmq \
    && chmod 1777 "$RABBITMQ_DATA_DIR" /etc/rabbitmq /etc/rabbitmq/conf.d /tmp/rabbitmq-ssl /var/log/rabbitmq \
    && ln -sf "$RABBITMQ_DATA_DIR/.erlang.cookie" /root/.erlang.cookie

COPY --from=builder --chown=rabbitmq:rabbitmq $RABBITMQ_HOME $RABBITMQ_HOME

# verify assumption of no stale cookies
RUN	apt-get update \
    && apt-get install -y --no-install-recommends gosu tzdata \
    && rm -rf /var/lib/apt/lists/* \
    \
    && [ ! -e "$RABBITMQ_DATA_DIR/.erlang.cookie" ] \
# Ensure RabbitMQ was installed correctly by running a few commands that do not depend on a running server, as the rabbitmq user
# If they all succeed, it's safe to assume that things have been set up correctly
    && gosu rabbitmq rabbitmqctl help \
    && gosu rabbitmq rabbitmqctl list_ciphers \
    && gosu rabbitmq rabbitmq-plugins list \
# no stale cookies
    && rm "$RABBITMQ_DATA_DIR/.erlang.cookie"

# Enable Prometheus-style metrics by default (https://github.com/docker-library/rabbitmq/issues/419)
RUN gosu rabbitmq rabbitmq-plugins enable --offline rabbitmq_prometheus

# Added for backwards compatibility - users can simply COPY custom plugins to /plugins
RUN ln -sf /opt/rabbitmq/plugins /plugins

# set home so that any `--user` knows where to put the erlang cookie
ENV HOME=$RABBITMQ_DATA_DIR
# Hint that the data (a.k.a. home dir) dir should be separate volume
VOLUME $RABBITMQ_DATA_DIR

ENV APP_NAME="rabbitmq" \
    APP_VERSION="4.1.4" \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8 \
    LC_ALL=C.UTF-8

COPY --chown=rabbitmq:rabbitmq 10-defaults.conf 20-management_agent.disable_metrics_collector.conf /etc/rabbitmq/conf.d/
COPY docker-entrypoint.sh /usr/local/bin/

EXPOSE 4369 5671 5672 15691 15692 25672
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["rabbitmq-server"]
