FROM sourcemation/debian-13-slim:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH
ARG USER=azure-cli

LABEL name="azure-cli" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="MIT" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Azure CLI on Debian 13 Slim Container" \
      description="Provides Azure CLI on Debian 13 Slim Container" \
      version="2.83.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Azure CLI on Debian 13 Slim Container" \
      io.k8s.description="Provides Azure CLI on Debian 13 Slim Container" \
      io.openshift.tags="azure-cli debian-13-slim"

ENV DEBIAN_FRONTEND=noninteractive

RUN useradd -m -s /bin/bash $USER

RUN apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        --no-install-suggests \
        curl \
        ca-certificates \
        gnupg \
        lsb-release \
    && curl -sLS https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/keyrings/microsoft.gpg > /dev/null\
    # Using bookworm repository for Azure CLI as trixie is not yet available.
    # See: https://github.com/Azure/azure-cli/issues/32069
    && echo "deb [signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ bookworm main" >  /etc/apt/sources.list.d/azure-cli.list \
    && apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        --no-install-suggests \
        azure-cli \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/archives/* \
        /var/log/* \
        /tmp/* \
        /var/tmp/*

USER $USER
CMD ["az"]
