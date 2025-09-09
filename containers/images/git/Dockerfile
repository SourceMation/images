FROM sourcemation/debian-12-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="git" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="git on Debian 12 Slim Container" \
      description="Provides git on Debian 12 Slim Container" \
      version="2.39.5" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="git on Debian 12 Slim Container" \
      io.k8s.description="Provides git on Debian 12 Slim Container" \
      io.openshift.tags="git debian-12-slim"

ENV LANG=C.UTF-8 DEBIAN_FRONTEND=noninteractive HOME=/home/git

RUN apt update \
    && apt install -y \
        --no-install-recommends \
        --no-install-suggests \
        ca-certificates \
        openssl \
        curl \
        git \
    && apt clean \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/archives/* \
        /var/log/* \
        /var/tmp/* \
        /tmp/*

RUN useradd --shell /bin/bash -d $HOME git \
    && mkdir -p $HOME && chown git:git $HOME

USER git
WORKDIR $HOME
CMD [ "/bin/bash" ]