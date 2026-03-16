#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the Quarkus image
# Author: Alex Baranowski
# ---------------------------------------------------

set -euo pipefail

echo "Checking the latest versions for Quarkus and JBang"

# Get latest jbang.sh checksum
JBANG_SUM=$(curl -sL https://sh.jbang.dev | sha256sum | awk '{print $1}')

# Get latest stable quarkus-cli version from Maven Central
# Filter to only exactly X.Y.Z versions (excludes CR/Final/4-part versions)
QUARKUS_VER=$(curl -s https://repo1.maven.org/maven2/io/quarkus/quarkus-cli/maven-metadata.xml | \
    grep -oP '(?<=<version>)\d+\.\d+\.\d+(?=</version>)' | sort -V | tail -1)

if [ -z "$QUARKUS_VER" ]; then
    echo "Could not find Quarkus version, falling back to 3.19.1"
    QUARKUS_VER="3.19.1"
fi

echo "Latest Quarkus version: $QUARKUS_VER"
echo "JBang checksum: $JBANG_SUM"

# Update Dockerfile
# Update QUARKUS_VERSION ARG
sed -i "s/ARG QUARKUS_VERSION=[0-9.].*/ARG QUARKUS_VERSION=$QUARKUS_VER/" Dockerfile
# Update version LABEL
sed -i "s/version=\"[^\"]*\"/version=\"$QUARKUS_VER\"/" Dockerfile
# Update jbang.sh checksum
sed -i "s/sha256sum --check <( echo \"[a-f0-9]* jbang.sh\" )/sha256sum --check <( echo \"$JBANG_SUM jbang.sh\" )/" Dockerfile

# Update README.md
sed -i "s/Quarkus version [^ <]*/Quarkus version $QUARKUS_VER/" README.md

echo "Init script completed successfully"
