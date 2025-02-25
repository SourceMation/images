#!/usr/bin/env bash

# Author: Alex Baranowski
# Date: 2024-02-26

# Strict mode
set -euox pipefail

# Get Jenkins helpers files from the official repository
echo "-> Getting Jenkins helpers files from the official repository"
curl https://raw.githubusercontent.com/jenkinsci/docker/master/jenkins-support > jenkins-support
curl https://raw.githubusercontent.com/jenkinsci/docker/master/jenkins.sh > jenkins.sh
curl https://raw.githubusercontent.com/jenkinsci/docker/master/jenkins-plugin-cli.sh > jenkins-plugin-cli.sh
chmod 755 jenkins.sh

# Getting the newest Jenkins version from RPM stable repository
echo "-> Determining the newest Jenkins version from RPM stable repository"
newest_ver=$(repoquery --disableplugin='*' --disablerepo='*' --enablerepo='jenkins' --repofrompath='jenkins,https://pkg.jenkins.io/redhat-stable' --latest-limit 1 --queryformat='%{VERSION}')

# Replace the Jenkins version in the Dockerfile
echo "-> Replacing the Jenkins version in the Dockerfile with the newest version: ${newest_ver}"
sed -i "s#^ARG JENKINS_VERSION=.*#ARG JENKINS_VERSION=${newest_ver}#" Dockerfile

# Find the sha256 of the newest Jenkins version

echo "-> Determining the sha256 of the newest Jenkins version (war file)"
JENKINS_URL=https://repo.jenkins-ci.org/public/org/jenkins-ci/main/jenkins-war/${newest_ver}/jenkins-war-${newest_ver}.war
sha256sum=$(curl -sSL "${JENKINS_URL}" | sha256sum | awk '{print $1}')

# Replace the sha256 in the Dockerfile
echo "-> Replacing the sha256 in the Dockerfile with the newest sha256: ${sha256sum}"
sed -i "s#^ARG JENKINS_SHA=.*#ARG JENKINS_SHA=${sha256sum}#" Dockerfile

echo "image_version=$newest_ver" > conf.sh
echo "image_user=jenkins" >> conf.sh
echo 'port_exposed="8080 50000"' >> conf.sh
