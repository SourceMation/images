# Node Exporter packaged by Sourcemation

Node Exporter is a Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors. It exposes a wide variety of hardware- and kernel-related metrics such as CPU, memory, disk space, disk I/O, network bandwidth, and more.

This Node Exporter distribution is provided by the Sourcemation packaging team, built on a secure Debian 13 Slim base image.

## Usage

Run a temporary container with Node Exporter:

```bash
docker run --rm -it -p 9100:9100 sourcemation/node_exporter:latest
```

The Node Exporter metrics endpoint will be available at [http://localhost:9100/metrics](http://localhost:9100/metrics).

### Advanced usage examples

Run Node Exporter with persistent storage for textfile collector:

```bash
docker run -d --name node_exporter \
  -p 9100:9100 \
  -v /path/to/textfiles:/var/lib/node_exporter/textfile_collector \
  sourcemation/node_exporter:latest \
  --collector.textfile.directory=/var/lib/node_exporter/textfile_collector
```

Run with host monitoring (recommended for production):

```bash
docker run -d \
  --name node_exporter \
  --net="host" \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  sourcemation/node_exporter:latest \
  --path.rootfs=/host
```

Run with specific collectors enabled/disabled:

```bash
docker run -d --name node_exporter \
  -p 9100:9100 \
  sourcemation/node_exporter:latest \
  --collector.disable-defaults \
  --collector.cpu \
  --collector.meminfo \
  --collector.loadavg \
  --collector.filesystem
```

Run with filesystem monitoring and custom mount point exclusions:

```bash
docker run -d --name node_exporter \
  -p 9100:9100 \
  -v "/:/host:ro,rslave" \
  sourcemation/node_exporter:latest \
  --path.rootfs=/host \
  --collector.filesystem.mount-points-exclude=^/(dev|proc|sys|var/lib/docker/.+|var/lib/kubelet/.+)($|/)
```

Run with custom web configuration (TLS support):

```bash
docker run -d --name node_exporter \
  -p 9100:9100 \
  -v /path/to/web-config.yml:/etc/node_exporter/web-config.yml \
  sourcemation/node_exporter:latest \
  --web.config.file=/etc/node_exporter/web-config.yml
```

Run with additional collectors enabled:

```bash
docker run -d --name node_exporter \
  -p 9100:9100 \
  -v "/:/host:ro,rslave" \
  sourcemation/node_exporter:latest \
  --path.rootfs=/host \
  --collector.systemd \
  --collector.processes \
  --collector.interrupts \
  --log.level=info
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

This image exposes the following ports:

- **9100** - Node Exporter metrics endpoint

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Volumes

- **/var/lib/node_exporter/textfile_collector** - Directory for textfile collector (optional)
- **/host** - Host root filesystem mount point (when using `--path.rootfs=/host`)

## Configuration

### Collector Configuration
Enable specific collectors:
```bash
--collector.systemd --collector.processes
```

Disable default collectors:
```bash
--no-collector.arp --no-collector.bcache
```

Enable only specific collectors:
```bash
--collector.disable-defaults --collector.cpu --collector.meminfo --collector.loadavg
```

### Filtering Options
Many collectors support include/exclude patterns:

```bash
# Exclude certain filesystem types
--collector.filesystem.fs-types-exclude=^(autofs|binfmt_misc|bpf|cgroup2?|configfs|debugfs|devpts|devtmpfs|fusectl|hugetlbfs|iso9660|mqueue|nsfs|overlay|proc|procfs|pstore|rpc_pipefs|securityfs|selinuxfs|squashfs|sysfs|tracefs)$

# Exclude certain mount points
--collector.filesystem.mount-points-exclude=^/(dev|proc|sys|var/lib/docker/.+|var/lib/kubelet/.+)($|/)

# Include only specific network devices
--collector.netdev.device-include=^(eth0|wlan0)$
```

### Textfile Collector
The textfile collector allows you to expose custom metrics from files:

```bash
# Enable textfile collector
--collector.textfile.directory=/var/lib/node_exporter/textfile_collector

# Example: Create a custom metric file
echo 'my_custom_metric{label="value"} 42' > /var/lib/node_exporter/textfile_collector/custom.prom
```

## Security

This image runs as the `nobody` user (non-root) for enhanced security.

For production host monitoring, it's recommended to run the container with:
- Host network namespace (`--net="host"`)
- Host PID namespace (`--pid="host"`)
- Read-only bind mount of host root (`-v "/:/host:ro,rslave"`)
- `--path.rootfs=/host` argument

## Docker Compose Example

```yaml
version: '3.8'
services:
  node_exporter:
    image: sourcemation/node_exporter:latest
    container_name: node_exporter
    command:
      - '--path.rootfs=/host'
      - '--collector.filesystem.mount-points-exclude=^/(dev|proc|sys|var/lib/docker/.+|var/lib/kubelet/.+)($|/)'
      - '--collector.systemd'
      - '--collector.processes'
    network_mode: host
    pid: host
    restart: unless-stopped
    volumes:
      - '/:/host:ro,rslave'
```

## Prometheus Configuration

Example Prometheus scrape configuration:

```yaml
scrape_configs:
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']
    scrape_interval: 15s
    scrape_timeout: 10s
```

## Common Metrics

Some of the most useful metrics exposed by Node Exporter:

- `node_cpu_seconds_total` - CPU time spent in different modes
- `node_memory_MemTotal_bytes` - Total memory in bytes
- `node_memory_MemAvailable_bytes` - Available memory in bytes
- `node_filesystem_size_bytes` - Filesystem size in bytes
- `node_filesystem_avail_bytes` - Filesystem space available in bytes
- `node_load1`, `node_load5`, `node_load15` - Load averages
- `node_network_receive_bytes_total` - Network bytes received
- `node_network_transmit_bytes_total` - Network bytes transmitted
- `node_disk_read_bytes_total` - Disk bytes read
- `node_disk_written_bytes_total` - Disk bytes written

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the Sourcemation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/node_exporter` image is not affiliated with the Prometheus Node Exporter project. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/node_exporter` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [Sourcemation platform](https://www.sourcemation.com/).

For more information, check out the [Node Exporter documentation](https://prometheus.io/docs/guides/node-exporter/) and the [official Node Exporter repository](https://github.com/prometheus/node_exporter).

### Licenses

The base license for the solution (Node Exporter) is the [Apache License 2.0](https://github.com/prometheus/node_exporter/blob/master/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate Sourcemation entry](https://www.sourcemation.com/).
