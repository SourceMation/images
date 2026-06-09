# Rocky Linux 10 base container image packaged by Sourcemation

Rocky Linux 10 is a community-driven, enterprise-grade Linux distribution
maintained by the Rocky Enterprise Software Foundation. It aims for 100% binary
compatibility with RHEL.


## Usage

Run a temporary Rocky Linux 10 container:

```
docker run --rm -it sourcemation/rocky-10:latest
```

## Environment Vars, Ports, Volumes

The image uses the following environment variables:

```
LANG=C.utf8
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

## Contributing and Reporting Issues

Your contributions are valued! Feel free to suggest enhancements or request new
images by opening an issue, or submit your own contributions via pull requests
to the Sourcemation GitHub repository.

- [Creating issues (bugs) and images requests](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)


### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [Sourcemation platform](https://www.sourcemation.com/).

For more information, check out the [overview of Rocky
Linux®](https://rockylinux.org/) page.

### Licenses

Each package license can be listed by running the following command:

```
rpm -qa --qf '%{NAME}-%{VERSION}-%{RELEASE} %{LICENSE}\n'
```
