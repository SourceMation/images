#!/bin/bash
set -eo pipefail

# Logging functions
mariadb_log() {
    local type="$1"; shift
    printf '%s [%s] [Entrypoint]: %s\n' "$(date --rfc-3339=seconds)" "$type" "$*"
}
mariadb_note() {
    mariadb_log Note "$@"
}
mariadb_warn() {
    mariadb_log Warn "$@" >&2
}
mariadb_error() {
    mariadb_log ERROR "$@" >&2
    exit 1
}

# Get config value
mariadb_get_config() {
    local conf="$1"; shift
    "$@" --verbose --help 2>/dev/null \
        | awk -v conf="$conf" '$1 == conf { print $2; exit }'
}

# Check if we want help
_mariadb_want_help() {
    local arg
    for arg; do
        case "$arg" in
            -'?'|--help|--print-defaults|-V|--version)
                return 0
                ;;
        esac
    done
    return 1
}

# Map MYSQL_* to MARIADB_* for backwards compatibility
if [ ! -z "$MYSQL_ROOT_PASSWORD" ]; then
    export MARIADB_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD"
fi
if [ ! -z "$MYSQL_DATABASE" ]; then
    export MARIADB_DATABASE="$MYSQL_DATABASE"
fi
if [ ! -z "$MYSQL_USER" ]; then
    export MARIADB_USER="$MYSQL_USER"
fi
if [ ! -z "$MYSQL_PASSWORD" ]; then
    export MARIADB_PASSWORD="$MYSQL_PASSWORD"
fi
if [ ! -z "$MYSQL_ALLOW_EMPTY_PASSWORD" ]; then
    export MARIADB_ALLOW_EMPTY_PASSWORD="$MYSQL_ALLOW_EMPTY_PASSWORD"
fi
if [ ! -z "$MYSQL_RANDOM_ROOT_PASSWORD" ]; then
    export MARIADB_RANDOM_ROOT_PASSWORD="$MYSQL_RANDOM_ROOT_PASSWORD"
fi
if [ ! -z "$MYSQL_INITDB_SKIP_TZINFO" ]; then
    export MARIADB_INITDB_SKIP_TZINFO="$MYSQL_INITDB_SKIP_TZINFO"
fi

# if command starts with an option, prepend mariadbd
if [ "${1:0:1}" = '-' ]; then
    set -- mariadbd "$@"
fi

