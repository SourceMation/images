FROM sourcemation/golang-1.24:latest AS builder

COPY ./sealed-secrets /sealed-secrets



RUN apt-get update && \
    apt-get install -y make git ca-certificates && \
    cd /sealed-secrets && \
    make all

FROM gcr.io/distroless/static-debian12

LABEL name="sealed-secrets-controller" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="Apache License Version 2.0," \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Sealed Secrets Controller on Debian 12 Distroless image" \
      description="Provides Sealed Secrets Controller on Debian 12 Distroless image" \
      version="v0.30.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Sealed Secrets Controller on Debian 12 Distroless" \
      io.k8s.description="Provides Sealed Secrets Controller on Debian 12 Distroless image" \
      io.openshift.tags="sealed-secrets-controller, controller, debian12, distroless"

USER 1001

# We left TARGETARCH as sealed secret is using arm64/amd64 instead of `arch` or `uname -m` like output
ARG TARGETARCH
COPY --from=builder /sealed-secrets/controller /usr/local/bin/controller

EXPOSE 8080 8081

ENTRYPOINT ["controller"]
