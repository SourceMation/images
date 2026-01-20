ARG IMAGE_REF=spassky-1
FROM docker.io/manageiq/manageiq-ui-worker:${IMAGE_REF}

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="manageiq" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="Apache-2.0 license" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="ManageIQ on Debian Container" \
      description="Provides ManageIQ on UBI Container" \
      version="spassky-1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="ManageIQ on UBI Container" \
      io.k8s.description="ManageIQ on UBI 12 Container" \
      io.openshift.tags="manageiq"


ENV DATABASE_URL=postgresql://root@localhost/vmdb_production?encoding=utf8&pool=5&wait_timeout=5

RUN echo "# This file intentionally left blank. ManageIQ maintains its own SSL configuration" > /etc/httpd/conf.d/ssl.conf && \
    dnf -y --setopt=tsflags=nodocs install \
      manageiq-appliance      \
      memcached               \
      postgresql-server       \
      mod_ssl                 \
      python3-pip             \
      &&                      \
    dnf clean all && \
    /usr/bin/python3 -m pip install pyvmomi && \
    /usr/bin/python3 -m pip install  passlib[bcrypt] && \
    ansible-galaxy collection install community.vmware --upgrade && \
    rm -rf /var/cache/dnf

## Overwrite entrypoint from pods repo
COPY manageiq/container-assets/entrypoint /usr/local/bin

EXPOSE 443

VOLUME "/var/lib/pgsql/data"
VOLUME ${APP_ROOT}
