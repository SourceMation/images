# Redis packaged by SourceMation

Redis is a performant in-memory key-value database. Its simplicity, accompanied
by optimal data structures, contribute to the high operational speed.

This Redis distribution is provided by the downstream Rocky Linux 9 packaging
team in the version respective to that system (7.2.7). Due to licensing
changes, an up-to-date release will be provided as a separate product.

## Usage

Run a temporary container with Redis, ready to accept connections from your
localhost's `redis-cli`:

```
docker run -p 6379:6379 --rm --ulimit nofile=64000:64000 --ulimit nproc=64000:64000 -it sourcemation/redis:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
APP_VERSION="XXX - set during build"
APP_NAME="redis"
```

This image exposes the following ports: 

- 6379 : the default Redis port for remote connections

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/redis` image is not affiliated with Redis
Ltd. The respective companies and organisations own the trademarks mentioned in
the offering. The `sourcemation/redis` image is a separate project and is
maintained by [SourceMation](https://sourcemation.com).

## Extra notes

The server runs as the system user and group `redis`, them having UID 998 and
GID 996.

As of March 20, 2024, [Redis has changed their
licensing](https://redis.io/blog/redis-adopts-dual-source-available-licensing/),
starting with Redis 7.4. This image ships version 7.2.7, which is unaffected by
this change. Newer releases will be provided as separate products.

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation
platform](https://www.sourcemation.com/products/7e370e6a-baad-4b48-8e85-bdc7504cf06d/deployments).

For more information, check out the [overview of
Redis](https://redis.io/about/) page.

### Licenses

The base license for the solution (Redis version 7.2.7) is BSD/MIT. The
licenses for each component shipped as part of this image can be found on [the
image's appropriate SourceMation
entry](https://www.sourcemation.com/products/7e370e6a-baad-4b48-8e85-bdc7504cf06d/deployments).
