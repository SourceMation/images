# RabbitMQ-4 packaged by SourceMation

RabbitMQ is a high-performant, scalable message broker for AMQP clients.

This image contains RabbitMQ Server version 4 running on Debian 12 Slim. It's built on top of the latest stable Erlang image to ensure compatibility and optimal performance.

## Usage

Run a temporary container with the RabbitMQ

```
docker run --rm -it sourcemation/rabbitmq-4:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
APP_NAME="rabbitmq-4"
APP_VERSION="4.0.8"
HOME=/var/lib/rabbitmq
RABBITMQ_DATA_DIR=/var/lib/rabbitmq
RABBITMQ_HOME=/opt/rabbitmq
PATH=/opt/rabbitmq/sbin:/opt/erlang/bin:/opt/openssl/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=C.UTF-8
LANGUAGE=C.UTF-8
LC_ALL=C.UTF-8
```

This image exposes the following ports: 

- 4369 : the Erlang Port Mapping Daemon port
- 5671 : the default port for AMQP clients (HTTPS)
- 5672 : the default port for AMQP clients (HTTP)
- 15691 : the Prometheus exporter API port (HTTPS)
- 15692 : the Prometheus exporter API port (HTTP)
- 25672 : the Erlang distribution server port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

This image uses the following volumes:

- `/var/lib/rabbitmq`

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/rabbitmq-4` image is not affiliated with
the Broadcom. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/rabbitmq-4` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

### Licenses

The base license for the solution (RabbitMQ Server) is the [Mozilla Public
License Version 2.0 and Apache License Version
2.0](https://github.com/rabbitmq/rabbitmq-server/blob/main/LICENSE).  
The Erlang licence is the [Apache License 2.0](https://raw.githubusercontent.com/erlang/otp/refs/heads/master/LICENSE.txt).  
The OpenSSL licence is [Apache License 2.0](https://raw.githubusercontent.com/openssl/openssl/refs/heads/master/LICENSE.txt).  
The Debian licence is the  [GNU General Public License v3.0](https://raw.githubusercontent.com/bibledit/debian/refs/heads/main/LICENSE).