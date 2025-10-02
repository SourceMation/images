#!/bin/bash

# --- Configuration ---
# Check if KEYCLOAK_HOME is set
if [ -z "$KEYCLOAK_HOME" ]; then
    echo "ERROR: The KEYCLOAK_HOME environment variable is not set."
    exit 1
fi

# Path to the Keycloak configuration file
CONF_FILE="${KEYCLOAK_HOME}/conf/keycloak.conf"
# --- End of Configuration ---

# # Helper function to retrieve a value (file has priority over variable)
# get_value() {
#     local file_var_name="$1"
#     local direct_var_name="$2"
#     local value=""
#     if [ -n "${!file_var_name}" ]; then
#         local file_path="${!file_var_name}"
#         if [ -r "$file_path" ]; then
#             value=$(cat "$file_path")
#             echo "$value"
#             return
#         else
#             echo "WARNING: File '$file_path' specified by '$file_var_name' does not exist or is not readable." >&2
#         fi
#     fi
#     if [ -n "${!direct_var_name}" ]; then
#         value="${!direct_var_name}"
#         echo "$value"
#     fi
# }

set_config() {
    local key="$1"
    local value="$2"
    if [ -z "$value" ]; then return; fi
    echo "-> Setting '$key'..."
    if grep -q -E "^\s*${key}\s*=" "$CONF_FILE"; then
        sed -i "s|^\s*${key}\s*=.*|${key} = ${value}|" "$CONF_FILE"
        echo "   Updated active key '$key'."
    elif grep -q -E "^\s*#\s*${key}\s*=" "$CONF_FILE"; then
        sed -i "s|^\s*#\s*${key}\s*=.*|${key} = ${value}|" "$CONF_FILE"
        echo "   Uncommented and set key '$key'."
    else
        echo "${key} = ${value}" >> "$CONF_FILE"
        echo "   Added new key '$key'."
    fi
}

keycloak_env_vars=(
    KEYCLOAK_MOUNTED_CONF_DIR
    KC_RUN_IN_CONTAINER
    KEYCLOAK_PRODUCTION
    KEYCLOAK_EXTRA_ARGS
    KEYCLOAK_EXTRA_ARGS_PREPENDED
    KC_HTTP_MANAGEMENT_PORT
    KEYCLOAK_ENABLE_HTTPS
    KEYCLOAK_HTTPS_USE_PEM
    KC_BOOTSTRAP_ADMIN_USERNAME
    KC_BOOTSTRAP_ADMIN_PASSWORD
    KC_HTTP_PORT
    KC_HTTPS_PORT
    KC_HTTP_RELATIVE_PATH
    KC_LOG_LEVEL
    KC_LOG_CONSOLE_OUTPUT
    KC_METRICS_ENABLED
    KC_HEALTH_ENABLED
    KC_CACHE
    KC_CACHE_STACK
    KC_CACHE_CONFIG_FILE
    KC_HOSTNAME
    KC_HOSTNAME_ADMIN
    KC_HOSTNAME_STRICT
    KC_HTTPS_TRUST_STORE_FILE
    KC_HTTPS_TRUST_STORE_PASSWORD
    KC_HTTPS_KEY_STORE_FILE
    KC_HTTPS_KEY_STORE_PASSWORD
    KC_HTTPS_CERTIFICATE_FILE
    KC_HTTPS_CERTIFICATE_KEY_FILE
    KC_DB
    KEYCLOAK_DATABASE_HOST
    KEYCLOAK_DATABASE_PORT
    KEYCLOAK_DATABASE_NAME
    KEYCLOAK_JDBC_PARAMS
    KEYCLOAK_JDBC_DRIVER
    KC_DB_USERNAME
    KC_DB_PASSWORD
    KC_DB_SCHEMA
    KEYCLOAK_INIT_MAX_RETRIES
    KEYCLOAK_DAEMON_USER
    KEYCLOAK_DAEMON_GROUP
    KEYCLOAK_HTTP_PORT
    KEYCLOAK_HTTPS_PORT
    KEYCLOAK_HTTP_RELATIVE_PATH
    KEYCLOAK_LOG_LEVEL
    KEYCLOAK_LOG_OUTPUT
    KEYCLOAK_ENABLE_STATISTICS
    KEYCLOAK_ENABLE_HEALTH_ENDPOINTS
    KEYCLOAK_CACHE_TYPE
    KEYCLOAK_CACHE_STACK
    KEYCLOAK_CACHE_CONFIG_FILE
    KEYCLOAK_HOSTNAME
    KEYCLOAK_HOSTNAME_ADMIN
    KEYCLOAK_HOSTNAME_STRICT
    KEYCLOAK_HTTPS_TRUST_STORE_FILE
    KEYCLOAK_HTTPS_TRUST_STORE_PASSWORD
    KEYCLOAK_HTTPS_KEY_STORE_FILE
    KEYCLOAK_HTTPS_KEY_STORE_PASSWORD
    KEYCLOAK_HTTPS_CERTIFICATE_FILE
    KEYCLOAK_HTTPS_CERTIFICATE_KEY_FILE
    KEYCLOAK_DATABASE_VENDOR
    KEYCLOAK_DATABASE_USER
    KEYCLOAK_DATABASE_PASSWORD
    KEYCLOAK_DATABASE_SCHEMA
)
for env_var in "${keycloak_env_vars[@]}"; do
    file_env_var="${env_var}_FILE"
    if [[ -n "${!file_env_var:-}" ]]; then
        if [[ -r "${!file_env_var:-}" ]]; then
            export "${env_var}=$(< "${!file_env_var}")"
            unset "${file_env_var}"
        else
            warn "Skipping export of '${env_var}'. '${!file_env_var:-}' is not readable."
        fi
    fi
