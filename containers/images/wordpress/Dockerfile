FROM sourcemation/debian-12-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="WordPress on Debian 12 Slim Container"

LABEL name="wordpress" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      source="https://github.com/Sourcemation/images/issues" \
      licenses="GPL-2.0-or-later" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="6.8.3" \
      io.k8s.display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="wordpress php apache debian-12-slim"

ENV APACHE_DOCUMENT_ROOT=/var/www/html \
    WORDPRESS_DB_HOST=mysql \
    WORDPRESS_DB_USER=wordpress \
    WORDPRESS_DB_PASSWORD=wordpress \
    WORDPRESS_DB_NAME=wordpress

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends \
        curl ed apache2 \
        php libapache2-mod-php \
        php-mysql php-gd php-curl php-mbstring php-zip php-xml php-intl \
        netcat-openbsd \
        ca-certificates; \
    a2dissite 000-default.conf; \
    a2enmod rewrite; \
    echo "ServerName localhost" >> /etc/apache2/apache2.conf; \
    rm -rf /var/lib/apt/lists/*

COPY --chown=www-data:www-data wordpress /usr/src/wordpress

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR ${APACHE_DOCUMENT_ROOT}

EXPOSE 80

VOLUME /var/www/html

ENTRYPOINT ["entrypoint.sh"]

CMD . /etc/apache2/envvars && exec /usr/sbin/apache2 -DFOREGROUND