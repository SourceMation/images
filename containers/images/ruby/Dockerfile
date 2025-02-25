FROM rockylinux/rockylinux:9

ARG TARGETARCH

LABEL name="ruby" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Ruby on EL9 Container" \
      description="Provides Ruby on Rocky Linux 9 Container" \
      version="3.0.7" \
      io.k8s.display-name="Ruby on EL9 Container" \
      io.k8s.description="Provides Ruby on Rocky Linux 9 Container" \
      io.openshift.tags="ruby rockylinux"

RUN yum install -y ruby irb
RUN dnf update -y && dnf clean all

ENV APP_VERSION="3.0.7" \
    APP_NAME="ruby"

# IN CASE OF INSTALLING RAILS
EXPOSE 3000

CMD [ "irb" ]
