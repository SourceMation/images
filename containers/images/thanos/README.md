# Thanos packaged by Sourcemation

Thanos is a set of components that can be composed into a highly available metric system with unlimited storage capacity, which can be added seamlessly on top of existing Prometheus deployments. Thanos leverages the Prometheus 2.0 storage format to cost-efficiently store historical metric data in any object storage while retaining fast query latencies.

This Thanos distribution is provided by the Sourcemation packaging team, built on a secure Debian 13 Slim base image with version.

## Usage

Run a temporary container to see available Thanos subcommands:

```bash
docker run --rm -it sourcemation/thanos:latest --help
```

### Core Components and Basic Usage

Thanos consists of multiple components that can be deployed independently. Here are the main components:

#### Sidecar

Run Thanos Sidecar alongside Prometheus:

```bash
docker run --rm -it sourcemation/thanos:latest sidecar --help
```

```bash
docker run -d --name thanos-sidecar \
  -p 10901:10901 -p 10902:10902 \
  -v /path/to/prometheus/data:/prometheus \
  sourcemation/thanos:latest sidecar \
  --tsdb.path=/prometheus \
  --prometheus.url=http://prometheus:9090 \
  --grpc-address=0.0.0.0:10901 \
  --http-address=0.0.0.0:10902
```

#### Query

Run Thanos Query to provide a global query view:

```bash
docker run -d --name thanos-query \
  -p 10904:10904 \
  sourcemation/thanos:latest query \
  --http-address=0.0.0.0:10904 \
  --store=thanos-sidecar:10901 \
  --store=thanos-store:10905
```

#### Store Gateway

Run Thanos Store Gateway to serve metrics from object storage:

```bash
docker run -d --name thanos-store \
  -p 10905:10905 -p 10906:10906 \
  -v /path/to/bucket/config:/etc/thanos \
  sourcemation/thanos:latest store \
  --data-dir=/var/thanos/store \
  --objstore.config-file=/etc/thanos/bucket.yml \
  --grpc-address=0.0.0.0:10905 \
  --http-address=0.0.0.0:10906
```

#### Compactor

Run Thanos Compactor to compact and downsample metrics:

```bash
docker run -d --name thanos-compact \
  -p 10912:10912 \
  -v /path/to/bucket/config:/etc/thanos \
  sourcemation/thanos:latest compact \
  --data-dir=/var/thanos/compact \
  --objstore.config-file=/etc/thanos/bucket.yml \
  --http-address=0.0.0.0:10912 \
  --wait
```

#### Receiver

Run Thanos Receiver for remote write from Prometheus:

```bash
docker run -d --name thanos-receive \
  -p 10907:10907 -p 10908:10908 -p 10909:10909 \
  -v /path/to/bucket/config:/etc/thanos \
  sourcemation/thanos:latest receive \
  --grpc-address=0.0.0.0:10907 \
  --remote-write.address=0.0.0.0:10908 \
  --http-address=0.0.0.0:10909 \
  --objstore.config-file=/etc/thanos/bucket.yml \
  --tsdb.path=/var/thanos/receive
```

#### Ruler

Run Thanos Ruler for recording and alerting rules:

```bash
docker run -d --name thanos-ruler \
  -p 10910:10910 -p 10911:10911 \
  -v /path/to/rules:/etc/thanos/rules \
  -v /path/to/bucket/config:/etc/thanos \
  sourcemation/thanos:latest rule \
  --grpc-address=0.0.0.0:10910 \
  --http-address=0.0.0.0:10911 \
  --rule-file=/etc/thanos/rules/*.yml \
  --objstore.config-file=/etc/thanos/bucket.yml \
  --query=thanos-query:10904
```

### Advanced Usage Examples

Run with custom log level and format:

```bash
docker run -d --name thanos-query \
  -p 10904:10904 \
  sourcemation/thanos:latest query \
  --http-address=0.0.0.0:10904 \
  --store=thanos-sidecar:10901 \
  --log.level=debug \
  --log.format=json
```

Run with tracing enabled:

