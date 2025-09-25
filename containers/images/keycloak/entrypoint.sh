#!/usr/bin/env bash
# ---------------------------------------------------
# Set environment variables
export KC_BOOTSTRAP_ADMIN_USERNAME=tmpadmin
export KC_BOOTSTRAP_ADMIN_PASSWORD=temppassword
export KC_LOG=console,file
export KC_LOG_FILE="/opt/keycloak/logs/keycloak.log"

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
    if grep "Listening on:" $KC_LOG_FILE; then
        echo "Keycloak started"
        break
    fi
done
if ! grep "Listening on:" $KC_LOG_FILE; then
    echo "Keycloak failed to start within 150 seconds. Check the logs for details."
    exit 1
fi

# Set admin user and password from arguments
if [ -z "${KEYCLOAK_ADMIN_USERNAME}" ]; then
    KEYCLOAK_ADMIN_USERNAME="user"
fi
if [ -z "${KEYCLOAK_ADMIN_PASSWORD}" ]; then
    KEYCLOAK_ADMIN_PASSWORD=$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 16)
    echo "---"
    echo "Generated random password for Keycloak admin:"
    echo "${KEYCLOAK_ADMIN_PASSWORD}"
    echo "Set the KEYCLOAK_ADMIN_PASSWORD environment variable to override."
    echo "---"
fi

# Add admin user
bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user ${KC_BOOTSTRAP_ADMIN_USERNAME} --password ${KC_BOOTSTRAP_ADMIN_PASSWORD}
bin/kcadm.sh create users -r master -s username=${KEYCLOAK_ADMIN_USERNAME} -s enabled=true
bin/kcadm.sh set-password -r master --username ${KEYCLOAK_ADMIN_USERNAME} --new-password ${KEYCLOAK_ADMIN_PASSWORD}
bin/kcadm.sh add-roles -r master --uusername ${KEYCLOAK_ADMIN_USERNAME} --rolename admin

# Remove temp admin
ID=$(bin/kcadm.sh get users -r master -q username=${KC_BOOTSTRAP_ADMIN_USERNAME})
ID=$(echo $ID | grep '"id"' | head -1 | awk -F'"' '{print $4}')
if [ -z "$ID" ] || [ "$ID" == "null" ]; then
    echo "Temporary admin user not found, cannot delete."
    exit 1
fi
bin/kcadm.sh delete users/${ID} -r master

# Stop Keycloak
kill $PID

exec "$@"