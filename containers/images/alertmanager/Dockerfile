FROM docker.io/sourcemation/debian-12-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Alertmanager on Debian 12 Slim Container"

LABEL name="alertmanager" \
  vendor="SourceMation" \
  url="https://sourcemation.com"\
  source="https://github.com/SourceMation/images/issues"\
  licenses="Apache-2.0" \
  created="${BUILD_DATE}" \
  architecture="${TARGETARCH}" \
  summary="${LONGNAME}" \
  description="Provides ${LONGNAME}" \
  version="0.28.1" \
  io.k8s.display-name="${LONGNAME}" \
  io.k8s.description="Provides ${LONGNAME}" \
  io.openshift.tags="alertmanager debian-12-slim"

# RUN update and setup user
RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*

# INSTAL OR COPY --from=builder /builder/path /path
COPY amtool             /bin/amtool
COPY alertmanager       /bin/alertmanager
COPY alertmanager.yml   /etc/alertmanager/alertmanager.yml

WORKDIR /alertmanager
RUN chown -R nobody:nogroup /etc/alertmanager /alertmanager && chmod g+w /alertmanager

EXPOSE     9093
VOLUME     [ "/alertmanager" ]
ENTRYPOINT [ "/bin/alertmanager" ]
CMD        [ "--config.file=/etc/alertmanager/alertmanager.yml", \
             "--storage.path=/alertmanager" ]
