# OAuth2 Proxy packaged by Sourcemation

> A reverse proxy that provides authentication with Google, Azure, OpenID Connect and many more identity providers.

This OAuth2 Proxy distribution is compiled and packaged by Sourcemation, based on the upstream source code.

## Usage

Run a temporary container with the OAuth2 Proxy

```docker
docker run --rm -it sourcemation/oauth2-proxy:latest --help
```

### Advanced usage examples

To run with a config file:

```bash
docker run --rm -it \
  -v $(pwd)/oauth2-proxy.cfg:/etc/oauth2-proxy.cfg \
  sourcemation/oauth2-proxy:latest \
  --config /etc/oauth2-proxy.cfg
```

## Image tags and versions

The `sourcemation/oauth2-proxy` image is based on `sourcemation/debian-13-slim` and is compiled from source.

## Environment Vars, Ports, Volumes

This image uses the standard OAuth2 Proxy environment variables. See [OAuth2 Proxy Configuration](https://oauth2-proxy.github.io/oauth2-proxy/docs/configuration/overview) for details.

This image typically listens on port `4180`.

Please note that the ports need to be either manually forwarded with the
-p option or let Docker choose some for you with the -P option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/oauth2-proxy` image is not affiliated with
the OAuth2 Proxy project. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/oauth2-proxy` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation platform](https://sourcemation.com).

For more information, check out the [overview of OAuth2 Proxy](https://oauth2-proxy.github.io/oauth2-proxy/).

### Licenses

The base license for the solution (OAuth2 Proxy) is the MIT License.
