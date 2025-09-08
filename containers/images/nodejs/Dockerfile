FROM sourcemation/rocky-9:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="nodejs" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="NodeJS on EL9 Container" \
      description="Provides NodeJS on Rocky Linux 9 Container" \
      version="22.16.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="NodeJS on EL9 Container" \
      io.k8s.description="Provides NodeJS on Rocky Linux 9 Container" \
      io.openshift.tags="nodejs rockylinux"

# Install required system packages and dependencies
RUN dnf module install -y nodejs:22 && dnf update -y && dnf clean all


EXPOSE 3000

CMD [ "node" ]
