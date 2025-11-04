# MariaDB packaged by Sourcemation

> MariaDB is a popular open source relational database that was created by the original developers of MySQL. MariaDB is developed as open source software and as a relational database it provides an SQL interface for accessing data.

This MariaDB distribution is provided by the upstream MariaDB packaging team.

## Usage

Run a temporary container with MariaDB

```bash
docker run --rm -it sourcemation/mariadb
```

### Advanced usage examples

#### Run MariaDB with custom root password

```bash
docker run --name mariadb-server \
  -e MARIADB_ROOT_PASSWORD=my-secret-pw \
  -p 3306:3306 \
  -d sourcemation/mariadb
```

#### Run MariaDB with custom database and user

```bash
docker run --name mariadb-server \
  -e MARIADB_ROOT_PASSWORD=my-secret-pw \
  -e MARIADB_DATABASE=myapp \
  -e MARIADB_USER=myuser \
  -e MARIADB_PASSWORD=mypass \
  -p 3306:3306 \
  -d sourcemation/mariadb
```

#### Run with persistent data volume

```bash
docker run --name mariadb-server \
  -e MARIADB_ROOT_PASSWORD=my-secret-pw \
  -v mariadb-data:/var/lib/mysql \
  -p 3306:3306 \
  -d sourcemation/mariadb
```

#### Run with initialization scripts

```bash
docker run --name mariadb-server \
  -e MARIADB_ROOT_PASSWORD=my-secret-pw \
  -v /path/to/init-scripts:/docker-entrypoint-initdb.d:ro \
  -v mariadb-data:/var/lib/mysql \
  -p 3306:3306 \
  -d sourcemation/mariadb
```

## Image tags and versions

The `sourcemation/mariadb` image itself comes in `debian-13` flavor. The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```bash
MARIADB_ROOT_PASSWORD=<password>     # Set root password
MARIADB_RANDOM_ROOT_PASSWORD=no
MARIADB_ALLOW_EMPTY_PASSWORD=no

# Optional database creation:
MARIADB_DATABASE=<database_name>     # Create database on startup
MARIADB_USER=<username>              # Create user on startup
MARIADB_PASSWORD=<password>          # Password for MARIADB_USER

# Backwards compatibility (legacy MySQL_ variables are also supported):
MYSQL_ROOT_PASSWORD, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, etc.
```

This image exposes the following ports:

- `3306` - MariaDB server port

This image defines the following volumes:

- `/var/lib/mysql` - Database data directory
- `/docker-entrypoint-initdb.d` - Initialization scripts directory

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the Sourcemation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/mariadb` image is not affiliated with the MariaDB Foundation. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/mariadb` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Initialization Scripts

The container supports initialization scripts that will be executed when the database is first created. Place your scripts in the `/docker-entrypoint-initdb.d` directory:

- `*.sh` files will be executed as shell scripts
- `*.sql` files will be executed as SQL scripts
- `*.sql.gz` and `*.sql.xz` files will be decompressed and executed as SQL scripts

### Security Considerations

- The container runs as the `mysql` user (non-root) for improved security
- Anonymous users are removed during initialization
- Remote root access is disabled by default (root can only connect from localhost)
- The test database is removed during initialization

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [Sourcemation platform](https://sourcemation.com).

For more information, check out the [overview of MariaDB](https://mariadb.org/) page.

### Licenses

The base license for the solution (MariaDB) is the [GPLv2](https://github.com/MariaDB/server/blob/11.4/COPYING). The licenses for each component shipped as part of this image can be found on [the image's appropriate Sourcemation entry](https://sourcemation.com).