done
unset keycloak_env_vars


# Paths
export BITNAMI_VOLUME_DIR="/"
export JAVA_HOME="/opt/java"
export KEYCLOAK_BASE_DIR="/opt/keycloak"
export KEYCLOAK_BIN_DIR="$KEYCLOAK_BASE_DIR/bin"
export KEYCLOAK_PROVIDERS_DIR="$KEYCLOAK_BASE_DIR/providers"
export KEYCLOAK_LOG_DIR="$KEYCLOAK_PROVIDERS_DIR/log"
export KEYCLOAK_TMP_DIR="$KEYCLOAK_PROVIDERS_DIR/tmp"
export KEYCLOAK_DOMAIN_TMP_DIR="$KEYCLOAK_BASE_DIR/domain/tmp"
export KEYCLOAK_VOLUME_DIR="/keycloak"
export KEYCLOAK_CONF_DIR="$KEYCLOAK_BASE_DIR/conf"
export KEYCLOAK_DEFAULT_CONF_DIR="$KEYCLOAK_BASE_DIR/conf.default"
export KEYCLOAK_MOUNTED_CONF_DIR="${KEYCLOAK_MOUNTED_CONF_DIR:-${KEYCLOAK_VOLUME_DIR}/conf}"
# export KEYCLOAK_INITSCRIPTS_DIR="/docker-entrypoint-initdb.d"
export KEYCLOAK_CONF_FILE="keycloak.conf"

# Keycloak kc.sh context
export KC_RUN_IN_CONTAINER="${KC_RUN_IN_CONTAINER:-true}"

