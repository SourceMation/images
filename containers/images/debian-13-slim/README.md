# Debian 13 Trixie Slim Image by SourceMation

Debian is the most popular and trusted base distribution for countless other
projects. It's a cornerstone of the free and open-source software movement.
It's well known for its rock-solid stability and commitment to its users.
Version 13 is the latest stable release, which continues this legacy by
providing updated software packages, better hardware support, and security
enhancements.

The Debian community is well known for its unparalleled commitment to quality
and software reproducibility. The reproducible builds initiative ensures the
supply chain security, transparency, and integrity of the software provided by
the Debian distribution. That's why most of our images are based on Debian.

This image is build from scratch and contains only the essential packages that
are required to run a **slim** version of Debian 13 Trixie container.

## Quick Start

To launch a temporary Debian 13 trixie slim container, execute:

```bash
docker run --rm -it sourcemation/debian-13-slim:latest
```

To use this container as a base image in your own Dockerfile:

```Dockerfile
FROM sourcemation/debian-13-slim:latest
...
... Your instructions here ...
...
```

## Environment Settings, Network Ports, and Storage Volumes

The image utilizes these environment variables:

```bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

The default command is `/bin/bash`.


## Contributing and Reporting Issues

Your contributions are valued! Feel free to suggest enhancements or request new
images by opening an issue, or submit your own contributions via pull requests
to the SourceMation GitHub repository.

- [Creating issues (bugs) and images requests](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

### Security Assessment of the Image and its Components

A comprehensive security analysis report detailing the image and its
constituent packages is accessible on the [SourceMation platform](https://www.sourcemation.com/)

For more information, check out the [Debian Official Website](https://www.debian.org/).

### Package Licenses

License information for each package is located within its respective
directory: `/usr/share/doc/PACKAGE_NAME/copyright`. For example, to view the
licenses for the apt package:

```bash
cat /usr/share/doc/apt/copyright | grep '^License'
```
