FROM rockylinux/rockylinux:9

# YOU MUST CHANGE IT MANUALLY HERE AND IN THE LABEL!
ARG QUARKUS_VERSION=3.13.2

LABEL name="quarkus" \
      vendor="SourceMation" \
      url="https://sourcemation.com"\
      licenses="Apache-2.0" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Quarkus development container on RL9" \
      description="Provides Quarkus development container on Rocky Linux 9" \
      version="3.13.2" \
      io.k8s.display-name="Quarkus on EL9 Container" \
      io.k8s.description="Provides Quarkus on Rocky Linux 9" \
      io.openshift.tags="quarkus rockylinux"


RUN useradd -ms /bin/bash quarkus
USER quarkus
WORKDIR /home/quarkus

# Install Quarkus with JBang - Bang bang!
# install jbang
RUN curl -sL https://sh.jbang.dev -o jbang.sh && \
    sha256sum --check <( echo "bae58bd807ac8e18b5d5f8dfae650a4a318a27fb87a31d91a4594863538a95cb jbang.sh" ) && \
    cat jbang.sh | bash -s - app setup

# modify the PATH to include jbang
ENV PATH="/home/quarkus/.jbang/bin:/home/quarkus/.jbang/currentjdk/bin:${PATH}"

# Trust the Quarkus Maven repo and Install Quarkus CLI
RUN mkdir -p /home/quarkus/.local/bin && \
    cd /home/quarkus/.local/bin && \
    jbang trust add https://repo1.maven.org/maven2/io/quarkus/quarkus-cli/ && \
    jbang app install --name quarkus https://repo1.maven.org/maven2/io/quarkus/quarkus-cli/${QUARKUS_VERSION}/quarkus-cli-${QUARKUS_VERSION}-runner.jar

RUN echo "quarkus: ${QUARKUS_VERSION}" >> /var/tmp/sourcemation.yml && \
    jbang_version=$(cat /home/quarkus/.jbang/cache/urls/jbang/version.txt  | grep -oP '^\d+\.\d+\.\d+' ) && \
    echo "jbang: ${jbang_version}" >> /var/tmp/sourcemation.yml

CMD ["/bin/bash"]
