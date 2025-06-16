#!/usr/bin/env bash

# This script invokes the `init.sh` for each Dockerfile. `init.sh` Should
# update the dockerfiles.
# Author: Alex Baranowski

# Be more strict with errors
set -euo pipefail


# Global vars

BASE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Source the lib.sh
. "${BASE}/lib.sh"


# Find the names


for i in $(find . -name 'Dockerfile' | sort); do
    #dir_path=$(dirname "$i")
    # Get the latest directory on the path
    #container_dir=$(basename "$dir_path")
    container_dir=$(dirname "$i")
    print_info "Updating ${container_dir} Dockerfile"
    prepare_build || true
done

echo "The changes that might be incorporated are"

git diff
