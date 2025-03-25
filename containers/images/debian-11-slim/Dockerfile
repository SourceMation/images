FROM scratch
ADD rootfs.tar.gz /

LABEL name="debian-11-slim" \
  maintainer="Sourcemation Containers team <contact@sourcemation.com>" \
  vendor="System - Debian project; Image - SourceMation" \
  url="https://sourcemation.com"\
  source="https://github.com/Sourcemation/images"\
  licenses="GPLv2" \
  created="$(date --utc --rfc-3339=seconds)" \
  architecture="$(arch)" \
  summary="Debian 11 (bullseye) Slim Base Container" \
  description="Provides Debian 11 Slim Base Container" \
  version="11" \
  io.k8s.display-name="Debian 11 Slim Base Container" \
  io.k8s.description="Provides Debian 11 Slim Base Container" \
  io.openshift.tags="base debian"

CMD ["/bin/bash"]
