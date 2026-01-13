FROM sourcemation/rocky-9:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="helidon" \
      vendor="Sourcemation" \
      url="https://Sourcemation.com/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Helidon with OpenJDK 21 and Maven 3.8 on EL9 Container" \
      description="Provides Helidon with OpenJDK 21 and Maven 3.8 on Rocky Linux 9 Container" \
      version="4.1.6" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Helidon with OpenJDK 21 and Maven 3.8 on EL9 Container" \
      io.k8s.description="Provides Helidon with OpenJDK 21 and Maven 3.8 on Rocky Linux 9 Container" \
      io.openshift.tags="helidon java maven rockylinux"

RUN dnf module enable maven:3.8 -y && \
    dnf install -y --setopt=tsflags=nodocs --setopt=install_weak_deps=0 --nobest --allowerasing java-21-headless java-21-jmods maven-openjdk21  && \
    dnf update -y && \
    dnf clean all

# Using alternatives to set the default java and javac - javac is already set,
# by maven module but we are setting it again - just to be sure

RUN alternatives --set java "java-21-openjdk.$(uname -m)" && \
    alternatives --set javac "java-21-openjdk.$(uname -m)"

ENV JAVA_HOME /usr/lib/jvm/java-21

# Install helidon binary
RUN curl -L -O https://helidon.io/cli/latest/linux/helidon && chmod +x helidon && mv helidon /usr/bin

RUN version=$(helidon --version | grep 'default.helidon.version' | grep -oP '(\d+\.\d+\.\d+)') && \
    echo "helidon: $version" >> /var/tmp/sourcemation.yml

# Add application user
RUN useradd -ms /bin/bash helidon
USER helidon

WORKDIR /home/helidon

EXPOSE 8080

CMD ["/bin/bash"]
