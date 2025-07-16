# Redis Operator packaged by SourceMation

A Golang based redis operator that will make/oversee Redis standalone and 
cluster mode setup on top of the Kubernetes. It can create a redis cluster 
setup with best practices on Cloud as well as the Bare metal environment. 
Also, it provides an in-built monitoring capability using redis-exporter.

Built by SourceMation's automation team, this Redis release undergoes regular
updates, following the official `stable` release. The foundation is the latest
distroless image at build time, ensuring a compact, secure and current setup.

## Usage

Run a temporary container with the Redis Operator

```
docker run --rm -it sourcemation/redis-operator:latest
```

## Environment Vars, Ports, Volumes

This image does not expose any environment variables, ports or volumes.

## Contributions and Issue Reporting

Contributions are welcome! Propose new features by creating issues or submit
pull requests on the SourceMation GitHub repository.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/redis` image is not affiliated with Redis
Ltd. The respective companies and organisations own the trademarks mentioned in
the offering. The `sourcemation/redis` image is a separate project and is
maintained by [SourceMation](https://sourcemation.com).

## Extra notes

Redis operator requires a Kubernetes cluster of version `>=1.18.0`. If you have just started with Operators, it's highly recommended using the latest version of Kubernetes.

As of March 20, 2024, [Redis has changed its
licensing](https://redis.io/blog/redis-adopts-dual-source-available-licensing/).

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation
platform](https://www.sourcemation.com/products/7e370e6a-baad-4b48-8e85-bdc7504cf06d/deployments).

For more information, check out the [overview of
Redis](https://redis.io/about/) page.
