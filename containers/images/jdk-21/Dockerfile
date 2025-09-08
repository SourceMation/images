FROM sourcemation/debian-12-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="jdk-21" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="Multiple licenses" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="JDK 21 on Debian 12 Slim Container" \
      description="Provides JDK 21 on Debian 12 Slim Container" \
      version="jdk-21.0.8-9" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="JDK 21 on Debian 12 Slim Container" \
      io.k8s.description="Provides JDK 21 on Debian 12 Slim Container" \
      io.openshift.tags="jdk jdk-21 debian-12-slim"

ENV JAVA_VERSION="jdk-21.0.8+9"
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH=$JAVA_HOME/bin:$PATH
# Default to UTF-8 file.encoding
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'


RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        # curl required for historical reasons, see https://github.com/adoptium/containers/issues/255
        curl \
        wget \
        # gnupg required to verify the signature
        gnupg \
        fontconfig \
        ca-certificates p11-kit \
        tzdata \
        locales \
    ; \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen; \
    locale-gen en_US.UTF-8; \
    rm -rf /var/lib/apt/lists/*


# Original image contains the `ESUM` var to verify download, checksum. But
# it's unnecessary as we are getting the GPG signed checksum file, and verify
# file against the signature...
# DL_VER_WITHOUT_PREFIX replaces the + with _
RUN set -eux; \
    DL_VER_WITHOUT_PREFIX="$(echo "${JAVA_VERSION}" | cut -d '-' -f 2 | sed 's/+/_/g')"; \
    ARCH="$(dpkg --print-architecture)"; \
    case "${ARCH}" in \
       amd64) \
         #BINARY_URL="https://github.com/adoptium/temurin21-binaries/releases/download/${JAVA_VERSION}/OpenJDK21U-jre_x64_linux_hotspot_21.0.7_6.tar.gz"; \
         BINARY_URL="https://github.com/adoptium/temurin21-binaries/releases/download/${JAVA_VERSION}/OpenJDK21U-jdk_x64_linux_hotspot_${DL_VER_WITHOUT_PREFIX}.tar.gz"; \
         ;; \
       arm64) \
         BINARY_URL="https://github.com/adoptium/temurin21-binaries/releases/download/${JAVA_VERSION}/OpenJDK21U-jdk_aarch64_linux_hotspot_${DL_VER_WITHOUT_PREFIX}.tar.gz"; \
         ;; \
       *) \
         echo "Unsupported arch: ${ARCH}"; \
         exit 1; \
         ;; \
    esac; \
    wget --progress=dot:giga -O /tmp/openjdk.tar.gz ${BINARY_URL}; \
    wget --progress=dot:giga -O /tmp/openjdk.tar.gz.sig ${BINARY_URL}.sig; \
    export GNUPGHOME="$(mktemp -d)"; \
    # gpg: key 843C48A565F8F04B: "Adoptium GPG Key (DEB/RPM Signing Key) <temurin-dev@eclipse.org>" imported
    gpg --batch --keyserver keyserver.ubuntu.com --recv-keys 3B04D753C9050D9A5D343F39843C48A565F8F04B; \
    gpg --batch --verify /tmp/openjdk.tar.gz.sig /tmp/openjdk.tar.gz; \
    mkdir -p "$JAVA_HOME"; \
    tar --extract \
        --file /tmp/openjdk.tar.gz \
        --directory "$JAVA_HOME" \
        --strip-components 1 \
        --no-same-owner \
    ; \
    rm -f /tmp/openjdk.tar.gz; \
    # https://github.com/docker-library/openjdk/issues/331#issuecomment-498834472
    find "$JAVA_HOME/lib" -name '*.so' -exec dirname '{}' ';' | sort -u > /etc/ld.so.conf.d/docker-openjdk.conf; \
    ldconfig; \
    # https://github.com/docker-library/openjdk/issues/212#issuecomment-420979840
    # https://openjdk.java.net/jeps/341
    java -Xshare:dump;

COPY --chmod=755 entrypoint.sh /__cacert_entrypoint.sh
ENTRYPOINT ["/__cacert_entrypoint.sh"]
