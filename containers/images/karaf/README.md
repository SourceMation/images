# Apache Karaf packaged by SourceMation

Karaf is an OSGi-based application container. Just drop your application to the
relevant deploy directory, and let Karaf take care of the rest. Comes with
batteries included like: shell, remote access, among others.

This Karaf distribution is shipped with the OpenJDK 11, 17 and 21 JRE
builds provided by the downstream Rocky Linux 9 packaging team. OpenJDK
11 is being used as the default JRE.

## Usage

Run a temporary container with:

```
docker run --rm sourcemation/karaf:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/apache-karaf/bin"
KARAF_INSTALL_PATH="/opt"
KARAF_HOME="/opt/apache-karaf"
KARAF_EXEC="exec"
KARAF_VERSION="XXX - set during build"
```

Please note that this image does **not** have the `JAVA_HOME` variable
set.

This image exposes the following ports:

- 1099 : JMX RMI registry
- 8101 : connection to console via SSH (Note: needs
  "/opt/apache-karaf/etc/users.properties" to be edited according to
  user's requirements)
- 8181 : Apache Karaf WebContainer (not installed by default)
- 44444 : JMX RMI server
- 9999 : JMXMP (Java Management Extensions Message Protocol)

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues


We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/karaf` image is not affiliated with
the Apache Software Foundation (ASF). The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/karaf` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation platform](https://sourcemation.com).

For more information, check out the [overview of
Karaf](https://karaf.apache.org/) page.

### Licenses

The base license for the solution (Karaf) is the Apache License, Version
2.0. The licenses for each component shipped as part of this image can
be found on the image's appropriate SourceMation entry.

The Dockerfile in this directory is based on the [upstream
Dockerfile](https://github.com/apache/karaf/blob/efdf64d27afddcfa04e15916aba11581e5acfab4/assemblies/docker/Dockerfile)
by the Apache Software Foundation (ASF).

