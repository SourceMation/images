#!/usr/bin/bash
# ---------------------------------------------------
# Automated build process for the fluentd image
# Author: Paweł Piasek
# e-mail: pawel.piasek@linuxpolska.pl
# ---------------------------------------------------

set -euo pipefail
# Get latest version
echo "Checking the latest available version of the fluentd"
version=$(curl -LSso /dev/null -w %{url_effective} https://github.com/fluent/fluentd/releases/latest | sed 's/.*\///')
VERSION=${version#v}
# Exit if the version variable contains anything other than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

ruby_install_version=$(curl -LSso /dev/null -w %{url_effective} https://github.com/postmodern/ruby-install/releases/latest | sed 's/.*\///')
ruby_install=https://github.com/postmodern/ruby-install/releases/download/${ruby_install_version}/ruby-install-${ruby_install_version#v}.tar.gz
ruby_install=${ruby_install//\//\\&} # escape slashes for sed

echo "Setup version and ruby-install source in Dockerfile"
sed -i "
  s/^ARG VERSION.*/ARG VERSION=$VERSION/
  s/version=.*/version=\"$VERSION\" \\\\/
  s/^ARG RUBY_INSTALL.*/ARG RUBY_INSTALL=$ruby_install/
" Dockerfile
