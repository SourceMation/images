FROM sourcemation/rocky-9:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="servicemix" \
      vendor="Sourcemation" \
      url="https://sourcemation.com"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Apache ServiceMix on EL9 Container" \
      description="Provides Apache ServiceMix on Rocky Linux 9 Container" \
      version="7.0.1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Apache ServiceMix on EL9 Container" \
      io.k8s.description="Provides Apache ServiceMix on Rocky Linux 9 Container" \
      io.openshift.tags="servicemix rockylinux"

ENV SERVICEMIX_RELEASE="7.0.1"
ENV JAVA_HOME="/usr/lib/jvm/jre-1.8.0"

# Apache Software Foundation dev keys: https://downloads.apache.org/servicemix/KEYS
ADD KEYS /

RUN dnf install -y --setopt=install_weak_deps=0 --setopt=tsflags=nodocs gpg hostname procps-ng java-1.8.0-openjdk-headless unzip && dnf clean all &&\
    gpg --import KEYS &&\
    curl -L -o servicemix.zip "https://dlcdn.apache.org/servicemix/servicemix-${SERVICEMIX_RELEASE//.*}/${SERVICEMIX_RELEASE}/apache-servicemix-${SERVICEMIX_RELEASE}.zip" &&\
    curl -L -o servicemix.zip.asc "https://www.apache.org/dist/servicemix/servicemix-${SERVICEMIX_RELEASE//.*}/${SERVICEMIX_RELEASE}/apache-servicemix-${SERVICEMIX_RELEASE}.zip.asc" &&\
    gpg --verify servicemix.zip.asc servicemix.zip &&\
    unzip servicemix.zip -d /opt/ &&\
    mv /opt/apache-servicemix-* /opt/servicemix

RUN echo "servicemix: ${SERVICEMIX_RELEASE}" >> /var/tmp/sourcemation.yml

ENTRYPOINT ["/opt/servicemix/bin/servicemix"]
