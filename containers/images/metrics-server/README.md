# Metrics Server packaged by Sourcemation

> Kubernetes Metrics Server is a scalable, efficient source of container resource metrics for Kubernetes built-in autoscaling pipelines.

This Metrics Server distribution is provided by the upstream Kubernetes SIG (Special Interest Group) Instrumentation packaging team in version 0.19.0.

## Usage

Run a temporary container with the Metrics Server

```
docker run --rm -it sourcemation/metrics-server --help
```

### Advanced usage examples

Run Metrics Server with custom configuration:

```bash
docker run -it sourcemation/metrics-server \
  --cert-dir=/usr/local/share/ca-certificates \
  --secure-port=8443 \
  --kubelet-insecure-tls \
  --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
```

## Image tags and versions

The `sourcemation/metrics-server` image itself comes in `debian-13` flavors. The tag `latest` refers to the Debian-based flavor.

## Ports

This image exposes the following ports: 

- **8443/TCP**: HTTPS port for serving metrics API (secure port)

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

### Volumes

- `/usr/local/share/ca-certificates`: CA certificates directory

### Default Command Arguments

The image comes with the following default arguments:

- `--cert-dir=/usr/local/share/ca-certificates`: Directory where TLS certs are stored
- `--secure-port=8443`: Port to bind the secure server to
- `--kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname`: Priority order for connecting to kubelet
- `--kubelet-use-node-status-port`: Use the port in the node status for connecting to kubelet
- `--metric-resolution=15s`: The resolution at which metrics-server will retain metrics

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/metrics-server` image is not affiliated with
the Kubernetes SIG Instrumentation team. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/metrics-server` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation
platform](https://sourcemation.com/catalog/metrics-server).

For more information, check out the [overview of
Metrics Server](https://github.com/kubernetes-sigs/metrics-server) page.

### Licenses

The base license for the solution (Metrics Server) is the
[Apache License 2.0](https://github.com/kubernetes-sigs/metrics-server/blob/master/LICENSE). The licenses for each component shipped as
part of this image can be found on [the image's appropriate Sourcemation
entry](https://sourcemation.com/catalog/metrics-server).
