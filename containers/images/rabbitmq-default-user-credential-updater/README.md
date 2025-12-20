# RabbitMQ Default User Credential Updater packaged by Sourcemation

> A utility tool for updating default RabbitMQ user credentials in containerized environments.

This RabbitMQ Default User Credential Updater distribution is provided by the upstream Sourcemation packaging team.

## Usage

Run a temporary container with the RabbitMQ Default User Credential Updater

```
docker run --rm -it sourcemation/rabbitmq-default-user-credential-updater:latest --help
```

## Image tags and versions

The `sourcemation/rabbitmq-default-user-credential-updater` image itself comes in `debian-13` flavor.  The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
APP_NAME="rabbitmq-default-credential-updater"
APP_VERSION="1.0.10"
```

This image exposes the following ports: 

- No ports are exposed by this utility container

Please note that this is a utility container that connects to an existing RabbitMQ instance and does not expose any ports itself.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the Sourcemation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/rabbitmq-default-user-credential-updater` image is not affiliated with the RabbitMQ team or Broadcom Inc. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/rabbitmq-default-user-credential-updater` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [Sourcemation platform](https://sourcemation.com/catalog/rabbitmq-default-user-credential-updater).

For more information, check out the [overview of RabbitMQ](https://www.rabbitmq.com/) page.

### Licenses

The base license for the solution (RabbitMQ Default User Credential Updater) is the [MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/). The licenses for each component shipped as part of this image can be found on [the image's appropriate Sourcemation entry](https://sourcemation.com/catalog/rabbitmq-default-user-credential-updater).
