# JMX Exporter packaged by Sourcemation

> A process for exposing JMX Beans via HTTP for Prometheus consumption.

This container image contains the JMX Exporter (Java Agent and HTTP Server)
from the Prometheus project.

## Usage

Run a temporary container with the JMX Exporter to see help:

```bash
docker run --rm -it sourcemation/jmx-exporter:latest --help
```

### Advanced usage examples

To run the standalone HTTP server:

```bash
docker run -p 5556:5556 -v $(pwd)/config.yaml:/config.yaml sourcemation/jmx-exporter:latest 5556 /config.yaml
```

To use the Java Agent, you can mount the jar from this image or copy it in a multi-stage build.

```dockerfile
COPY --from=sourcemation/jmx-exporter:latest /opt/jmx_exporter/jmx_prometheus_javaagent.jar /opt/jmx_exporter/
```

## Image tags and versions

The `sourcemation/jmx-exporter` image is based on `sourcemation/jre-21`, the
build is based on the `sourcemation/maven` image.

## Environment Vars, Ports, Volumes

This image exposes the JMX Exporter.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/jmx-exporter` image is not affiliated with
the Prometheus project. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/jmx-exporter` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [Sourcemation platform](https://sourcemation.com).

For more information, check out the [JMX Exporter
documentation](https://github.com/prometheus/jmx_exporter).

### Licenses

The base license for the solution is the Apache 2.0 License.
