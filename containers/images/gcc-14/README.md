# GCC 14 packaged by SourceMation

This container image delivers the GNU Compiler Collection (GCC) version 14,
providing an immediate environment for compiling projects written in C, C++,
GO, Fortran, and other supported programming languages.

Built upon the foundation of the SourceMation Debian 12 Slim image.


## Usage

To initiate a container with GCC 14 and gain shell access:

```bash
docker run -it sourcemation/gcc-14 /bin/bash
```

For compiling your source code, you can link your project directory into the container:

```bash
docker run -v /path/to/your/project:/app -w /app sourcemation/gcc-14 gcc main.c -o main
```

Here, the `-v` option establishes a mount between your local directory and
`/app` within the container, while `-w` sets `/app` as the active working
directory.


You also have the option to construct a personalized Dockerfile extending this
image:

```dockerfile
FROM sourcemation/gcc-14

# Include your specific files
COPY . /app
WORKDIR /app
RUN gcc main.c -o main

CMD ["./main"]
```

Subsequently, build and execute your tailored image:

```bash
docker build -t my-gcc-app .
docker run -it my-gcc-app
```

## Environment Vars, Ports, Volumes


This image, in its standard configuration, does not define any particular
environment variables, expose any network ports, or necessitate persistent
volumes. Nevertheless, you retain the flexibility to mount volumes for sharing
your project files and build artifacts.

The following environment variables are defined within the image:

```bash
GCC_VERSION="14.2.0" # This may vary based on the precise version
GPG_KEYS="B215C1633BCA0477615F1B35A5B3A004745C015A (...)" # A collection of keys for verifying the GPG signature of the GCC tarball
```

Furthermore, this image employs `dpkg-divert` to rename the original `gcc` and
`g++` executables. They are still present within the system.

```
/usr/bin/gcc.orig
/usr/bin/g++.orig
/usr/bin/gfortran.orig
```

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)


**Disclaimer:** The `sourcemation/gcc-14` image is not affiliated with the GNU
Project. The respective companies and organisations own the trademarks
mentioned in the offering. The `sourcemation/gcc-14` image is a separate
project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

This GCC 14 image is built on a Debian 12 Slim base image, which is a minimal
consistent compilation environment. This image is loosely based on the Docker
official image for `gcc` and is built using a separate, independent SourceMaton
images build chain.

## Image and its components Risk Analysis report

A detailed risk analysis report of the images and their components can be found
on the [SourceMation platform](https://www.sourcemation.com/).

For more information about GCC, check out the [official GCC
website](https://gcc.gnu.org/).

## Licenses

The base license for GCC is the GNU General Public License version 3 with [GCC
Runtime Library Exception](https://www.gnu.org/licenses/gcc-exception-3.1).