# Keycloak configuration
export KEYCLOAK_PRODUCTION="${KEYCLOAK_PRODUCTION:-false}"
export KEYCLOAK_EXTRA_ARGS="${KEYCLOAK_EXTRA_ARGS:-}"
export KEYCLOAK_EXTRA_ARGS_PREPENDED="${KEYCLOAK_EXTRA_ARGS_PREPENDED:-}"
export KC_HTTP_MANAGEMENT_PORT="${KC_HTTP_MANAGEMENT_PORT:-9000}"
export KEYCLOAK_ENABLE_HTTPS="${KEYCLOAK_ENABLE_HTTPS:-false}"
export KEYCLOAK_HTTPS_USE_PEM="${KEYCLOAK_HTTPS_USE_PEM:-false}"
export KC_BOOTSTRAP_ADMIN_USERNAME="${KC_BOOTSTRAP_ADMIN_USERNAME:-user}"
export KC_BOOTSTRAP_ADMIN_PASSWORD="${KC_BOOTSTRAP_ADMIN_PASSWORD:-}"
KC_HTTP_PORT="${KC_HTTP_PORT:-"${KEYCLOAK_HTTP_PORT:-}"}"
export KC_HTTP_PORT="${KC_HTTP_PORT:-8080}"
KC_HTTPS_PORT="${KC_HTTPS_PORT:-"${KEYCLOAK_HTTPS_PORT:-}"}"
export KC_HTTPS_PORT="${KC_HTTPS_PORT:-8443}"
KC_HTTP_RELATIVE_PATH="${KC_HTTP_RELATIVE_PATH:-"${KEYCLOAK_HTTP_RELATIVE_PATH:-}"}"
export KC_HTTP_RELATIVE_PATH="${KC_HTTP_RELATIVE_PATH:-/}"
KC_LOG_LEVEL="${KC_LOG_LEVEL:-"${KEYCLOAK_LOG_LEVEL:-}"}"
export KC_LOG_LEVEL="${KC_LOG_LEVEL:-info}"
KC_LOG_CONSOLE_OUTPUT="${KC_LOG_CONSOLE_OUTPUT:-"${KEYCLOAK_LOG_OUTPUT:-}"}"
export KC_LOG_CONSOLE_OUTPUT="${KC_LOG_CONSOLE_OUTPUT:-default}"
KC_METRICS_ENABLED="${KC_METRICS_ENABLED:-"${KEYCLOAK_ENABLE_STATISTICS:-}"}"
export KC_METRICS_ENABLED="${KC_METRICS_ENABLED:-false}"
KC_HEALTH_ENABLED="${KC_HEALTH_ENABLED:-"${KEYCLOAK_ENABLE_HEALTH_ENDPOINTS:-}"}"
export KC_HEALTH_ENABLED="${KC_HEALTH_ENABLED:-false}"
KC_CACHE="${KC_CACHE:-"${KEYCLOAK_CACHE_TYPE:-}"}"
export KC_CACHE="${KC_CACHE:-ispn}"
KC_CACHE_STACK="${KC_CACHE_STACK:-"${KEYCLOAK_CACHE_STACK:-}"}"
export KC_CACHE_STACK="${KC_CACHE_STACK:-}"
KC_CACHE_CONFIG_FILE="${KC_CACHE_CONFIG_FILE:-"${KEYCLOAK_CACHE_CONFIG_FILE:-}"}"
export KC_CACHE_CONFIG_FILE="${KC_CACHE_CONFIG_FILE:-cache-ispn.xml}"
KC_HOSTNAME="${KC_HOSTNAME:-"${KEYCLOAK_HOSTNAME:-}"}"
export KC_HOSTNAME="${KC_HOSTNAME:-}"
KC_HOSTNAME_ADMIN="${KC_HOSTNAME_ADMIN:-"${KEYCLOAK_HOSTNAME_ADMIN:-}"}"
export KC_HOSTNAME_ADMIN="${KC_HOSTNAME_ADMIN:-}"
KC_HOSTNAME_STRICT="${KC_HOSTNAME_STRICT:-"${KEYCLOAK_HOSTNAME_STRICT:-}"}"
export KC_HOSTNAME_STRICT="${KC_HOSTNAME_STRICT:-false}"
KC_HTTPS_TRUST_STORE_FILE="${KC_HTTPS_TRUST_STORE_FILE:-"${KEYCLOAK_HTTPS_TRUST_STORE_FILE:-}"}"
export KC_HTTPS_TRUST_STORE_FILE="${KC_HTTPS_TRUST_STORE_FILE:-}"
KC_HTTPS_TRUST_STORE_PASSWORD="${KC_HTTPS_TRUST_STORE_PASSWORD:-"${KEYCLOAK_HTTPS_TRUST_STORE_PASSWORD:-}"}"
export KC_HTTPS_TRUST_STORE_PASSWORD="${KC_HTTPS_TRUST_STORE_PASSWORD:-}"
KC_HTTPS_KEY_STORE_FILE="${KC_HTTPS_KEY_STORE_FILE:-"${KEYCLOAK_HTTPS_KEY_STORE_FILE:-}"}"
export KC_HTTPS_KEY_STORE_FILE="${KC_HTTPS_KEY_STORE_FILE:-}"
KC_HTTPS_KEY_STORE_PASSWORD="${KC_HTTPS_KEY_STORE_PASSWORD:-"${KEYCLOAK_HTTPS_KEY_STORE_PASSWORD:-}"}"
export KC_HTTPS_KEY_STORE_PASSWORD="${KC_HTTPS_KEY_STORE_PASSWORD:-}"
KC_HTTPS_CERTIFICATE_FILE="${KC_HTTPS_CERTIFICATE_FILE:-"${KEYCLOAK_HTTPS_CERTIFICATE_FILE:-}"}"
export KC_HTTPS_CERTIFICATE_FILE="${KC_HTTPS_CERTIFICATE_FILE:-}"
KC_HTTPS_CERTIFICATE_KEY_FILE="${KC_HTTPS_CERTIFICATE_KEY_FILE:-"${KEYCLOAK_HTTPS_CERTIFICATE_KEY_FILE:-}"}"
export KC_HTTPS_CERTIFICATE_KEY_FILE="${KC_HTTPS_CERTIFICATE_KEY_FILE:-}"

