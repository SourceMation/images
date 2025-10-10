FROM scratch
ADD rootfs.tar.gz /

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="debian-13-slim" \
      maintainer="Sourcemation Containers team <contact@sourcemation.com>" \
      vendor="System - Debian project; Image - SourceMation" \
      url="https://sourcemation.com"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Debian 13 (trixie) Slim Base Container" \
      description="Provides Debian 13 Slim Base Container" \
      version="13" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Debian 13 Slim Base Container" \
      io.k8s.description="Provides Debian 13 Slim Base Container" \
      io.openshift.tags="base debian"

CMD ["/bin/bash"]
