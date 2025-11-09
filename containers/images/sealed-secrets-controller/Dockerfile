FROM sourcemation/golang-1.25:latest AS builder

COPY ./sealed-secrets /sealed-secrets



RUN apt-get update && \
    apt-get install -y make git ca-certificates && \
    cd /sealed-secrets && \
    make all

FROM gcr.io/distroless/static-debian13

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="sealed-secrets-controller" \
      vendor="Sourcemation" \
      url="https://sourcemation.com/"\
      licenses="Apache License Version 2.0," \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Sealed Secrets Controller on Debian 13 Distroless image" \
      description="Provides Sealed Secrets Controller on Debian 13 Distroless image" \
      version="v0.33.1" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Sealed Secrets Controller on Debian 13 Distroless" \
      io.k8s.description="Provides Sealed Secrets Controller on Debian 13 Distroless image" \
      io.openshift.tags="sealed-secrets-controller, controller, debian12, distroless"

USER 1001

# We left TARGETARCH as sealed secret is using arm64/amd64 instead of `arch` or `uname -m` like output
ARG TARGETARCH
COPY --from=builder /sealed-secrets/controller /usr/local/bin/controller

EXPOSE 8080 8081

ENTRYPOINT ["controller"]
