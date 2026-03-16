#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the Micronaut image
# Author: Alex Baranowski
# ---------------------------------------------------

set -euo pipefail

echo "Checking the latest versions for Micronaut and GraalVM 21"

# Get latest sdkman.sh checksum
SDKMAN_SUM=$(curl -s "https://get.sdkman.io" | sha256sum | awk '{print $1}')

# Get latest micronaut version
MICRONAUT_VER=$(curl -s https://api.sdkman.io/2/candidates/default/micronaut)

# Get latest GraalVM 21 version
# We use linuxx64 as a representative platform to get the version identifier
# We prefer 'graal' over 'graalce' and sort to get the latest
JAVA_VER=$(curl -s "https://api.sdkman.io/2/candidates/java/linuxx64/versions/list?installed=" | grep "21\..*-graal" | grep -v "graalce" | sort -V | tail -1 | awk -F'|' '{print $NF}' | tr -d ' ')

if [ -z "$JAVA_VER" ]; then
    echo "Could not find Java 21 GraalVM version, falling back to 21.0.10-graal"
    JAVA_VER="21.0.10-graal"
fi

echo "Latest Micronaut version: $MICRONAUT_VER"
echo "Latest Java 21 GraalVM version: $JAVA_VER"
echo "SDKMAN checksum: $SDKMAN_SUM"

# Update Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$MICRONAUT_VER\"/" Dockerfile
sed -i "s/sdk install micronaut [0-9.]*/sdk install micronaut $MICRONAUT_VER/" Dockerfile
sed -i "s/sdk install java [0-9.a-z-]*/sdk install java $JAVA_VER/" Dockerfile
sed -i "s/sha256sum --check <( echo \"[a-f0-9]* sdkman.sh\")/sha256sum --check <( echo \"$SDKMAN_SUM sdkman.sh\")/" Dockerfile

# Update README.md
sed -i "s/Micronaut version [0-9.]*/Micronaut version $MICRONAUT_VER/" README.md

echo "Init script completed successfully"
