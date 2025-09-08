FROM sourcemation/rocky-9

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="micronaut" \
      vendor="SourceMation" \
      url="https://SourceMation.com/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Micronaut CLI, Java-21 GraalVM and SDKMAN with GCC on EL9 Container" \
      description="Provides Micronaut CLI, Java-21 GraalVM and SDKMAN with GCC Rocky Linux 9 Container" \
      version="4.7.6" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Micronaut CLI, Java-21 GraalVM and SDKMAN with GCC on EL9 Container" \
      io.k8s.description="Provides Micronaut CLI, Java-21 GraalVM and SDKMAN with GCC on Rocky Linux 9 Container" \
      io.openshift.tags="micronaut java-21 sdkman gcc rockylinux"

# Install dependencies
RUN dnf install -y zip unzip which gcc zlib-devel git glibc-devel && \
    dnf clean all

# Add Micronaut user
RUN useradd -ms /bin/bash micronaut

# Switch to Micronaut user
USER micronaut
WORKDIR /home/micronaut

EXPOSE 8080

# Install the SDKMAN, grallvm and micronaut
RUN curl -s "https://get.sdkman.io" -o sdkman.sh &&\
    sha256sum --check <( echo "2775b4d5d331f8ba9ba598e90ee77945e047857d760820c7399d3ac6f9af58e3 sdkman.sh") && \
    bash sdkman.sh && \
    source "/home/micronaut/.sdkman/bin/sdkman-init.sh" && \
    sdk install micronaut 4.8.0 && \
    sdk install java 21.0.6-graal
