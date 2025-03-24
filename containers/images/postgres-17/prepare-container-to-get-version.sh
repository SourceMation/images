#!/usr/bin/env bash

apt-get update
apt-get install ca-certificates gpg -y
mkdir -p /usr/local/share/keyrings/
key='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8'
gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$key"
gpg --batch --export --armor "$key" > /usr/local/share/keyrings/postgres.gpg.asc
aptRepo="[ signed-by=/usr/local/share/keyrings/postgres.gpg.asc ] http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main 17"
# Add the repository to apt sources.list.d
echo "deb $aptRepo" > /etc/apt/sources.list.d/pgdg.list 
apt update

apt-cache madison postgresql-17 | awk '{print $3}' | head -n 1 > /version
