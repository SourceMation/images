# Rocky Linux 9 minimal container image packaged by SourceMation

Rocky Linux 9 is a community-driven, enterprise-grade Linux distribution
maintained by the Rocky Enterprise Software Foundation. It aims for 100% binary
compatibility with RHEL.


## Usage

**MINIMAL IMAGES USES MICRODNF INSTEAD OF DNF/YUM** Please use `microdnf`
instead of `dnf` or `yum` in minimal images.

Run a temporary Rocky Linux 9 container:

```
docker run --rm -it sourcemation/rocky-9:latest
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
to the SourceMation GitHub repository.

- [Creating issues (bugs) and images requests](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)


### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [overview of Rocky
Linux®](https://rockylinux.org/) page.

### Licenses

Each package license can be listed by running the following command:

```
rpm -qa --qf '%{NAME}-%{VERSION}-%{RELEASE} %{LICENSE}\n'
```
