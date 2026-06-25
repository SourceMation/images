#!/usr/bin/env bash
set -euo pipefail

echo "-> Downloading new entrypoints and configs"
wget -q https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/stable/debian/10-listen-on-ipv6-by-default.sh
wget -q https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/stable/debian/15-local-resolvers.envsh
wget -q https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/stable/debian/20-envsubst-on-templates.sh
wget -q https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/stable/debian/30-tune-worker-processes.sh
wget -q https://raw.githubusercontent.com/nginx/docker-nginx/refs/heads/master/stable/debian/docker-entrypoint.sh
chmod +x 10-listen-on-ipv6-by-default.sh 15-local-resolvers.envsh 20-envsubst-on-templates.sh 30-tune-worker-processes.sh docker-entrypoint.sh
