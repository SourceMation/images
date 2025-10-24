# Memcached packaged by SourceMation

> Memcached is a high-performance, distributed memory object caching system, designed to speed up dynamic web applications by alleviating database load.

This Memcached distribution has been compiled using the source code provided by the Memcached packaging team.

## Usage

Run a temporary container with Memcached:

```bash
docker run --rm -it sourcemation/memcached --help
```

### Advanced usage examples

Run Memcached with custom memory limit (256MB):
```bash
docker run --rm -p 11211:11211 sourcemation/memcached -m 256
```

Run Memcached with multiple connections:
```bash
docker run --rm -p 11211:11211 sourcemation/memcached:debian-12 memcached -c 1024
```

Run Memcached with SASL authentication enabled:
```bash
docker run --rm -p 11211:11211 sourcemation/memcached:debian-12 memcached -S
```

## Image tags and versions

The `sourcemation/memcached` image comes in the `debian-12` flavor based on Debian 12 Slim. The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image exposes the following ports: 

- `11211` - Default Memcached port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/memcached` image is not affiliated with
the Memcached project or Danga Interactive. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/memcached` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://sourcemation.com/catalog/memcached).

For more information, check out the [overview of
Memcached](https://memcached.org/) page.

### Licenses

The base license for the solution (Memcached) is the
[BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause). The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/catalog/memcached).
