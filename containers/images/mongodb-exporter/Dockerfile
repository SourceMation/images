FROM sourcemation/golang-1.23:latest AS builder

ARG TARGETARCH
ARG MONGODB_EXPORTER_VERSION="v2.35.0"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

# Download source
RUN curl -L "https://github.com/percona/mongodb_exporter/archive/${MONGODB_EXPORTER_VERSION}.tar.gz" -o mongodb_exporter.tar.gz && \
    tar -xzf mongodb_exporter.tar.gz --strip-components=1 && \
    rm mongodb_exporter.tar.gz

# Build
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build -ldflags "-s -w -X main.version=${MONGODB_EXPORTER_VERSION}" -o mongodb_exporter .

FROM sourcemation/debian-13-slim:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="mongodb-exporter" \
      vendor="Sourcemation" \
      url="https://sourcemation.com"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="MongoDB Exporter on Debian 13 Slim Container" \
      description="Provides mongodb-exporter on Debian 13 Slim Container" \
      version="v2.35.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="MongoDB Exporter on Debian 13 Slim Container" \
      io.k8s.description="Provides mongodb-exporter on Debian 13 Slim Container" \
      io.openshift.tags="mongodb-exporter debian-13"

ENV MONGODB_EXPORTER_VERSION="v2.35.0"

RUN apt-get update && apt-get install --no-install-recommends -y ca-certificates && \
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

# Copy binary from builder
COPY --from=builder /app/mongodb_exporter /usr/local/bin/mongodb_exporter

RUN chmod +x /usr/local/bin/mongodb_exporter && \
    groupadd -g 1001 mongodb-exporter && \
    useradd -u 1001 -g mongodb-exporter -m mongodb-exporter

USER 1001
WORKDIR /home/mongodb-exporter/

ENTRYPOINT [ "mongodb_exporter" ]
CMD [ "--help" ]
