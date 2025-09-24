#!/bin/bash
set -e

chown -R openldap:openldap ${LDAP_DATA_DIR} ${LDAP_CONF_DIR}

if [ -f "${LDAP_DATA_DIR}/data.mdb" ]; then
    echo "Found existing LDAP database. Starting slapd..."
    exec "$@"
fi

echo "First run detected. Initializing OpenLDAP..."

LDAP_ORGANISATION=${LDAP_ORGANISATION:-"Example Inc"}
LDAP_DOMAIN=${LDAP_DOMAIN:-"example.org"}

if [ -z "${LDAP_ADMIN_PASSWORD}" ]; then
    LDAP_ADMIN_PASSWORD_RAW=$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 16)
    echo "---"
    echo "Generated random password for LDAP admin:"
    echo "${LDAP_ADMIN_PASSWORD_RAW}"
    echo "Set the LDAP_ADMIN_PASSWORD environment variable to override."
    echo "---"
    LDAP_ADMIN_PASSWORD=$(slappasswd -s "${LDAP_ADMIN_PASSWORD_RAW}")
else
    LDAP_ADMIN_PASSWORD=$(slappasswd -s "${LDAP_ADMIN_PASSWORD}")
fi

IFS='.' read -ra dc_parts <<< "$LDAP_DOMAIN"
LDAP_BASE_DN=""
for part in "${dc_parts[@]}"; do
    LDAP_BASE_DN="${LDAP_BASE_DN},dc=${part}"
done
LDAP_BASE_DN=${LDAP_BASE_DN:1}

cat > ${LDAP_CONF_DIR}/slapd.conf <<EOF
include     ${LDAP_CONF_DIR}/schema/core.schema
include     ${LDAP_CONF_DIR}/schema/cosine.schema
include     ${LDAP_CONF_DIR}/schema/nis.schema
include     ${LDAP_CONF_DIR}/schema/inetorgperson.schema

pidfile     /var/run/slapd/slapd.pid
argsfile    /var/run/slapd/slapd.args

database    mdb
suffix      "${LDAP_BASE_DN}"
rootdn      "cn=admin,${LDAP_BASE_DN}"
rootpw      ${LDAP_ADMIN_PASSWORD}
directory   ${LDAP_DATA_DIR}
EOF

mkdir -p ${LDAP_CONF_DIR}/slapd.d
find ${LDAP_CONF_DIR}/slapd.d/ -mindepth 1 -delete

slaptest -f ${LDAP_CONF_DIR}/slapd.conf -F ${LDAP_CONF_DIR}/slapd.d || true

chown -R openldap:openldap ${LDAP_CONF_DIR}/slapd.d

cat > /tmp/base.ldif <<EOF
dn: ${LDAP_BASE_DN}
objectClass: top
objectClass: dcObject
objectClass: organization
o: ${LDAP_ORGANISATION}
dc: ${dc_parts[0]}

dn: cn=admin,${LDAP_BASE_DN}
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP Administrator
userPassword: ${LDAP_ADMIN_PASSWORD}
EOF

su openldap -s /bin/sh -c "slapadd -n 1 -F ${LDAP_CONF_DIR}/slapd.d -l /tmp/base.ldif"

rm ${LDAP_CONF_DIR}/slapd.conf /tmp/base.ldif

echo "OpenLDAP initialization complete."
echo "Starting server..."

exec "$@"