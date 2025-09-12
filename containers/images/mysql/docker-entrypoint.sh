#!/bin/bash
set -eo pipefail
shopt -s nullglob

# logging functions
mysql_log() {
	local type="$1"; shift
	printf '%s [%s] [Entrypoint]: %s\n' "$(date --rfc-3339=seconds)" "$type" "$*"
}
mysql_note() {
	mysql_log Note "$@"
}
mysql_warn() {
	mysql_log Warn "$@" >&2
}
mysql_error() {
	mysql_log ERROR "$@" >&2
	exit 1
}

# check if we're running as root and use gosu if needed
mysql_check_gosu() {
	if [ "$1" = 'mysqld' ] && [ "$(id -u)" = '0' ]; then
		mysql_note 'Switching to dedicated user "mysql"'
		exec gosu mysql "$BASH_SOURCE" "$@"
	fi
}

# usage: file_env VAR [DEFAULT]
#    ie: file_env 'XYZ_DB_PASSWORD' 'example'
# (will allow for "$XYZ_DB_PASSWORD_FILE" to fill in the value of
#  "$XYZ_DB_PASSWORD" from a file, especially for Docker's secrets feature)
file_env() {
	local var="$1"
	local fileVar="${var}_FILE"
	local def="${2:-}"
	if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
		mysql_error "Both $var and $fileVar are set (but are exclusive)"
	fi
	local val="$def"
	if [ "${!var:-}" ]; then
		val="${!var}"
	elif [ "${!fileVar:-}" ]; then
		val="$(< "${!fileVar}")"
	fi
	export "$var"="$val"
	unset "$fileVar"
}

# check to see if this file is being run or sourced from another script
_is_sourced() {
	[ "${#FUNCNAME[@]}" -gt 2 ] \
		&& [ "${FUNCNAME[1]}" = 'source' -o "${FUNCNAME[1]}" = 'main' ] \
		&& [ "${FUNCNAME[0]}" = '_is_sourced' ]
}

# usage: docker_process_init_files [file [file [...]]]
#    ie: docker_process_init_files /always-initdb.d/*
# process initializer files, based on file extensions
docker_process_init_files() {
	mysql_note 'Processing init files'
	
	for f; do
		case "$f" in
			*.sh)
				if [ -x "$f" ]; then
					mysql_note "Sourcing $f"
					. "$f"
				else
					mysql_note "Running $f"
					. "$f"
				fi
				;;
			*.sql)    mysql_note "Running $f"; docker_process_sql < "$f"; echo ;;
			*.sql.gz) mysql_note "Running $f"; gunzip -c "$f" | docker_process_sql; echo ;;
			*.sql.xz) mysql_note "Running $f"; xzcat "$f" | docker_process_sql; echo ;;
			*)        mysql_warn "Ignoring $f" ;;
		esac
		echo
	done
}

mysql_install_db() {
	if [ ! -d /var/lib/mysql/mysql ]; then
		mysql_note 'Initializing database'
		mysqld --initialize-insecure --user=mysql --datadir=/var/lib/mysql
		mysql_note 'Database initialized'
	fi
}

docker_temp_server_start() {
	mysql_note 'Starting temporary server'
	mysqld --user=mysql --skip-networking --socket=/tmp/mysql_init.sock &
	declare -g MYSQL_PID="$!"
	mysql_note "Waiting for server startup"
	local i
	for i in {30..0}; do
		if echo 'SELECT 1' | mysql --protocol=socket -uroot --socket=/tmp/mysql_init.sock &> /dev/null; then
			break
		fi
		sleep 1
	done
	if [ "$i" = 0 ]; then
		mysql_error 'Unable to start server.'
	fi
}

docker_temp_server_stop() {
	if ! kill -s TERM "$MYSQL_PID" || ! wait "$MYSQL_PID"; then
		mysql_error 'Unable to shut down server.'
	fi
}

docker_process_sql() {
	mysql --protocol=socket -uroot --socket=/tmp/mysql_init.sock --comments "$@"
}

