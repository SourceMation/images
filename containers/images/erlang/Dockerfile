FROM sourcemation/debian-13-slim:latest AS builder

ARG ERLANG_VERSION=28.3
ARG ERLANG_DOWNLOAD_URL="https://github.com/erlang/otp/releases/download/OTP-${ERLANG_VERSION}/otp_src_${ERLANG_VERSION}.tar.gz"
ARG ERLANG_SHA256=1956ad6584678b631ab4f9b8aebe2dac037cd7401abb44564a01134ff0ac5bed
ARG ERLANG_INSTALL_PATH_PREFIX=/opt/erlang

ARG OPENSSL_VERSION=3.6.0
ARG OPENSSL_DOWNLOAD_URL="https://github.com/openssl/openssl/releases/download/openssl-${OPENSSL_VERSION}/openssl-${OPENSSL_VERSION}.tar.gz"
ARG OPENSSL_SHA256=b6a5f44b7eb69e3fa35dbf15524405b44837a481d43d81daddde3ff21fcbb8e9
ARG OPENSSL_INSTALL_PATH_PREFIX=/opt/openssl
ARG OPENSSL_CONFIG_DIR="$OPENSSL_INSTALL_PATH_PREFIX/etc/ssl"

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    build-essential \
    libncurses5-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/src

# Download and build OpenSSL
RUN curl -fSL -o openssl.tar.gz "${OPENSSL_DOWNLOAD_URL}" \
    && echo "${OPENSSL_SHA256} openssl.tar.gz" | sha256sum -c - \
    && mkdir -p openssl \
    && tar -xzf openssl.tar.gz -C openssl --strip-components=1 \
    && rm openssl.tar.gz \
    && cd openssl \
    && gnuArch="$(dpkg-architecture --query DEB_HOST_GNU_TYPE |awk -F'-' '{print "linux-" $1}')" \
    && ./config \
        "$gnuArch" \
        --prefix="$OPENSSL_INSTALL_PATH_PREFIX" \
        --openssldir="$OPENSSL_CONFIG_DIR" \
        --libdir="$OPENSSL_INSTALL_PATH_PREFIX/lib" \
        -Wl,-rpath="$OPENSSL_INSTALL_PATH_PREFIX/lib" \
        enable-fips \
    && make -j$(nproc) \
    && make install_sw install_ssldirs install_fips \
    && ldconfig \
    && rmdir "$OPENSSL_CONFIG_DIR/certs" "$OPENSSL_CONFIG_DIR/private" \
	&& ln -sf /etc/ssl/certs /etc/ssl/private "$OPENSSL_CONFIG_DIR"

# Verify installation
RUN openssl version

# Download and build Erlang with custom OpenSSL
RUN curl -fSL -o otp_src.tar.gz "${ERLANG_DOWNLOAD_URL}" \
    && echo "${ERLANG_SHA256} otp_src.tar.gz" | sha256sum -c - \
    && mkdir -p erlang \
    && tar -xzf otp_src.tar.gz -C erlang --strip-components=1 \
    && rm otp_src.tar.gz \
    && cd erlang \
    && export ERL_TOP=$(pwd) \
    && export CFLAGS="$(dpkg-buildflags --get CFLAGS)" \
    && export CFLAGS="$CFLAGS -Wl,-rpath=$OPENSSL_INSTALL_PATH_PREFIX/lib" \
    && export hostArch="$(dpkg-architecture --query DEB_HOST_GNU_TYPE)" \
	&& export buildArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
    && ./configure \
        --prefix="$ERLANG_INSTALL_PATH_PREFIX" \
        --host="$hostArch" \
		--build="$buildArch" \
        --disable-hipe \
        --disable-sctp \
        --disable-silent-rules \
        --enable-builtin-zlib \
        --enable-clock-gettime \
        --enable-hybrid-heap \
        --enable-kernel-poll \
        --enable-smp-support \
        --enable-threads \
        --with-microstate-accounting=extra \
        --with-ssl="$OPENSSL_INSTALL_PATH_PREFIX" \
        --without-common_test \
        --without-debugger \
        --without-dialyzer \
        --without-diameter \
        --without-edoc \
        --without-erl_docgen \
        --without-et \
        --without-eunit \
        --without-ftp \
        --without-hipe \
        --without-jinterface \
        --without-megaco \
        --without-observer \
        --without-odbc \
        --without-reltool \
        --without-snmp \
        --without-ssh \
        --without-tftp \
        --without-wx \
        --enable-jit \
    && make -j$(nproc) GEN_OPT_FLGS="-O2 -fno-strict-aliasing" \
    && make install \
    \
