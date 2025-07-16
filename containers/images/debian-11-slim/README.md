# Debian 11 Bullseye Slim Image by SourceMation

Debian stands as a highly regarded, purely community-driven Linux distribution.
Known for its stability, security, and versatility, it serves as a robust
operating system. The Debian project thrives on the contributions of a global
network of volunteers, ensuring its continuous development and maintenance.


## Quick Start

To launch a transient Debian 11 Bullseye slim container, execute:

```bash
docker run --rm -it sourcemation/debian-11-slim:latest
```

## Environment Settings, Network Ports, and Storage Volumes

The image utilizes these environment variables:

```bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

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
