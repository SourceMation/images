#!/usr/bin/env bash
# ---------------------------------------------------
# Set environment variables

set -e

export KEYCLOAK_ADMIN=tmpadmin
export KEYCLOAK_ADMIN_PASSWORD=temppassword
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
if [ -z "${ADMIN_USERNAME}" ]; then
    ADMIN_USERNAME="user"
fi
if [ -z "${ADMIN_PASSWORD}" ]; then
    ADMIN_PASSWORD=$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 16)
    echo "###############################################"
    echo "Keycloak admin username: "
    echo "${ADMIN_USERNAME}"
    echo "Keycloak admin password: "
    echo "${ADMIN_PASSWORD}"
    echo "###############################################"
    echo "Set the ADMIN_PASSWORD environment variable to override."
fi

# Add admin user
bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user ${KEYCLOAK_ADMIN} --password ${KEYCLOAK_ADMIN_PASSWORD} 2>&1 | tee -a $KC_LOG_FILE
bin/kcadm.sh create users -r master -s username=${ADMIN_USERNAME} -s enabled=true 2>&1 | tee -a $KC_LOG_FILE
bin/kcadm.sh set-password -r master --username ${ADMIN_USERNAME} --new-password ${ADMIN_PASSWORD} 2>&1 | tee -a $KC_LOG_FILE
bin/kcadm.sh add-roles -r master --uusername ${ADMIN_USERNAME} --rolename admin 2>&1 | tee -a $KC_LOG_FILE

# Remove temp admin
ID=$(bin/kcadm.sh get users -r master -q username=${KEYCLOAK_ADMIN})
ID=$(echo $ID | grep '"id"' | head -1 | awk -F'"' '{print $4}')
bin/kcadm.sh delete users/${ID} -r master 2>&1 | tee -a $KC_LOG_FILE

# Stop Keycloak
kill $PID

exec "$@"