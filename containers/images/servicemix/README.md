# Apache ServiceMix packaged by SourceMation

Apache ServiceMix is an Enterprise Service Bus (ESB), acting as an integration
container that combines various components and functionalities, enabling
organizations to build and manage service-oriented architecture (SOA)
applications effectively.

This image contains the official upstream ServiceMix artifacts provided by
Apache Software Foundation. It is built for SourceMation content delivery and
open source analysis platform.

## Usage

Run a temporary container with ServiceMix (grants the builtin Karaf shell):

```
docker run --rm -it sourcemation/servicemix:latest
```

## Environment Vars, Ports, Volumes

The following environment variables are present:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
SERVICEMIX_RELEASE="7.0.1"
JAVA_HOME="/usr/lib/jvm/jre-1.8.0"
```

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/servicemix` image is not affiliated with the
Apache Software Foundation. The respective companies and organisations own the
trademarks mentioned in the offering. The `sourcemation/servicemix` image is a
separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

The image provides the 1.8.0 OpenJDK JRE release, as newer releases might be
incompatible with ServiceMix. In particular, the `Unrecognized VM option
'UnsyncloadClass'` error might be thrown at startup. See [OpenJDK's issue
tracker](https://bugs.openjdk.org/browse/JDK-8140284) for more details.

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the SourceMation platform.

For more information about ServiceMix, check out the [Apache
ServiceMix](https://servicemix.apache.org/) page.

### Licenses

The base license for the solution (Apache ServiceMix) is the [Apache License,
Version 2.0](https://github.com/apache/servicemix/blob/master/LICENSE). Please
visit that link for a more in-depth information about the licensing of the
third-party components used as part of the upstream product. The licenses for
additional components shipped as part of this image can be found on the image's
appropriate SourceMation entry.
