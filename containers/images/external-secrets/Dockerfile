FROM sourcemation/golang-1.24:latest AS builder

ARG TARGETOS
ARG TARGETARCH
ENV CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH}

COPY ./external-secrets /external-secrets

RUN apt-get update && \
    apt-get install -y ca-certificates && \
    cd /external-secrets && \
    go mod download && \
    go build -o external-secrets main.go


FROM gcr.io/distroless/static-debian12

LABEL name="external-secrets" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="Apache License Version 2.0," \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="External Secrets Controller on Debian 12 Distroless image" \
      description="Provides External Secrets Controller on Debian 12 Distroless image" \
      version="v0.19.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="External Secrets Controller on Debian 12 Distroless" \
      io.k8s.description="Provides External Secrets Controller on Debian 12 Distroless image" \
      io.openshift.tags="external-secrets-controller, controller, debian12, distroless"

# nobody
USER 65534

COPY --from=builder /external-secrets/external-secrets /bin/external-secrets

ENTRYPOINT ["/bin/external-secrets"]
