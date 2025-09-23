# MinIO packaged by SourceMation

MinIO is a high-performance, S3-compatible object storage server that delivers scalable and secure data storage for cloud-native applications. MinIO's distributed architecture provides fault tolerance and high availability while maintaining simplicity and ease of deployment.

This MinIO distribution is provided by the SourceMation packaging team, built on a secure Debian 12 Slim base image with MinIO server.

## Usage

Run a temporary container with MinIO:

```bash
docker run --rm -it -p 9000:9000 -p 9001:9001 sourcemation/minio:latest server /data --console-address ":9001"
```

The MinIO API will be available at [http://localhost:9000](http://localhost:9000) and the web console at [http://localhost:9001](http://localhost:9001).

Default credentials: `minioadmin` / `minioadmin`

### Advanced usage examples

Run MinIO with persistent storage:

```bash
docker run -d --name minio \
  -p 9000:9000 -p 9001:9001 \
  -v /path/to/your/data:/data \
  sourcemation/minio:latest server /data
```

Run MinIO with custom credentials:

```bash
docker run -d --name minio \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=secretpassword123 \
  -v /path/to/your/data:/data \
  sourcemation/minio:latest server /data
```

Run MinIO with custom API and console addresses:

```bash
docker run -d --name minio \
  -p 9000:9000 -p 9090:9090 \
  -v /path/to/your/data:/data \
  sourcemation/minio:latest server /data \
  --address :9000 \
  --console-address :9090
```

Run MinIO with specific configuration directory:

```bash
docker run -d --name minio \
  -p 9000:9000 -p 9001:9001 \
  -v /path/to/your/data:/data \
  -v /path/to/your/config:/config \
  sourcemation/minio:latest server /data \
  --config-dir /config
```

Run distributed MinIO (4 nodes example):

```bash
# Node 1
docker run -d --name minio-1 \
  -p 9001:9000 -p 9011:9001 \
  -v /mnt/data1:/data \
  sourcemation/minio:latest server \
  http://minio-1:9000/data \
  http://minio-2:9000/data \
  http://minio-3:9000/data \
  http://minio-4:9000/data

# Node 2
docker run -d --name minio-2 \
  -p 9002:9000 -p 9012:9001 \
  -v /mnt/data2:/data \
  sourcemation/minio:latest server \
  http://minio-1:9000/data \
  http://minio-2:9000/data \
  http://minio-3:9000/data \
  http://minio-4:9000/data

# Repeat for nodes 3 and 4...
```

Run MinIO with JSON logs and debug mode:

```bash
docker run -d --name minio \
  -p 9000:9000 -p 9001:9001 \
  -v /path/to/your/data:/data \
  -e MINIO_LOGGER_WEBHOOK_ENABLE_target1=on \
  -e MINIO_LOGGER_WEBHOOK_ENDPOINT_target1=http://logger:8080/minio/logs \
  sourcemation/minio:latest server /data \
  --json
```

Run MinIO with SSL/TLS:

```bash
docker run -d --name minio \
  -p 9000:9000 -p 9001:9001 \
  -v /path/to/your/data:/data \
  -v /path/to/certs:/certs \
  sourcemation/minio:latest server /data \
  --certs-dir /certs
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

### Core Configuration
- **MINIO_ROOT_USER** - Root access key (default: `minioadmin`)
- **MINIO_ROOT_PASSWORD** - Root secret key (default: `minioadmin`)
- **MINIO_SITE_NAME** - Name of the site (optional)
- **MINIO_SITE_REGION** - Region name for the server (default: `us-east-1`)

### Network Configuration
- **MINIO_SERVER_URL** - External hostname for the server
- **MINIO_BROWSER_REDIRECT_URL** - External hostname for the console

### Logging Configuration
- **MINIO_LOG_LEVEL** - Set log level (ERROR, WARN, INFO, DEBUG)
- **MINIO_LOG_FILE** - Set log file path
- **MINIO_LOG_JSON** - Enable JSON formatted logging

### Other Configuration
- **MINIO_CONFIG_ENV_FILE** - Path to environment file for additional configs

This image exposes the following ports:

- **9000** - MinIO API server port
- **9001** - MinIO Console (web interface) port

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Volumes

- **/data** - Default data storage directory

## Command Line Arguments

The MinIO server supports various command line arguments for configuration. Here are the most commonly used ones:

### Basic Server Command

```bash
minio server [FLAGS] [PATHS...]
```

### Network Configuration

- `--address` - Bind to a specific network address and port. Specify as `ADDRESS:PORT` (default: `:9000`)
- `--console-address` - Bind console to a specific network address and port. Specify as `ADDRESS:PORT` (auto-assigned by default)

### Storage Configuration

- `PATHS...` - One or more paths to use as storage backend. For distributed setup, use `http://host:port/path` format

### Security Configuration

- `--certs-dir` - Path to TLS certificates directory (default: `${HOME}/.minio/certs`)
- `--config-dir` - Path to configuration directory (default: `${HOME}/.minio`)

### Logging Configuration

- `--json` - Output server logs and startup information in JSON format
- `--quiet` - Disable startup information

### Advanced Configuration

- `--ftp` - Enable and configure FTP server (format: `[username[:password]@]host:port`)
- `--sftp` - Enable and configure SFTP server (format: `[username[:password]@]host:port`)

### Operational Flags

- `--help, -h` - Show help
- `--version, -v` - Print version information

### Examples of Common Flags

Start server with custom addresses:
```bash
minio server --address :9000 --console-address :9090 /data
```

Start server with TLS certificates:
```bash
minio server --certs-dir /certs /data
```

Start server with JSON logging:
```bash
minio server --json /data
```

Start distributed server:
```bash
minio server http://server{1...4}:9000/data{1...4}
```

## Security

This image runs as the `nobody` user (non-root) for enhanced security. The data directory `/data` is accessible by the nobody user.

## MinIO Client (mc) Tools

This image includes the MinIO binary for server operations. For client operations, you can use the official MinIO client `mc` from another container or install it separately.

Example using MinIO client with this server:

```bash
# Add server alias (from another container or host)
mc alias set myminio http://localhost:9000 minioadmin minioadmin

# Create a bucket
mc mb myminio/mybucket

# Upload files
mc cp /path/to/file myminio/mybucket/

# List buckets
mc ls myminio
```

## Health Checks

MinIO provides built-in health check endpoints:

- `/minio/health/live` - Liveness probe
- `/minio/health/ready` - Readiness probe
- `/minio/health/cluster` - Cluster health (distributed mode)

Example health check in Docker:

```bash
docker run -d --name minio \
  --health-cmd="curl -f http://localhost:9000/minio/health/live || exit 1" \
  --health-interval=30s \
  --health-timeout=20s \
  --health-retries=3 \
  -p 9000:9000 -p 9001:9001 \
  -v /data:/data \
  sourcemation/minio:latest server /data
```

## Distributed Deployment

For production distributed deployments, MinIO requires:

- **Minimum 4 drives** spread across multiple servers
- **Network connectivity** between all nodes
- **Synchronized time** across all nodes
- **Consistent network addresses** for all nodes

Example distributed deployment:

```bash
# Start 4 nodes (run on different hosts)
minio server http://node{1...4}:9000/data{1...4}
```

## Performance Tuning

For optimal performance:

- Use XFS or ext4 filesystems
- Mount drives with `noatime` option
- Use RAID configurations for redundancy
- Ensure adequate network bandwidth between nodes
- Configure appropriate memory limits

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the SourceMation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/minio` image is not affiliated with the MinIO project. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/minio` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [MinIO documentation](https://docs.min.io/).

### Licenses

The base license for the solution (MinIO) is the [GNU AGPLv3](https://github.com/minio/minio/blob/master/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate SourceMation entry](https://www.sourcemation.com/).
