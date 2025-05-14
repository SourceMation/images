#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the Maven 3.9 on OpenJDK 21 image
# Author: Aleksander Baranowski
# e-mail: aleksander.baranowski@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail

APP="Maven 3.9"

echo "Checking the latest version of $APP"

MAVEN_VER=$(git ls-remote --tags  https://github.com/apache/maven.git | grep -v rc | grep -o  'maven-3.9[.+0-9]*' | sort --version-sort -r | head -1)

# Exit with an error if the returned version contains anything other
# than digits and dots
echo "Checking the latest version of $APP against the regex"
echo "$MAVEN_VER" | grep -q 'maven-3.9.[.0-9]*' || exit 1

echo "Latest version of $APP is $MAVEN_VER"

VER_STR="${MAVEN_VER//maven-/}"

LABEL_STR="${VER_STR}-jdk-21"

sed -i "s/version=\"[^\"]*\"/version=\"$LABEL_STR\"/" Dockerfile || exit 1
sed -i "s/MAVEN_VER=\"[^\"]*\"/MAVEN_VER=\"$MAVEN_VER\"/" Dockerfile || exit 1

BASE_URL17=https://raw.githubusercontent.com/carlossg/docker-maven/refs/heads/main/eclipse-temurin-17/
BASE_URL21=https://raw.githubusercontent.com/carlossg/docker-maven/refs/heads/main/eclipse-temurin-21/


echo 'Downloading settings and entrypoint scripts'
rm -fv settings-docker.xml mvn-entrypoint.sh
wget $BASE_URL17/settings-docker.xml || wget $BASE_URL21/settings-docker.xml
wget $BASE_URL17/mvn-entrypoint.sh || wget $BASE_URL21/mvn-entrypoint.sh
chmod +x mvn-entrypoint.sh

echo "Init script completed successfully"
