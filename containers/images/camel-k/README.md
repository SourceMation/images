# Apache Camel-K packaged by SourceMation

Camel-K is an Integration Toolkit for Apache Camel aimed to increase the
scope of Camel components and patterns, like Camel DSL, for Kubernetes
integration scenarios, mainly serverless and microservice-based ones.

This Camel-K distribution is a proprietary compilation provided by the
[SourceMation](https://sourcemation.com) packaging team.

## Usage

Let's run a temporary container with Camel-K. Log in to your cluster first
(with `kubectl` or `oc`), then run the following:

```
$ echo 'from('timer:tick?period=3000')
  .setBody().constant('Hello world from Camel K')
  .to('log:info')' > helloworld.groovy

$ docker run --rm -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/camel-k:latest kamel run helloworld.groovy
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
MAVEN_USER_HOME="/usr/share/maven"
MAVEN_OPTS=" -Dlogback.configurationFile=/usr/share/maven/conf/logback.xml"
```

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/camel-k` image is not affiliated with the
Apache Software Foundation (ASF). The respective companies and organisations
own the trademarks mentioned in the offering. The `sourcemation/camel-k` image
is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

This Camel-K distribution is shipped with the OpenJDK 17 and 21 JRE builds
provided by the downstream Rocky Linux 9 packaging team. OpenJDK 17 is being
used as the default JRE with Maven preconfigured to use it.

The application runs as the unnamed system user UID 1001 belonging to the group
GID 0 (root).

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the SourceMation platform.

For more information, check out the [Camel-K Introduction page entries on
apache.org](https://camel.apache.org/camel-k/2.3.x/index.html).

### Licenses

The base license for the solution (Camel-K v2.3.3) is the [Apache License
Version 2.0](https://github.com/apache/camel-k/blob/v2.3.3/LICENSE). The
licenses for each component shipped as part of this image can be found on the
image's appropriate SourceMation entry.
