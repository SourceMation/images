FROM sourcemation/rocky-9:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="python" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="Python" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Python on EL9 Container" \
      description="Provides Python on Rocky Linux 9 Container" \
      version="3.9.25" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Python on EL9 Container" \
      io.k8s.description="Provides Python on Rocky Linux 9 Container" \
      io.openshift.tags="python rockylinux"

RUN dnf install -y python3 python3-pip && dnf clean all
RUN dnf update -y && dnf clean all


ENV APP_VERSION="3.9.25" \
    APP_NAME="python"

EXPOSE 8000

CMD [ "python3" ]
