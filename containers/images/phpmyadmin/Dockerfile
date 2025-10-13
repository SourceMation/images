FROM sourcemation/debian-13-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="phpMyAdmin on Debian 13 Slim Container"

LABEL name="phpmyadmin" \
      vendor="SourceMation" \
      url="https://sourcemation.com" \
      source="https://github.com/SourceMation/images/issues" \
      licenses="GPL-2.0-only" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="5.2.3" \
      io.k8s.display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="phpmyadmin debian-12-slim"

ENV APACHE_DOCUMENT_ROOT=/var/www/html

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends \
        apache2 \
        php libapache2-mod-php \
        php-mysql php-mbstring php-json php-zip php-gd \
        pwgen; \
    a2dissite 000-default.conf; \
    a2enmod rewrite; \
    echo "ServerName localhost" >> /etc/apache2/apache2.conf; \
    rm -rf /var/lib/apt/lists/*

COPY --chown=www-data:www-data phpmyadmin/ ${APACHE_DOCUMENT_ROOT}/

RUN mkdir -p ${APACHE_DOCUMENT_ROOT}/tmp; \
    chown -R www-data:www-data ${APACHE_DOCUMENT_ROOT}/tmp

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR ${APACHE_DOCUMENT_ROOT}

EXPOSE 80

VOLUME /var/www/html

ENTRYPOINT ["entrypoint.sh"]

CMD . /etc/apache2/envvars && exec /usr/sbin/apache2 -DFOREGROUND