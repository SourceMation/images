#!/bin/bash
set -e

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

if [[ -n "$ZK_SERVER_ID" ]]; then
    log "Setting server ID to $ZK_SERVER_ID"
    echo "$ZK_SERVER_ID" > "$ZK_DATA_DIR/myid"
else
    log "Setting server ID to 1"
    echo "1" > "$ZK_DATA_DIR/myid"
fi

if [[ "$1" = 'zkServer.sh' ]]; then
    log "Starting Zookeeper server..."
    exec "$ZK_HOME/bin/zkServer.sh" start-foreground
else
    exec "$@"
fi
