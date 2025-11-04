FROM sourcemation/golang-1.24:latest AS builder

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates

COPY default-credential-updater/go.mod go.mod
COPY default-credential-updater/go.sum go.sum
RUN go mod download

# Copy the go source
COPY default-credential-updater/main.go main.go
COPY default-credential-updater/updater/ updater/

# Build
ARG TARGETOS
ARG TARGETARCH
ENV GOOS=$TARGETOS
ENV GOARCH=$TARGETARCH
ENV CGO_ENABLED=0

RUN go build -o /go/bin/app

FROM scratch

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="rabbitmq-default-user-credential-updater" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="MPL-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="RabbitMQ Default User Credential Updater on Debian 12 Slim Container" \
      description="Provides RabbitMQ Default User Credential Updater on Debian 12 Slim Container" \
      version="1.0.9" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="RabbitMQ Default User Credential Updater on Debian 12 Slim Container" \
      io.k8s.description="Provides RabbitMQ Default User Credential Updater on Debian 12 Slim Container" \
      io.openshift.tags="rabbitmq-default-user-credential-updater debian-12-slim"

COPY --from=builder /go/bin/app/ /usr/local/bin/default-user-credential-updater

ENV APP_NAME="rabbitmq-default-credential-updater" \
    APP_VERSION="1.0.9"

USER 1000:1000
ENTRYPOINT ["default-user-credential-updater"]
