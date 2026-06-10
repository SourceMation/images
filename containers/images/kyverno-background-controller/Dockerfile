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

RUN go test -v ./cmd/background-controller/...

RUN CGO_ENABLED=0 GO111MODULE=on go build -a -tags timetzdata -o kyverno-background-controller ./cmd/background-controller

# Final image
FROM docker.io/sourcemation/debian-13-slim:latest

ARG BUILD_DATE
ARG TARGETARCH
ARG LONGNAME="Kyverno Background Controller on Debian 13 Slim"

LABEL name="kyverno-background-controller" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="$LONGNAME" \
      description="Provides $LONGNAME" \
      version="1.18.1" \
      io.k8s.display-name="$LONGNAME" \
      io.k8s.description="$LONGNAME" \
      io.openshift.tags="kyverno"

COPY --from=builder /workspace/kyverno-background-controller /usr/local/bin/kyverno-background-controller

ENV APP_NAME="kyverno-background-controller" \
    APP_VERSION="1.18.1" \
    PATH=/usr/local/bin:$PATH

USER 1000:1000

ENTRYPOINT ["/usr/local/bin/kyverno-background-controller"]
