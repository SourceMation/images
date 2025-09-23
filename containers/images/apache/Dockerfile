FROM sourcemation/debian-12-slim:latest

ARG BUILD_DATE
ARG TARGETARCH
ARG APACHE_VER="2.4.65"
ENV APACHE_INSTALL_DIR /opt/apache2

LABEL name="apache" \
  vendor="Linux Polska" \
  url="https://sourcemation.com"\
  source="https://github.com/SourceMation/images/issues"\
  licenses="GPLv2" \
  created="$BUILD_DATE" \
  architecture="$TARGETARCH" \
  summary="Apache on Debian 12 Slim Container" \
  description="Provides Apache on Debian 12 Slim Container" \
  version="2.4.65" \
  io.k8s.display-name="Apache on Debian 12 Slim Container" \
  io.k8s.description="Provides Apache on Debian 12 Slim Container" \
  io.openshift.tags="apache debian"

# Install packages
RUN set -eux \
    && apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        tar \
        gzip \
        wget \
    && apt-get install -y \
        gcc \
        g++ \
        make \
        libapr1-dev \
        libaprutil1-dev \
        libpcre2-dev

# Install Apache
RUN set -eux \
    && wget -O /tmp/apache.tar.gz "https://dlcdn.apache.org/httpd/httpd-${APACHE_VER}.tar.gz" \
    && gzip -d /tmp/apache.tar.gz \
    && mkdir /tmp/apache \
    && tar -xf /tmp/apache.tar -C /tmp/apache --strip-components 1\
    && cd /tmp/apache \
    && ./configure \
        --prefix=${APACHE_INSTALL_DIR} \
    && make -j "$(nproc)" \
    && make install

COPY entrypoint.sh /entrypoint.sh
RUN chown -R 1001:1001 ${APACHE_INSTALL_DIR}

USER 1001
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE "443" "80"