# Redis Exporter packaged by SourceMation

The `redis-exporter` acts as a helpful informant for your Redis server,
diligently gathering key performance indicators regarding its operation and
well-being. It then presents this information in a structured manner that
Prometheus can readily comprehend, thus enabling insightful monitoring and
timely alerts through Grafana. In essence, it provides a clear and concise
overview of your Redis's status, facilitating proactive management.


This image is built from `scratch`, meaning it’s distroless with a single
binary (statically compiled) image.


## Usage

Run a Redis exporter docker image that contains only the exporter binary:

```
docker run -d --name redis_exporter -p 9121:9121 sourcemation/redis-exporter:latest
```

If you try to access a Redis instance running on the host node, you'll need to
add --network host so the redis_exporter container can access it:

```
docker run -d --name redis_exporter --network host sourcemation/redis-exporter:latest
```

## Command line flags

The full list of the flags can be found on
[here](https://github.com/oliver006/redis_exporter/blob/master/README.md#command-line-flags).

## Environment Vars, Ports, Volumes

This image does not expose any environment variables or volumes.

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

It is loosely based on the `oliver006/redis_exporter` image, which publicly
available here https://hub.docker.com/r/oliver006/redis_exporter/ .


**This image is drop-in replacement for the `oliver006/redis_exporter` image,
please consult upstream documentation for more information about redis exporter
project/binary and its usage.**


### Image and its components Risk Analysis report

A detailed risk analysis report of our images and its components might be found
on the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [GitHub project
page](https://github.com/oliver006/redis_exporter)

### Licenses

The project is MIT-licensed.
