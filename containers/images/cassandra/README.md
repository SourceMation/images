# Apache Cassandra packaged by Sourcemation

> Apache Cassandra is a free and open-source, distributed, wide-column store, NoSQL database management system designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure.

This Cassandra distribution is provided by the upstream Apache packaging team.

## Usage

### Scenario 1: Running a Single Node (for Development/Testing)

This command starts a single Cassandra node, which is useful for application development and testing.

```bash
docker run -d --name cassandra-node1 \
  -p 9042:9042 \
  --restart always \
  -e CASSANDRA_CLUSTER_NAME="TestCluster" \
  -e JVM_EXTRA_OPTS="-Xms1g -Xmx1g" \
  sourcemation/cassandra
```

After a minute, you can check its status by running `docker exec cassandra-node1 nodetool status`.

## Advanced usage examples

This image is designed to easily form a cluster. To allow the nodes to communicate with each other, they must be on the same Docker network.

**Step 1: Create a Docker Network** (you only need to do this once)

This command creates a dedicated network for your cluster.

```bash
docker network create my-cassandra-net
```

**Step 2: Start the first node (the "seed" node)**

The first node will act as the contact point for other nodes joining the cluster. It must be connected to the network you just created.

```bash
docker run -d --name cassandra-seed-1 \
  --network my-cassandra-net \
  -e CASSANDRA_CLUSTER_NAME="MyCassandraCluster" \
  -e JVM_EXTRA_OPTS="-Xms1g -Xmx1g" \
  sourcemation/cassandra
```

**Step 3: Start the second node and connect it to the seed**

Wait about 60 seconds for the seed node to initialize. Then, start the second node, connecting it to the same network and pointing it to the first node using its container name (`cassandra-seed-1`) as the seed address.

```bash
docker run -d --name cassandra-node-2 \
  --network my-cassandra-net \
  -e CASSANDRA_CLUSTER_NAME="MyCassandraCluster" \
  -e CASSANDRA_SEEDS="cassandra-seed-1" \
  -e JVM_EXTRA_OPTS="-Xms1g -Xmx1g" \
  sourcemation/cassandra
```

**Step 4: Verify the cluster status**

After another minute, you can check the status from the seed node. You should see two nodes listed with a "UN" (Up/Normal) status.

```bash
docker exec -it cassandra-seed-1 nodetool status
```

## Image tags and versions

The `sourcemation/cassandra` image itself comes in `debian-12` flavor.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This container is configured at runtime using the following environment variables:

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`CASSANDRA_CLUSTER_NAME`** | The name of the Cassandra cluster. All nodes in a cluster must have the same name. | `My Cassandra Cluster` |
| **`CASSANDRA_SEEDS`** | A comma-separated list of IP addresses or container names of the seed nodes. For the first node, this can be omitted. | (The container's own IP) |
| **`JVM_EXTRA_OPTS`** | Optional. Allows passing additional options to the JVM, such as memory limits. **Crucial for development on machines with limited RAM.** | (empty) |
| **`CASSANDRA_LISTEN_ADDRESS`** | The IP address that Cassandra listens on for connections from other nodes. | `auto` (detects container IP) |
| **`CASSANDRA_RPC_ADDRESS`** | The IP address that Cassandra listens on for client connections (CQL). | `auto` (detects container IP) |

-----

This image exposes the following ports: 

- 9042 - The primary port for clients to connect using the CQL native protocol.
- 7000 - Port used for inter-node communication within the cluster.

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

-----

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/cassandra` image is not affiliated with
the Apache Software Foundation. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/cassandra` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation
platform](https://sourcemation.com/).

For more information, check out the [Apache Cassandra website](https://cassandra.apache.org/).

### Licenses

The base license for the solution (Apache Cassandra) is the
[Apache License 2.0](https://github.com/apache/cassandra/blob/trunk/LICENSE.txt). The licenses for each component shipped as
part of this image can be found on [the image's appropriate Sourcemation
entry](https://sourcemation.com/).
