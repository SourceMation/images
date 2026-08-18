# NGINX Ingress Controller packaged by Sourcemation

> The NGINX Ingress Controller for Kubernetes using NGINX as a reverse proxy and load balancer.

## Important Note: NGINX Ingress Controller v1.15 is End-of-Life (EOL)

This NGINX Ingress Controller distribution, version v1.15.1, is provided specifically for
compatibility workflows that require this specific version. **The upstream `kubernetes/ingress-nginx`
project officially reached End-of-Life in March 2026, and the repository was archived. It no longer
receives security updates or bug fixes.**

While the NGINX Ingress Controller application itself is EOL and archived, this Sourcemation image is
built on our regularly updated and patched `sourcemation/debian-13-slim` base
image. This ensures that the underlying system components are current, even
though the application itself is deprecated.

This distribution contains the binary from the community Kubernetes Ingress NGINX project, packaged with standard Debian NGINX.

## Usage

Run a temporary container with the NGINX Ingress Controller to see help:

```bash
docker run --rm -it sourcemation/nginx-ingress-controller:latest --help
```

### Advanced usage examples

Typically, this image is used as part of a Kubernetes deployment (Ingress Controller).

## Image tags and versions

The `sourcemation/nginx-ingress-controller` image is based on `sourcemation/debian-13-slim`.

## Environment Vars, Ports, Volumes

This image uses standard NGINX Ingress Controller flags and environment variables.

It typically binds to ports `80` and `443` for traffic, and `10254` for health checks.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/nginx-ingress-controller` image is not affiliated with
the Kubernetes project or NGINX Inc. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/nginx-ingress-controller` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation platform](https://sourcemation.com).

For more information, check out the [Kubernetes Ingress NGINX documentation](https://kubernetes.github.io/ingress-nginx/).

### Licenses

The base license for the solution (Ingress NGINX) is the Apache 2.0 License.
