# OpenAPI Generator CLI packaged by SourceMation

This image provides a CLI for the OpenAPI Generator project. It is based on the
Rocky Linux 9 base image.  The image uses `maven-3.8` as the default toolchain
from the official Rocky Linux 9 repository. Note that this DNF/YUM module is
not enabled by default in the base. Headless OpenJDK 21 is used as the default
Java runtime.

This image has `appuser` as the default user for security reasons.

**The images uses entrypoint similar to the one used in the official OpenAPI
image. The default executed command is `help` that prints the help message for
generator CLI JAR.**

This image also comes with a `openapi-generator-cli` script that simplifies
dealing with different versions of the OpenAPI Generator CLI JAR. The script is
installed in `/usr/local/bin` and is available in the PATH for the `appuser`.

## Usage

To generate code using the OpenAPI Generator CLI, for
[petstore.yaml](https://raw.githubusercontent.com/openapitools/openapi-generator/master/modules/openapi-generator/src/test/resources/3_0/petstore.yaml),
you can use the following command:

```bash
docker run -u root --rm -v $(pwd):/local sourcemation/openapi-generator-cli:latest generate -i /home/appuser/examples/petstore.yaml -g python -o /local/out
```

This command will generate a Python client in the `out` directory in current
working directory.

**In the examples above we are using `root` user to avoid permission issues
with volume mounts. Podman will still run container with user privileges. More
advanced deployment on Kubernetes should use `SecurityContext` to run container
with non-root user, and with volume mounts with proper permissions.**

To use different version of the OpenAPI Generator CLI JAR, you can use the
`openapi-generator-cli` script. For example, to generate code using the OpenAPI
Generator CLI JAR version 5.3.0, you can use the following command to get a
shell inside your container:

```bash
docker run -it -v $(pwd):/local sourcemation/openapi-generator-cli:latest /bin/bash
```

Then, inside the container, you can specify the `OPEN_API_GENERATOR_VERSION`
environment variable to set the version of the OpenAPI Generator CLI JAR:

```
export OPENAPI_GENERATOR_VERSION=4.3.1
openapi-generator-cli generate -i /local/petstore.yaml -g go -o ~/go-generated
```

This command will generate a Go client code in the `go-generated` directory in
the container user's home directory.


## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
GENERATOR_VERSION="7.7.0"
```

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/openapi-generator-cli` image is not
affiliated with the [OpenAPI Generator core
team](https://openapi-generator.tech/docs/core-team). The respective companies
and organisations own the trademarks mentioned in the offering. The
`sourcemation/openapi-generator-cli` image is a separate project and is
maintained by [SourceMation](https://sourcemation.com).

## Extra notes

- [The Project's Official Docker Image](https://hub.docker.com/r/openapitools/openapi-generator-cli/)
- [OpenAPI Generator Official Website](https://openapi-generator.tech/)

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the SourceMation platform.

For more information, check out the [OpenAPI Generator official
website](https://openapi-generator.tech/).

### Licenses

The base license for the solution (OpenAPI Generator) is the [Apache License,
Version
2.0](https://github.com/OpenAPITools/openapi-generator/blob/master/LICENSE).
The licenses for each component shipped as part of this image can be found on
the image's appropriate SourceMation entry.
