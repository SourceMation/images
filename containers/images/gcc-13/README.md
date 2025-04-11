# GCC 13 packaged by SourceMation

This image provides the GNU Compiler Collection (GCC) version 13. It's ready to
compile your C, C++, Fortran, and other supported languages right out
of the container.

This image is built on top of SourceMation Debian 12 Slim image:

```dockerfile
from sourcemation/debian:12-slim
(...)
```

## Usage

To run a container with GCC 13 and access a shell:

```bash
docker run -it sourcemation/gcc-13 /bin/bash
```

To compile your code, you can mount your project directory into the container:

```bash
docker run -v /path/to/your/project:/app -w /app sourcemation/gcc-13 gcc main.c -o main
```

Where the `-v` flag mounts your local directory to `/app` in the container, and
`-w` sets the working directory to `/app`.


You can also create a custom Dockerfile to extend this image:

```dockerfile
FROM sourcemation/gcc-13

# Add your custom files
COPY . /app
WORKDIR /app
RUN gcc main.c -o main

CMD ["./main"]
```

Then build and run your custom image:

```bash
docker build -t my-gcc-app .
docker run -it my-gcc-app
```

## Environment Vars, Ports, Volumes

This image doesn't define any specific environment variables, expose ports, or
require persistent volumes for basic usage. You can, however, mount volumes to
share your source code and build output.

There are the following variables defined in the image:

```bash
GCC_VERSION="13.3.0" # this might change depending on exact version
GPG_KEYS="B215C1633BCA0477615F1B35A5B3A004745C015A (...)" # It's set of keys that can be used to verify the GPG signature of the GCC tarball
```

This image also uses `dpkg-divert` to mask the original `gcc` and `g++`
binaries. They still exist in the system.

```
/usr/bin/gcc.orig
/usr/bin/g++.orig
/usr/bin/gfortran.orig
```

## Contributing and Issues

We’d love for you to contribute! You can request new features by creating an
issue or submitting a pull request with your contribution to this image on the
SourceMation GitHub repository.

- [Creating issues and image requests](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)


**Disclaimer:** The `sourcemation/gcc-13` image is not affiliated with the GNU
Project. The respective companies and organisations own the trademarks
mentioned in the offering. The `sourcemation/gcc-13` image is a separate
project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

This GCC 13 image is built on a stable Linux distribution to provide a
consistent compilation environment. This image is loosely based on the Docker
official image for `gcc` and is built using a separate, independent SourceMaton
images build chain.

## Image and its components Risk Analysis report

A detailed risk analysis report of the images and their components can be found
on the [SourceMation platform](https://www.sourcemation.com/).

For more information about GCC, check out the [official GCC website](https://gcc.gnu.org/).

## Licenses

The base license for GCC is the GNU General Public License version 3 with [GCC
Runtime Library Exception](https://www.gnu.org/licenses/gcc-exception-3.1).
