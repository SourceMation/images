# PostgreSQL packaged by SourceMation

PostgreSQL is an industry-proven, mature, feature-rich relational database
management system with a flexible support for both small applications and
large-scale venues.

This PostgreSQL distribution is provided by The PostgreSQL Global Development
Group packaging team.

## Usage

Run a temporary container with a PostgreSQL server with no authentication:

```
docker run -e POSTGRES_HOST_AUTH_METHOD=trust sourcemation/postgresql:latest
```

Please note that this is **not** recommended for production usage.
Substitute `-e POSTGRES_HOST_AUTH_METHOD=trust` with `-e
POSTGRES_PASSWORD=<ADMIN_PASSWORD>` for any authentication method.

### Advanced usage examples

For database persistence and password-based authentication, use a
command similar to:

```
mkdir $HOME/my-postgresql-files
sudo chown 26:26 $HOME/my-postgresql-files
docker run -e POSTGRES_PASSWORD=changeme -v $HOME/my-postgresql-files:/var/lib/postgresql sourcemation/postgresql:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
LANG="pl_PL.utf8"
PG_MAJOR="14"
PG_VERSION="14.13"
LC_ALL="pl_PL.utf8"
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/pgsql-14/bin"
PGDATA="/var/lib/postgresql/pg-data"
APP_VERSION="14.13"
APP_NAME="postgresql"
```

This image exposes the following ports: 

- 5432 : the default PostgreSQL listening port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features or images by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/postgresql` image is not affiliated with The
PostgreSQL Global Development Group. The respective companies and organisations
own the trademarks mentioned in the offering. The `sourcemation/postgresql`
image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

The server runs as the system user and group `postgres`, them having UID and
GID 26 (contrary to the default value of 70). The `/var/lib/postgresql`
directory holds the user's home directory, the databases, and is preconfigured
as a volume - for persistence, in case of a container removal and recreation,
mount that directory during the container startup command - see the ["Advanced
usage examples"](#advanced-usage-examples) paragraph for examples.

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation
platform](https://www.sourcemation.com/products/a702cf04-27d5-4b4f-b4b7-099e2dc7a407/deployments).

For more information, check out the [overview of
PostgreSQL®](https://www.postgresql.org/about/) page.

### Licenses

The base license for the solution (PostgreSQL) is the [PostgreSQL
License](https://www.postgresql.org/about/licence/). The licenses for each
component shipped as part of this image can be found on [the image's
appropriate SourceMation
entry](https://www.sourcemation.com/products/a702cf04-27d5-4b4f-b4b7-099e2dc7a407/deployments).
