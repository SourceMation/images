FROM sourcemation/debian-12-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

# It's based on the Docker Official image for gcc with some tweaks :)

# Do not split the description, otherwise we will see a blank space in the labels
LABEL name="gcc-15" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="GPLv3+ with GCC Runtime Library Exception" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="GCC 15 on Debian 12 Slim Container" \
      description="Provides GCC 15 on Debian 12 Slim Container" \
      version="15.2.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="GCC 15 on Debian 12 Slim Container" \
      io.k8s.description="Provides GCC 15 on Debian 12 Slim Container" \
      io.openshift.tags="gcc gcc-15 debian-12-slim"

ENV GCC_VERSION="15.2.0"

# abigail-tools - abidiff later to verify that it's not breaking the debian packages
# Most of this packages are from buildpack-deps that is based on old Heroku stack,
# that now we mimic - how poetic!
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends  \
        abigail-tools \
        autoconf \
        automake \
        bzip2 \
        ca-certificates \
        curl \
        default-libmysqlclient-dev \
        dpkg-dev \
        file \
        g++ \
        gcc \
        imagemagick \
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
        zlib1g-dev; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*;

# https://gcc.gnu.org/mirrors.html
ENV GPG_KEYS="B215C1633BCA0477615F1B35A5B3A004745C015A \
    B3C42148A44E6983B3E4CC0793FA9B1AB75C61B8 \
    90AA470469D3965A87A5DCB494D03953902C9419 \
    80F98B2E0DAB6C8281BDF541A7C8C3B2F71EDF1C \
    7F74F97C103468EE5D750B583AB00996FC26A641 \
    33C235A34C46AA3FFB293709A328C3A2C3C45C06 \
    D3A93CAD751C2AF4F8C7AD516C35B99309B5FA62"


RUN set -ex; \
    \
    savedAptMark="$(apt-mark showmanual)"; \
    apt-get update; \
    apt-get install -y --no-install-recommends flex gnupg; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* ;\
    \
    curl -fL "https://mirrors.kernel.org/gnu/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.xz.sig" -o "gcc.tar.xz.sig"; \
    curl -fL "https://mirrors.kernel.org/gnu/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.xz" -o "gcc.tar.xz"; \
    export GNUPGHOME="$(mktemp -d)"; \
    for key in $GPG_KEYS; do \
        gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$key"; \
    done; \
    gpg --batch --verify gcc.tar.xz.sig gcc.tar.xz; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME"; \
    mkdir -p /usr/src/gcc; \
    tar -xf gcc.tar.xz -C /usr/src/gcc --strip-components=1; \
    rm gcc.tar.xz*; \
    cd /usr/src/gcc; \
    \
# "download_prerequisites" pulls down a bunch of tarballs and extracts them,
# but then leaves the tarballs themselves lying around
    ./contrib/download_prerequisites; \
    { rm *.tar.* || true; }; \
    \
# download the patched config.guess and config.sub from gist as git savannah.gnu.org is down/flaky consistently...
    wget -O config.sub "https://gist.githubusercontent.com/AlexBaranowski/187ac45796d6c1702da8c826554ec45a/raw/fcc2ca7b6a4abcebac6e3104572e5b22b54beee5/config.sub" ; \
    wget -O config.guess "https://gist.githubusercontent.com/AlexBaranowski/9cb5af9049348266afa7220469cb3ac7/raw/09680facc6ddbaa053e9a5652aef5ca1ff764ac2/config.guess"; \
# explicitly update autoconf config.guess and config.sub so they support more arches/libcs
    for f in config.guess config.sub; do \
#   wget -O "$f" "https://git.savannah.gnu.org/cgit/config.git/plain/$f?id=7d3d27baf8107b630586c962c057e22149653deb"; \
# find any more (shallow) copies of the file we grabbed and update them too
        find -mindepth 2 -name "$f" -exec cp -v "$f" '{}' ';'; \
    done; \
    \
    dir="$(mktemp -d)"; \
    cd "$dir"; \
    \
    extraConfigureArgs=''; \
    gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; \
    /usr/src/gcc/configure \
        --build="$gnuArch" \
        --disable-multilib \
        --enable-languages=c,c++,fortran,go \
        $extraConfigureArgs \
    ; \
    make -j "$(nproc)"; \
    make install-strip; \
    \
    cd ..; \
    \
    rm -rf "$dir" /usr/src/gcc; \
    \
    apt-mark auto '.*' > /dev/null; \
    [ -z "$savedAptMark" ] || apt-mark manual $savedAptMark; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false ; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*;

# gcc installs .so files in /usr/local/lib64 (and /usr/local/lib)...
RUN set -ex; \
# this filename needs to sort higher than all the architecture filenames ("aarch64-...", "armeabi...", etc)
    { echo '/usr/local/lib64'; echo '/usr/local/lib'; } > /etc/ld.so.conf.d/000-local-gcc-lib.conf; \
    ldconfig -v; \
    # the libc created by gcc might be too old for a newer Debian
    # check that the Debian libstdc++ doesn't have newer requirements than the gcc one
    deb="$(readlink -ve /usr/lib/*/libstdc++.so* | head -1)"; \
    gcc="$(readlink -ve /usr/local/lib*/libstdc++.so | head -1)"; \
# using LD_PRELOAD to make sure "abidiff" itself doesn't fail with the exact error we're trying to test for
    LD_PRELOAD="$deb" abidiff --no-added-syms "$deb" "$gcc"

# ensure that freshly built gcc is used instead of the one from the debian package
RUN set -ex; \
    dpkg-divert --divert /usr/bin/gcc.orig --rename /usr/bin/gcc; \
    dpkg-divert --divert /usr/bin/g++.orig --rename /usr/bin/g++; \
    dpkg-divert --divert /usr/bin/gfortran.orig --rename /usr/bin/gfortran; \
    update-alternatives --install /usr/bin/cc cc /usr/local/bin/gcc 999
