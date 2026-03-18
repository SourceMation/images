FROM sourcemation/rocky-9

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="micronaut" \
      vendor="Sourcemation" \
      url="https://Sourcemation.com/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Micronaut CLI, Java-21 GraalVM and SDKMAN with GCC on EL9 Container" \
      description="Provides Micronaut CLI, Java-21 GraalVM and SDKMAN with GCC Rocky Linux 9 Container" \
      version="4.10.10" \
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
    sha256sum --check <( echo "65a794a9a052d5688a3a8eef9562f2405e714dc71f571ef9feb144699d3ba4ac sdkman.sh") && \
    bash sdkman.sh && \
    . "/home/micronaut/.sdkman/bin/sdkman-init.sh" && \
    sdk install micronaut 4.10.10 && \
    sdk install java 21.0.10-graal
