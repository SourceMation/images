FROM rockylinux/rockylinux:9

LABEL name="redis" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Redis on EL9 Container" \
      description="Provides Redis on Rocky Linux 9 Container" \
      version="6.2.7" \
      io.k8s.display-name="Redis on EL9 Container" \
      io.k8s.description="Provides Redis on Rocky Linux 9 Container" \
      io.openshift.tags="redis rockylinux"

RUN set -eux; \
    dnf update -y && \
    dnf install -y hostname redis && \
	redis-cli --version && \
	redis-server --version && \
    dnf clean all

COPY redis.conf /etc/redis/redis.conf

COPY entrypoint.sh setupMasterSlave.sh healthcheck.sh /usr/bin/

RUN chown 998:0 /usr/bin/entrypoint.sh /usr/bin/setupMasterSlave.sh /usr/bin/healthcheck.sh /etc/redis/redis.conf && \
    chmod 750 /usr/bin/entrypoint.sh /usr/bin/setupMasterSlave.sh /usr/bin/healthcheck.sh /etc/redis/redis.conf && \
    mkdir /data && \
    mkdir /node-conf && \
    chown -R 998:0 /data && \
    chown -R 998:0 /node-conf && \
    chmod -R g+rw /data && \
    chmod -R g+rw /node-conf

ENV APP_VERSION="6.2.7" \
    APP_NAME="redis"

VOLUME ["/data"]

WORKDIR /data

EXPOSE 6379

USER 998

CMD ["/usr/bin/entrypoint.sh"]
