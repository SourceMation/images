# Quarkus packaged by SourceMation

Quarkus is a framework for the Java programming language designed to provide a
first-class support for containerization, creating microservices and running
your applications in a Kubernetes cluster.

This image contains the quarkus-cli JAR provided on the courtesy of the
[maven.org repository](https://repo1.maven.org), and of the
[JBang](https://www.jbang.dev/)'s package manager.

## Usage

Run a temporary container with the Quarkus installation (spawn Bash by
default):

```
docker run --rm -it sourcemation/quarkus:latest
```

Then, follow the example from the [official Getting
Started](https://quarkus.io/guides/getting-started) page.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/home/quarkus/.jbang/bin:/home/quarkus/.jbang/currentjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

## Contributing and Issues

We welcome your contributions! If you have new feature requests, want to report
a bug, or wish to submit a pull request with your code or an image request, you
can do so via the SourceMation GitHub repository for this image.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/SourceMation/images/issues/new/choose)
- [Submit a pull request](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/quarkus` image is not affiliated with Red
Hat, Inc. or the Quarkus community. The respective companies and organisations
own the trademarks mentioned in the offering. The `sourcemation/quarkus` image
is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

Please note that the image contains the JDK distribution (version 17 LTS)
provided by JBang as part of installing the Quarkus JAR, located in the
`/home/quarkus/.jbang/currentjdk/` directory.

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the SourceMation platform.

For more information, check out the [official Quarkus
website](https://quarkus.io/about/).

### Licenses

The base license for the solution (Quarkus) is the [Apache License, Version
2.0](https://github.com/quarkusio/quarkus/blob/main/LICENSE). The licenses for
each component shipped as part of this image can be found on the image's
appropriate SourceMation entry.
