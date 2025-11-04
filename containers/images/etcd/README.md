# etcd packaged by Sourcemation

**etcd** is a distributed, reliable key-value store for the most critical data of a distributed system. It provides a reliable way to store data that needs to be accessed by a distributed system or cluster of machines. It gracefully handles leader elections during network partitions and can tolerate machine failure, even in the leader node.

This etcd distribution is provided by the Sourcemation packaging team, built on a secure Debian 13 Slim base image.

## Usage

Run a temporary container with etcd:

```bash
docker run --rm -it -p 2379:2379 -p 2380:2380 sourcemation/etcd:latest
```

The etcd client API will be available at [http://localhost:2379](http://localhost:2379).

### Advanced usage examples

Run etcd with persistent storage:

```bash
docker run -d --name etcd \
  -p 2379:2379 -p 2380:2380 \
  -v /path/to/your/data:/var/lib/etcd \
  sourcemation/etcd:latest
```

Run etcd with custom configuration:

```bash
docker run -d --name etcd \
  -p 2379:2379 -p 2380:2380 \
  -v /path/to/your/data:/var/lib/etcd \
  sourcemation/etcd:latest \
  --name my-etcd-node \
  --data-dir /var/lib/etcd \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster my-etcd-node=http://localhost:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster-state new
```

Run etcd cluster (3 nodes):

```bash
# Node 1
docker run -d --name etcd-1 \
  -p 2379:2379 -p 2380:2380 \
  -v /path/to/your/data1:/var/lib/etcd \
  sourcemation/etcd:latest \
  --name etcd-1 \
  --data-dir /var/lib/etcd \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://etcd-1:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://etcd-1:2380 \
  --initial-cluster etcd-1=http://etcd-1:2380,etcd-2=http://etcd-2:2380,etcd-3=http://etcd-3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster-state new

# Node 2
docker run -d --name etcd-2 \
  -p 2381:2379 -p 2382:2380 \
  -v /path/to/your/data2:/var/lib/etcd \
  sourcemation/etcd:latest \
  --name etcd-2 \
  --data-dir /var/lib/etcd \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://etcd-2:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://etcd-2:2380 \
  --initial-cluster etcd-1=http://etcd-1:2380,etcd-2=http://etcd-2:2380,etcd-3=http://etcd-3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster-state new

# Node 3
docker run -d --name etcd-3 \
  -p 2383:2379 -p 2384:2380 \
  -v /path/to/your/data3:/var/lib/etcd \
  sourcemation/etcd:latest \
  --name etcd-3 \
  --data-dir /var/lib/etcd \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://etcd-3:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://etcd-3:2380 \
  --initial-cluster etcd-1=http://etcd-1:2380,etcd-2=http://etcd-2:2380,etcd-3=http://etcd-3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster-state new
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

This image exposes the following ports:

- **2379** - Client communication port
- **2380** - Server-to-server communication port

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Volumes

- **/var/lib/etcd** - Data directory for etcd database storage

## Default Configuration

The container runs with default etcd settings suitable for single-node development use. For production deployments, you should specify appropriate configuration parameters as command-line arguments.

Common configuration options:
- `--name` - Human-readable name for this member
- `--data-dir` - Path to the data directory
- `--listen-client-urls` - List of URLs to listen on for client traffic
- `--advertise-client-urls` - List of this member's client URLs to advertise to the public
- `--listen-peer-urls` - List of URLs to listen on for peer traffic
- `--initial-advertise-peer-urls` - List of this member's peer URLs to advertise to other members
- `--initial-cluster` - Initial cluster configuration for bootstrapping
- `--initial-cluster-token` - Initial cluster token for the etcd cluster during bootstrap
- `--initial-cluster-state` - Initial cluster state ('new' or 'existing')

## Security

This image runs as the `nobody` user (non-root) for enhanced security. The data directories `/var/lib/etcd` and `/var/etcd` are accessible by the nobody user.

## Tools Included

This image includes the following tools:

- **etcd** - The main etcd server binary
- **etcdctl** - Command-line client for etcd
- **etcdutl** - Administrative utility for etcd

Example etcdctl usage:

```bash
# Set a key-value pair
docker exec etcd etcdctl put greeting "Hello, etcd"

# Get a value
docker exec etcd etcdctl get greeting

# List all keys
docker exec etcd etcdctl get "" --prefix

# Check cluster health
docker exec etcd etcdctl endpoint health

# Get cluster status
docker exec etcd etcdctl endpoint status --write-out=table

# Create a backup
docker exec etcd etcdctl snapshot save /var/lib/etcd/backup.db
```

Example etcdutl usage:

```bash
# Check snapshot status
docker exec etcd etcdutl snapshot status /var/lib/etcd/backup.db

# Restore from snapshot
docker exec etcd etcdutl snapshot restore /var/lib/etcd/backup.db \
  --data-dir /var/lib/etcd/restored
```

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the Sourcemation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/etcd` image is not affiliated with the etcd project. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/etcd` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [Sourcemation platform](https://www.sourcemation.com/).

For more information, check out the [overview of etcd](https://etcd.io/) page.

### Licenses

The base license for the solution (etcd) is the [Apache License 2.0](https://github.com/etcd-io/etcd/blob/main/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate Sourcemation entry](https://www.sourcemation.com/).
