# MySQL Community Server packaged by Sourcemation

> MySQL is the world's most popular open source database. With its proven performance, reliability and ease-of-use, MySQL has become the leading database choice for web-based applications, used by high profile web properties including Facebook, Twitter, YouTube, Yahoo! and many more.

This MySQL distribution is provided by the upstream MySQL packaging team.

## Usage

Run a temporary MySQL container with random root password

```bash
docker run --rm -e MYSQL_RANDOM_ROOT_PASSWORD=yes -it sourcemation/mysql
```

### Advanced usage examples

#### Run MySQL with custom root password

```bash
docker run --name mysql-server \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -p 3306:3306 \
  -d sourcemation/mysql
```

#### Run MySQL with custom database and user

```bash
docker run --name mysql-server \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -e MYSQL_DATABASE=myapp \
  -e MYSQL_USER=myuser \
  -e MYSQL_PASSWORD=mypass \
  -p 3306:3306 \
  -d sourcemation/mysql
```

#### Run with persistent data volume

```bash
docker run --name mysql-server \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  -d sourcemation/mysql
```

#### Run with initialization scripts

```bash
docker run --name mysql-server \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -v /path/to/init-scripts:/docker-entrypoint-initdb.d:ro \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  -d sourcemation/mysql
```

## Image tags and versions

The `sourcemation/mysql` image itself comes in `debian-12` flavor. The tag `latest` refers to the Debian-based flavor.  
***We are not building a MySQL image for the arm64 architecture. The official MySQL repository doesn't provide packages for the arm64 architecture.***

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```bash
MYSQL_ROOT_PASSWORD=<password>       # Set root password
MYSQL_RANDOM_ROOT_PASSWORD=no
MYSQL_ALLOW_EMPTY_PASSWORD=no

# Optional database creation:
MYSQL_DATABASE=<database_name>       # Create database on startup
MYSQL_USER=<username>                # Create user on startup
MYSQL_PASSWORD=<password>            # Password for MYSQL_USER

# Additional options:
MYSQL_INITDB_SKIP_TZINFO=no          # Skip timezone info loading
```

This image exposes the following ports:

- `3306` - MySQL server port

This image defines the following volumes:

- `/var/lib/mysql` - Database data directory
- `/docker-entrypoint-initdb.d` - Initialization scripts directory

Please note that the ports need to be either manually forwarded with the `-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the Sourcemation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/mysql` image is not affiliated with Oracle Corporation. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/mysql` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Initialization Scripts

The container supports initialization scripts that will be executed when the database is first created. Place your scripts in the `/docker-entrypoint-initdb.d` directory:

- `*.sh` files will be executed as shell scripts
- `*.sql` files will be executed as SQL scripts
- `*.sql.gz` and `*.sql.xz` files will be decompressed and executed as SQL scripts

### Security Considerations

- The container runs as the `mysql` user (non-root) for improved security
- Anonymous users are removed during initialization
- Remote root access is enabled but secured with password authentication
- The test database is removed during initialization

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [Sourcemation platform](https://sourcemation.com).

For more information, check out the [overview of MySQL](https://mysql.com/) page.

### Licenses

The base license for the solution (MySQL Community Server) is the [GPLv2](https://github.com/mysql/mysql-server/blob/8.0/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate Sourcemation entry](https://sourcemation.com).