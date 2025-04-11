# GCC 15 packaged by SourceMation

This container image delivers the GNU Compiler Collection (GCC) version 15,
supplying an immediate environment for compiling projects written in C, C++,
GO, D, Fortran, and other supported programming languages. This image is built
upon an unstable snapshot of GCC, as an official 15 release is not yet
available.

Built upon the foundation of the SourceMation Debian 12 Slim image.

**Security Note**: This image is built from a snapshot of GCC 15, which is not
signed! The snapshot is taken from the official GCC Mirror with an HTTPS
connection but without GPG signature verification, as they are unavailable.

Note that that rust compiler that is experimental requires:

```bash
GCCRS_EXTRA_ARGS="-frust-incomplete-and-experimental-compiler-do-not-use"
```
or 
```bash
gccrs -frust-incomplete-and-experimental-compiler-do-not-use ...
```

## Usage

To start a container with GCC 15 and gain shell access:

```bash
docker run -it sourcemation/gcc-15 /bin/bash
```

For compiling your source code, you can link your project directory into the
container:

```bash
docker run -v {/path/to/your/project}:/app -w /app sourcemation/gcc-15 gcc main.c -o main
```

Here, the `-v` option establishes a mount between your local directory and
`/app` within the container, while `-w` sets `/app` as the active working
directory.

You also have the option to construct a personalized Dockerfile extending this
image:

```dockerfile
FROM sourcemation/gcc-15
Include your specific files

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
your project files and building artefacts.

The following environment variables are defined within the image:

```bash
GCC_VERSION="01012025" # This may vary based on the precise snapshot
# A collection of keys for verifying the GPG signature of the GCC tarball - not used for snapshot
GPG_KEYS="B215C1633BCA0477615F1B35A5B3A004745C015A (...)" ```

Furthermore, this image employs dpkg-divert to rename the original gcc and g++
executables. They are still present within the system.

```
/usr/bin/gcc.orig
/usr/bin/g++.orig
/usr/bin/gfortran.orig
```

## Contributing and Issues

We’d love for you to contribute! You can request new features/images by
creating an issue or submitting a pull request with your contribution to this
image on the SourceMation GitHub repository.

- [Creating issues and image requests](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/gcc-15` image is not affiliated with the GNU
Project. The respective companies and organisations own the trademarks
mentioned in the offering. The sourcemation/gcc-15 image is a separate project
and is maintained by SourceMation.

## Extra notes

This GCC 15 image is built on a Debian 12 Slim base image, which is a minimal
consistent compilation environment. This image is loosely based on the Docker
official image for gcc and is built using a separate, independent SourceMaton
images build chain.

## Image and its components Risk Analysis report

The Sourcemation platform provides a detailed risk analysis report of the
images and their components. However, some images might not have them ready;
you can always create an issue to request them.


For more information about GCC, visit the [official GCC
website](https://gcc.gnu.org/).

## Licenses

The base license for GCC is the GNU General Public License version 3 with [GCC
Runtime Library Exception](https://www.gnu.org/licenses/gcc-exception-3.1).
