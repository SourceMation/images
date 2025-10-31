FROM sourcemation/debian-13-slim:latest as builder

ARG APACHE_VER="2.4.65"
ENV APACHE_INSTALL_DIR /opt/apache2

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

FROM sourcemation/debian-13-slim:latest

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
  summary="Apache on Debian 13 Slim Container" \
  description="Provides Apache on Debian 13 Slim Container" \
  version="2.4.65" \
  io.k8s.display-name="Apache on Debian 13 Slim Container" \
  io.k8s.description="Provides Apache on Debian 13 Slim Container" \
  io.openshift.tags="apache debian"


RUN set -eux \
    && apt-get update && apt-get install -y --no-install-recommends \
        libaprutil1 \
        libapr1 \
        libpcre2-8-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy install directory
COPY --from=builder $APACHE_INSTALL_DIR $APACHE_INSTALL_DIR
RUN chown -R 1001:1001 ${APACHE_INSTALL_DIR}

RUN sed -Ei "s|#ServerName.*|ServerName localhost|g" "${APACHE_INSTALL_DIR}/conf/httpd.conf"
RUN sed -i "s|Listen 80|Listen 8080|g" "${APACHE_INSTALL_DIR}/conf/httpd.conf"

# END INSTALL
USER 1001

EXPOSE 8080
CMD ["/opt/apache2/bin/apachectl", "-D", "FOREGROUND"]