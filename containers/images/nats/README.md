# NATS Server packaged by Sourcemation

> A simple, secure and performant communications system for digital systems, services and devices.

This distribution contains the NATS Server binaries.

## Usage

Run a temporary container with the NATS Server:

```bash
docker run --rm -p 4222:4222 -p 8222:8222 sourcemation/nats:latest
```

## Image tags and versions

The `sourcemation/nats` image is based on `sourcemation/debian-13-slim`.

## Environment Vars, Ports, Volumes

- **Ports**: 
    - `4222`: NATS client port
    - `8222`: HTTP monitoring port
    - `6222`: Clustering port
- **Volumes**:
    - `/etc/nats`: Configuration directory

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/nats` image is not affiliated with
the NATS project. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/nats` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation platform](https://sourcemation.com).

For more information, check out the [NATS documentation](https://docs.nats.io/).

### Licenses

The base license for the solution is the Apache 2.0 License.
