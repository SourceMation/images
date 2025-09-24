FROM sourcemation/debian-12-slim:latest AS builder

ARG VERSION=2.6.10

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libtool libsasl2-dev libssl-dev libdb-dev curl groff \
    && rm -rf /var/lib/apt/lists/*

RUN curl -skL "https://www.openldap.org/software/download/OpenLDAP/openldap-release/openldap-${VERSION}.tgz" \
    -o /tmp/openldap.tgz \
    && mkdir -p /build \
    && tar -xzf /tmp/openldap.tgz -C /build --strip-components=1 \
    && rm /tmp/openldap.tgz

WORKDIR /build

RUN ./configure \
        --prefix=/usr \
        --sysconfdir=/etc/ldap \
        --localstatedir=/var \
        --sbindir=/usr/sbin \
        --libexecdir=/usr/sbin \
        --disable-static \
        --enable-dynamic \
        --with-tls=openssl \
        --with-cyrus-sasl \
    && make depend \
    && make \
    && make install DESTDIR=/install

FROM sourcemation/debian-12-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="OpenLDAP on Debian 12 Slim Container"

LABEL name="openldap" \
      vendor="SourceMation" \
      url="https://sourcemation.com" \
      source="https://github.com/SourceMation/images/issues" \
      licenses="OLDAP-2.8" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="2.6.10" \
      io.k-display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="openldap debian-12-slim"

ENV LDAP_CONF_DIR=/etc/ldap \
    LDAP_DATA_DIR=/var/lib/ldap \
    LDAP_ORGANISATION="Example Inc" \
    LDAP_DOMAIN="example.org" \
    LDAP_ADMIN_PASSWORD=""

RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends libsasl2-2 libssl3 libdb5.3; \
    apt-mark hold libldap-common; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 1001 openldap; \
    useradd --uid 1001 --gid 1001 --shell /bin/false openldap

COPY --from=builder /install/usr/ /usr/
COPY --from=builder /install/etc/ldap/openldap/ /etc/ldap/

RUN mkdir -p ${LDAP_DATA_DIR} /var/run/slapd; \
    chown -R openldap:openldap ${LDAP_CONF_DIR} ${LDAP_DATA_DIR} /var/run/slapd

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 389 636

VOLUME [ "${LDAP_DATA_DIR}", "${LDAP_CONF_DIR}/slapd.d" ]

ENTRYPOINT ["entrypoint.sh"]

CMD ["/usr/sbin/slapd", "-F", "/etc/ldap/slapd.d", "-h", "ldap:/// ldaps:///", "-g", "openldap", "-u", "openldap", "-d", "STATS"]