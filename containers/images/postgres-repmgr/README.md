# PostgreSQL with Repmgr Container

This image provides a complete PostgreSQL and **repmgr** environment for building high-availability database clusters. It's designed to simplify the setup of primary and standby nodes with automated failover capabilities, which is critical for production database environments.

Maintained by SourceMation, this distribution is regularly updated to ensure it's current and secure. It is a focused container designed for easy integration into your existing infrastructure, providing a robust foundation for a resilient PostgreSQL setup.

-----

## Core Features

  * **High Availability:** Implements a full primary/standby replication cluster.
  * **Automated Failover:** `repmgr` continuously monitors the cluster and can automatically promote a standby node to primary in case of a failure.
  * **Simplified Cluster Management:** Easily add new standby nodes that clone data from the primary, scaling your read capacity and improving redundancy.
  * **Configuration via Environment:** The entire cluster setup is managed through environment variables, making it perfect for containerized and orchestrated environments like Kubernetes.

-----

## Operational Use

This image is intended for production environments where database uptime is critical. The setup requires starting at least two containers: one primary and one or more standbys.

### Step 1: Create network
```
docker network create my-network
```

### Step 2: Start the Primary Node

The first node in the cluster must be started with the `REPMGR_ROLE` set to `primary`.

```bash
docker run -d --network  my-network --name primary \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e REPMGR_ROLE=primary \
  -e REPMGR_USER=repmgr \
  -e REPMGR_PASSWORD=repmgrpass \
  -e REPMGR_DB=repmgr \
  -e NODE_ID=1 \
  -e NODE_NAME=primary \
  sourcemation/postgres-repmgr
```

### Step 3: Start a Standby Node

A standby node clones its data from an upstream node (usually the primary). You must provide the IP address or hostname of the primary in the `REPMGR_UPSTREAM_HOST` variable.

First, get the primary container's IP address:

```bash
PRIMARY_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' primary)
```

Now, start the standby container, pointing it to the primary:

```bash
docker run -d --network  my-network --name standby \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e REPMGR_ROLE=standby \
  -e REPMGR_USER=repmgr \
  -e REPMGR_PASSWORD=repmgrpass \
  -e REPMGR_DB=repmgr \
  -e REPMGR_UPSTREAM_HOST=$PRIMARY_IP \
  -e NODE_ID=2 \
  -e NODE_NAME=standby \
  sourcemation/postgres-repmgr
```

### Step 4: Verify the Cluster Status

You can check the health and status of your replication cluster by running the `repmgr cluster show` command inside any of the containers.

```bash
docker exec -it primary repmgr cluster show
```

-----

## Key Environment Variables

This container uses the following environment variables for configuration:

| Variable | Description | Example |
| :--- | :--- | :--- |
| **`POSTGRES_PASSWORD`** | **Required.** Sets the password for the main `postgres` superuser. | `mysecretpassword` |
| **`REPMGR_ROLE`** | **Required.** Defines the node's role. Must be `primary` or `standby`. | `primary` |
| **`REPMGR_USER`** | **Required.** The username `repmgr` will use to connect for replication. | `repmgr` |
| **`REPMGR_PASSWORD`** | **Required.** The password for the `repmgr` user. | `repmgrpass` |
| **`REPMGR_DB`** | **Required.** The database `repmgr` will use for its metadata. | `repmgr` |
| **`REPMGR_UPSTREAM_HOST`** | **Required for standbys.** The IP or hostname of the primary node to clone from. | `172.17.0.2` |
| **`NODE_ID`** | **Required.** A unique integer ID for each node in the cluster. | `1` |
| **`NODE_NAME`** | **Required.** A unique name for each node, often matching the container name. | `primary-db` |

-----

## Port Exposure

The standard **PostgreSQL** port, **5432**, is exposed by default for database connections.

-----

## Contributing and Reporting Issues

Your contributions are valued\! Feel free to suggest enhancements or request new
images by opening an issue, or submit your own contributions via pull requests
to the SourceMation GitHub repository.

  - [Creating issues (bugs) and images requests](https://github.com/SourceMation/images/issues/new/choose)
  - [Creating pull requests](https://github.com/SourceMation/images/compare)

-----

## Extra notes

**Disclaimer:** The `sourcemation/postgres-repmgr` image is not affiliated with the PostgreSQL Global Development Group or EnterpriseDB. The respective entities own the trademarks mentioned in the offering. The `sourcemation/postgres-repmgr` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://www.sourcemation.com/products/b95ab2de-202b-45f2-a2a3-086e64968979/deployments).

### Licenses

The base licenses for the solution are the [PostgreSQL License](https://www.postgresql.org/about/licence/) and the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) for repmgr.