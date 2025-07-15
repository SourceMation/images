FROM sourcemation/debian-12-slim:latest

LABEL name="nodejs-24" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="Multiple licenses" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="NodeJS 24 on Debian 12 Slim Container" \
      description="Provides NodeJS 24 on Debian 12 Slim Container" \
      version="24.3.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="NodeJS 24 on Debian 12 Slim Container" \
      io.k8s.description="Provides NodeJS 24 on Debian 12 Slim Container" \
      io.openshift.tags="nodejs nodejs-24 debian-12-slim"


RUN groupadd --gid 1000 node \
  && useradd --uid 1000 --gid node --shell /bin/bash --create-home node

ENV NODE_VERSION="24.3.0"
ENV YARN_VERSION="1.22.22"

# Most of this packages are from buildpack-deps that is based on old Heroku
# stack, that now we mimic - how poetic!
RUN set -eux; echo "Installing development packages - buildpacks-deps style ;)!"; \
    apt-get update; \
    apt-get install -y --no-install-recommends  \
        autoconf \
        automake \
        bzip2 \
        ca-certificates \
        curl \
        default-libmysqlclient-dev \
        dirmngr \
        dpkg-dev \
        file \
        g++ \
        gcc \
        gpg \
        imagemagick \
        libatomic1 \
        libbz2-dev \
        libc6-dev \
        libcurl4-openssl-dev \
        libdb-dev \
        libevent-dev \
        libffi-dev \
        libgdbm-dev \
        libglib2.0-dev \
        libgmp-dev \
        libjpeg-dev \
        libkrb5-dev \
        liblzma-dev \
        libmagickcore-dev \
        libmagickwand-dev \
        libmaxminddb-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libpng-dev \
        libpq-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libtool \
        libwebp-dev \
        libxml2-dev \
        libxslt-dev \
        libyaml-dev \
        make \
        patch \
        unzip \
        wget \
        xz-utils \
        zlib1g-dev;

# gpg keys listed at https://github.com/nodejs/node#release-keys

RUN ARCH= && dpkgArch="$(dpkg --print-architecture)" \
  && case "${dpkgArch##*-}" in \
    amd64) ARCH='x64' OPENSSL_ARCH='linux-x86_64';; \
    arm64) ARCH='arm64' OPENSSL_ARCH='linux-aarch64';; \
    *) echo "unsupported architecture"; exit 1 ;; \
  esac \
  && export GNUPGHOME="$(mktemp -d)" \
  && set -ex \
  && for key in \
    C0D6248439F1D5604AAFFB4021D900FFDB233756 \
    DD792F5973C6DE52C432CBDAC77ABFA00DDBF2B7 \
    CC68F5A3106FF448322E48ED27F5E38D5B0A215F \
    8FCCA13FEF1D0C2E91008E09770F7A9A5AE15600 \
    890C08DB8579162FEE0DF9DB8BEAB4DFCF555EF4 \
    C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C \
    108F52B48DB57BB0CC439B2997B01419BD92F80A \
    A363A499291CBBC940DD62E41F10027AF002F8B0 \
  ; do \
      gpg --batch --keyserver-options timeout=5 --keyserver hkps://keys.openpgp.org --recv-keys "$key" && \
      gpg --batch --keyserver-options timeout=10 --keyserver keyserver.ubuntu.com --recv-keys "$key" || true ;\
  done \
  && curl -LO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
  && curl -LO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
  && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
  && gpgconf --kill all \
  && rm -rf "$GNUPGHOME" \
  && grep " node-v$NODE_VERSION-linux-$ARCH.tar.xz\$" SHASUMS256.txt | sha256sum -c - \
  && tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
  && rm "node-v$NODE_VERSION-linux-$ARCH.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt \
  && ln -s /usr/local/bin/node /usr/local/bin/nodejs \
  && rm -rf /tmp/* \
  && echo "Removing OpenSSL headers to save space" \
  && cd /usr/local/include/node/openssl/archs -mindepth 1 -maxdepth 1 ! -name "$OPENSSL_ARCH" -exec rm -rfv {} \;  \
  echo "OK, installed nodejs $NODE_VERSION"


RUN set -ex \
  && export GNUPGHOME="$(mktemp -d)" \
  && for key in \
    6A010C5166006599AA17F08146C2130DFD2497F5 \
  ; do \
      gpg --batch --keyserver-options timeout=5 --keyserver hkps://keys.openpgp.org --recv-keys "$key" || \
      gpg --batch --keyserver-options timeout=10 --keyserver keyserver.ubuntu.com --recv-keys "$key" ; \
  done \
  && curl -LO "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz" \
  && curl -LO "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz.asc" \
  && gpg --batch --verify yarn-v$YARN_VERSION.tar.gz.asc yarn-v$YARN_VERSION.tar.gz \
  && gpgconf --kill all \
  && rm -rf "$GNUPGHOME" \
  && mkdir -p /opt \
  && tar -xzf yarn-v$YARN_VERSION.tar.gz -C /opt/ \
  && ln -s /opt/yarn-v$YARN_VERSION/bin/yarn /usr/local/bin/yarn \
  && ln -s /opt/yarn-v$YARN_VERSION/bin/yarnpkg /usr/local/bin/yarnpkg \
  && rm yarn-v$YARN_VERSION.tar.gz.asc yarn-v$YARN_VERSION.tar.gz \
  && rm -rf /tmp/* \
  echo "OK, installed yarn $YARN_VERSION"

COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

CMD [ "node" ]
