# Redis sentinel packaged by SourceMation

Redis is a performant in-memory key-value database. Its simplicity, accompanied
by optimal data structures, contribute to the high operational speed.

Built by SourceMation's automation team, this Redis release undergoes regular
updates, following the official `stable` release. The foundation is the latest
`sourcemation/debian-12-slim` image at build time, ensuring a compact, secure,
and current setup.

## Usage

Run a temporary container with Redis, ready to accept connections from your
localhost's `redis-cli`:

```
docker run -p 26379:26379 --rm --ulimit nofile=64000:64000 --ulimit nproc=64000:64000 -it sourcemation/redis-sentinel:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
REDIS_PORT=26379
```

This image exposes the following ports:

- 26379 : the default Redis sentinel port for remote connections

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

**The server runs as the system user and group `redis` with UID 1000 and GID
1000.** Our older images were using UID 998 and GID 998. The new (1000/1000)
user/group is more compatible with other Redis images.

As of March 20, 2024, [Redis has changed its
licensing](https://redis.io/blog/redis-adopts-dual-source-available-licensing/).

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation
platform](https://www.sourcemation.com/products/7e370e6a-baad-4b48-8e85-bdc7504cf06d/deployments).

For more information, check out the [overview of
Redis](https://redis.io/about/) page.