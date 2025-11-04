# Prometheus packaged by Sourcemation

Prometheus is an open-source monitoring system and time series database that collects metrics from configured targets at given intervals, evaluates rule expressions, displays the results, and can trigger alerts when specified conditions are observed.

This Prometheus distribution is provided by the Sourcemation packaging team, built on a secure Debian 12 Slim base image with version 3.5.0.

## Usage

Run a temporary container with Prometheus:

```bash
docker run --rm -it -p 9090:9090 sourcemation/prometheus:latest
```

The Prometheus web interface will be available at [http://localhost:9090](http://localhost:9090).

### Advanced usage examples

Run Prometheus with persistent storage:

```bash
docker run -d --name prometheus \
  -p 9090:9090 \
  -v /path/to/your/data:/prometheus \
  sourcemation/prometheus:latest
```

Run with custom configuration file:

```bash
docker run -d --name prometheus \
  -p 9090:9090 \
  -v /path/to/your/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v /path/to/your/data:/prometheus \
  sourcemation/prometheus:latest
```

Run with additional command line arguments:

```bash
docker run -d --name prometheus \
  -p 9090:9090 \
  -v /path/to/your/data:/prometheus \
  sourcemation/prometheus:latest \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.console.libraries=/usr/share/prometheus/console_libraries \
  --web.console.templates=/usr/share/prometheus/consoles \
  --storage.tsdb.retention.time=15d \
  --web.enable-lifecycle
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

This image exposes the following ports: 

- **9090** - Prometheus web interface and API

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Volumes

- **/prometheus** - Data directory for time series database storage

## Default Configuration

The container includes a default `prometheus.yml` configuration file located at `/etc/prometheus/prometheus.yml`. You can override this by mounting your own configuration file to this path.

## Security

This image runs as the `nobody` user (non-root) for enhanced security. The data directory `/prometheus` is writable by the nobody group.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the Sourcemation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/prometheus` image is not affiliated with the Prometheus project. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/prometheus` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [Sourcemation platform](https://www.sourcemation.com/).

For more information, check out the [overview of Prometheus](https://prometheus.io/) page.

### Licenses

The base license for the solution (Prometheus) is the [Apache License 2.0](https://github.com/prometheus/prometheus/blob/main/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate Sourcemation entry](https://www.sourcemation.com/).
