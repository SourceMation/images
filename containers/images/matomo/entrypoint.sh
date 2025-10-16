#!/bin/bash
set -e

if [ -f "config/config.ini.php" ]; then
    echo "Found existing Matomo installation. Checking for updates..."
else
    echo "First run. Installing Matomo to $(pwd)..."

    rm -f index.html
    
    tar cf - -C /usr/src/matomo . | tar xf -
    echo "Copying complete."

    chown -R www-data:www-data .

    echo "Matomo installation is complete."
fi

echo "Starting Apache server..."
exec "$@"