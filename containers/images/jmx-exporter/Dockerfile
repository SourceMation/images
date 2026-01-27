FROM sourcemation/maven:latest AS builder

ARG TARGETARCH
ARG JMX_EXPORTER_VERSION="1.5.0"

WORKDIR /app

RUN git clone --depth 1 --branch ${JMX_EXPORTER_VERSION} https://github.com/prometheus/jmx_exporter.git . \
    && mvn package -DskipTests

FROM sourcemation/jre-21:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="jmx-exporter" \
      vendor="Sourcemation" \
      url="https://sourcemation.com"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="JMX Exporter on JRE 21 Container" \
      description="Provides JMX Exporter on JRE 21 Container" \
      version="1.5.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="JMX Exporter on JRE 21 Container" \
      io.k8s.description="Provides JMX Exporter on JRE 21 Container" \
      io.openshift.tags="jmx-exporter jre-21"

ENV JMX_EXPORTER_VERSION="1.5.0"

WORKDIR /opt/jmx_exporter

# Copy jar from builder
COPY --from=builder /app/jmx_prometheus_standalone/target/jmx_prometheus_standalone-*.jar /opt/jmx_exporter/jmx_prometheus_httpserver.jar
COPY --from=builder /app/jmx_prometheus_javaagent/target/jmx_prometheus_javaagent-*.jar /opt/jmx_exporter/jmx_prometheus_javaagent.jar

USER 1001

ENTRYPOINT ["java", "-jar", "/opt/jmx_exporter/jmx_prometheus_httpserver.jar"]
CMD ["--help"]