docker_setup_db() {
	# Create a single SQL script that does everything in one connection
	local setup_sql_file="/tmp/setup.sql"
	
	cat > "$setup_sql_file" <<-EOSQL
		SET @@SESSION.SQL_LOG_BIN=0;
		
		-- Load timezone info if needed
	EOSQL
	
	if [ "$MYSQL_INITDB_SKIP_TZINFO" != "yes" ]; then
		mysql_note 'Adding timezone info to setup'
		echo "USE mysql;" >> "$setup_sql_file"
		mysql_tzinfo_to_sql /usr/share/zoneinfo 2>/dev/null | sed 's/Local time zone must be set--see zic manual page/-- &/' >> "$setup_sql_file"
	fi
	
	mysql_note 'Creating database users and setting up security'
	cat >> "$setup_sql_file" <<-EOSQL
		
		-- Set root password for localhost
		ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';
		
		-- Create root user for remote connections
		CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';
		GRANT ALL ON *.* TO 'root'@'%' WITH GRANT OPTION;
		
		-- Ensure mysql.infoschema user exists (required for MySQL 8.0+)
		CREATE USER IF NOT EXISTS 'mysql.infoschema'@'localhost' IDENTIFIED WITH caching_sha2_password AS '\$A\$005\$THISISACOMBINATIONOFINVALIDSALTANDPASSWORDTHATMUSTNEVERBRBEUSED' ACCOUNT LOCK;
		
		-- Clean up anonymous users and test database
		DELETE FROM mysql.user WHERE user = '';
		DROP DATABASE IF EXISTS test;
		DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
	EOSQL
	
	if [ -n "$MYSQL_DATABASE" ]; then
		mysql_note "Adding database creation: $MYSQL_DATABASE"
		echo "CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE\`;" >> "$setup_sql_file"
	fi
	
	if [ -n "$MYSQL_USER" ] && [ -n "$MYSQL_PASSWORD" ]; then
		mysql_note "Adding user creation: $MYSQL_USER"
		cat >> "$setup_sql_file" <<-EOSQL
			CREATE USER '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
		EOSQL
		
		if [ -n "$MYSQL_DATABASE" ]; then
			mysql_note "Adding user permissions for database $MYSQL_DATABASE"
			cat >> "$setup_sql_file" <<-EOSQL
				GRANT ALL ON \`$MYSQL_DATABASE\`.* TO '$MYSQL_USER'@'%';
			EOSQL
		fi
	fi
	
	echo "FLUSH PRIVILEGES;" >> "$setup_sql_file"
	
	# Execute the entire setup in one go
	mysql --protocol=socket -uroot --socket=/tmp/mysql_init.sock --comments < "$setup_sql_file"
	
	# Clean up
	rm -f "$setup_sql_file"
}

_main() {
	mysql_check_gosu "$@"
	
	# Fetch value from environment variables or files
	file_env 'MYSQL_ROOT_PASSWORD'
	file_env 'MYSQL_DATABASE'
	file_env 'MYSQL_USER'
	file_env 'MYSQL_PASSWORD'
	
	if [ "$1" = 'mysqld' ]; then
		# Check for the existence of a mysql directory in the data directory
		if [ ! -d /var/lib/mysql/mysql ]; then
			# Require a password for MySQL
			if [ -z "$MYSQL_ROOT_PASSWORD" ] && [ "$MYSQL_ALLOW_EMPTY_PASSWORD" != "yes" ] && [ "$MYSQL_RANDOM_ROOT_PASSWORD" != "yes" ]; then
				mysql_error 'Database is uninitialized and MYSQL_ROOT_PASSWORD not set. Did you forget to add -e MYSQL_ROOT_PASSWORD=... ?'
			fi
			
			# Generate random root password if requested
			if [ "$MYSQL_RANDOM_ROOT_PASSWORD" = "yes" ]; then
				export MYSQL_ROOT_PASSWORD="$(pwgen -1 32)"
				mysql_note "GENERATED ROOT PASSWORD: $MYSQL_ROOT_PASSWORD"
			fi
			
			mysql_install_db
			docker_temp_server_start
			
            # Process init files
			docker_process_init_files /docker-entrypoint-initdb.d/*
            
            docker_setup_db
			docker_temp_server_stop
			
			mysql_note 'MySQL init process done. Ready for start up.'
		fi
	fi
	
	exec "$@"
}

# If we are sourced from elsewhere, don't perform any further actions
if ! _is_sourced; then
	_main "$@"
fi