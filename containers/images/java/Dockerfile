FROM sourcemation/rocky-9:latest

ARG TARGETARCH

LABEL name="java" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Java on EL9 Container" \
      description="Provides Java on Rocky Linux 9 Container" \
      version="21" \
      io.k8s.display-name="Java on EL9 Container" \
      io.k8s.description="Provides Java on Rocky Linux 9 Container" \
      io.openshift.tags="java rockylinux"

RUN dnf module enable maven:3.8 -y && \
    dnf install -y --setopt=tsflags=nodocs --setopt=install_weak_deps=0 --nobest --allowerasing ca-certificates curl procps wget java-21-headless java-21-jmods maven-openjdk21  && \
    dnf update -y && \
    dnf clean all

# Using alternatives to set the default java and javac - javac is already set,
# by maven module but we are setting it again - just to be sure

RUN alternatives --set java java-21-openjdk.$(uname -m) && \
    alternatives --set javac java-21-openjdk.$(uname -m)

ENV JAVA_HOME /usr/lib/jvm/java-21

RUN touch /etc/locale.conf; sed -i 's/^LANG=.*/LANG="en_US.utf8"/' /etc/locale.conf

ENV APP_NAME="java" \
    LANG="en_US.UTF-8" \
    LANGUAGE="en_US:en"

CMD [ "bash" ]
