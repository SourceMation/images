# RabbitMQ packaged by SourceMation

RabbitMQ is a high-performant, scalable message broker for AMQP clients.

This image contains the RabbitMQ Server version 3.11.10 distribution packaged
and provided by SourceMation.

## Usage

Run a temporary container with RabbitMQ

```
docker run --rm -it sourcemation/rabbitmq:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/sbin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
LANG="C.UTF-8"
LANGUAGE="C.UTF-8"
LC_ALL="C.UTF-8"
RABBITMQ_LOGS="-"
RABBITMQ_DATA_DIR="/var/lib/rabbitmq"
APP_VERSION="3.11.10"
APP_NAME="rabbitmq"
```

This image exposes the following ports: 

- 4369 : the Erlang Port Mapping Daemon port
- 5671 : the default port for AMQP clients (HTTPS)
- 5672 : the default port for AMQP clients (HTTP)
- 15691 : the Prometheus exporter API port (HTTPS)
- 15692 : the Prometheus exporter API port (HTTP)
- 25672 : the Erlang distribution server port
- 15671 : the RabbitMQ Management UI (HTTPS)
- 15672 : the RabbitMQ Management UI (HTTP)

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/rabbitmq` image is not affiliated with
Broadcom, Inc. The respective companies and organisations own the trademarks
mentioned in the offering. The `sourcemation/rabbitmq` image is a separate
project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation
platform](https://www.sourcemation.com/products/2630e078-ddb3-4845-aacd-d054190c7912/deployments).

For more information, check out the [Getting Started tutorials on the RabbitMQ
official website](https://www.rabbitmq.com/tutorials) page.

### Licenses

The base license for the solution (RabbitMQ Server) is the [Mozilla Public
License Version 2.0 and Apache License Version
2.0](https://github.com/rabbitmq/rabbitmq-server/blob/v3.11.10/LICENSE) . The
licenses for each component shipped as part of this image can be found on [the
image's appropriate SourceMation entry](https://www.sourcemation.com/products/2630e078-ddb3-4845-aacd-d054190c7912/deployments).
