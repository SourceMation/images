FROM sourcemation/jdk-21:latest AS builder

ENV MAVEN_VERSION="3.9.11"
ENV MAVEN_HOME=/usr/share/maven

RUN set -eux; \
  apt-get update \
  && apt-get install -y ca-certificates curl git gnupg dirmngr --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*
RUN set -eux; curl -LO https://dlcdn.apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz \
  && curl -LO https://dlcdn.apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz.asc \
  && export GNUPGHOME="$(mktemp -d)"; \
  for key in 88BE34F94BDB2B5357044E2E3A387D43964143E3 29BEA2A645F2D6CED7FB12E02B172E3E156466E8 6A814B1F869C2BBEAB7CB7271A2A1C94BDE89688 84789D24DF77A32433CE1F079EB80E92EB2135B1; do \
      gpg --batch --keyserver hkps://keyserver.ubuntu.com --recv-keys "$key" ; \
  done; \
  gpg --batch --verify apache-maven-${MAVEN_VERSION}-bin.tar.gz.asc apache-maven-${MAVEN_VERSION}-bin.tar.gz \
  && mkdir -p ${MAVEN_HOME} ${MAVEN_HOME}/ref \
  && tar -xzf apache-maven-${MAVEN_VERSION}-bin.tar.gz -C ${MAVEN_HOME} --strip-components=1 \
  && ln -s ${MAVEN_HOME}/bin/mvn /usr/bin/mvn


FROM sourcemation/jdk-21:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="maven" \
      vendor="SourceMation" \
      url="https://sourcemation.com/"\
      licenses="Multiple licenses" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="Maven with JDK 21 on Debian 13 Slim Container" \
      description="Provides Maven with JDK 21 on Debian 13 Slim Container" \
      version="3.9.11-jdk-21" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="Maven with JDK 21 on Debian 13 Slim Container" \
      io.k8s.description="Provides Maven with JDK 21 on Debian 13 Slim Container" \
      io.openshift.tags="maven jdk jdk-21 debian-13-slim"


RUN apt-get update \
  && apt-get install -y ca-certificates curl git openssh-client --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

ENV MAVEN_HOME=/usr/share/maven

COPY --from=builder ${MAVEN_HOME} ${MAVEN_HOME}
COPY mvn-entrypoint.sh /usr/local/bin/mvn-entrypoint.sh
COPY settings-docker.xml /usr/share/maven/ref/

RUN ln -s ${MAVEN_HOME}/bin/mvn /usr/bin/mvn

ENV MAVEN_VERSION="3.9.11"
ENV USER_HOME_DIR="/root"
ENV MAVEN_CONFIG="$USER_HOME_DIR/.m2"

ENTRYPOINT ["/usr/local/bin/mvn-entrypoint.sh"]
CMD ["mvn"]
