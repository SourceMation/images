# Build stage
FROM sourcemation/rocky-9:latest AS builder

ENV CAMEL_K_VER="v2.5.1"
RUN yum install maven-openjdk17 go git gcc make cmake which -y
# THE MAKEFILE targets are taken from the camel-k Makefile and `images:` without final image build
# REMOVE ./pkg/cmd/source/util_test.go as they make everything to hang out or fail
RUN mkdir /build && cd /build && git clone --depth 1 -b ${CAMEL_K_VER} https://github.com/apache/camel-k.git &&\
    cd camel-k && rm -fv ./pkg/cmd/source/util_test.go &&\
    NOTEST=1 make build maven-overlay build-kamel-platform
RUN echo "Creating empty _maven_output - same as in the images make rule" && mkdir -v /build/camel-k/build/_maven_output


FROM sourcemation/rocky-9:latest

LABEL name="camel-k" \
      vendor="Linux Polska" \
      url="https://linuxpolska.com/en/"\
      licenses="Apache-2.0" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Apache Camel-K on EL9 Container" \
      description="Provides Camel-K on Rocky Linux 9 Container" \
      version="2.5.1" \
      io.k8s.display-name="Apache Camel-K on EL9 Container" \
      io.k8s.description="Provides Camel-K on Rocky Linux 9 Container" \
      io.openshift.tags="camel-k rockylinux"

ARG IMAGE_ARCH

ARG MAVEN_DEFAULT_VERSION="3.8.6"
ARG MAVEN_HOME="/usr/share/maven"
ARG MAVEN_DIST_URL="https://archive.apache.org/dist/maven/maven-3/${MAVEN_DEFAULT_VERSION}/binaries/apache-maven-${MAVEN_DEFAULT_VERSION}-bin.zip"
ARG MVNW_DIR="/usr/share/maven/mvnw/"
ARG MVN_REPO="/etc/maven/m2"
ARG MAVEN_OPTS=""

USER 0
RUN dnf -y install java-17-openjdk-headless java-17-openjdk-devel java-21-openjdk-headless java-21-openjdk-devel delve && dnf clean all && rm -rf /var/cache/dnf

RUN echo "SYMLINKING delve to /usr/local/bin/" && ln -s /usr/bin/dlv /usr/local/bin/dlv

# Maven configuration
RUN mkdir -p ${MAVEN_HOME}
RUN mkdir -p ${MVN_REPO}
COPY --from=builder /build/camel-k/build/_maven_overlay/ /usr/share/maven/lib/
COPY --from=builder /build/camel-k/build/_maven_overlay/logback.xml /usr/share/maven/conf/

# Prepare the maven wrapper required in the build Pod strategy
COPY --from=builder /build/camel-k/build/mvnw/mvnw.tar ${MVNW_DIR}
RUN tar -xC ${MVNW_DIR} -f ${MVNW_DIR}mvnw.tar \
    && rm -v ${MVNW_DIR}mvnw.tar \
    && sed -i "s;distributionUrl=.*;distributionUrl=${MAVEN_DIST_URL};" ${MVNW_DIR}.mvn/wrapper/maven-wrapper.properties
# Used by mvnw to download maven dist into it
ENV MAVEN_USER_HOME="${MAVEN_HOME}"
# Install a default mvnw distribution at build time and prepare the config for formatting log
RUN ${MVNW_DIR}/mvnw --version | grep "Maven home:" | sed 's/Maven home: //' >> ${MVNW_DIR}default \
    && cp -r /usr/share/maven/lib/. $(cat ${MVNW_DIR}default)/lib \
    && rm $(cat ${MVNW_DIR}default)/lib/maven-slf4j-provider* \
    && rm $(cat ${MVNW_DIR}default)/lib/slf4j-api-1.* 

ENV MAVEN_OPTS="${MAVEN_OPTS} -Dlogback.configurationFile=${MAVEN_HOME}/conf/logback.xml"

COPY --from=builder /build/camel-k/build/_maven_output ${MVN_REPO}
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
