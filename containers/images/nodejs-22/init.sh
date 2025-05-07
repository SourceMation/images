#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the NodeJS 22 image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="NodeJS 22"

echo "Checking the latest version of $APP"

NODE_VERSION=$(git ls-remote --tags https://github.com/nodejs/node.git | grep  -o 'v22.[.0-9]*$'  | tr -d 'v' | sort --version-sort --reverse | head -1)

# Exit with an error if the returned version contains anything other
# than digits and dots
echo "Checking the latest version of $APP against the regex"
[[ ! $NODE_VERSION =~ ^[0-9.]+$ ]] && exit 1

echo "Latest version of $APP is $NODE_VERSION"

sed -i "s/version=\"[^\"]*\"/version=\"$NODE_VERSION\"/" Dockerfile || exit 1
sed -i "s/NODE_VERSION=\"[^\"]*\"/NODE_VERSION=\"$NODE_VERSION\"/" Dockerfile || exit 1


APP="YARN Classic"

echo "Checking the latest version of $APP"

YARN_VERSION=$(git ls-remote --tags https://github.com/yarnpkg/yarn.git | grep -o 'v1.[.0-9]*$' | tr -d 'v' | sort --version-sort --reverse | head -1)

echo "Checking the latest version of $APP against the regex"
[[ ! $YARN_VERSION =~ ^[0-9.]+$ ]] && exit 1

echo "Latest version of $APP is $YARN_VERSION"

sed -i "s/YARN_VERSION=\"[^\"]*\"/YARN_VERSION=\"$YARN_VERSION\"/" Dockerfile || exit 1

echo "Downloading entrypoint script"
curl -LO https://github.com/nodejs/docker-node/raw/refs/heads/main/22/bookworm-slim/docker-entrypoint.sh
chmod +x docker-entrypoint.sh 

echo "Init script completed successfully"
