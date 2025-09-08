FROM sourcemation/rocky-9:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="openapi-generator-cli" \
      vendor="SourceMation" \
      url="https://SourceMation.com/"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Openapi Generators with CLI, Java-21, Maven 3.8" \
      description="Provides Openapi Generators with CLI, Java-21, Maven 3.8 on Rocky Linux 9 Container" \
      version="7.12.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Openapi Generators with CLI, Java-21, Maven 3.8 on EL9 Container" \
      io.k8s.description="Provides Openapi Generators with CLI, Java-21, Maven 3.8 on Rocky Linux 9 Container" \
      io.openshift.tags="openapi-generator java-21 maven-3.8 rockylinux"

ENV GENERATOR_VERSION=7.12.0

# Install dependencies
RUN dnf module enable -y maven:3.8 && \
    dnf install -y maven-openjdk21 jq -y --setopt=install_weak_deps=0 --setopt=tsflags=nodocs && \
    dnf clean all

# Add appuser user
RUN useradd -ms /bin/bash appuser

COPY 6ec715bc3c95e279daf65531c09c9f4f39ecc176.asc /

# Install the OpenAPI Generator CLI
RUN gpg --import /6ec715bc3c95e279daf65531c09c9f4f39ecc176.asc && \
    mkdir -p /opt/openapi-generator/modules/openapi-generator-cli/target/ && \
    curl -L https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/${GENERATOR_VERSION}/openapi-generator-cli-${GENERATOR_VERSION}.jar -o /opt/openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar && \
    curl -L https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/${GENERATOR_VERSION}/openapi-generator-cli-${GENERATOR_VERSION}.jar.asc -o /opt/openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar.asc && \
    gpg --verify /opt/openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar.asc /opt/openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar && \
    chown -R appuser:appuser /opt/openapi-generator

COPY openapi-generator-cli.sh /usr/bin/openapi-generator-cli

# Switch to appuser
USER appuser
WORKDIR /home/appuser

# Example petstore.yaml demonstration (for usage description in README)
RUN mkdir -p /home/appuser/examples/

COPY petstore.yaml /home/appuser/examples/petstore.yaml

# NOTE: We intentionally omit openapi-generator-cli.sh from the Dockerfile to
# minimize image size by avoiding additional jar downloads. However,
# openapi-generator-cli.sh updates automatically to the latest version, which
# improves security. Even though the script's version might differ from the
# image version (after running), the automatic updates provide a security
# benefit.

RUN echo "openapi-generator: $GENERATOR_VERSION" >> /var/tmp/sourcemation.yml

COPY docker-entrypoint.sh /usr/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["help"]