# Keycloak database configuration
KC_DB="${KC_DB:-"${KEYCLOAK_DATABASE_VENDOR:-}"}"
export KC_DB="${KC_DB:-postgres}"
export KEYCLOAK_DATABASE_HOST="${KEYCLOAK_DATABASE_HOST:-postgresql}"
export KEYCLOAK_DATABASE_PORT="${KEYCLOAK_DATABASE_PORT:-5432}"
export KEYCLOAK_DATABASE_NAME="${KEYCLOAK_DATABASE_NAME:-keycloak}"
export KEYCLOAK_JDBC_PARAMS="${KEYCLOAK_JDBC_PARAMS:-}"
export KEYCLOAK_JDBC_DRIVER="${KEYCLOAK_JDBC_DRIVER:-postgresql}"
KC_DB_USERNAME="${KC_DB_USERNAME:-"${KEYCLOAK_DATABASE_USER:-}"}"
export KC_DB_USERNAME="${KC_DB_USERNAME:-keycloak}"
KC_DB_PASSWORD="${KC_DB_PASSWORD:-"${KEYCLOAK_DATABASE_PASSWORD:-}"}"
export KC_DB_PASSWORD="${KC_DB_PASSWORD:-}"
KC_DB_SCHEMA="${KC_DB_SCHEMA:-"${KEYCLOAK_DATABASE_SCHEMA:-}"}"
export KC_DB_SCHEMA="${KC_DB_SCHEMA:-public}"
export KEYCLOAK_INIT_MAX_RETRIES="${KEYCLOAK_INIT_MAX_RETRIES:-10}"

# System users (when running with a privileged user)
export KEYCLOAK_DAEMON_USER="${KEYCLOAK_DAEMON_USER:-keycloak}"
export KEYCLOAK_DAEMON_GROUP="${KEYCLOAK_DAEMON_GROUP:-keycloak}"



echo "Starting environment and file configuration for Keycloak..."

# --- PART 1: Set Admin Credentials (Environment Variables) ---
echo "--- Checking Admin Credentials ---"
admin_pass=$KC_BOOTSTRAP_ADMIN_PASSWORD
if [ -z "$admin_pass" ]; then
    echo "-> Admin password not set. Generating a random password."
    NEW_PASSWORD=$(head /dev/urandom | tr -dc 'A-Za-z0-9' | head -c 24)
    export KC_BOOTSTRAP_ADMIN_PASSWORD="$NEW_PASSWORD"
    echo "--------------------------------------------------------"
    echo "IMPORTANT: Generated admin password: $NEW_PASSWORD"
    echo "Save it in a safe place!"
    echo "--------------------------------------------------------"
else
    echo "-> Admin password is already set via environment variable."
fi

# --- PART 2: Modify keycloak.conf ---
echo ""
echo "--- Configuring file: $CONF_FILE ---"

if [ ! -f "$CONF_FILE" ]; then
    echo "ERROR: Configuration file '$CONF_FILE' not found! Skipping file modifications."
elif [ ! -w "$CONF_FILE" ]; then
    echo "ERROR: No write permissions for file '$CONF_FILE'! Skipping file modifications."
else
    # Special handling for the database URL (db-url)
    db_host=$KEYCLOAK_DATABASE_HOST
    db_port=$KEYCLOAK_DATABASE_PORT
    db_name=$KEYCLOAK_DATABASE_NAME

    if [ -n "$db_host" ] && [ -n "$db_port" ] && [ -n "$db_name" ]; then
        set_config "db" "postgres"
        db_schema=$KC_DB_SCHEMA
        new_db_url="jdbc:postgresql://${db_host}:${db_port}/${db_name}?currentSchema=${db_schema}"
        set_config "db-url" "$new_db_url"
    elif [ -n "$db_host" ] || [ -n "$db_port" ] || [ -n "$db_name" ]; then
        echo "WARNING: To set 'db-url', all three variables (host, port, and database name) must be defined. Skipping." >&2
    fi
fi

echo ""
echo "Configuration finished. Preparing to start Keycloak process..."

# --- PART 3: Determine startup command and execute ---
# Default command is from the Dockerfile's CMD (available in "$@")
cmd=("$@")

# Switch to production 'start' command if KEYCLOAK_PRODUCTION is true
if [[ "${KEYCLOAK_PRODUCTION}" == "true" ]]; then
    echo "-> Production mode enabled. Switching to 'start' command."
    # Replace 'start-dev' with 'start' in the command array
    cmd=("${cmd[@]/start-dev/start}")
else
    echo "-> Development mode enabled. Using 'start-dev' command."
fi

# Check if KEYCLOAK_EXTRA_ARGS is set and append them to the command
if [ -n "$KEYCLOAK_EXTRA_ARGS" ]; then
    echo "-> Appending extra arguments to the startup command: $KEYCLOAK_EXTRA_ARGS"
    # The variable is intentionally unquoted to allow for word splitting by the shell
    exec "${cmd[@]}" $KEYCLOAK_EXTRA_ARGS
else
    exec "${cmd[@]}"
fi