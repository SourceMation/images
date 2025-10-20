# Rabbitmq Messaging Topology Operator packaged by SourceMation

> The RabbitMQ Messaging Topology Operator manages RabbitMQ messaging topologies within a Kubernetes cluster using the Operator pattern. It allows you to declare RabbitMQ resources such as queues, exchanges, bindings, users, and policies as Kubernetes custom resources.

This RabbitMQ Messaging Topology Operator distribution is provided by the upstream SourceMation packaging team.

## Usage

Run a temporary container with the rabbitmq-messaging-topology-operator

```bash
docker run --rm -it sourcemation/rabbitmq-messaging-topology-operator --help
```

## Image tags and versions

The `sourcemation/rabbitmq-messaging-topology-operator` image is built from `scratch`.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
APP_NAME="rabbitmq-messaging-topology-operator"
APP_VERSION="1.18.0"
```

This image does not expose any ports. However, you can expose the ports you need by using the `-p` option, setting up the ports manually, or with kubernetes or docker-compose. You can also create an image with the ports exposed by default.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/rabbitmq-messaging-topology-operator` image is not affiliated with
Broadcom Inc. or VMware (original RabbitMQ maintainers). The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/rabbitmq-messaging-topology-operator` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://sourcemation.com/images/rabbitmq-messaging-topology-operator).

For more information, check out the [overview of
RabbitMQ Messaging Topology Operator](https://github.com/rabbitmq/messaging-topology-operator) page.

### Licenses

The base license for the solution (RabbitMQ Messaging Topology Operator) is the
[Mozilla Public License 2.0 (MPLv2)](https://www.mozilla.org/en-US/MPL/2.0/). The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/images/rabbitmq-messaging-topology-operator).