# Apache Active MQ Artemis packaged by SourceMation

Apache ActiveMQ® is a message broker with the support for a variety of
industry-standard protocols for a diverse clientele support.

This ActiveMQ distribution is provided by the upstream Apache Software
Foundation packaging team.

## Usage

Run a temporary container with ActiveMQ

```
docker run --rm -P -it sourcemation/activemq:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/apache-activemq/bin"
ACTIVEMQ_INSTALL_PATH="/opt"
ACTIVEMQ_HOME="/opt/apache-activemq"
ACTIVEMQ_CONF="/opt/apache-activemq/conf"
ACTIVEMQ_OPTS_MEMORY="-Xms64M -Xmx1G"
ACTIVEMQ_EXEC="exec"
ACTIVEMQ_OPTS="-Xms64M -Xmx1G -Djava.util.logging.config.file=logging.properties -Djava.security.auth.login.config=/opt/apache-activemq/conf/login.config -Djetty.host=0.0.0.0"
ACTIVEMQ_VERSION="6.1.2"
JAVA_HOME="/usr/lib/jvm/jre-17-openjdk"
```

This image exposes the following ports:

- 1099 : JMX RMI registry
- 1883 : `acceptor` element for MQTT connections
- 5672 : the default port for AMQP 1.0 clients
- 8161 : the default Artemis HTTP server port
- 61613 : `acceptor` element for STOMP connections
- 61614 : `acceptor` element for STOMP over Web Sockets connections
- 61616 : `acceptor` element for every protocol supported by Artemis

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/activemq` image is not affiliated with the
Apache Software Foundation. The respective companies and organisations own the
trademarks mentioned in the offering. The `sourcemation/activemq` image is a
separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

This ActiveMQ distribution is shipped with the OpenJDK 17 and 21 JRE builds
provided by the downstream Rocky Linux 9 packaging team. OpenJDK 17 is being
used as the default JRE. Eclipse Jetty 11.0.X is provided as well.

The Dockerfile in this directory is based on the [upstream
Dockerfile](https://github.com/apache/activemq/blob/main/assembly/src/docker/Dockerfile)
by the Apache Software Foundation (ASF).

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://www.sourcemation.com/).

For more information, check out the [overview of
ActiveMQ®](https://activemq.apache.org/) page.

### Licenses

The base license for the solution (ActiveMQ) is the Apache License 2.0. The
licenses for each component shipped as part of this image can be found on the
image's appropriate SourceMation entry.
