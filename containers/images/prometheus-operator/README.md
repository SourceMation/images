# Prometheus Operator packaged by SourceMation

Prometheus Operator is a Kubernetes native operator that automates the management of Prometheus instances, ServiceMonitors, PrometheusRules, and other monitoring components in Kubernetes clusters.

This Prometheus Operator distribution is provided by the SourceMation packaging team, built on a secure Debian 12 Slim base image with Prometheus Operator.

## Usage

Run a temporary container with Prometheus Operator:

```bash
docker run --rm -it sourcemation/prometheus-operator:latest
```

### Advanced usage examples

Run Prometheus Operator with specific namespaces:

```bash
docker run -d --name prometheus-operator \
  sourcemation/prometheus-operator:latest \
  --namespaces=monitoring,default
```

Run with custom log level and format:

```bash
docker run -d --name prometheus-operator \
  sourcemation/prometheus-operator:latest \
  --log-level=debug \
  --log-format=json
```

Run with resource limits for config reloader:

```bash
docker run -d --name prometheus-operator \
  sourcemation/prometheus-operator:latest \
  --config-reloader-cpu-request=20m \
  --config-reloader-memory-request=100Mi \
  --config-reloader-cpu-limit=50m \
  --config-reloader-memory-limit=200Mi
```

Run with custom base images:

```bash
docker run -d --name prometheus-operator \
  sourcemation/prometheus-operator:latest \
  --prometheus-default-base-image=quay.io/prometheus/prometheus:v2.53.0 \
  --alertmanager-default-base-image=quay.io/prometheus/alertmanager:v0.27.0
```

Run with web interface enabled:

```bash
docker run -d --name prometheus-operator \
  -p 8080:8080 \
  sourcemation/prometheus-operator:latest \
  --web.listen-address=:8080
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

This image does not expose any ports by default. However, you can expose the web interface port:

- **8080** - Web interface and metrics endpoint (when enabled with `--web.listen-address`)

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Command Line Arguments

The Prometheus Operator supports numerous command line arguments for configuration. Here are some of the most commonly used ones:

### Core Configuration

- `--namespaces` - Namespaces to scope the interaction of the Prometheus Operator (allow list)
- `--deny-namespaces` - Namespaces not to scope the interaction of the Prometheus Operator (deny list)
- `--log-level` - Log level to use (all, debug, info, warn, error, none). Default: info
- `--log-format` - Log format to use (logfmt, json). Default: logfmt
- `--cluster-domain` - The domain of the cluster for generating service FQDNs

### Instance Management

- `--prometheus-instance-namespaces` - Namespaces where Prometheus custom resources are watched
- `--prometheus-instance-selector` - Label selector to filter Prometheus Custom Resources
- `--alertmanager-instance-namespaces` - Namespaces where Alertmanager custom resources are watched
- `--alertmanager-instance-selector` - Label selector to filter Alertmanager Custom Resources

### Resource Configuration

- `--config-reloader-cpu-request` - Config Reloader CPU requests. Default: 10m
- `--config-reloader-cpu-limit` - Config Reloader CPU limits. Default: 10m  
- `--config-reloader-memory-request` - Config Reloader memory requests. Default: 50Mi
- `--config-reloader-memory-limit` - Config Reloader memory limits. Default: 50Mi

### Base Images

- `--prometheus-default-base-image` - Prometheus default base image. Default: quay.io/prometheus/prometheus
- `--alertmanager-default-base-image` - Alertmanager default base image. Default: quay.io/prometheus/alertmanager
- `--thanos-default-base-image` - Thanos default base image. Default: quay.io/thanos/thanos

### Web Interface

- `--web.listen-address` - Address to expose metrics and web interface. Default: :8080
- `--web.enable-tls` - Enable TLS for the web server
- `--web.cert-file` - Certificate file for the web server. Default: /etc/tls/private/tls.crt
- `--web.key-file` - Private key file for the web server. Default: /etc/tls/private/tls.key

### Feature Gates

- `--feature-gates` - Feature gates are key=value pairs that describe Prometheus-Operator features
  - `PrometheusAgentDaemonSet` - Enables DaemonSet mode for PrometheusAgent
  - `PrometheusShardRetentionPolicy` - Enables shard retention policy for Prometheus
  - `PrometheusTopologySharding` - Enables zone aware sharding for Prometheus

For a complete list of command line arguments, refer to the [official CLI reference](https://prometheus-operator.dev/docs/platform/operator/).

## Security

This image runs as the `nobody` user (non-root) for enhanced security.

## Kubernetes Deployment

For production deployments in Kubernetes, refer to the [official Prometheus Operator documentation](https://prometheus-operator.dev/docs/getting-started/introduction/) for complete setup guides and YAML manifests.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the SourceMation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/prometheus-operator` image is not affiliated with the Prometheus project or the Cloud Native Computing Foundation. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/prometheus-operator` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [Prometheus Operator documentation](https://prometheus-operator.dev/docs/getting-started/introduction/).

### Licenses

The base license for the solution (Prometheus Operator) is the [Apache License 2.0](https://github.com/prometheus-operator/prometheus-operator/blob/main/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate SourceMation entry](https://www.sourcemation.com/).
