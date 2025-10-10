#!/bin/bash
set -e

# Check if WordPress is already installed in the volume
# We check for wp-config.php, which doesn't exist in the original archive
if [ -f "wp-config.php" ]; then
    echo "Found existing WordPress installation. Starting server..."
else
    echo "First run. Installing WordPress to $(pwd)..."

    # Copy files from /usr/src/wordpress to the current directory /var/www/html
    # Using tar is faster and preserves permissions
    tar cf - -C /usr/src/wordpress . | tar xf -

    echo "Copying complete."

    rm -f index.html

    # Set default values for variables if they are not provided
    : "${WORDPRESS_DB_HOST:=mysql}"
    : "${WORDPRESS_DB_USER:=wordpress}"
    : "${WORDPRESS_DB_PASSWORD:=wordpress}"
    : "${WORDPRESS_DB_NAME:=wordpress}"
    : "${WORDPRESS_DB_TABLE_PREFIX:=wp_}"

    # Wait for the database to be ready
    echo "Waiting for database at ${WORDPRESS_DB_HOST}..."
    while ! nc -z "$WORDPRESS_DB_HOST" 3306; do
        sleep 1
    done
    echo "Database is ready."

    echo "Creating wp-config.php file..."
    
    # Fetch unique security salts from the WordPress.org API
    SALT=$(curl -sL https://api.wordpress.org/secret-key/1.1/salt/)
    
    # Create wp-config.php from the sample file
    cp wp-config-sample.php wp-config.php
    
    # Replace placeholder values in the config file
    sed -i "s/database_name_here/${WORDPRESS_DB_NAME}/" wp-config.php
    sed -i "s/username_here/${WORDPRESS_DB_USER}/" wp-config.php
    sed -i "s/password_here/${WORDPRESS_DB_PASSWORD}/" wp-config.php
    sed -i "s/localhost/${WORDPRESS_DB_HOST}/" wp-config.php
    sed -i "s/\$table_prefix = 'wp_'/\$table_prefix = '${WORDPRESS_DB_TABLE_PREFIX}'/" wp-config.php
    
    # Insert the security salts
    printf '%s\n' 'g/put your unique phrases here/d' a "$SALT" . w | ed -s wp-config.php

    # Set permissions for the web server
    chown -R www-data:www-data .

    echo "WordPress installation is complete."
fi

echo "Starting Apache server..."
# Execute the main process passed from CMD
exec "$@"