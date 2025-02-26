#!/usr/bin/env bash
# This image scripts was used to generate EL9 images with podman
# Taken from EuroLinux :)
# Author: Alex Baranowski
# License: Apache 2.0

# install deps
yum install -y podman yum-utils buildah zip

set -euo pipefail

install_packages=()

install_packages_file="./package_list"
yum_config="./yum.conf"


set -x

readarray install_packages < $install_packages_file

script=$(mktemp)

newcontainer=$(buildah from scratch)

echo "hack on the host system"
echo '%_install_langs C.utf8' | tee /etc/rpm/macros.image-language-conf
echo 'LANG="C.utf8"' | tee /etc/locale.conf

cat > "$script" <<EOF
#!/bin/sh
scratchmnt=\$(buildah mount "$newcontainer")
echo "\$scratchmnt" > /tmp/PODMAN_MOUNT
dnf -y install \
  --disableplugin '*' \
  --installroot "\$scratchmnt" \
  --setopt install_weak_deps=false \
  --setopt tsflasg=nodocs \
  -c "$yum_config" $(echo ${install_packages[*]} | tr -d '\n')
dnf --disableplugin '*' --installroot "\$scratchmnt" list --installed > /tmp/packages_list_yum
echo '%_install_langs en_US.UTF-8' | tee \$scratchmnt/etc/rpm/macros.image-language-conf
dnf -y reinstall \
  --disableplugin '*' \
  --installroot "\$scratchmnt" \
  --setopt install_weak_deps=false \
  --setopt tsflasg=nodocs \
  -c "$yum_config" krb5-libs || true # might be not installed at this point!
dnf --disableplugin='*' -y --installroot "\$scratchmnt" clean all
set -x
rm -rfv \$scratchmnt/var/log/dnf* \$scratchmnt/var/log/yum.* \$scratchmnt/var/cache/dnf \$scratchmnt/var/lib/dnf/repos
rm -rf \$scratchmnt/var/lib/dnf/history* \$scratchmnt/var/log/hawkey.log \$scratchmnt/boot \$scratchmnt/dev/null \$scratchmnt/run/*
#mkdir -p \$scratchmnt/run/lock
/bin/date +%Y%m%d_%H%M > \$scratchmnt/etc/BUILDTIME
echo '%_install_langs C.utf8' > \$scratchmnt/etc/rpm/macros.image-language-conf
echo 'LANG="C.utf8"' >  \$scratchmnt/etc/locale.conf
echo '0.0 0 0.0' > \$scratchmnt/etc/adjtime
echo '0' >> \$scratchmnt/etc/adjtime
echo 'UTC' >> \$scratchmnt/etc/adjtime
echo 'KEYMAP="us"' > \$scratchmnt/etc/vconsole.conf
rm -rf \$scratchmnt/usr/share/locale/en_CA/ \$scratchmnt/usr/share/locale/en_GB/ \$scratchmnt/usr/share/i18n/charmaps \$scratchmnt/usr/share/i18n/locales
rm -f \$scratchmnt/etc/machine-id
touch \$scratchmnt/etc/machine-id
touch \$scratchmnt/etc/resolv.conf
touch \$scratchmnt/etc/hostname
mkdir -p \$scratchmnt/var/cache/private \$scratchmnt/var/lib/private \$scratchmnt/var/lib/systemd/coredump
chmod 700 \$scratchmnt/var/cache/private
chmod 700 \$scratchmnt/var/lib/private
groupadd -R "\$scratchmnt/" -r -p '!*' -g 996 sgx && groupadd -R "\$scratchmnt/" -r -p '!*' -g 995 systemd-oom
useradd -R "\$scratchmnt/" -r -c 'systemd Userspace OOM Killer' -g 995 -u 995 -s '/usr/sbin/nologin' -M -d '/' systemd-oom
sed -i "/sgx/d" "\$scratchmnt/etc/group-"
sed -i "/sgx/d" "\$scratchmnt/etc/gshadow-"
cd \$scratchmnt/etc
ln -s ../usr/share/zoneinfo/UTC localtime
rm -rvf \$scratchmnt/tmp/*

buildah unmount "$newcontainer"
EOF
chmod +x "$script"
# We are using naked bash as we are running it in the container as root
# normally it should be run with 
bash "$script"
podman rmi -f "tmp-build"  || true
buildah commit "$newcontainer" "tmp-build"
podman save -o "base-image.tar" "tmp-build"
buildah rmi -f "tmp-build"  || true
buildah rmi --all -f || true
podman rmi --all -f

# after that we have to recreate from saved layer
rm -rf tmp
mkdir tmp
pushd tmp
tar xf ../"base-image.tar" 
# there was bug with podman having date set to Jan  1  1970  after extraction
touch *.tar*
# we have only one layer
gzip -9 < *.tar  > /tmp/base-image.tar.gz

popd 
