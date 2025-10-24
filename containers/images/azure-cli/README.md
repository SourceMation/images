# Azure CLI packaged by SourceMation

> Azure CLI is Microsoft's command-line tool that provides a great experience for managing Azure resources.

This Azure CLI distribution is provided by the upstream Microsoft packaging team.

## Usage

Run a temporary container with the Azure CLI and help option

```bash
docker run --rm -it sourcemation/azure-cli az --help
```

### Advanced usage examples

#### Mount Azure credentials from host

```bash
docker run --rm -it \
  -v ~/.azure:/home/azure-cli/.azure \
  sourcemation/azure-cli /bin/bash
```

## Image tags and versions

The `sourcemation/azure-cli` image itself comes in `debian-12` flavor. The tag `latest` refers to the Debian-based flavor.

## Ports

This image exposes no network ports as Azure CLI is a command-line tool that makes outbound HTTPS connections to Azure APIs.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the SourceMation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/azure-cli` image is not affiliated with Microsoft Corporation. Microsoft and Azure are trademarks of Microsoft Corporation. The `sourcemation/azure-cli` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [SourceMation platform](https://sourcemation.com/catalog/azure-cli).

For more information, check out the [overview of Azure CLI](https://docs.microsoft.com/en-us/cli/azure/) page.

### Licenses

The base license for the solution (Azure CLI) is the [MIT License](https://github.com/Azure/azure-cli/blob/dev/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate SourceMation entry](https://sourcemation.com/catalog/azure-cli).