```bash
docker run -d --name thanos-query \
  -p 10904:10904 \
  sourcemation/thanos:latest query \
  --http-address=0.0.0.0:10904 \
  --store=thanos-sidecar:10901 \
  --tracing.config-file=/etc/thanos/tracing.yml
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

This image exposes the following ports (depending on component):

- **10901** - Sidecar gRPC API
- **10902** - Sidecar HTTP API and web UI
- **10903** - Query gRPC API
- **10904** - Query HTTP API and web UI
- **10905** - Store Gateway gRPC API
- **10906** - Store Gateway HTTP API and web UI
- **10907** - Receiver gRPC API (Store API)
- **10908** - Receiver HTTP API (Remote Write)
- **10909** - Receiver HTTP API and web UI
- **10910** - Ruler gRPC API
- **10911** - Ruler HTTP API and web UI
- **10912** - Compactor HTTP API and web UI
- **10913** - Query Frontend HTTP API and web UI

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Volumes

Common volume mount points:

- **/var/thanos** - Default data directory for various components
- **/etc/thanos** - Configuration files directory
- **/prometheus** - Prometheus TSDB path (for Sidecar)

## Common Command Line Arguments

### Global Arguments

All Thanos components support these common arguments:

- `--log.level` - Log filtering level (debug, info, warn, error) [default: info]
- `--log.format` - Log format to use (logfmt, json) [default: logfmt]
- `--tracing.config-file` - Path to YAML file with tracing configuration
- `--version` - Show application version

### Component-Specific Key Arguments

#### Sidecar
- `--tsdb.path` - Data directory of TSDB
- `--prometheus.url` - URL at which to reach Prometheus's HTTP API
- `--grpc-address` - Listen address for gRPC endpoints
- `--http-address` - Listen address for HTTP endpoints
- `--objstore.config-file` - Path to YAML file for object store configuration

#### Query
- `--http-address` - Listen address for HTTP endpoints
- `--grpc-address` - Listen address for gRPC endpoints
- `--store` - Addresses of statically configured store API servers
- `--store.sd-files` - Path to files that contain addresses of store API servers
- `--query.timeout` - Maximum time to process query
- `--query.replica-label` - Labels to treat as a replica indicator

#### Store Gateway
- `--data-dir` - Data directory for local cache
- `--objstore.config-file` - Path to YAML file for object store configuration
- `--grpc-address` - Listen address for gRPC endpoints
- `--http-address` - Listen address for HTTP endpoints
- `--index-cache.config-file` - Path to YAML file for index cache configuration

#### Compactor
- `--data-dir` - Data directory for compactor cache
- `--objstore.config-file` - Path to YAML file for object store configuration
- `--http-address` - Listen address for HTTP endpoints
- `--wait` - Do not exit after all compactions have been processed
- `--wait-interval` - Wait interval between consecutive compaction runs

#### Receiver
- `--grpc-address` - Listen address for gRPC endpoints (Store API)
- `--remote-write.address` - Address to listen on for remote write requests
- `--http-address` - Listen address for HTTP endpoints
- `--tsdb.path` - Data directory of TSDB
- `--objstore.config-file` - Path to YAML file for object store configuration

#### Ruler
- `--grpc-address` - Listen address for gRPC endpoints
- `--http-address` - Listen address for HTTP endpoints
- `--rule-file` - Path to the rule files
- `--objstore.config-file` - Path to YAML file for object store configuration
- `--query` - Addresses of statically configured query API servers

### Getting Help

To see all available arguments for any component:

```bash
docker run --rm sourcemation/thanos:latest <component> --help
```

For example:
```bash
docker run --rm sourcemation/thanos:latest query --help
docker run --rm sourcemation/thanos:latest sidecar --help
docker run --rm sourcemation/thanos:latest store --help
```

## Object Storage Configuration

Thanos supports various object storage backends. Create a `bucket.yml` configuration file:

### S3 Example:
```yaml
type: S3
config:
  bucket: "thanos-bucket"
  endpoint: "s3.amazonaws.com"
  region: "us-east-1"
  access_key: "ACCESS_KEY"
  secret_key: "SECRET_KEY"
```

### GCS Example:
```yaml
type: GCS
config:
  bucket: "thanos-bucket"
  service_account: |
    {
      "type": "service_account",
      ...
    }
```

## Security

This image runs as the `nobody` user (non-root) for enhanced security. The Thanos binary is located at `/usr/local/bin/thanos` and is executable by all users.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the Sourcemation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/thanos` image is not affiliated with the Thanos project. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/thanos` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [Sourcemation platform](https://www.sourcemation.com/).

For more information, check out the [overview of Thanos](https://thanos.io/tip/thanos/getting-started.md/) page.

### Licenses

The base license for the solution (Thanos) is the [Apache License 2.0](https://github.com/thanos-io/thanos/blob/main/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate Sourcemation entry](https://www.sourcemation.com/).
