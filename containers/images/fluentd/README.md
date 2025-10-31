# Fluentd packaged by SourceMation

Fluentd is an open-source data collector that unifies the data collection and consumption for better use and understanding of data. It allows you to unify data collection and consumption for a better understanding and use of data by providing a unified logging layer.

Built by SourceMation's automation team, this Fluentd distribution is regularly updated to ensure it's current, secure, and compact. It's built on a minimal Debian 13 Slim base image.

## Usage

Run a temporary container with Fluentd:

```bash
docker run --rm -it -p 24224:24224 sourcemation/fluentd:latest
```

Fluentd will be ready to accept log data on port 24224.

### Advanced usage examples

Run Fluentd with persistent configuration:

```bash
docker run -d --name fluentd \
  -p 24224:24224 \
  -v /path/to/your/config/dir:/etc/fluent:Z \
  sourcemation/fluentd:latest
```

Run with custom configuration file:

```bash
docker run -d --name fluentd \
  -p 24224:24224 \
  -v /path/to/your/fluent.conf:/etc/fluent/fluent.conf:Z \
  sourcemation/fluentd:latest \
  -c /etc/fluent/fluent.conf
```

Run with additional command line arguments:

```bash
docker run -d --name fluentd \
  -p 24224:24224 \
  -v /path/to/your/config:/etc/fluent:Z \
  sourcemation/fluentd:latest \
  -c /etc/fluent/fluent.conf \
  -v
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/ruby/bin
```

This image exposes the following ports:

- **24224** - Fluentd forward protocol port

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Volumes

- **/etc/fluent** - Configuration directory for Fluentd

## Default Configuration

The container includes a default Fluentd configuration set up at `/etc/fluent`. You can override this by mounting your own configuration directory or file to this path.

## Security

This image runs as the `nobody` user (non-root) for enhanced security.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the SourceMation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/fluentd` image is not affiliated with the Fluentd project. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/fluentd` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [overview of Fluentd](https://www.fluentd.org/) page.

### Licenses

The base license for the solution (Fluentd) is the [Apache License 2.0](https://github.com/fluent/fluentd/blob/master/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate SourceMation entry](https://www.sourcemation.com/).
