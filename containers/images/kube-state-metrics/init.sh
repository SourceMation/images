#!/usr/bin/bash
# ---------------------------------------------------
# Automated build process for the kube-state-metrics image
# Author: Paweł Piasek
# e-mail: pawel.piasek@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail
# Get latest version
echo "Checking the latest available version of the kube-state-metrics"
version=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/kubernetes/kube-state-metrics/releases/latest | sed 's/.*\///')
VERSION=${version#v}
## Exit if the version variable contains anything other than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

echo "Setup version in kube-state-metrics Dockerfile"
sed -i "s/version=.*/version=\"$VERSION\" \\\\/;s/^ARG VERSION.*/ARG VERSION=$version/;" Dockerfile

