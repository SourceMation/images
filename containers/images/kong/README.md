# Kong Community Edition packaged by Sourcemation

This image uses the official Kong Community Edition package and deploys it on
Rocky Linux 9. The following changes were made to the original image:

- Unsupported by OCI `HEALTHCHECK` instruction was removed from the Dockerfile.
- Kong is started with the `start` command instead of `docker-start`

## Usage

Deploying Kong requires multiple steps. Please use the official documentation.
You can safely skip the license part as this is the community edition.

- [Kong installation on Kubernetes](https://docs.konghq.com/gateway/3.7.x/install/kubernetes/)
- [Kong installation on Docker](https://docs.konghq.com/gateway/3.7.x/install/docker/)

To use this image, replace the official image mentioned in the official
documentation with `sourcemation/kong:latest`.

## Environment Vars, Ports, Volumes

This image exposes the following ports:

- 8000
- 8001
- 8002
- 8003
- 8004
- 8443
- 8444
- 8445
- 8446
- 8447

Please note that the ports need to be either manually forwarded with the `-p`
option or let Docker choose some for you with the `-P` option. Refer to the
[Kong installation instructions](#usage) for more information.

## Contributions and Issue Reporting

Contributions are welcome! Propose new features by creating issues or submit
pull requests on the Sourcemation GitHub repository.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)


**Disclaimer:** The `sourcemation/kong` image is not affiliated with Kong,
Inc.. The respective companies and organisations own the trademarks mentioned
in the offering. The `sourcemation/kong` image is a separate project and is
maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

- Problem with docker-start -> [GitHub
  Issue](https://github.com/Kong/docker-kong/issues/224)
- `HEALTHCHECK` is not part of OCI but still mentioned as optional in official
  specs -> [GitHub Issue with
discussion](https://github.com/opencontainers/image-spec/issues/749)
- Instead of `HEALTHCHECK`,  startup, readiness, and liveness probes should be
  used in Kubernetes -> [Kubernetes
Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- Both the upstream Kong developers and the Rocky Linux developers do **not**
  support these images. They are built for Sourcemation.

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the Sourcemation platform.

For more information, check out the [official Kong
documentation](https://docs.konghq.com/).

### Licenses

The base license for the solution (Kong Community Edition) is the [Apache
License, Version 2.0](https://github.com/Kong/kong/blob/master/LICENSE). The
licenses for each component shipped as part of this image can be found on the
image's appropriate Sourcemation entry.
