# PostgreSQL 18 on Debian Slim packaged by Sourcemation

PostgreSQL is a powerful, open source object-relational database system. It
has more than 35 years of active development and has earned a strong reputation
for reliability, feature robustness, and performance. This distribution
provides PostgreSQL 18 running on a Debian Slim base image.

This PostgreSQL distribution is built by the Sourcemation automation team. The
version is 18.X.Y and it's regularly updated. The base image is the latest
`sourcemation/debian-13-slim` image at the time of the build, providing a
small, secure, and up-to-date foundation. The build process incorporates
cryptographic signatures to ensure the integrity of the source code and
packages.

## Usage

Run a temporary PostgreSQL container (the `-e POSTGRES_PASSWORD=...` is must for container to start):

```bash
docker run --rm -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 sourcemation/postgres-18:latest
```

You can set the connection to very insecure "trust" authentication method by setting `POSTGRES_HOST_AUTH_METHOD=trust`:

```bash
docker run --rm -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 sourcemation/postgres-18:latest
```


To persist data, you should mount a volume to `/var/lib/postgresql/data`:

```bash
docker run --rm -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -v my-postgres-data:/var/lib/postgresql/data sourcemation/postgres-18:latest
```

To run the shell in the container, use the following command:

```bash
docker run --rm -it sourcemation/postgres-18:latest /bin/bash
```

### Advanced usage examples

Connect to the PostgreSQL instance using `psql` from another container in same
podman network (should work with Docker as well):

```bash
podman network create my-net
# Start postgesql container
podman run -d --network my-net -e POSTGRES_PASSWORD=superPassw0rd --name postgres-container-name sourcemation/postgres-18:latest
# Now start second container in interactive mode -> the password is not required we are not running the server
podman run -it --network my-net sourcemation/postgres-18:latest /bin/bash
# In second container that you just started, you can connect to the postgresql container it would ask for password
psql -h postgres-container-name -U postgres
```

(Replace `my-net` and `postgres-container-name` with your network and container
name, respectively. You'll need to create a Podman/Docker network first if you
haven't already.)

## Most important environment variables

This image uses the following environment variables:

```
LANG=en_US.utf8
PG_MAJOR=18
PATH=$PATH:/usr/lib/postgresql/$PG_MAJOR/bin
PGDATA=/var/lib/postgresql/data
PG_VERSION=18.X.Y # For example 18.0
GOSU_VERSION=1.17
```

You can set `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` to
customize the initial superuser and database. See the official PostgreSQL
Docker documentation for details (though this image aims to follow it closely).

## Ports

This image exposes port `5432` by default, which is the standard PostgreSQL
port.

## Contributions and Issue Reporting

Contributions are welcome! Propose new features by creating issues or submit
pull requests on the Sourcemation GitHub repository.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/postgres-18` image is not directly affiliated
with the PostgreSQL Global Development Group. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/postgres-18` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of our images and its components might be found
on the [Sourcemation platform](https://www.sourcemation.com/).

However, not all images have a risk analysis report yet. If you need additional
software components or have any questions, please contact us.

### Licenses

The base license for the solution (PostgreSQL) is the [PostgreSQL
License](https://www.postgresql.org/about/licence/).
