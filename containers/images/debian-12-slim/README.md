# Debian 12 Slim Image by SourceMation

Debian is the most popular, truly independent Linux distribution. It is a
versatile, stable, and secure operating system. Debian is a community-driven
project developed and maintained by a large and growing community of volunteers
from around the world.


## Usage

Run a temporary Debian 12 slim container:

```bash
docker run --rm -it sourcemation/debian-12-slim:latest
```


## Environment Vars, Ports, Volumes

The image uses the following environment variables:

```bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```


## Contributing and Issues

We’d love for you to contribute! You can request new features/images by
creating an issue or submitting a pull request with your contribution to this
image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)


### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [Debian Official Website](https://www.debian.org/).

### Licenses

Each package license can be found in the proper directory, `/usr/share/doc/PACKAGE_NAME/copyright`. For example, you can list the apt package licenses with:

```bash
cat /usr/share/doc/apt/copyright  | grep '^License'
```
