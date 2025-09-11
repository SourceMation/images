FROM sourcemation/postgres-17

ARG BUILD_DATE
ARG TARGETARCH

ENV PGEXPORTER_VER="0.17.1"
ENV BINARY_URL="https://github.com/prometheus-community/postgres_exporter/releases/download/v${PGEXPORTER_VER}/postgres_exporter-${PGEXPORTER_VER}.linux-${TARGETARCH}.tar.gz"

LABEL name="postgres-exporter" \
  vendor="Linux Polska" \
  url="https://sourcemation.com"\
  source="https://github.com/SourceMation/images/issues"\
  licenses="GPLv2" \
  created="$BUILD_DATE" \
  architecture="$TARGETARCH" \
  summary="Postgresql-exporter on Debian 12 Slim Container" \
  description="Provides postgres-exporter on Debian 12 Slim Container" \
  version="0.17.1" \
  io.k8s.display-name="Postgresql-exporter on Debian 12 Slim Container" \
  io.k8s.description="Provides postgres-exporter on Debian 12 Slim Container" \
  io.openshift.tags="postgres-exporter debian"

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      tar \
      wget; 
RUN wget --progress=dot:giga -O /tmp/postgres-exporter.tar.gz ${BINARY_URL}; \
    tar --extract \
        --file /tmp/postgres-exporter.tar.gz \
        --directory "/bin" \
        --strip-components 1 \
        --no-same-owner; \
    rm -f /tmp/postgres-exporter.tar.gz;

RUN bash -c 'echo -e "auth_modules: \n\
  db: # Set this to any name you want \n\
    type: userpass \n\
    userpass: \n\
      username: \$DATA_SOURCE_USER \n\
      password: \$DATA_SOURCE_PASS \n\
    options: # options become key=value parameters of the DSN \n\
      sslmode: disable \n\
" >> ./postgres_exporter.yml'

# END INSTALL
EXPOSE 9187

USER postgres

ENTRYPOINT ["/bin/postgres_exporter"]