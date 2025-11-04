# Cloud Native PostgreSQL 18 on Debian Slim packaged by Sourcemation (cnpg-18)

This image, `sourcemation/cnpg-18`, is built upon `sourcemation/postgres-18`
and extends it to provide a PostgreSQL 18 environment optimized for Cloud
Native PostgreSQL (CNPG) deployments. It includes essential extensions and
configurations for CNPG, such as `pgaudit`, `pgvector`, and
`pg-failover-slots`.

This PostgreSQL distribution is built by the Sourcemation automation team. The
version is 18.X.Y and it's regularly updated. The base image is the latest
`sourcemation/debian-12-slim` image at the time of the build, providing a
small, secure, and up-to-date foundation. The build process incorporates
cryptographic signatures to ensure the integrity of the source code and
packages.

## Key Features

* **Based on `sourcemation/postgres-18`:** Inherits all the benefits and security features of the base image.
* **CNPG Optimized:** Includes pre-installed extensions commonly used with Cloud Native PostgreSQL.
    * `postgresql-18-pgaudit`: Provides detailed audit logging.
    * `postgresql-18-pgvector`: Enables efficient storage and querying of vector embeddings.
    * `postgresql-18-pg-failover-slots`: Facilitates seamless failover in high-availability setups.
* **Barman Cloud Integration:** Includes `barman-cloud` for cloud-based backup and recovery.
* **Polish Locale:** The default locale is set to `pl_PL.UTF-8`.
* **Postgres UID:** The postgres user's UID is set to 26.

## Usage

Since this image is based on `sourcemation/postgres-18`, you can use it in the same way. However, it's primarily intended for CNPG deployments.

**Example for local testing (not recommended for production use):**

```bash
docker run --rm -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 sourcemation/cnpg-18:latest
```

**Using with Cloud Native PostgreSQL:**

Refer to the official Cloud Native PostgreSQL documentation for instructions on how to use custom images.

## Locale Configuration

The images support following locales en_US.UTF-8 (default), pl_PL.UTF-8. To
modify the locale in a child image, override the `LANG` environment variable
and regenerate the locale settings.


**Example Dockerfile snippet for switching to `ja_JP.UTF-8` (Japanese) locale:**

```dockerfile
FROM sourcemation/cnpg-18

# Change locale to ja_JP.UTF-8
RUN localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8; \
    sed -i -e 's/en_US/ja_JP/g' /etc/locale.gen && locale-gen
ENV LANG=ja_JP.UTF-8
```

## Most important environment variables

This image uses the following environment variables:

```bash
LANG=en_US.UTF-8
PG_MAJOR=18
PATH=$PATH:/usr/lib/postgresql/$PG_MAJOR/bin
PGDATA=/var/lib/postgresql/data
PG_VERSION=18.X.Y # For example 18.0-1.pgdg120+2
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

**Disclaimer:** The `sourcemation/cnpg-18` image is not directly affiliated
with the PostgreSQL Global Development Group. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/cnpg-18` image is a separate project and is maintained by
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

Cloud Native PostgreSQL containers are licensed under the [Apache License
2.0](https://github.com/cloudnative-pg/postgres-containers/blob/main/LICENSE).
