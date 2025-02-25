# Helidon packaged by SourceMation

Helidon is a release of libraries for the Java programming language for writing
microservices. This container image provides the essential development
environment for Helidon applications. It is based on Rocky Linux 9 and includes
the following tools:

- Java 21 with development packages
- Java 21 jmods
- Maven 3.8 from the official (provided by the Rocky Linux 9 packaging team)
  `maven:3.8` dnf module
- Helidon CLI 4.10.0

The jmods double the image size, but are necessary for `jlink` custom runtime
creation.

Lastly, the image runs the `helidon` non-root user by default for security
reasons.

## Usage

Example usage with creating a new Helidon project.

Firstly, run the container:

```bash
$ docker run --name helidon-dev-env --rm -it sourcemation/helidon:latest
```

Having a shell in this container, create and start your Helidon project:

```bash
$ helidon --version # returns version build date etc
$ helidon init --name my-helidon-project --package com.example --batch
$ cd my-helidon-project
$ helidon dev
```

Now you can access the application at `http://localhost:8080/` with the
`http://localhost:8080/simple-greet` endpoint enabled (from the inside of the
container).

You can additionally customize your experience by mounting volumes to the
container, using it with your IDE, and exposing ports to the host machine. For
example:

```bash
$ podman run --name helidon-dev-env --rm -it -v $(pwd):/helidon/my-helidon-project -p 8080:8080 sourcemation/helidon:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
JAVA_HOME="/usr/lib/jvm/java-21"
```

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues](https://github.com/SourceMation/containers/issues/new)
[Creating pull
requests](https://github.com/SourceMation/containers/compare)

**Disclaimer:** The `sourcemation/helidon` image is not affiliated with Oracle,
Inc. The respective companies and organisations own the trademarks mentioned in
the offering. The `sourcemation/helidon` image is a separate project and is
maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the SourceMation platform.

For more information, check out the [Getting started with Helidon
CLI](https://helidon.io/docs/v4/about/cli) page.

### Licenses

The base license for the solution (Helidon) is the [Apache License, Version
2.0](https://github.com/helidon-io/helidon/blob/main/LICENSE.txt). The licenses
for each component shipped as part of this image can be found on the image's
appropriate SourceMation entry.
