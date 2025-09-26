#!/usr/bin/env bash
# ---------------------------------------------------
# Set environment variables

set -e

export KC_BOOTSTRAP_ADMIN_USERNAME=tmpadmin
export KC_BOOTSTRAP_ADMIN_PASSWORD=temppassword
export KC_LOG=console,file
export KC_LOG_FILE="/opt/keycloak/logs/keycloak.log"

# Check if Keycloak is already initialized
if [ -f $KC_LOG_FILE ]; then
    OLDEST_LOG_FILE=$(ls -lt /opt/keycloak/logs/keycloak.log* 2>/dev/null | tail -1 | awk '{print $9}')
    if grep "Created new user with id " $OLDEST_LOG_FILE 2>&1 >/dev/null; then
        echo "Keycloak already initialized, skipping setup."
        exec "$@"
    fi
fi

# Start Keycloak with temp admin
mkdir -p /opt/keycloak/logs
bin/kc.sh start-dev &
PID=$!
echo "Keycloak starting with PID: $PID"

# Wait for Keycloak to start
echo "Waiting for Keycloak to start... "
sleep 20
for i in {1..30}; do
    sleep 5
    if [ -f $KC_LOG_FILE ] && grep "Listening on:" $KC_LOG_FILE; then
        echo "Keycloak started"
        break
    fi
done
if [ -f $KC_LOG_FILE ] && ! grep "Listening on:" $KC_LOG_FILE; then
    echo "Keycloak failed to start within 150 seconds. Check the logs for details."
    exit 1
fi

# Set admin user and password from arguments
if [ -z "${KEYCLOAK_ADMIN_USERNAME}" ]; then
    KEYCLOAK_ADMIN_USERNAME="user"
fi
if [ -z "${KEYCLOAK_ADMIN_PASSWORD}" ]; then
    KEYCLOAK_ADMIN_PASSWORD=$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 16)
    echo "###############################################"
    echo "Keycloak admin username: "
    echo "${KEYCLOAK_ADMIN_USERNAME}"
    echo "Keycloak admin password: "
    echo "${KEYCLOAK_ADMIN_PASSWORD}"
    echo "###############################################"
    echo "Set the KEYCLOAK_ADMIN_PASSWORD environment variable to override."
fi

# Add admin user
bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user ${KC_BOOTSTRAP_ADMIN_USERNAME} --password ${KC_BOOTSTRAP_ADMIN_PASSWORD} 2>&1 | tee -a $KC_LOG_FILE
bin/kcadm.sh create users -r master -s username=${KEYCLOAK_ADMIN_USERNAME} -s enabled=true 2>&1 | tee -a $KC_LOG_FILE
bin/kcadm.sh set-password -r master --username ${KEYCLOAK_ADMIN_USERNAME} --new-password ${KEYCLOAK_ADMIN_PASSWORD} 2>&1 | tee -a $KC_LOG_FILE
bin/kcadm.sh add-roles -r master --uusername ${KEYCLOAK_ADMIN_USERNAME} --rolename admin 2>&1 | tee -a $KC_LOG_FILE

# Remove temp admin
ID=$(bin/kcadm.sh get users -r master -q username=${KC_BOOTSTRAP_ADMIN_USERNAME})
ID=$(echo $ID | grep '"id"' | head -1 | awk -F'"' '{print $4}')
bin/kcadm.sh delete users/${ID} -r master 2>&1 | tee -a $KC_LOG_FILE

# Stop Keycloak
kill $PID

exec "$@"