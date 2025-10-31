# Grafana packaged by SourceMation

> Grafana is an open-source analytics and interactive visualization web application. It allows you to query, visualize, alert on, and explore your metrics no matter where they are stored.

This Grafana distribution is provided by the upstream Grafana packaging
team.

## Usage

Run a temporary container with the Grafana

```
docker run --rm -it -p 3000:3000 sourcemation/grafana:latest
```

### Advanced usage examples

Run Grafana with persistent storage

```
docker run -d --name grafana \
  -p 3000:3000 \
  -v grafana-data:/usr/share/grafana/data \
  sourcemation/grafana
```

Run with a custom configuration file

```
docker run -d --name grafana \
  -p 3000:3000 \
  -v /path/to/your/grafana.ini:/usr/share/grafana/conf/defaults.ini \
  -v grafana-data:/usr/share/grafana/data \
  sourcemation/grafana
```

## Configuration

The repository includes a sample `grafana.ini` configuration file, which provides a comprehensive starting point for configuring Grafana. It pre-configures some settings such as paths, server options, security defaults, and logging behavior, among others. You can override any setting in this file by mounting your own configuration.

## Image tags and versions

The `sourcemation/grafana` image itself comes in `debian-13` flavor.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
GRAFANA_HOME=/usr/share/grafana
```

This image exposes the following ports: 

- 3000 - Grafana web interface and API

Volumes:

- `/usr/share/grafana/data` - Data directory for Grafana's internal database (SQLite), plugins, and other persistent data.

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/grafana` image is not affiliated with
the Grafana. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/grafana` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://sourcemation.com/).

For more information, check out the [overview of
Grafana](https://grafana.com/grafana/) page.

### Licenses

The base license for the solution (Grafana) is the
[AGPL-3.0 license](https://github.com/grafana/grafana/blob/main/LICENSE). The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/).
