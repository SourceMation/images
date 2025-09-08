FROM scratch
ADD base-image.tar.gz /

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="rocky-9-minimal" \
      maintainer="Sourcemation Containers team <contact@sourcemation.com>" \
      vendor="System - Rocky Linux; Image - SourceMation" \
      url="https://sourcemation.com"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Rocky Linux 9 Minimal Base Container" \
      description="Provides Rocky Linux 9 Minimal Base Container" \
      version="9" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Rocky Linux 9 Base Container" \
      io.k8s.description="Provides RockyLinux 9 Base Container" \
      io.openshift.tags="base rockylinux"

CMD ["/bin/bash"]
