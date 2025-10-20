#!/bin/bash
set -e

DEST_CONTENT="/var/lib/ghost/content"

if [ -z "$(find "${DEST_CONTENT}" -mindepth 1 -print -quit)" ]; then
    echo "First run: Seeding initial content..."
    cp -a /var/lib/ghost/content.orig/. "${DEST_CONTENT}/"
fi

chown -R node:node "${DEST_CONTENT}"

echo "Starting Ghost server..."
exec gosu node "$@"