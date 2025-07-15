# Build the manager or agent binary
FROM docker.io/sourcemation/golang-1.23:latest AS builder
ARG BUILDOS
ARG BUILDPLATFORM
ARG BUILDARCH
ARG BUILDVARIANT
ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT
ARG IMG

WORKDIR /workspace
# Copy the Go Modules manifests
COPY redis-operator/go.mod go.mod
COPY redis-operator/go.sum go.sum
# cache deps before building and copying source so that we don't need to re-download as much
# and so that source changes don't invalidate our downloaded layer
RUN apt-get update && apt-get install -y ca-certificates
RUN go mod download

# Copy the go source
COPY redis-operator/cmd/ cmd/
COPY redis-operator/api/ api/
COPY redis-operator/internal/ internal/
COPY redis-operator/mocks/ mocks/

# Build
ARG LDFLAGS="-s -w -X github.com/OT-CONTAINER-KIT/redis-operator/internal/image.operatorImage=${IMG}"
ENV GOOS=$TARGETOS
ENV GOARCH=$TARGETARCH
ENV CGO_ENABLED=0

# Build the unified binary
RUN GO111MODULE=on go build -ldflags "${LDFLAGS}" -a -o operator cmd/main.go

# Use distroless as minimal base image to package the binary
# Refer to https://github.com/GoogleContainerTools/distroless for more details
FROM gcr.io/distroless/static:nonroot
LABEL name="redis-operator" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Redis Operator on Distroless Container" \
      description="Provides Redis Operator on Distroless Container" \
      version="0.21.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Redis Operator on Distroless Container" \
      io.k8s.description="Provides Redis Operator on Distroless Container" \
      io.openshift.tags="redis operator distroless"
WORKDIR /

COPY --from=builder /workspace/operator /operator
USER 65532:65532

ENTRYPOINT ["/operator", "manager"] 
