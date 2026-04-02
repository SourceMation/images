# BUILD STAGE
FROM sourcemation/jdk-25:latest AS builder

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV CATALINA_HOME=/usr/local/tomcat
RUN mkdir -p "$CATALINA_HOME"
WORKDIR $CATALINA_HOME

ENV TOMCAT_NATIVE_LIBDIR=$CATALINA_HOME/native-jni-lib
ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$TOMCAT_NATIVE_LIBDIR

ENV TOMCAT_MAJOR=11
ENV TOMCAT_VERSION=11.0.20
ENV TOMCAT_SHA512=8edf12ae9ffb837d1fa1542beae9a80b40419c341963eabed074f2f11d8168e0a82307d5fdc010102db5ee2b983b404816b13435f8c6810b7684fe7b3c19191d

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        xz-utils \
        dpkg-dev \
        gcc \
        libapr1-dev \
        libssl-dev \
        make \
    ; \
    \
    get_resource() { \
        local target="$1"; \
        local path="$2"; \
        local alt_path="${3:-}"; \
        local success=; \
        local urls=( \
            "https://dlcdn.apache.org/$path" \
            "https://archive.apache.org/dist/$path" \
        ); \
        if [ -n "$alt_path" ]; then \
            urls+=("https://repo1.maven.org/maven2/org/apache/tomcat/tomcat/$alt_path"); \
        fi; \
        for url in "${urls[@]}"; do \
            if curl -fsSL -o "$target" "$url" && [ -s "$target" ]; then \
                success=1; \
                break; \
            fi; \
        done; \
        [ -n "$success" ]; \
    }; \
    \
    get_resource 'tomcat.tar.gz' "tomcat/tomcat-$TOMCAT_MAJOR/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz" "$TOMCAT_VERSION/tomcat-$TOMCAT_VERSION.tar.gz"; \
    echo "$TOMCAT_SHA512 *tomcat.tar.gz" | sha512sum --strict --check -; \
    get_resource 'tomcat.tar.gz.asc' "tomcat/tomcat-$TOMCAT_MAJOR/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz.asc" "$TOMCAT_VERSION/tomcat-$TOMCAT_VERSION.tar.gz.asc"; \
    GNUPGHOME="$(mktemp -d)"; export GNUPGHOME; \
    curl -fL -o upstream-KEYS "https://downloads.apache.org/tomcat/tomcat-$TOMCAT_MAJOR/KEYS"; \
    gpg --batch --import upstream-KEYS; \
    gpg --batch --verify tomcat.tar.gz.asc tomcat.tar.gz; \
    tar -xf tomcat.tar.gz --strip-components=1; \
    rm bin/*.bat; \
    rm tomcat.tar.gz*; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME"; \
    \
    mv webapps webapps.dist; \
    mkdir webapps; \
    \
    nativeBuildDir="$(mktemp -d)"; \
    tar -xf bin/tomcat-native.tar.gz -C "$nativeBuildDir" --strip-components=1; \
    ( \
        export CATALINA_HOME="$PWD"; \
        cd "$nativeBuildDir/native"; \
        gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; \
        aprConfig="$(command -v apr-1-config)"; \
        ./configure \
            --build="$gnuArch" \
            --libdir="$TOMCAT_NATIVE_LIBDIR" \
            --prefix="$CATALINA_HOME" \
            --with-apr="$aprConfig" \
            --with-java-home="$JAVA_HOME" \
        ; \
        nproc="$(nproc)"; \
        make -j "$nproc"; \
        make install; \
    ); \
    rm -rf "$nativeBuildDir"; \
    rm bin/tomcat-native.tar.gz; \
    \
    find "$TOMCAT_NATIVE_LIBDIR" -type f -executable -exec ldd '{}' ';' \
        | awk '/=>/ { print $(NF-1) }' \
        | xargs -rt readlink -e \
        | sort -u \
        | xargs -rt dpkg-query --search \
        | cut -d: -f1 \
        | sort -u \
        | tee "$TOMCAT_NATIVE_LIBDIR/.dependencies.txt" \
    ; \
    \
    find ./bin/ -name '*.sh' -exec sed -ri 's|^#!/bin/sh$|#!/usr/bin/env bash|' '{}' +; \
    chmod -R +rX .; \
    chmod 1777 logs temp work; \
    rm -rf /var/lib/apt/lists/*

# FINAL STAGE
FROM sourcemation/jre-25:latest

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="tomcat-11" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Apache Tomcat 11 on JRE 25 Container" \
      description="Provides Apache Tomcat 11 on JRE 25 Container" \
      version="11.0.20" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Apache Tomcat 11 on JRE 25 Container" \
      io.k8s.description="Provides Apache Tomcat 11 on JRE 25 Container" \
      io.openshift.tags="tomcat tomcat-11 jre-25"

ENV CATALINA_HOME=/usr/local/tomcat
ENV PATH=$CATALINA_HOME/bin:$PATH
WORKDIR $CATALINA_HOME

# let "Tomcat Native" live somewhere isolated
ENV TOMCAT_NATIVE_LIBDIR=$CATALINA_HOME/native-jni-lib
ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$TOMCAT_NATIVE_LIBDIR

COPY --from=builder $CATALINA_HOME $CATALINA_HOME

RUN set -eux; \
    apt-get update; \
    if [ -f "$TOMCAT_NATIVE_LIBDIR/.dependencies.txt" ]; then \
        xargs -rt apt-get install -y --no-install-recommends < "$TOMCAT_NATIVE_LIBDIR/.dependencies.txt"; \
    fi; \
    rm -rf /var/lib/apt/lists/*; \
    catalina.sh version; \
    nativeLines="$(catalina.sh configtest 2>&1)"; \
    nativeLines="$(echo "$nativeLines" | grep 'Apache Tomcat Native')"; \
    nativeLines="$(echo "$nativeLines" | sort -u)"; \
    if ! echo "$nativeLines" | grep -E 'INFO: Loaded( APR based)? Apache Tomcat Native library' >&2; then \
        echo >&2 "$nativeLines"; \
        exit 1; \
    fi; \
    echo "tomcat: $TOMCAT_VERSION" >> /var/tmp/sourcemation.yml

EXPOSE 8080
CMD ["catalina.sh", "run"]
