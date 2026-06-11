FROM --platform=$BUILDPLATFORM docker.io/sourcemation/golang-1.26:latest AS builder

WORKDIR /workspace

COPY go.mod go.sum ./
RUN go mod download

COPY cmd/ cmd/
COPY api/ api/
COPY internal/ internal/
COPY pkg/ pkg/
COPY ext/ ext/

ARG TARGETOS
ARG TARGETARCH
ENV GOOS=$TARGETOS
ENV GOARCH=$TARGETARCH

RUN go test -v ./cmd/kyverno-init/... && \
    CGO_ENABLED=0 GO111MODULE=on go build -a -tags timetzdata -o kyvernopre ./cmd/kyverno-init

# Final image
FROM docker.io/sourcemation/debian-13-slim:latest

ARG BUILD_DATE
ARG TARGETARCH
ARG LONGNAME="Kyverno Init Container on Debian 13 Slim"

LABEL name="kyvernopre" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="$LONGNAME" \
      description="Provides $LONGNAME" \
      version="1.18.1" \
      io.k8s.display-name="$LONGNAME" \
      io.k8s.description="Provides $LONGNAME" \
      io.openshift.tags="kyvernopre"

COPY --from=builder /workspace/kyvernopre /usr/local/bin/kyvernopre

ENV APP_NAME="kyvernopre" \
    APP_VERSION="1.18.1" \
    PATH=/usr/local/bin:$PATH

USER 1000:1000

ENTRYPOINT ["/usr/local/bin/kyvernopre"]
