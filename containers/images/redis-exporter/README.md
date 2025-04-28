# Redis exporter packaged by SourceMation

Prometheus Exporter for Redis Metrics. Supports Redis 2.x, 3.x, 4.x and 5.x

## Usage

Run a Redis exporter docker image that contains only the exporter binary:

```
docker run -d --name redis_exporter -p 9121:9121 sourcemation/redis-exporter:latest
```

If you try to access a Redis instance running on the host node, you'll need to add --network host so the redis_exporter container can access it:

```
docker run -d --name redis_exporter --network host oliver006/redis_exporter
```

## What's exported
Most items from the INFO command are exported, see Redis documentation for details.
In addition, for every database there are metrics for total keys, expiring keys and the average TTL for keys in the database.
You can also export values of keys by using the `-check-keys` (or related) flag. The exporter will also export the size (or, depending on the data type, the length) of the key. This can be used to export the number of elements in (sorted) sets, hashes, lists, streams, etc. If a key is in string format and matches with `--check-keys` (or related) then its string value will be exported as a label in the `key_value_as_string` metric.

If you require custom metric collection, you can provide comma separated list of path(s) to Redis Lua script(s) using the `-script` flag. If you pass only one script, you can omit comma.

### The redis_memory_max_bytes metric
The metric `redis_memory_max_bytes` will show the maximum number of bytes Redis can use.
It is zero if no memory limit is set for the Redis instance you're scraping (this is the default setting for Redis).
You can confirm that's the case by checking if the metric `redis_config_maxmemory` is zero or by connecting to the Redis instance via redis-cli and running the command `CONFIG GET MAXMEMORY`.

## Command line flags
Full list of the flags can be found on [here](https://github.com/oliver006/redis_exporter/blob/master/README.md#command-line-flags).

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
APP_VERSION="XXX - set during build"
APP_NAME="redis-exporter"
```

This image exposes the following ports: 

- 9121 : the default Redis exporter web interface and telemetry port

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