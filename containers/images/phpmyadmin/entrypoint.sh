#!/bin/bash
set -e

CONFIG_FILE="/var/www/html/config.inc.php"

if [ -f "$CONFIG_FILE" ]; then
    echo "Found existing config.inc.php. Starting Apache..."
else
    echo "First run. Creating config.inc.php..."

    rm -f index.html

    BLOWFISH_SECRET=$(pwgen -s 32 1)

    cat > "$CONFIG_FILE" <<-EOF
<?php
declare(strict_types=1);

/**
 * This is a minimalist configuration file for phpMyAdmin.
 *
 * All directives are explained in documentation:
 * https://docs.phpmyadmin.net/en/latest/config.html
 */

\$cfg['blowfish_secret'] = '${BLOWFISH_SECRET}';

\$i = 0;
EOF

    if [ -n "$PMA_HOST" ]; then
        cat >> "$CONFIG_FILE" <<-EOF

\$i++;
\$cfg['Servers'][\$i]['host'] = '${PMA_HOST}';
if (getenv('PMA_PORT')) {
    \$cfg['Servers'][\$i]['port'] = getenv('PMA_PORT');
}
\$cfg['Servers'][\$i]['compress'] = false;
\$cfg['Servers'][\$i]['AllowNoPassword'] = false;
EOF
    else
        cat >> "$CONFIG_FILE" <<-EOF

/**
 * Allow login to any server
 */
\$cfg['AllowArbitraryServer'] = true;
EOF
    fi

    cat >> "$CONFIG_FILE" <<-EOF

/**
 * Directories for saving/loading files from server
 */
\$cfg['UploadDir'] = '';
\$cfg['SaveDir'] = '';

/**
 * Temp directory for some features
 */
\$cfg['TempDir'] = '/var/www/html/tmp';
?>
EOF

    chown www-data:www-data "$CONFIG_FILE"
    chmod 644 "$CONFIG_FILE"
    echo "config.inc.php created successfully."
fi

echo "Starting Apache server..."
exec "$@"