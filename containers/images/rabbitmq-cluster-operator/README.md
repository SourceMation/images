# RabbitMQ-Cluster-Operator packaged by Sourcemation

RabbitMQ is a high-performant, scalable message broker for AMQP clients.

This container image provides the RabbitMQ Cluster Operator, a Kubernetes operator that automates the deployment and management of RabbitMQ clusters on Kubernetes.  

## Usage

Run a temporary container with the RabbitMQ Cluster Operator

```
docker run --rm -it sourcemation/rabbitmq-cluster-operator:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
APP_NAME="rabbitmq-cluster-operator"
APP_VERSION="2.17.0"
HOME=/home/rabbitmq-cluster-operator
```

This image does not expose any ports. However, you can expose the ports you need by using the `-p` option, setting up the ports manually, or with kubernetes or docker-compose. You can also create an image with the ports exposed by default.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/rabbitmq-cluster-operator` image is not affiliated with 
Broadcom, Inc. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/rabbitmq-cluster-operator` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

### Licenses

The base license for the solution (RabbitMQ Cluster Operator) is the [Mozilla Public
License Version 2.0 and Apache License Version
2.0](https://github.com/rabbitmq/rabbitmq-server/blob/main/LICENSE).  