# skip setup if they aren't running mariadbd or want an option that stops mariadbd
if [ "$1" = 'mariadbd' ] && ! _mariadb_want_help "$@"; then
    mariadb_note "Entrypoint script for MariaDB Server started."

    # Get config
    DATADIR="$(mariadb_get_config 'datadir' "$@")"
    DATADIR="${DATADIR:-/var/lib/mysql}"
    SOCKET="$(mariadb_get_config 'socket' "$@")"
    SOCKET="${SOCKET:-/var/run/mysqld/mysqld.sock}"
    
    mariadb_note "Got DATADIR=$DATADIR"
    mariadb_note "Got SOCKET=$SOCKET"

    # Check if we're running as mysql user (rootless)
    if [ "$(id -u)" != "0" ]; then
        mariadb_note "Running as non-root user: $(whoami)"
    fi

    # Check if database exists
    if [ ! -d "$DATADIR/mysql" ]; then
        mariadb_note "Database not found, initializing..."

        # Verify environment MARIADB_ variables
        if [ -z "$MARIADB_ROOT_PASSWORD" ] && [ "$MARIADB_ALLOW_EMPTY_PASSWORD" != "yes" ] && [ "$MARIADB_RANDOM_ROOT_PASSWORD" != "yes" ]; then
            mariadb_error $'Database is uninitialized and password option is not specified\n\tYou need to specify one of MARIADB_ROOT_PASSWORD, MARIADB_ALLOW_EMPTY_PASSWORD or MARIADB_RANDOM_ROOT_PASSWORD'
        fi

        # Initialize database
        mariadb_note "Initializing database files"
        mariadb-install-db --user=mysql --datadir="$DATADIR" --rpm --auth-root-authentication-method=normal --skip-test-db --basedir=/usr
        mariadb_note "Database files initialized"

        # Start temporary server
        mariadb_note "Starting temporary server"
        "$@" --skip-networking --socket="${SOCKET}" --wsrep-on=OFF --default-time-zone=SYSTEM --init-file=/dev/null &
        pid="$!"

        mariadb_client=(mariadb --protocol=socket -uroot -hlocalhost --socket="${SOCKET}")

        # Wait for server to start
        for i in {30..0}; do
            if echo 'SELECT 1' | "${mariadb_client[@]}" &> /dev/null; then
                break
            fi
            sleep 1
        done
        if [ "$i" = 0 ]; then
            mariadb_error "Unable to start server."
        fi

        mariadb_note "Temporary server started."

        # Load timezone info into database (unless skipped)
        if [ -z "$MARIADB_INITDB_SKIP_TZINFO" ]; then
            mariadb_note "Loading timezone info"
            # Load timezone data, but ignore any potential errors
            mariadb-tzinfo-to-sql /usr/share/zoneinfo 2>/dev/null | "${mariadb_client[@]}" mysql || true
        fi

        # Setup root password
        if [ "$MARIADB_RANDOM_ROOT_PASSWORD" == "yes" ]; then
            export MARIADB_ROOT_PASSWORD="$(pwgen -1 32)"
            mariadb_note "GENERATED ROOT PASSWORD: $MARIADB_ROOT_PASSWORD"
        fi

        # Setup root user and password
        "${mariadb_client[@]}" <<-EOSQL
			-- Secure the installation
			SET @@SESSION.SQL_LOG_BIN=0;
			
			-- Remove anonymous users
			DELETE FROM mysql.user WHERE user='';
			
			-- Remove remote root (keep only localhost)
			DELETE FROM mysql.user WHERE user='root' AND host NOT IN ('localhost', '127.0.0.1', '::1');
			
			-- Remove test database
			DROP DATABASE IF EXISTS test;
			DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';

			-- Set root password if provided
			$([ ! -z "$MARIADB_ROOT_PASSWORD" ] && echo "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('${MARIADB_ROOT_PASSWORD}');")
			$([ ! -z "$MARIADB_ROOT_PASSWORD" ] && echo "CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY '${MARIADB_ROOT_PASSWORD}';")
			$([ ! -z "$MARIADB_ROOT_PASSWORD" ] && echo "GRANT ALL ON *.* TO 'root'@'%' WITH GRANT OPTION;")
			
			FLUSH PRIVILEGES;
		EOSQL

        # Update client connection to use password if set
        if [ ! -z "$MARIADB_ROOT_PASSWORD" ]; then
            mariadb_client+=(--password="$MARIADB_ROOT_PASSWORD")
        fi

        # Create database
        if [ ! -z "$MARIADB_DATABASE" ]; then
            mariadb_note "Creating database ${MARIADB_DATABASE}"
            echo "CREATE DATABASE IF NOT EXISTS \`$MARIADB_DATABASE\`;" | "${mariadb_client[@]}"
        fi

        # Create user
        if [ ! -z "$MARIADB_USER" -a ! -z "$MARIADB_PASSWORD" ]; then
            mariadb_note "Creating user ${MARIADB_USER}"
            
            "${mariadb_client[@]}" <<-EOSQL
				CREATE USER '${MARIADB_USER}'@'%' IDENTIFIED BY '${MARIADB_PASSWORD}';
				$([ ! -z "$MARIADB_DATABASE" ] && echo "GRANT ALL ON \`${MARIADB_DATABASE}\`.* TO '${MARIADB_USER}'@'%';")
				FLUSH PRIVILEGES;
			EOSQL
        fi

        # Process init files
        mariadb_note "Processing initialization files"
        for f in /docker-entrypoint-initdb.d/*; do
            [ -f "$f" ] || continue
            case "$f" in
                *.sh)
                    if [ -x "$f" ]; then
                        mariadb_note "Running $f"
                        "$f"
                    else
                        mariadb_note "Sourcing $f"
                        . "$f"
                    fi
                    ;;
                *.sql)
                    mariadb_note "Running $f"
                    "${mariadb_client[@]}" < "$f"
                    echo
                    ;;
                *.sql.gz)
                    mariadb_note "Running $f"
                    gunzip -c "$f" | "${mariadb_client[@]}"
                    echo
                    ;;
                *.sql.xz)
                    mariadb_note "Running $f"
                    xzcat "$f" | "${mariadb_client[@]}"
                    echo
                    ;;
                *)
                    mariadb_warn "Ignoring $f"
                    ;;
            esac
        done

        # Stop temporary server
        mariadb_note "Stopping temporary server"
        if ! kill -s TERM "$pid" || ! wait "$pid"; then
            mariadb_error "Unable to shut down server."
        fi
        mariadb_note "Temporary server stopped"

        echo
        mariadb_note "MariaDB init process done. Ready for start up."
        echo
    else
        mariadb_note "Database already initialized, skipping setup"
    fi
fi

# Execute the command
exec "$@"
