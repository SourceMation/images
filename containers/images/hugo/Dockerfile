FROM sourcemation/golang-1.25:latest

ARG BUILD_DATE
ARG TARGETARCH

ENV HUGO_VERSION=0.152.0
ENV DART_SASS_VERSION=1.93.2
ENV PATH="/usr/local/bin/src:${PATH}"

LABEL name="hugo" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      source="https://github.com/Sourcemation/images/issues" \
      licenses="Apache-2.0" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="Hugo (extended+withdeploy) on Debian 12 Slim Container" \
      description="Provides Hugo (extended+withdeploy) on Debian 12 Slim Container" \
      version="0.152.0" \
      io.k8s.display-name="Hugo (extended+withdeploy) on Debian 12 Slim Container" \
      io.k8s.description="Provides Hugo (extended+withdeploy) on Debian 12 Slim Contaner" \
      io.openshift.tags="Hugo debian-12-slim"

ARG NODEJS_INSTALL_SUM=f4198ec5609a209710de3e8b8a527e44be8a4df0ffb02a3fed4e4aef0f25c528

RUN apt-get update && apt-get install -y curl ca-certificates gnupg git gcc g++ \
    && curl -sSL -o /tmp/setup_24.x https://deb.nodesource.com/setup_24.x \
    && echo "${NODEJS_INSTALL_SUM} /tmp/setup_24.x" | sha256sum -c - \
    && bash /tmp/setup_24.x \
    && rm -f /tmp/setup_24.x \
    && apt-get update \
    && apt-get install -y nodejs \
    && apt-get clean \
    && if [ "${TARGETARCH}" = "amd64" ]; then DARTFILEARCH="x64"; else DARTFILEARCH="${TARGETARCH}"; fi \
    && curl -sSL -o /tmp/dart-sass-${DART_SASS_VERSION}-linux-${DARTFILEARCH}.tar.gz https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-${DARTFILEARCH}.tar.gz \
    && tar -xf /tmp/dart-sass-${DART_SASS_VERSION}-linux-${DARTFILEARCH}.tar.gz -C /tmp \
    && cp -r /tmp/dart-sass/* /usr/local/bin \
    && curl -sSL -o /tmp/hugo_extended_withdeploy_${HUGO_VERSION}_linux-${TARGETARCH}.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_withdeploy_${HUGO_VERSION}_linux-${TARGETARCH}.deb \
    && echo "$(curl -sSL https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_checksums.txt | awk -v HUGO_FILE=hugo_extended_withdeploy_${HUGO_VERSION}_linux-${TARGETARCH}.deb '$2 ~ HUGO_FILE {print $1}') /tmp/hugo_extended_withdeploy_${HUGO_VERSION}_linux-${TARGETARCH}.deb" | sha256sum -c - \
    && apt install -y /tmp/hugo_extended_withdeploy_${HUGO_VERSION}_linux-${TARGETARCH}.deb \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/*

WORKDIR /src

EXPOSE 1313

CMD ["hugo", "server", "-D", "--bind", "0.0.0.0"]
