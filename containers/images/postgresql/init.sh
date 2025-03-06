#!/usr/bin/env bash
# ----------------------------------------------------
# Automated build process for the PostgreSQL 14 Docker image
# Author: Jarosław Mazurkiewicz
# e-mail: jaroslaw.mazurkiewicz@linuxpolska.pl
# ----------------------------------------------------

# Test image:
# docker run --name postgres-test -p 5432:5432 -e POSTGRES_PASSWORD=pass1234 -e PGPORT=5432 -d IMAGE_ID 
# docker logs postgres-test
# docker exec -it postgres-test psql -U postgres
# \l
# Remote:
# psql -h localhost -U postgres -W
# \l

APP="postgresql14-server"
ARCH="$(arch)"
IMG=$(head -1 Dockerfile | awk '{print $2}')
SPATH=$(dirname "$0")

echo "Checking the latest available version of the ${APP} app"
# Updating repository metadata and downloading the latest available version of the
# application, including adding the PostgreSQL repository
VERSION=$(docker run --rm ${IMG} /bin/bash -c \
          "dnf install -qy --nogpgcheck https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm > /dev/null && dnf check-update --nogpgcheck --refresh > /dev/null; dnf info --nogpgcheck --available ${APP}.${ARCH} | grep Version | awk '{print \$3}'")

# Exit with an error if the returned version contains anything other than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

# Replacing the version number in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/PG_VERSION=\"[^\"]*\"/PG_VERSION=\"$VERSION\"/" Dockerfile || exit 1


echo "Building the $APP $VERSION image"
