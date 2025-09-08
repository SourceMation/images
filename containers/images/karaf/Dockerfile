FROM sourcemation/rocky-9:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="apache-karaf" \
      vendor="Linux Polska" \
      url="https://linuxpolska.com/en/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Apache Karaf on EL9 Container" \
      description="Provides Apache Karaf on Rocky Linux 9 Container" \
      version="4.4.7" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Apache Karaf on EL9 Container" \
      io.k8s.description="Provides Apache Karaf on Rocky Linux 9 Container" \
      io.openshift.tags="karaf rockylinux"


RUN dnf -y install java-11-openjdk-headless java-17-openjdk-headless java-21-openjdk-headless && dnf clean all && rm -rf /var/cache/dnf


# Karaf environment variables with PATH
ENV KARAF_INSTALL_PATH /opt
ENV KARAF_HOME $KARAF_INSTALL_PATH/apache-karaf
ENV KARAF_EXEC exec
ENV PATH $PATH:$KARAF_HOME/bin

ENV KARAF_VERSION=4.4.7

RUN cd /opt; \
	curl -LO https://dlcdn.apache.org/karaf/${KARAF_VERSION}/apache-karaf-${KARAF_VERSION}.tar.gz && \
	tar -xzf apache-karaf-${KARAF_VERSION}.tar.gz; \
	mv apache-karaf-${KARAF_VERSION} apache-karaf; \
	rm -f apache-karaf-${KARAF_VERSION}.tar.gz

RUN set -x && \
  ln -s $KARAF_INSTALL_PATH/apache-karaf* $KARAF_HOME

RUN echo "karaf: $KARAF_VERSION" >> /var/tmp/sourcemation.yml

EXPOSE 8101 1099 44444 8181 9999
CMD ["karaf", "run"]
