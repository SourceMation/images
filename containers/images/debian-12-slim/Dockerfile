FROM scratch
ADD rootfs.tar.gz /

LABEL name="debian-12-slim" \
      maintainer="Sourcemation Containers team <contact@sourcemation.com>" \
      vendor="System - Debian project; Image - SourceMation" \
      url="https://sourcemation.com"\
      licenses="GPLv2" \
      created="$(date --utc --rfc-3339=seconds)" \
      architecture="$(arch)" \
      summary="Debian 12 Slim Base Container" \
      description="Provides Debian 12 Slim Base Container" \
      version="12" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Debian 12 Slim Base Container" \
      io.k8s.description="Provides Debian 12 Slim Base Container" \
      io.openshift.tags="base debian"

CMD ["/bin/bash"]
