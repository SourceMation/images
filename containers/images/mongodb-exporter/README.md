# MongoDB Exporter packaged by Sourcemation

> Prometheus exporter for MongoDB metrics.

This MongoDB Exporter distribution is compiled and packaged by Sourcemation,
based on the upstream Percona MongoDB Exporter source code.

## Usage

Run a temporary container with the MongoDB Exporter

```bash
docker run --rm -it sourcemation/mongodb-exporter:latest --help
```

### Advanced usage examples

To connect to a MongoDB instance:

```bash
docker run -d \
  -p 9216:9216 \
  -e MONGODB_URI=mongodb://user:password@mongo:27017 \
  sourcemation/mongodb-exporter:latest
```

## Image tags and versions

The `sourcemation/mongodb-exporter` image is based on `sourcemation/debian-13-slim` and is compiled from source.

## Environment Vars, Ports, Volumes

This image typically uses `MONGODB_URI` environment variable to connect to MongoDB.
See [MongoDB Exporter Documentation](https://github.com/percona/mongodb_exporter) for details.

This image typically listens on port `9216`.

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/mongodb-exporter` image is not affiliated with
Percona. The respective companies and organisations own the trademarks mentioned in the offering. The
`sourcemation/mongodb-exporter` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation platform](https://sourcemation.com).

For more information, check out the [overview of MongoDB Exporter](https://github.com/percona/mongodb_exporter).

### Licenses

The base license for the solution (MongoDB Exporter) is the Apache 2.0 License.
