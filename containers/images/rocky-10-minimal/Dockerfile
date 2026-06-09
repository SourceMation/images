FROM scratch
ADD base-image.tar.gz /

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="rocky-10-minimal" \
      maintainer="Sourcemation Containers team <contact@sourcemation.com>" \
      vendor="System - Rocky Linux; Image - Sourcemation" \
      url="https://sourcemation.com"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Rocky Linux 10 Minimal Base Container" \
      description="Provides Rocky Linux 10 Minimal Base Container" \
      version="10" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Rocky Linux 10 Base Container" \
      io.k8s.description="Provides RockyLinux 10 Base Container" \
      io.openshift.tags="base rockylinux"

CMD ["/bin/bash"]
