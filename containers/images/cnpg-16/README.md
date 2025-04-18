# SourceMation's Cloud Native PostgreSQL 16 on Debian Slim (cnpg-16)

This image, `sourcemation/cnpg-16`, builds upon `sourcemation/postgres-16` to
deliver a PostgreSQL 16 environment optimized for Cloud Native PostgreSQL
(CNPG) deployments. It integrates essential CNPG extensions and configurations,
notably `pgaudit`, `pgvector`, and `pg-failover-slots`.

Constructed by the SourceMation automation team, this PostgreSQL distribution,
version 16.X.Y, receives regular updates. Built upon the latest
`sourcemation/debian-12-slim` image at build time, it provides a compact,
secure, and current base. Cryptographic signatures are employed during the
build to ensure source and package integrity.

## Core Features

* **Based on `sourcemation/postgres-16`:** Inherits all benefits and security features of the underlying image.
* **CNPG Optimization:** Includes pre-installed extensions commonly used with Cloud Native PostgreSQL.
    * `postgresql-16-pgaudit`: Offers detailed audit logging capabilities.
    * `postgresql-16-pgvector`: Enables efficient storage and retrieval of vector embeddings.
    * `postgresql-16-pg-failover-slots`: Facilitates seamless failover in high-availability setups.
* **Barman Cloud Integration:** Integrates `barman-cloud` for cloud-based backup and recovery.
* **Default Polish Locale:** Sets the default locale to `pl_PL.UTF-8`.
* **Postgres User ID:** Assigns the postgres user a UID of 26.

## Operational Use

As this image is derived from `sourcemation/postgres-16`, it can be used
similarly. However, its primary purpose is CNPG deployments.

**Example for local testing (not suitable for production):**

```bash
docker run --rm -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 sourcemation/cnpg-16:latest
```

**Integration with Cloud Native PostgreSQL:**

Consult the official Cloud Native PostgreSQL documentation for instructions on
utilizing custom images.

## Locale Configuration

The images support following locales en_US.UTF-8 (default), pl_PL.UTF-8. To
modify the locale in a child image, override the `LANG` environment variable
and regenerate the locale settings.


**Example Dockerfile snippet for switching to `ja_JP.UTF-8` (Japanese) locale:**

```dockerfile
FROM sourcemation/cnpg-16

# Change locale to ja_JP.UTF-8
RUN localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8; \
    sed -i -e 's/ja_JP/ja_JP/g' /etc/locale.gen && locale-gen
ENV LANG=ja_JP.UTF-8
```

## Key Environment Variables

This image utilizes:

```bash
LANG=en_US.UTF-8
PG_MAJOR=16
PATH=$PATH:/usr/lib/postgresql/$PG_MAJOR/bin
PGDATA=/var/lib/postgresql/data
PG_VERSION=16.X.Y # Example: 16.8-1.pgdg120+2
GOSU_VERSION=1.17
```

Customize the initial superuser and database using `POSTGRES_USER`,
`POSTGRES_PASSWORD`, and `POSTGRES_DB`. Refer to the official PostgreSQL Docker
documentation for details.

## Port Exposure

Port `5432`, the standard PostgreSQL port, is exposed by default.

## Contributions and Issue Reporting

Contributions are welcome! Propose new features by creating issues or submit
pull requests on the SourceMation GitHub repository.

[Creating issues and image requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/cnpg-16` image is independent of the
PostgreSQL Global Development Group. Trademarks mentioned are owned by their
respective entities. This image is a separate project maintained by
[SourceMation](https://sourcemation.com).

## Additional Information

### Image Component Risk Analysis

Detailed risk analysis reports for our images and their components are
available on the [SourceMation platform](https://www.sourcemation.com/).

Note: Risk analysis reports are not yet available for all images. Contact us
for additional software components or inquiries.

### Licensing

The core license for PostgreSQL is the [PostgreSQL
License](https://www.postgresql.org/about/licence/).

Cloud Native PostgreSQL containers are licensed under the [Apache License
2.0](https://github.com/cloudnative-pg/postgres-containers/blob/main/LICENSE).


