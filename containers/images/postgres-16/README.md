# SourceMation's PostgreSQL 16 on Debian Slim

This container delivers PostgreSQL 16, a robust, open-source object-relational
database system. Boasting over 35 years of active development, PostgreSQL is
renowned for its reliability, feature-richness, and performance. This
distribution operates on a lean Debian Slim base.

Built by SourceMation's automation team, this PostgreSQL release (version
16.X.Y) undergoes regular updates. The foundation is the latest
`sourcemation/debian-12-slim` image at build time, ensuring a compact, secure,
and current setup. Cryptographic signatures are employed during the build to
guarantee source code and package integrity.

## Getting Started

To launch a temporary PostgreSQL container (providing `-e
POSTGRES_PASSWORD=...` is essential for startup):

```bash
docker run --rm -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 sourcemation/postgres-16:latest
```

For a less secure "trust" authentication, set
`POSTGRES_HOST_AUTH_METHOD=trust`:

```bash
docker run --rm -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 sourcemation/postgres-16:latest
```

For persistent data, mount a volume to `/var/lib/postgresql/data`:

```bash
docker run --rm -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -v my-postgres-data:/var/lib/postgresql/data sourcemation/postgres-16:latest
```

To access a shell within the container:

```bash
docker run --rm -it sourcemation/postgres-16:latest /bin/bash
```

### Advanced Connection Example

Connecting to the PostgreSQL instance from another container within the same
podman network (compatible with Docker):

```bash
podman network create my-net
# Initiate the PostgreSQL container
podman run -d --network my-net -e POSTGRES_PASSWORD=superPassw0rd --name postgres-container-name sourcemation/postgres-16:latest
# Start a second container in interactive mode (password not required here)
podman run -it --network my-net sourcemation/postgres-16:latest /bin/bash
# From the second container, connect to PostgreSQL (password prompt will appear)
psql -h postgres-container-name -U postgres
```

(Replace `my-net` and `postgres-container-name` with your network and container name. Create a Podman/Docker network if needed.)

## Key Environment Variables

This image utilizes:

```bash
LANG=en_US.utf8
PG_MAJOR=16
PATH=$PATH:/usr/lib/postgresql/$PG_MAJOR/bin
PGDATA=/var/lib/postgresql/data
PG_VERSION=16.X.Y # Example: 16.4-1.pgdg120+2
GOSU_VERSION=1.17
```

Customize the initial superuser and database with `POSTGRES_USER`,
`POSTGRES_PASSWORD`, and `POSTGRES_DB`. Refer to the official PostgreSQL Docker
documentation for details.

## Port Exposure

Port `5432`, the standard PostgreSQL port, is exposed by default.

## Contributions and Issue Reporting

Contributions are welcome! Propose new features by creating issues or submit
pull requests on the SourceMation GitHub repository.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/postgres-16` image operates independently of
the PostgreSQL Global Development Group. Trademarks mentioned are owned by
their respective entities. This image is a distinct project maintained by
[SourceMation](https://sourcemation.com).

## Additional Information

### Image Component Risk Analysis

A detailed risk analysis of our images and their components is available on the [SourceMation platform](https://www.sourcemation.com/).

Note: Risk analysis reports are not yet available for all images. Contact us for additional software components or queries.

### Licensing

The core license for PostgreSQL is the [PostgreSQL License](https://www.postgresql.org/about/licence/).
