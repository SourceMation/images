FROM rockylinux/rockylinux:9

ARG TARGETARCH

LABEL name="nodejs" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="NodeJS on EL9 Container" \
      description="Provides NodeJS on Rocky Linux 9 Container" \
      version="20.16.0" \
      io.k8s.display-name="NodeJS on EL9 Container" \
      io.k8s.description="Provides NodeJS on Rocky Linux 9 Container" \
      io.openshift.tags="nodejs rockylinux"

# Install required system packages and dependencies
RUN dnf module install -y nodejs:20
RUN dnf update -y && dnf clean all


EXPOSE 3000

CMD [ "node" ]
