#!/bin/bash
set -e

CASSANDRA_CONF_DIR="/opt/cassandra/conf"
CASSANDRA_YAML="${CASSANDRA_CONF_DIR}/cassandra.yaml"

ln -sT /var/lib/cassandra "${CASSANDRA_HOME}/data"
ln -sT /var/log/cassandra "${CASSANDRA_HOME}/logs"
chown -R cassandra:cassandra /var/lib/cassandra /var/log/cassandra

: "${CASSANDRA_CLUSTER_NAME:=My Cassandra Cluster}"
: "${CASSANDRA_LISTEN_ADDRESS:=auto}"
: "${CASSANDRA_RPC_ADDRESS:=auto}"

if [ "$CASSANDRA_LISTEN_ADDRESS" = 'auto' ]; then
	CASSANDRA_LISTEN_ADDRESS="$(hostname -i)"
fi
if [ "$CASSANDRA_RPC_ADDRESS" = 'auto' ]; then
	CASSANDRA_RPC_ADDRESS="$(hostname -i)"
fi

: "${CASSANDRA_SEEDS:="$CASSANDRA_LISTEN_ADDRESS"}"

echo "Applying configuration to cassandra.yaml..."
sed -i -e "s/^cluster_name:.*/cluster_name: '${CASSANDRA_CLUSTER_NAME}'/" "$CASSANDRA_YAML"
sed -i -e "s/^listen_address:.*/listen_address: ${CASSANDRA_LISTEN_ADDRESS}/" "$CASSANDRA_YAML"
sed -i -e "s/^rpc_address:.*/rpc_address: ${CASSANDRA_RPC_ADDRESS}/" "$CASSANDRA_YAML"
sed -i -e "s/- seeds:.*/- seeds: \"${CASSANDRA_SEEDS}\"/" "$CASSANDRA_YAML"

echo "Configuration:"
echo "  - Cluster Name: ${CASSANDRA_CLUSTER_NAME}"
echo "  - Listen Address: ${CASSANDRA_LISTEN_ADDRESS}"
echo "  - RPC Address: ${CASSANDRA_RPC_ADDRESS}"
echo "  - Seed Nodes: ${CASSANDRA_SEEDS}"

if [[ "$CASSANDRA_SEEDS" != "$CASSANDRA_LISTEN_ADDRESS" ]]; then
    for seed in $(echo "$CASSANDRA_SEEDS" | tr ',' ' '); do
        echo "Waiting for seed node ${seed} to be ready..."
        while ! getent hosts "$seed"; do
            sleep 2
        done
        echo "Seed node ${seed} is ready."
    done
fi


exec gosu cassandra "$@"