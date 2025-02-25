FROM rockylinux/rockylinux:9

ARG JENKINS_VERSION=2.479.2

# Install basic requirements
RUN dnf update -y &&  \
    dnf install -y --setopt=install_weak_deps=0 --setopt=tsflags=nodocs  fontconfig java-17-openjdk-headless fontconfig freetype git git-lfs unzip which tzdata && \
    dnf clean all


ARG user=jenkins
ARG group=jenkins
ARG uid=1000
ARG gid=1000
ARG http_port=8080
ARG agent_port=50000
ARG JENKINS_HOME=/var/jenkins_home
ARG REF=/usr/share/jenkins/ref
ARG TINI_VERSION=v0.19.0

ENV LANG C.UTF-8
ENV JENKINS_HOME $JENKINS_HOME
ENV JENKINS_SLAVE_AGENT_PORT ${agent_port}
ENV REF $REF
ENV JENKINS_VERSION ${JENKINS_VERSION}

ARG TARGETARCH

LABEL name="jenkins-lts" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Jenkins LTS on EL9 Container with RL9 vanilla openjdk-17" \
      description="Provides Jenkins with RL9 vanilla openjdk-17 on Rocky Linux 9 Container" \
      version="{JENKINS_VERSION}" \
      io.k8s.display-name="Jenkins on EL9 Container with vanillia opejdk" \
      io.k8s.description="Provides Jenkins with RL9 vanilla openjdk-17 on Rocky Linux 9 Container" \
      io.openshift.tags="jenkins rockylinux"

# Changed by init.sh
ARG JENKINS_SHA=177c2c033f0d3ae4148e601d0fdada60112d83f250521f3a0a0fd97cbb138dbd
# Can be used to customize where jenkins.war get downloaded from
ARG JENKINS_URL=https://repo.jenkins-ci.org/public/org/jenkins-ci/main/jenkins-war/${JENKINS_VERSION}/jenkins-war-${JENKINS_VERSION}.war


# uid && gid == 1000
RUN mkdir -p $JENKINS_HOME \
  && chown ${uid}:${gid} $JENKINS_HOME \
  && groupadd -g ${gid} ${group} \
  && useradd -N -d "$JENKINS_HOME" -u ${uid} -g ${gid} -l -m -s /bin/bash ${user}


# Jenkins home directory is a volume, so configuration and build history
# can be persisted and survive image upgrades
VOLUME $JENKINS_HOME


# $REF (defaults to `/usr/share/jenkins/ref/`) contains all reference configuration we want
# to set on a fresh new installation. Use it to bundle additional plugins
# or config file with your custom jenkins Docker image.
RUN mkdir -p ${REF}/init.groovy.d


# Use tini as subreaper in container to adopt zombie processes
COPY tini_pub.gpg "${JENKINS_HOME}/tini_pub.gpg"
RUN curl -fsSL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-static-${TARGETARCH}" -o /sbin/tini \
  && curl -fsSL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-static-${TARGETARCH}.asc" -o /sbin/tini.asc \
  && gpg --no-tty --import "${JENKINS_HOME}/tini_pub.gpg" \
  && gpg --verify /sbin/tini.asc \
  && rm -rf /sbin/tini.asc /root/.gnupg \
  && chmod +x /sbin/tini


# jenkins version being bundled in this docker image


# could use ADD but this one does not check Last-Modified header neither does it allow to control checksum
# see https://github.com/docker/docker/issues/8331
RUN curl -fsSL ${JENKINS_URL} -o /usr/share/jenkins/jenkins.war \
  && echo "${JENKINS_SHA}  /usr/share/jenkins/jenkins.war" >/tmp/jenkins_sha \
  && sha256sum -c --strict /tmp/jenkins_sha \
  && rm -f /tmp/jenkins_sha


ENV JENKINS_UC https://updates.jenkins.io
ENV JENKINS_UC_EXPERIMENTAL=https://updates.jenkins.io/experimental
ENV JENKINS_INCREMENTALS_REPO_MIRROR=https://repo.jenkins-ci.org/incrementals
RUN chown -R ${user} "$JENKINS_HOME" "$REF"

ARG PLUGIN_CLI_VERSION=2.12.15
ARG PLUGIN_CLI_URL=https://github.com/jenkinsci/plugin-installation-manager-tool/releases/download/${PLUGIN_CLI_VERSION}/jenkins-plugin-manager-${PLUGIN_CLI_VERSION}.jar
RUN curl -fsSL ${PLUGIN_CLI_URL} -o /opt/jenkins-plugin-manager.jar

# for main web interface:
EXPOSE ${http_port}

# will be used by attached agents:
EXPOSE ${agent_port}

ENV COPY_REFERENCE_FILE_LOG $JENKINS_HOME/copy_reference_file.log

ENV JAVA_HOME=/usr/lib/jvm/jre-17-openjdk/
ENV PATH "${JAVA_HOME}/bin:${PATH}"


COPY jenkins-support /usr/local/bin/jenkins-support
COPY jenkins.sh /usr/local/bin/jenkins.sh
COPY jenkins-plugin-cli.sh /bin/jenkins-plugin-cli
RUN version=$(jenkins.sh --version | grep -oP "\d+\.\d+\.\d+") &&\
    echo "jenkins: $version"  >> /var/tmp/sourcemation.yml


USER ${user}
ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/jenkins.sh"]
