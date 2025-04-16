#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the GCC 15 - snapshot
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="gcc"

# NOTE that in the future we should use the similar way to the one used for
# gcc-13 and gcc-14 with use of git tags.

url="https://ftp.gwdg.de/pub/misc/gcc/snapshots/LATEST-15/"

# Download the HTML content
html_content=$(wget -qO- "$url")

# Extract the link using a more robust pattern than simple grep
latest_file=$(echo "$html_content" | sed -n 's/.*<a href="\([^"]*\)">gcc-15-[0-9]\{8\}\.tar\.xz<\/a>.*/\1/p')

if [ -n "$latest_file" ]; then
  latest_url="$url$latest_file"
  echo "The latest GCC 15 snapshot URL is: $latest_url"
else
  echo "Could not find the latest GCC 15 snapshot link."
fi

# Extract the version number from the filename
# The version number is in the format "gcc-15-YYYYMMDD.tar.xz"
# We want to extract "YYYYMMDD"
VERSION=$(echo "$latest_file" | sed -E 's/gcc-15-([0-9]{8})\.tar\.xz/\1/')

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/GCC_VERSION=\"[^\"]*\"/GCC_VERSION=\"$VERSION\"/" Dockerfile || exit 1

echo "Finished setting up the $APP $VERSION image"
