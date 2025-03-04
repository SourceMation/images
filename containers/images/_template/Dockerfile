# IF YOU HAVE TO BUILD THINGS, USE ANOTHER CONTAINER
# FROM rockylinux/rockylinux:9 as builder
# BUILD

# END BUILD
FROM rockylinux/rockylinux:9

# Architecture (amd64 / arm64) is passed with --platform="linux/$latest_arch" option during build cmd.
# We can use this in the dockerfile. Generally ${TARGETARCH} == amd64.
ARG TARGETARCH

LABEL name="..." \
  vendor="Linux Polska" \
  url="https://sourcemation.com"\
  source="https://github.com/SourceMation/images/issues"\
  licenses="GPLv2" \
  created="$(date +%Y%m%d)" \
  architecture="$(uname -m)" \
  summary="... on EL9 Container" \
  description="Provides ... on Rocky Linux 9 Container" \
  version="..." \
  io.k8s.display-name="... on EL9 Container" \
  io.k8s.description="Provides ... on Rocky Linux 9 Container" \
  io.openshift.tags="... rockylinux"
# INSTAL OR COPY --from=builder /builder/path /path


# RUN --security update as the image might be outdated
RUN dnf --security update -y && \
    dnf clean all && rm -rf /var/cache /var/log/dnf* /var/log/yum.*


# END INSTALL
USER 00000
EXPOSE 00000
ENTRYPOINT [ "" ]
