FROM sourcemation/debian-13-slim:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="kubectl" \
      vendor="Sourcemation" \
      url="https://sourcemation.com"\
      licenses="Apache-2.0" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Kubectl on Debian 13 Slim Container" \
      description="Provides kubectl on Debian 13 Slim Container" \
      version="v1.35.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Kubectl on Debian 13 Slim Container" \
      io.k8s.description="Provides kubectl on Debian 13 Slim Container" \
      io.openshift.tags="kubectl debian-13"

ENV KUBECTL_VERSION="v1.35.0"

RUN apt-get update && apt-get install --no-install-recommends -y ca-certificates curl gettext git jq procps  && \
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

# Install kubectl setup the dirs, user and perms
RUN curl -Lo /usr/local/bin/kubectl "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${TARGETARCH}/kubectl" && \
    curl -Lo /usr/local/bin/kubectl.sha256 "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${TARGETARCH}/kubectl.sha256" && \
    cd /usr/local/bin && \
    echo "$(cat kubectl.sha256) kubectl" | sha256sum --check && \
    rm kubectl.sha256 && \
    chmod +x /usr/local/bin/kubectl && \
    groupadd -g 1001 kubectl && \
    useradd -u 1001 -g kubectl -m kubectl && \
    mkdir -p /home/kubectl/.kube && \
    chown -R kubectl:kubectl /home/kubectl/.kube

USER 1001

VOLUME ["/home/kubectl/.kube"]
WORKDIR /home/kubectl/


ENTRYPOINT [ "kubectl" ]
CMD [ "--help" ]
