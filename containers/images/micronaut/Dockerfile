FROM sourcemation/rocky-9

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="micronaut" \
      vendor="Sourcemation" \
      url="https://Sourcemation.com/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Micronaut CLI, Java-25 GraalVM and SDKMAN with GCC on EL9 Container" \
      description="Provides Micronaut CLI, Java-25 GraalVM and SDKMAN with GCC Rocky Linux 9 Container" \
      version="5.2.2" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Micronaut CLI, Java-25 GraalVM and SDKMAN with GCC on EL9 Container" \
      io.k8s.description="Provides Micronaut CLI, Java-25 GraalVM and SDKMAN with GCC on Rocky Linux 9 Container" \
      io.openshift.tags="micronaut java-25 sdkman gcc rockylinux"

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
    sha256sum --check <( echo "151a6fa9494053deda70ae54f93c2edf43716ddf0da2a1033c1d65a19a24b78e sdkman.sh") && \
    bash sdkman.sh && \
    . "/home/micronaut/.sdkman/bin/sdkman-init.sh" && \
    sdk install micronaut 5.2.2 && \
    sdk install java 25.4.4+1-graal
