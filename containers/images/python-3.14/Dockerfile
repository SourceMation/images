FROM sourcemation/debian-13-slim
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# This Dockerfile originates from the official Docker Hub image. We have made modifications
# to improve readability and maintainability. Importantly, our images are automatically
# rebuilt and updated.
# License: MIT

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="python-3.14" \
      vendor="Sourcemation" \
      url="https://Sourcemation.com/"\
      licenses="PSF License Version 2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Python 3.14 on Debian 13 Slim Container" \
      description="Provides Python 3.14 on Debian 13 Slim Container" \
      version="3.14.2" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Python 3.14 on Debian 13 Slim Container" \
      io.k8s.description="Provides Python 3.14 on Debian 13 Slim Container" \
      io.openshift.tags="python-3.14 debian-13-slim"

# Python ditched the old PGP key signing their releases in favor of Sigstore
# signatures. Is it good? Nah it's awful giving power to the corporate
# overlords, but it's convenient so here we are.
# https://www.python.org/downloads/metadata/sigstore/ There you will find the
# REL_MANAGER and OIDC_ISSUER values.

ARG REL_MANAGER="hugo@python.org"
ARG OIDC_ISSUER="https://github.com/login/oauth"

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH
ENV PYTHON_VERSION="3.14.2"
ENV PYTHON_SHA256="ce543ab854bc256b61b71e9b27f831ffd1bfd60a479d639f8be7f9757cf573e9"

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
	savedAptMark="$(apt-mark showmanual)"; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
                dpkg-dev gcc gnupg libbluetooth-dev libbz2-dev libc6-dev \
                libdb-dev libffi-dev libgdbm-dev liblzma-dev libncursesw5-dev \
                libreadline-dev libsqlite3-dev libssl-dev make tk-dev uuid-dev \
                wget xz-utils zlib1g-dev libzstd-dev; \
    wget --progress=dot:giga -O python.tar.xz "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz"; \
    echo "Checking the Python Checksum"; \
    echo "$PYTHON_SHA256 *python.tar.xz" | sha256sum -c -; \
    wget --progress=dot:giga -O python.tar.xz.sigstore "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz.sigstore"; \
    echo "Verifying the Python Signature"; \
    wget --progress=dot:giga -O cosign "https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-${TARGETARCH}"; \
    chmod +x cosign; \
    ./cosign verify-blob \
           --new-bundle-format \
           --certificate-oidc-issuer 'https://github.com/login/oauth' \
           --certificate-identity 'hugo@python.org' \
           --bundle ./python.tar.xz.sigstore \
           ./python.tar.xz ;\
    rm cosign; \
    rm python.tar.xz.sigstore; \
    # Remove the .sigstore bundle after verification \
    rm -rvf $HOME/.sigstore; \
    mkdir -p /usr/src/python; \
    tar --extract --directory /usr/src/python --strip-components=1 --file python.tar.xz; \
    rm python.tar.xz; \
    \
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
            arch="$(dpkg --print-architecture)"; arch="${arch##*-}"; \
# https://docs.python.org/3.12/howto/perf_profiling.html
# https://github.com/docker-library/python/pull/1000#issuecomment-2597021615
            case "$arch" in \
                    amd64|arm64) \
                            # only add "-mno-omit-leaf" on arches that support it
                            EXTRA_CFLAGS="${EXTRA_CFLAGS:-} -fno-omit-frame-pointer -mno-omit-leaf-frame-pointer"; \
                            ;; \
                    *) \
                            # other arches don't support "-mno-omit-leaf"
                            EXTRA_CFLAGS="${EXTRA_CFLAGS:-} -fno-omit-frame-pointer"; \
                            ;; \
            esac; \
    make -j "$nproc" \
            "EXTRA_CFLAGS=${EXTRA_CFLAGS:-}" \
            "LDFLAGS=${LDFLAGS:-}" \
    ; \
# https://github.com/docker-library/python/issues/784
# prevent accidental usage of a system installed libpython of the same version
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
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name 'libpython*.a' \) \) \
		\) -exec rm -rf '{}' + \
	; \
	\
	ldconfig; \
	\
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
	\
	export PYTHONDONTWRITEBYTECODE=1; \
	python3 --version; \
	pip3 --version

# make extra symlinks without 3
RUN set -eux; \
    for src in idle3 pip3 pydoc3 python3 python3-config; do \
        dst="$(echo "$src" | tr -d 3)"; \
        [ -s "/usr/local/bin/$src" ] && ln -svTn "$src" "/usr/local/bin/$dst" || true ; \
    done

CMD ["python3"]
