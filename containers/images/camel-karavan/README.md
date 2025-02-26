# Apache Camel-Karavan packaged by SourceMation

Karavan is a suite for cloud-related development, aimed to help visualize
integration processes and patterns, as well as deploy images directly to
Kubernetes.

This Karavan distribution is provided by the upstream Karavan packaging team.

## Usage

Run a temporary container with Karavan (note the forwarded port, and the
mounted Docker socket):

```
docker run -p 8080:8080 --rm -v /var/run/docker.sock:/var/run/docker.sock -it sourcemation/camel-karavan:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/jvm/jre-17-openjdk/bin"
JAVA_HOME="/usr/lib/jvm/jre-17-openjdk",
JAVA_OPTS="-Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager -XX:-UseG1GC -XX:+UseZGC"
LANG="en_US.UTF-8"
LANGUAGE="en_US:en"
LC_ALL="en_US.UTF-8"
KARAVAN_VERSION="4.7.0"
```

This image exposes the following ports: 

- 8080 : the default port for the Karavan dashboard

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues](https://github.com/SourceMation/containers/issues/new)
[Creating pull
requests](https://github.com/SourceMation/containers/compare)

**Disclaimer:** The `sourcemation/camel-karavan` image is not affiliated with
the Apache Software Foundation (ASF). The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/camel-karavan` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

This Karavan distribution is shipped with the OpenJDK 17 and 21 JRE builds
provided by the downstream Rocky Linux 9 packaging team. OpenJDK 17 is being
used as the default JRE.

The Dockerfile in this directory is based on the [upstream Dockerfile for
Karavan version
4.7.0](https://github.com/apache/camel-karavan/blob/4.7.0/karavan-app/src/main/docker/Dockerfile)
by the Apache Software Foundation (ASF).

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the SourceMation platform.

For more information, check out the [Karavan entries on
apache.org](https://camel.apache.org/categories/Karavan/).

### Licenses

The base license for the solution (Karavan) is the [Apache License Version
2.0](https://github.com/apache/camel-karavan/blob/main/LICENSE.txt). The
licenses for each component shipped as part of this image can be found on the
image's appropriate SourceMation entry.
