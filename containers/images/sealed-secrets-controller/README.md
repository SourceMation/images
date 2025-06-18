# Sealed Secrets Controller packed by SourceMation

This container image delivevers the Sealed Secret Controller, which is used to
manage sealed secrets in Kubernetes clusters. It's independent build of the one
of most popular way to manage secrets in Kubernetes.

## How to replace the default Sealed Secret Controller

To replace the default Sealed Secret Controller installed you have to edit the
`values.yaml` file of the `sealed-secrets` chart from the following

```yaml
(...)
image:
  registry: docker.io
  repository: bitnami/sealed-secrets-controller
  tag: 0.30.0
(...)
```

To the

```yaml
(...)
image:
  registry: docker.io
  repository: sourcemation/sealed-secrets-controller
  tag: 0.30.0
(...)
```

or you can use the `--set` flag when installing the chart:

```bash
helm install sealed-secrets bitnami/sealed-secrets \
  --set image.registry=docker.io \
  --set image.repository=sourcemation/sealed-secrets-controller \
  --set image.tag=0.30.0
```

## Why use this image?

This image comes with all the goodies of publicly built images from
SourceMation and is based on newer Debian 12 instead of older Debian 11 (both
images are distroless). **This image is also regularly updated and rebuilt, so
you can be sure that your static binary is up to date with the latest security
fixes.**

## Extra notes

This image has very narrow scope, and it not intended to be used as single
image, but rather as the part of Helm charts installing the Sealed Secrets :).

To understand how Sealed Secrets works, should read the official documentation
in the main repository [Official Sealed Secrets GitHub
Repository](https://github.com/bitnami-labs/sealed-secrets#overview)


**Note that the main tags like v0.30.0 are overwritten, even if the base
software does not change (but the go binary is rebuilt for security reasons),
so you can use more specific tags like v0.30.0-20250608 to ensure that you are
using the fixed version of the image.**

## Image and its components Risk Analysis report

The Sourcemation platform provides a detailed risk analysis report of the
images and their components. However, some images might not have them ready;
you can always create an issue to request them.

Visit the [SourceMation website](https://sourcemation.com) to see the available
Open Source SCARM risk analysis reports.

## Licenses

The base license for the Sealed Secret Controller is the Apache License 2.0,
which is a permissive license that allows for both personal and commercial use.