# Remove unnecessary files
    && find "$ERLANG_INSTALL_PATH_PREFIX/lib/erlang" -type d -name examples -exec rm -rf '{}' + \
    && find "$ERLANG_INSTALL_PATH_PREFIX/lib/erlang" -type d -name src -exec rm -rf '{}' + \
    && find "$ERLANG_INSTALL_PATH_PREFIX/lib/erlang" -type d -name include -exec rm -rf '{}' +

# Check that Erlang/OTP crypto & ssl were compiled against OpenSSL correctly
ENV PATH $ERLANG_INSTALL_PATH_PREFIX/bin:$PATH
RUN find $ERLANG_INSTALL_PATH_PREFIX -type f -name 'crypto.so' -exec ldd {} \; | awk '/libcrypto\.so/ { if (!index($3,ENVIRON["OPENSSL_INSTALL_PATH_PREFIX"])) exit 1 }'

RUN set -eux \
# Configure OpenSSL to use system certs
	&& ln -vsf /etc/ssl/certs /etc/ssl/private "$OPENSSL_INSTALL_PATH_PREFIX/etc/ssl" \
	&& ldconfig \
	\
# Include the fips module configuration
    && sed -i.ORIG -e "/\.include.*fips/ s!.*!.include $OPENSSL_INSTALL_PATH_PREFIX/etc/ssl/fipsmodule.cnf!" \
		-e '/# fips =/s/.*/fips = fips_sect/' "$OPENSSL_INSTALL_PATH_PREFIX/etc/ssl/openssl.cnf" \
	&& sed -i.ORIG -e '/^activate/s/^/#/' "$OPENSSL_INSTALL_PATH_PREFIX/etc/ssl/fipsmodule.cnf"

RUN erl -noshell -eval 'ok = crypto:start(), ok = io:format("~p~n~n~p~n~n", [crypto:supports(), ssl:versions()]), init:stop().'

# Create a minimal runtime image
FROM sourcemation/debian-13-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="erlang" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Erlang on Debian 13-slim" \
      description="Provides Erlang on Debian 13-slim" \
      version="28.3" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Erlang on Debian 13-slim Container" \
      io.k8s.description="Provides Erlang Debian 13-slim Container" \
      io.openshift.tags="erlang debian-13-slim"


ARG ERLANG_INSTALL_PATH_PREFIX=/opt/erlang
ARG OPENSSL_INSTALL_PATH_PREFIX=/opt/openssl

COPY --from=builder $ERLANG_INSTALL_PATH_PREFIX $ERLANG_INSTALL_PATH_PREFIX
COPY --from=builder $OPENSSL_INSTALL_PATH_PREFIX $OPENSSL_INSTALL_PATH_PREFIX
COPY --from=builder /etc/ssl/private /etc/ssl/private
COPY --from=builder /etc/ssl/certs /etc/ssl/certs

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsctp1 \
    libodbc2 \
    zlib1g \
    && rm -rf /var/lib/apt/lists/* \
    && ldconfig

ENV APP_NAME="erlang" \
    APP_VERSION="28.3" \
    PATH=$ERLANG_INSTALL_PATH_PREFIX/bin:$OPENSSL_INSTALL_PATH_PREFIX/bin:$PATH

CMD ["erl"]
