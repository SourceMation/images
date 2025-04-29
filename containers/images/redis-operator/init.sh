
#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the redis image
# Author: Radosław Kolba
# e-mail: radoslaw.kolba@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

REDIS_OPERATOR_GIT="https://github.com/OT-CONTAINER-KIT/redis-operator.git"
VERSION=$(git ls-remote --tags $REDIS_OPERATOR_GIT | grep -o 'v.*' | sort --version-sort --reverse | head -1)

sed -i "s/version=\"[^\"]*\"/version=\"${VERSION:1}\"/" Dockerfile || exit 1

echo "Finished setting up the Redis Operator ${VERSION:1} image"