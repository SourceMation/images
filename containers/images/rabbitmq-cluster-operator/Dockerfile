# Build the manager binary
FROM --platform=$BUILDPLATFORM sourcemation/golang-1.24:latest AS builder

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates

# Dependencies are cached unless we change go.mod or go.sum
COPY go.mod go.mod
COPY go.sum go.sum
RUN go mod download

# Copy the go source
COPY main.go main.go
COPY api/ api/
COPY controllers/ controllers/
COPY internal/ internal/
COPY pkg/ pkg/

# Build
ARG TARGETOS
ARG TARGETARCH
ENV GOOS=$TARGETOS
ENV GOARCH=$TARGETARCH
RUN CGO_ENABLED=0 GO111MODULE=on go build -a -tags timetzdata -o manager main.go

# ---------------------------------------
FROM sourcemation/debian-13-slim:latest AS etc-builder

RUN echo "rabbitmq-cluster-operator:x:1000:" > /etc/group && \
    echo "rabbitmq-cluster-operator:x:1000:1000::/home/rabbitmq-cluster-operator:/usr/sbin/nologin" > /etc/passwd

# ---------------------------------------
FROM scratch

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="rabbitmq-cluster-operator" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="MPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="RabbitMQ Cluster Operator" \
      description="Provides RabbitMQ Cluster Operator" \
      version="2.18.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="RabbitMQ Cluster Operator Container" \
      io.k8s.description="Provides RabbitMQ Cluster Operator Container" \
      io.openshift.tags="rabbitmq-cluster-operator"

WORKDIR /
COPY --from=builder /workspace/manager /usr/local/bin/
COPY --from=etc-builder /etc/passwd /etc/group /etc/
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

ENV APP_NAME="rabbitmq-cluster-operator" \
    APP_VERSION="2.18.0" \
    PATH=/usr/local/bin:$PATH

USER 1000:1000

ENTRYPOINT ["manager"]
