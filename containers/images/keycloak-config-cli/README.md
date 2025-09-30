# Keycloak Config CLI packaged by SourceMation

> This image provides the `keycloak-config-cli` tool, a powerful utility for managing Keycloak configuration as code.

This Keycloak Config CLI distribution is provided by the upstream Keycloak Config CLI packaging team.

## Usage

Run a container with the Keycloak Config CLI

```
docker run \
    -e KEYCLOAK_MAJOR_VERSION="26" \
    -e KEYCLOAK_URL="http://<your keycloak host>:8080/" \
    -e KEYCLOAK_USER="<keycloak admin username>" \
    -e KEYCLOAK_PASSWORD="<keycloak admin password>" \
    -e IMPORT_FILES_LOCATIONS='/config/*' \
    -v <your config path>:/config/ \
    sourcemation/keycloak-config-cli
```
## Key Environment Variables

This container uses the following environment variables for configuration:

| Variable | Description | Example |
| :--- | :--- | :--- |
| **`KEYCLOAK_MAJOR_VERSION`** | **Optional.** Major version of Keycloak server to connect to. | `26` |
| **`KEYCLOAK_URL`** | **Required.** The full URL of the Keycloak server to connect to. | `http://keycloak.local:8080` |
| **`KEYCLOAK_USER`** | **Required.** The username for the Keycloak admin account. | `admin` |
| **`KEYCLOAK_PASSWORD`** | **Required.** The password for the Keycloak admin account. | `password` |
| **`IMPORT_FILES_LOCATIONS`** | **Required for import.** Tells the tool to perform an import. The value is the path **inside the container** where the configuration files are located. Use wildcards like `*` to import all files in a directory. | `/config/my-realm.json` or `/config/*` |

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
