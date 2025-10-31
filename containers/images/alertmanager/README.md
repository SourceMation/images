# Alertmanager packaged by SourceMation

Alertmanager is a component of the Prometheus monitoring system that handles alerts sent by client applications such as the Prometheus server. It takes care of deduplicating, grouping, and routing them to the correct receiver integrations such as email, PagerDuty, or OpsGenie. It also takes care of silencing and inhibition of alerts.

This Alertmanager distribution is provided by the SourceMation packaging team, built on a secure Debian 13 Slim base image with version 0.28.1.

## Usage

Run a temporary container with Alertmanager:

```bash
docker run --rm -it -p 9093:9093 sourcemation/alertmanager:latest
```

The Alertmanager web interface will be available at [http://localhost:9093](http://localhost:9093).

### Advanced usage examples

Run Alertmanager with persistent storage:

```bash
docker run -d --name alertmanager \
  -p 9093:9093 \
  -v /path/to/your/data:/alertmanager \
  sourcemation/alertmanager:latest
```

Run with custom configuration file:

```bash
docker run -d --name alertmanager \
  -p 9093:9093 \
  -v /path/to/your/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  -v /path/to/your/data:/alertmanager \
  sourcemation/alertmanager:latest
```

Run with additional command line arguments:

```bash
docker run -d --name alertmanager \
  -p 9093:9093 \
  -v /path/to/your/data:/alertmanager \
  sourcemation/alertmanager:latest \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --storage.path=/alertmanager \
  --web.listen-address=:9093 \
  --cluster.listen-address=0.0.0.0:9094 \
  --log.level=info
```

Run Alertmanager in cluster mode:

```bash
# Node 1
docker run -d --name alertmanager-1 \
  -p 9093:9093 -p 9094:9094 \
  -v /path/to/your/data1:/alertmanager \
  sourcemation/alertmanager:latest \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --storage.path=/alertmanager \
  --cluster.listen-address=0.0.0.0:9094 \
  --cluster.peer=alertmanager-2:9094

# Node 2
docker run -d --name alertmanager-2 \
  -p 9095:9093 -p 9096:9094 \
  -v /path/to/your/data2:/alertmanager \
  sourcemation/alertmanager:latest \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --storage.path=/alertmanager \
  --web.listen-address=:9093 \
  --cluster.listen-address=0.0.0.0:9094 \
  --cluster.peer=alertmanager-1:9094
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

This image exposes the following ports:

- **9093** - Alertmanager web interface and API
- **9094** - Cluster communication (when running in cluster mode)

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Volumes

- **/alertmanager** - Data directory for alert storage and persistence

## Default Configuration

The container includes a default `alertmanager.yml` configuration file located at `/etc/alertmanager/alertmanager.yml`. You can override this by mounting your own configuration file to this path.

Example minimal configuration:

```yaml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alertmanager@example.org'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
- name: 'web.hook'
  webhook_configs:
  - url: 'http://127.0.0.1:5001/'
```

## Security

This image runs as the `nobody` user (non-root) for enhanced security. The data directory `/alertmanager` is writable by the nobody group.

## Tools Included

This image includes the following tools:

- **alertmanager** - The main Alertmanager binary
- **amtool** - Command-line tool for interacting with Alertmanager

Example amtool usage:

```bash
# List all alerts
docker exec alertmanager amtool alert query

# Silence an alert
docker exec alertmanager amtool silence add alertname="HighErrorRate"

# Show configuration
docker exec alertmanager amtool config show
```

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the SourceMation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/alertmanager` image is not affiliated with the Alertmanager project. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/alertmanager` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [overview of Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) page.

### Licenses

The base license for the solution (Alertmanager) is the [Apache License 2.0](https://github.com/prometheus/alertmanager/blob/main/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate SourceMation entry](https://www.sourcemation.com/).
