FROM rockylinux/rockylinux:9

LABEL name="rabbitmq" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Rabbitmq on EL9 Container" \
      description="Provides Rabbitmq on Rocky Linux 9 Container" \
      version="4.0.7" \
      io.k8s.display-name="Rabbitmq on EL9 Container" \
      io.k8s.description="Provides Rabbitmq on Rocky Linux 9 Container" \
      io.openshift.tags="rabbitmq rockylinux"

ENV LANG=C.UTF-8 LANGUAGE=C.UTF-8 LC_ALL=C.UTF-8

COPY rabbitmq.repo /etc/yum.repos.d/rabbitmq.repo

RUN dnf update -y && dnf clean all
RUN dnf install -y erlang rabbitmq-server hostname logrotate


RUN set -eux; \
    /usr/sbin/rabbitmq-plugins enable --offline rabbitmq_prometheus; \
    /usr/sbin/rabbitmq-plugins enable --offline rabbitmq_management

# Add RabbitMQ to PATH, send all logs to TTY
ENV PATH=/usr/sbin:$PATH \
    RABBITMQ_LOGS=-

# set home so that any `--user` knows where to put the erlang cookie
ENV RABBITMQ_DATA_DIR=/var/lib/rabbitmq

ENV APP_VERSION="4.0.7" \
    APP_NAME="rabbitmq"

# Hint that the data (a.k.a. home dir) dir should be separate volume
VOLUME $RABBITMQ_DATA_DIR

USER rabbitmq

EXPOSE 4369 5671 5672 15691 15692 25672 15671 15672

CMD ["rabbitmq-server"]
