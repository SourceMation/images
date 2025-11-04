# Apache ZooKeeper packaged by Sourcemation

> Apache ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. All of these kinds of services are used in some form or other by distributed applications.

This Apache ZooKeeper distribution is provided by the upstream Apache ZooKeeper packaging team.

## Usage

Run a temporary container with Apache ZooKeeper

```bash
docker run --rm -it sourcemation/zookeeper
```

Run ZooKeeper in standalone mode:

```bash
docker run -d --name zookeeper \
  -p 2181:2181 \
  sourcemation/zookeeper
```

### Advanced usage examples

#### Running ZooKeeper with custom configuration

Create custom zoo.cfg

```bash
cat > zoo.cfg << 'EOF'
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/var/lib/zookeeper/data
dataLogDir=/var/lib/zookeeper/logs
clientPort=2181
maxClientCnxns=60
autopurge.snapRetainCount=3
autopurge.purgeInterval=24
admin.enableServer=true
admin.serverPort=8080
EOF
```

Run with custom configuration

```bash
docker run -d --name zookeeper \
  -p 2181:2181 \
  -p 8080:8080 \
  -v $(pwd)/zoo.cfg:/opt/zookeeper/conf/zoo.cfg:ro \
  sourcemation/zookeeper
```

#### Running ZooKeeper cluster

Create a network

```bash
docker network create zk-network
```

Run Node 1

```bash
docker run -d --name zk1 \
  --network zk-network \
  -p 2181:2181 \
  -e ZK_SERVER_ID=1 \
  -e ZK_SERVERS="server.1=zk1:2888:3888;2181 server.2=zk2:2888:3888;2181 server.3=zk3:2888:3888;2181" \
  sourcemation/zookeeper
```

Run Node 2

```bash
docker run -d --name zk2 \
  --network zk-network \
  -p 2182:2181 \
  -e ZK_SERVER_ID=2 \
  -e ZK_SERVERS="server.1=zk1:2888:3888;2181 server.2=zk2:2888:3888;2181 server.3=zk3:2888:3888;2181" \
  sourcemation/zookeeper
```

Run Node 3

```bash
docker run -d --name zk3 \
  --network zk-network \
  -p 2183:2181 \
  -e ZK_SERVER_ID=3 \
  -e ZK_SERVERS="server.1=zk1:2888:3888;2181 server.2=zk2:2888:3888;2181 server.3=zk3:2888:3888;2181" \
  sourcemation/zookeeper
```

## Image tags and versions

The `sourcemation/zookeeper` image itself comes in `debian-13` flavour. The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```bash
HOME=/opt/zookeeper
LANG=en_US.UTF-8
LANGUAGE=en_US:en
LC_ALL=en_US.UTF-8
ZK_USER=zookeeper
ZK_DATA_LOG_DIR=/var/lib/zookeeper/logs
ZK_LOG_DIR=/var/log/zookeeper
ZK_DATA_DIR=/var/lib/zookeeper/data
ZK_CONF_DIR=/opt/zookeeper/conf
ZK_HOME=/opt/zookeeper
JAVA_HOME=/opt/java/openjdk
PATH=/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/zookeeper/bin
```

This image exposes the following ports:

- `2181`: Client port for ZooKeeper connections
- `2888`: Follower port for cluster communication
- `3888`: Election port for leader election
- `8080`: Admin server port for HTTP-based administration

This image defines the following volumes:

- `/var/lib/zookeeper/data`: ZooKeeper data directory (snapshots)
- `/var/lib/zookeeper/logs`: ZooKeeper transaction log directory
- `/var/log/zookeeper`: ZooKeeper application log directory

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Security

The container runs as a non-root user (`zookeeper`) for enhanced security. All ZooKeeper processes and data are owned by this dedicated user.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/zookeeper` image is not affiliated with
the Apache Software Foundation. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/zookeeper` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation
platform](https://sourcemation.com/catalog/zookeeper).

For more information, check out the [overview of
Apache ZooKeeper](https://zookeeper.apache.org/) page.

### Licenses

The base license for the solution (Apache ZooKeeper) is the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). The licenses for each component shipped as
part of this image can be found on [the image's appropriate Sourcemation
entry](https://sourcemation.com/catalog/zookeeper).
