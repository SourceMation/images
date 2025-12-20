FROM sourcemation/rocky-9:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="ruby" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Ruby on EL9 Container" \
      description="Provides Ruby on Rocky Linux 9 Container" \
      version="3.3.10" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Ruby on EL9 Container" \
      io.k8s.description="Provides Ruby on Rocky Linux 9 Container" \
      io.openshift.tags="ruby rockylinux"

RUN yum module -y enable ruby:3.3 &&  yum install -y ruby irb && dnf update -y && dnf clean all

ENV APP_VERSION="3.3.10" \
    APP_NAME="ruby"

# IN CASE OF INSTALLING RAILS
EXPOSE 3000

CMD [ "irb" ]
