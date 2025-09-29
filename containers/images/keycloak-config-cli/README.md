# Keycloak Config CLI packaged by SourceMation

> This image provides the `keycloak-config-cli` tool, a powerful utility for managing Keycloak configuration as code.

This Keycloak Config CLI distribution is provided by the upstream Keycloak Config CLI packaging team.

## Usage

Run a temporary container with the Keycloak Config CLI

```
docker run --rm -it sourcemation/keycloak-config-cli:latest
```

## Image tags and versions

The `sourcemation/keycloak-config-cli` image itself comes in `debian-12` flavor.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
CLI_HOME=/opt/keycloak-config-cli
```

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/keycloak-config-cli` image is not affiliated with
the Keycloak Config CLI. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/keycloak-config-cli` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://sourcemation.com/).

For more information, check out the [Keycloak Config CLI](https://adorsys.github.io/keycloak-config-cli/) page.

### Licenses

The base license for the solution (Keycloak Config CLI) is the
[Apache License 2.0](https://github.com/adorsys/keycloak-config-cli/blob/main/LICENSE.txt). The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/).
