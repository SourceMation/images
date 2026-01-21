FROM sourcemation/debian-13-slim
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# This Dockerfile originates from the official Docker Hub image. We have made modifications
# to improve readability and maintainability. Importantly, our images are automatically
# rebuilt and updated.
# License: MIT

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="python-3.8" \
      vendor="Sourcemation" \
      url="https://Sourcemation.com/"\
      licenses="PSF License Version 2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Python 3.8 on Debian 13 Slim Container" \
      description="Provides Python 3.8 on Debian 13 Slim Container" \
      version="3.8.20" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Python 3.8 on Debian 13 Slim Container" \
      io.k8s.description="Provides Python 3.8 on Debian 13 Slim Container" \
      io.openshift.tags="python-3.8 debian-13-slim"

# New python is installed in /usr/local/bin
ENV PATH=/usr/local/bin:$PATH
# For Python < 3.13 lang should be set
ENV LANG=C.UTF-8
# Build vars
ENV GPG_KEY="E3FF2839C048B25C084DEBE9B26995E310250568"
ENV PYTHON_VERSION="3.8.20"
ENV PYTHON_SHA256="6fb89a7124201c61125c0ab4cf7f6894df339a40c02833bfd28ab4d7691fafb4"

# runtime dependencies
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        netbase \
        tzdata \
    ; \
    rm -rf /var/lib/apt/lists/*


RUN set -eux; \
    \
    # savedAptMark shows the packages that were manually installed \
    savedAptMark="$(apt-mark showmanual)"; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            dpkg-dev gcc gnupg libbluetooth-dev libbz2-dev libc6-dev \
            libdb-dev libffi-dev libgdbm-dev liblzma-dev libncursesw5-dev \
                            libreadline-dev libsqlite3-dev libssl-dev make tk-dev uuid-dev \
                            wget xz-utils zlib1g-dev; \
    wget --progress=dot:giga -O python.tar.xz "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz"; \
    echo "Checking the Python Checksum"; \
    echo "$PYTHON_SHA256 *python.tar.xz" | sha256sum -c -; \
    wget --progress=dot:giga -O python.tar.xz.asc "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz.asc"; \
    GNUPGHOME="$(mktemp -d)"; export GNUPGHOME; \
    gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys "$GPG_KEY"; \
    gpg --batch --verify python.tar.xz.asc python.tar.xz; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME" python.tar.xz.asc; \
    mkdir -p /usr/src/python; \
    tar --extract --directory /usr/src/python --strip-components=1 --file python.tar.xz; \
    rm python.tar.xz; \
    cd /usr/src/python; \
    gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; \
    ./configure \
            --build="$gnuArch" \
            --enable-loadable-sqlite-extensions \
            --enable-optimizations \
            --enable-option-checking=fatal \
            --enable-shared \
            --with-lto \
            --with-ensurepip \
    ; \
    nproc="$(nproc)"; \
    EXTRA_CFLAGS="$(dpkg-buildflags --get CFLAGS)"; \
    LDFLAGS="$(dpkg-buildflags --get LDFLAGS)"; \
    LDFLAGS="${LDFLAGS:--Wl},--strip-all"; \
    make -j "$nproc" \
            "EXTRA_CFLAGS=${EXTRA_CFLAGS:-}" \
            "LDFLAGS=${LDFLAGS:-}" \
    ; \
    rm python; \
    make -j "$nproc" \
        "EXTRA_CFLAGS=${EXTRA_CFLAGS:-}" \
        "LDFLAGS=${LDFLAGS:--Wl},-rpath='\$\$ORIGIN/../lib'" \
        python \
    ; \
    make install; \
    \
    cd /; \
    rm -rf /usr/src/python; \
    # remove the tests and pre-compiled python code \
    \
    find /usr/local -depth \
    \( \
        \( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
        -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name 'libpython*.a' \) \) \
    \) -exec rm -rf '{}' + \
    ; \
    ldconfig; \
    apt-mark auto '.*' > /dev/null; \
    apt-mark manual $savedAptMark; \
    # Basically, we're making sure crucial libraries don't get accidentally nuked.
    # 'ldd' tells us what's what, 'dpkg-query' figures out the package names,
    # and 'apt-mark' locks 'em down so they stick around.
    find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec ldd '{}' ';' \
            | awk '/=>/ { so = $(NF-1); if (index(so, "/usr/local/") == 1) { next }; gsub("^/(usr/)?", "", so); printf "*%s\n", so }' \
            | sort -u \
            | xargs -r dpkg-query --search \
            | grep -vE '^diversion' \
            | grep ':' \
            | cut -d: -f1 \
            | sort -u \
            | xargs -r apt-mark manual \
    ; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    rm -rf /var/lib/apt/lists/*; \
    # minimal tests + install setuptools \
    export PYTHONDONTWRITEBYTECODE=1; \
    python3 --version; \
    \
    pip3 install \
            --disable-pip-version-check \
            --no-cache-dir \
            --no-compile \
            'setuptools==65.5.1' \
            wheel \
    ; \
    pip3 --version

# make extra symlinks without 3
RUN set -eux; \
    for src in idle3 pip3 pydoc3 python3 python3-config; do \
        dst="$(echo "$src" | tr -d 3)"; \
        [ -s "/usr/local/bin/$src" ] && ln -svTn "$src" "/usr/local/bin/$dst" || true ; \
    done

CMD ["python3"]
