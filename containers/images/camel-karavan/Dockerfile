# Build stage
FROM rockylinux/rockylinux:9 AS builder

ADD ee10ba76e3be503a07b7550b09e4d19f8fd25848.asc /
ENV KARAVAN_VERSION="4.7.0"
RUN dnf install -y gpg maven-openjdk17 unzip npm wget && dnf clean all && rm -rf /var/cache/dnf
RUN gpg --import ee10ba76e3be503a07b7550b09e4d19f8fd25848.asc &&\
      mkdir /build &&\
      cd /build &&\
      wget https://github.com/apache/camel-karavan/releases/download/${KARAVAN_VERSION}/camel-karavan-${KARAVAN_VERSION}.zip https://github.com/apache/camel-karavan/releases/download/${KARAVAN_VERSION}/camel-karavan-${KARAVAN_VERSION}.zip.asc &&\
      gpg --verify camel-karavan-${KARAVAN_VERSION}.zip.asc camel-karavan-${KARAVAN_VERSION}.zip &&\
      unzip camel-karavan-${KARAVAN_VERSION}.zip &&\
      cd /build/camel-karavan-${KARAVAN_VERSION} &&\
      mvn clean compile exec:java -Dexec.mainClass="org.apache.camel.karavan.generator.KaravanGenerator" -f karavan-generator &&\
      cd karavan-core &&\
      npm install &&\
      cd  .. &&\
      mvn clean package -f karavan-app -Dquarkus.profile=public

RUN echo "Checking if there is proper jar" && ls -lh "/build/camel-karavan-${KARAVAN_VERSION}/karavan-app/target/karavan-${KARAVAN_VERSION}-runner.jar"

FROM rockylinux/rockylinux:9

LABEL name="camel-karavan" \
      vendor="Linux Polska" \
      url="https://linuxpolska.com/en/"\
      licenses="Apache-2.0" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Apache Camel Karavan on EL9 Container" \
      description="Provides Camel Karavan on Rocky Linux 9 Container" \
      version="4.7.0" \
      io.k8s.display-name="Apache Camel Karavan on EL9 Container" \
      io.k8s.description="Provides Camel Karavan on Rocky Linux 9 Container" \
      io.openshift.tags="camel karavan rockylinux"


RUN dnf -y install java-17-openjdk-headless java-21-openjdk-headless && dnf clean all && rm -rf /var/cache/dnf

ENV JAVA_HOME="/usr/lib/jvm/jre-17-openjdk"
ENV PATH $PATH:"$JAVA_HOME/bin"
ENV JAVA_OPTS="-Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager -XX:-UseG1GC -XX:+UseZGC"
ENV LANG="en_US.UTF-8"
ENV LANGUAGE="en_US:en"
ENV LC_ALL="en_US.UTF-8"
ENV KARAVAN_VERSION="4.7.0"


COPY --from=builder /build/camel-karavan-${KARAVAN_VERSION}/karavan-app/target/karavan-${KARAVAN_VERSION}-runner.jar /opt/app/karavan.jar
# Double grep because there is a lot of component with versions like NUM.NUM.NUM
RUN version=$(java -jar /opt/app/karavan.jar --version | grep -oP 'karavan (\d+)\.(\d+)\.(\d+) on JVM' | grep -oP "(\d+)\.(\d+)\.(\d+)") \
    && echo "camel-karavan: ${version}" >> /var/tmp/sourcemation.yml

EXPOSE 8080
CMD ["java", \
    "--add-modules", "java.se", \
    "--add-exports", "java.base/jdk.internal.ref=ALL-UNNAMED", \
    "--add-opens", "java.base/java.lang=ALL-UNNAMED", \
    "--add-opens", "java.base/java.nio=ALL-UNNAMED", \
    "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED", \
    "--add-opens", "java.management/sun.management=ALL-UNNAMED", \
    "--add-opens", "jdk.management/com.ibm.lang.management.internal=ALL-UNNAMED", \
    "--add-opens", "jdk.management/com.sun.management.internal=ALL-UNNAMED", \
    "-jar", "/opt/app/karavan.jar"]
