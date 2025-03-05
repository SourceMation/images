FROM sourcemation/rocky-9

LABEL name="micronaut" \
      vendor="SourceMation" \
      url="https://SourceMation.com/"\
      licenses="Apache-2.0" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Micronaut CLI, Java-21 GraalVM and SDKMAN with GCC on EL9 Container" \
      description="Provides Micronaut CLI, Java-21 GraalVM and SDKMAN with GCC Rocky Linux 9 Container" \
      version="4.7.6" \
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
    sha256sum --check <( echo "4cd75e4e8b1d3e1be5c50a4260db6fbe6b8f1a11afcb942481cb17ab8ba475db sdkman.sh") && \
    bash sdkman.sh && \
    source "/home/micronaut/.sdkman/bin/sdkman-init.sh" && \
    sdk install micronaut 4.7.6 && \
    sdk install java 21.0.4-graal
