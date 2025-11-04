# External Secrets packed by Sourcemation

This container image delivers the External Secrets, which is used to manage
secrets, with external providers, in Kubernetes clusters. It's independent
build of one of the most popular integrations for secrets management in
Kubernetes.

## How to replace the default External Secrets Image?

To replace the default External Secrets image installed, you have to edit the
`values.yaml` file of the `external-secrets` chart from the following

```yaml
(...)
image:
  repository: oci.external-secrets.io/external-secrets/external-secrets
  pullPolicy: IfNotPresent
  (...)
  # -- The image tag to use. The default is the chart appVersion.
  tag: ""
  (...)
  flavour: ""
```

To the following configuration:

```yaml
(...)
image:
  registry: docker.io # or quay.io
  repository: sourcemation/external-secrets
  (...)
  tag: ""
  (...)
(...)
```

You can also set tag to static one like `v0.18.0-20250620` to ensure that the image
is always the same - read the `Extra Notes` section below for more details. Empty tag
is also valid, and it will use the appVersion from the chart.


Alternatively, you can use the `--set` flag when installing the chart:

```bash
helm install external-secrets \
    external-secrets/external-secrets \
    -n external-secrets \
    --create-namespace \
    --set image.registry=docker.io \
    --set image.repository=sourcemation/external-secrets \
    --set image.tag=v0.18.0-20250620
```


## Why use this image?

This image comes with all the goodies of publicly built images from
Sourcemation and is based on newer Debian 13 instead of older Debian 12 (both
images are distroless). **This image is also regularly updated and rebuilt, so
you can be sure that your static binary is up to date with the latest security
fixes.**

## Extra notes

This image has a very narrow scope, and is not intended to be used as a single
image, but rather as part of the Helm charts installing the External Secret.

To understand how the External Secrets works, you can read the project
[Official Documentation](https://external-secrets.io/latest/).


**Note that the main tags like v0.18.0 are overwritten, even if the base
software does not change (but the go binary is rebuilt for security reasons),
so you can use more specific tags like v0.18.0-20250620 to ensure that you are
using the fixed version of the image.**

## Contributing and Issues

We welcome your contributions! If you have new feature requests, want to report
a bug, or wish to submit a pull request with your code or an image request, you
can do so via the Sourcemation GitHub repository for this image.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/Sourcemation/images/issues/new/choose)
- [Submit a pull request](https://github.com/Sourcemation/images/compare)

## Image and its components Risk Analysis report

The Sourcemation platform provides a detailed risk analysis report of the
images and their components. However, some images might not have them ready;
you can always create an issue to request them.

Visit the [Sourcemation website](https://sourcemation.com) to see the available
Open Source SCARM risk analysis reports.

## Licenses

The base license for the External Secrets is the Apache License 2.0, which is a
permissive license that allows for both personal and commercial use.
