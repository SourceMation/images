FROM sourcemation/rocky-9:latest

LABEL name="apache-activemq" \
      vendor="Linux Polska" \
      url="https://linuxpolska.com/en/"\
      licenses="Apache-2.0" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Apache ActiveMQ on EL9 Container" \
      description="Provides Apache ActiveMQ on Rocky Linux 9 Container" \
      version="6.1.5" \
      io.k8s.display-name="Apache ActiveMQ on EL9 Container" \
      io.k8s.description="Provides Apache ActiveMQ on Rocky Linux 9 Container" \
      io.openshift.tags="activemq rockylinux"


RUN dnf -y install java-17-openjdk-headless java-21-openjdk-headless && dnf clean all && rm -rf /var/cache/dnf


# ActiveMQ environment variables
ENV ACTIVEMQ_INSTALL_PATH /opt
ENV ACTIVEMQ_HOME $ACTIVEMQ_INSTALL_PATH/apache-activemq
ENV ACTIVEMQ_CONF $ACTIVEMQ_HOME/conf
ENV ACTIVEMQ_OPTS_MEMORY -Xms64M -Xmx1G
ENV ACTIVEMQ_EXEC exec
ENV PATH $PATH:$ACTIVEMQ_HOME/bin
# Make the Web console accesible from outside the container
ENV ACTIVEMQ_OPTS $ACTIVEMQ_OPTS_MEMORY -Djava.util.logging.config.file=logging.properties -Djava.security.auth.login.config=$ACTIVEMQ_CONF/login.config -Djetty.host=0.0.0.0
#WORKDIR $ACTIVEMQ_HOME
ENV ACTIVEMQ_VERSION=6.1.5
ENV JAVA_HOME=/usr/lib/jvm/jre-17-openjdk


RUN cd /opt && \
    curl -LO https://dlcdn.apache.org/activemq/${ACTIVEMQ_VERSION}/apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz && \
    tar -xzf apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz &&\
    mv apache-activemq-${ACTIVEMQ_VERSION} apache-activemq && \
    rm -f apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz

RUN version=$(activemq --version | grep -oP 'ActiveMQ \d+\.\d+\.\d+' | grep -oP '\d+\.\d+\.\d+') && echo "activemq: $version" >> /var/tmp/sourcemation.yml

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

EXPOSE 8161 61616 5672 61613 1883 61614 1099
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["activemq", "console"]
