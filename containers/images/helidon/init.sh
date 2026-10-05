#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the Helidon LTS image
# Author: Sourcemation
# ---------------------------------------------------

set -euo pipefail

APP="helidon"

echo "Checking the latest LTS version of $APP"

# Helidon uses Tip & Tail release model:
# - Tip: feature / non-LTS releases (27, 28...) aligned with OpenJDK rapid cadence
# - Tail: LTS releases (4.x currently; future LTS 29...) supported for 3 years
# We extract the latest LTS (4.x) version from the official Helidon CLI metadata.
LTS_VERSION=$(curl -s https://helidon.io/cli-data/versions.xml | grep -E '<version order="[0-9]+">' | grep -oE '4\.[0-9.]+' | head -n 1)

if [[ ! $LTS_VERSION =~ ^[0-9.]+$ ]]; then
    echo "Could not find a valid Helidon LTS version on helidon.io, falling back to 4.5.4"
    LTS_VERSION="4.5.4"
fi

echo "Latest Helidon LTS version: $LTS_VERSION"

# Replace the version in Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$LTS_VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $LTS_VERSION image"
