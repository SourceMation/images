# Pgpool-II Container on Debian 12 Slim packed by Sourcemation

This image, `sourcemation/pgpool`, is built on `sourcemation/postgresql-17` to provide a robust **Pgpool-II** environment. It's designed for handling connection pooling, load balancing, and high availability for your PostgreSQL database deployments. The image integrates essential Pgpool-II configurations and includes the Pgpool Command-line Protocol (PCP).

Maintained by the Sourcemation automation team, this Pgpool-II distribution (version 4.X.Y) is regularly updated to ensure it's current, secure, and compact. It's built on a minimal Debian base (`sourcemation/postgresql-17` itself is based on Debian Slim), and cryptographic signatures are used during the build process to guarantee the integrity of all source code and packages.

***

## Core Features

* **Based on `sourcemation/postgresql-17`:** Inherits all the core benefits and security features of the underlying PostgreSQL image.
* **Pgpool-II Integration:** Comes with pre-installed Pgpool-II tools for managing connections, distributing queries, and supporting high-availability setups.
* **PCP Protocol:** Enables administrative tasks and remote control via the Pgpool Command-line Protocol.
* **Postgres User ID:** Assigns the postgres user a consistent UID of 26 for better management and security across environments.

***

## Operational Use

This image is intended for production environments where connection pooling and load balancing are critical. It must be configured with backend PostgreSQL servers.

**Example for a local, non-production test:**

```bash
docker run --rm \
    -e PGPOOL_PARAMS_BACKEND_HOSTNAME0="test_hostname" \
    -e PGPOOL_PCP_USER="test" \
    -e PGPOOL_PCP_PASSWORD="test" \
    -p 9999:9999 \
    sourcemation/pgpool
```
## Key Environment Variables
This container uses the following environment variables for configuration:

* `PGPOOL_PARAMS_BACKEND_HOSTNAME0`: The hostname or IP address of the first backend PostgreSQL server.
* `PGPOOL_PCP_USER`: The username for the Pgpool Command-line Protocol.
* `PGPOOL_PCP_PASSWORD`: The password for the PCP user.

## Port Exposure
The standard Pgpool-II port, **9999**, is exposed by default.


## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/pgpool` image is not affiliated with the pgpool. The respective companies and
organisations own the trademarks mentioned in the offering. The `sourcemation/pgpool` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes
### Image and its components Risk Analysis report

A comprehensive risk analysis report detailing the image and its components can
be accessed on the [Sourcemation platform](https://www.sourcemation.com/).

For more information, check out the [overview of
pgpool](https://pgpool.net/mediawiki/index.php/Main_Page) page.

### Licenses

The base license for the pgpool is the
[pgpool-II](https://pgpool.net/mediawiki/index.php/pgpool-II_License)
