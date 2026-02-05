FROM sourcemation/debian-13-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Matomo on Debian 13 Slim Container"

LABEL name="matomo" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      source="https://github.com/Sourcemation/images/issues" \
      licenses="GPL-3.0-or-later" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="5.7.1" \
      io.k8s.display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="matomo debian-13-slim"

ENV APACHE_DOCUMENT_ROOT=/var/www/html

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends \
        apache2 \
        php libapache2-mod-php \
        php-mysql php-gd php-curl php-mbstring php-xml php-intl php-json \
        gosu \
        netcat-openbsd \
        unzip \
        ca-certificates; \
    a2dissite 000-default.conf; \
    a2enmod rewrite; \
    rm -rf /var/lib/apt/lists/*

COPY --chown=www-data:www-data matomo /usr/src/matomo

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR ${APACHE_DOCUMENT_ROOT}

EXPOSE 80

VOLUME /var/www/html

ENTRYPOINT ["entrypoint.sh"]

CMD ["/bin/sh", "-c", ". /etc/apache2/envvars && exec /usr/sbin/apache2 -DFOREGROUND"]