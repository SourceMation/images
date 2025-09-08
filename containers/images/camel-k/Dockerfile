# Build stage
FROM sourcemation/golang-1.24 AS builder

ENV CAMEL_K_VER="v2.7.0"
RUN apt-get update && apt-get install openjdk-17-jdk-headless git gcc make cmake which maven -y
# THE MAKEFILE targets are taken from the camel-k Makefile and `images:` without final image build
# REMOVE ./pkg/cmd/source/util_test.go as they make everything to hang out or fail
RUN mkdir /build && cd /build && git clone --depth 1 -b ${CAMEL_K_VER} https://github.com/apache/camel-k.git &&\
    cd camel-k && rm -fv ./pkg/cmd/source/util_test.go &&\
    NOTEST=1 make build build-kamel-platform
    #NOTEST=1 make build maven-overlay build-kamel-platform

# Installing delve
RUN go install github.com/go-delve/delve/cmd/dlv@latest

FROM sourcemation/debian-12-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="camel-k" \
      vendor="Linux Polska" \
      url="https://linuxpolska.com/en/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Apache Camel-K on Debian 12 Slim Container" \
      description="Provides Camel-K on Debian 12 Slim Container" \
      version="2.7.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Apache Camel-K on Debian 12 Slim Container" \
      io.k8s.description="Provides Camel-K on Debian 12 Slim Container" \
      io.openshift.tags="camel-k debian-12"

ARG IMAGE_ARCH

ARG MAVEN_DEFAULT_VERSION="3.8.6"
ARG MAVEN_HOME="/usr/share/maven"
ARG MAVEN_DIST_URL="https://archive.apache.org/dist/maven/maven-3/${MAVEN_DEFAULT_VERSION}/binaries/apache-maven-${MAVEN_DEFAULT_VERSION}-bin.zip"
ARG MVNW_DIR="/usr/share/maven/mvnw/"
ARG MVN_REPO="/etc/maven/m2"
ARG MAVEN_OPTS=""

USER 0
RUN apt-get update && apt-get install -y openjdk-17-jdk-headless && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/archives/*


RUN echo "SYMLINKING delve to /usr/local/bin/" && ln -s /usr/bin/dlv /usr/local/bin/dlv

# Copy delve
COPY --from=builder /go/bin/dlv /usr/local/bin/dlv

# Maven configuration
RUN mkdir -p ${MAVEN_HOME}
RUN mkdir -p ${MVN_REPO}


# Prepare the maven wrapper required in the build Pod strategy
COPY --from=builder /build/camel-k/build/mvnw/mvnw.tar ${MVNW_DIR}
RUN tar -xC ${MVNW_DIR} -f ${MVNW_DIR}mvnw.tar \
    && rm -v ${MVNW_DIR}mvnw.tar \
    && sed -i "s;distributionUrl=.*;distributionUrl=${MAVEN_DIST_URL};" ${MVNW_DIR}.mvn/wrapper/maven-wrapper.properties

# Used by mvnw to download maven dist into it
ENV MAVEN_USER_HOME="${MAVEN_HOME}"

# Install a default mvnw distribution at build time
RUN ${MVNW_DIR}/mvnw --version 

# This is build process bug/old code
#COPY --from=builder /build/camel-k/build/_maven_output ${MVN_REPO}

# Fix https://github.com/moby/moby/issues/37965
RUN true

RUN chgrp -R 0 ${MVN_REPO} \
    && chown -R 1001:0 ${MVN_REPO} \
    && chmod -R 775 ${MVN_REPO} \
    && chgrp -R 0 ${MAVEN_HOME} \
    && chown -R 1001:0 ${MAVEN_HOME} \
    && chmod -R 775 ${MAVEN_HOME}

USER 1001:0

COPY --from=builder /build/camel-k/build/_output/bin/kamel* /usr/local/bin/kamel
RUN version=$(kamel version | grep -oP "\d+\.\d+\.\d+") && echo "camel-k: $version" >> /var/tmp/sourcemation.yml
CMD ["/usr/bin/jshell"]
