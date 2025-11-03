FROM sourcemation/golang-1.24:latest AS builder

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates

COPY rabbitmq-messaging-topology-operator/go.mod go.mod
COPY rabbitmq-messaging-topology-operator/go.sum go.sum

RUN go mod download

# Copy the go source
COPY rabbitmq-messaging-topology-operator/main.go main.go
COPY rabbitmq-messaging-topology-operator/api/ api/
COPY rabbitmq-messaging-topology-operator/controllers/ controllers/
COPY rabbitmq-messaging-topology-operator/internal/ internal/
COPY rabbitmq-messaging-topology-operator/rabbitmqclient/ rabbitmqclient/

# Build
ARG TARGETOS
ARG TARGETARCH
ARG FIPS_MODE=off

ENV GOOS=$TARGETOS
ENV GOARCH=$TARGETARCH
ENV GOFIPS140=$FIPS_MODE

RUN CGO_ENABLED=0 GO111MODULE=on go build -a -tags timetzdata -o manager main.go

FROM sourcemation/debian-13-slim:latest AS etc-builder

RUN echo "messaging-topology-operator:x:1000:" > /etc/group && \
    echo "messaging-topology-operator:x:1000:1000::/home/messaging-topology-operator:/usr/sbin/nologin" > /etc/passwd

FROM scratch

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="rabbitmq-messaging-topology-operator" \
      vendor="SourceMation" \
      url="https://sourcemation.com" \
      licenses="MPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="RabbitMQ Messaging Topology Operator" \
      description="Provides RabbitMQ Messaging Topology Operator" \
      version="1.18.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="RabbitMQ Messaging Topology Operator Container" \
      io.k8s.description="Provides RabbitMQ Messaging Topology Operator Container" \
      io.openshift.tags="rabbitmq-messaging-topology-operator"

WORKDIR /
COPY --from=builder /workspace/manager /usr/local/bin/
COPY --from=etc-builder /etc/passwd /etc/group /etc/
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

ENV APP_NAME="rabbitmq-messaging-topology-operator" \
    APP_VERSION="1.18.0"

USER 1000:1000
ENTRYPOINT ["manager"]