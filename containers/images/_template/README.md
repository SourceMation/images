# <APP_NAME> packaged by SourceMation

> <APP_NAME_OVERVIEW>

This <APP_NAME> distribution is provided by the [downstream Rocky
Linux 9 packaging team in the version respective to that system
(<APP_VERSION>)|upstream <APP_VENDOR_NAME> packaging
team].

## Usage

Run a temporary container with the <APP_NAME>

```
docker run --rm -it sourcemation/<APP_NAME>:rocky-9
```

### Advanced usage examples

...

## Image tags and versions

The `sourcemation/<APP_NAME>` image itself comes in two flavors: `debian-12`
and `rocky-9`. The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
...
```

This image exposes the following ports: 

- ...

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/<APP_NAME>` image is not affiliated with
the <APP_VENDOR_NAME>. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/<APP_NAME>` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](<SOURCEMATION_LINK>).

For more information, check out the [overview of
<APP_NAME>](<APP_NAME_WEBSITE>) page.

### Licenses

The base license for the solution (<APP_NAME>) is the
[<APP_LICENSE>](<APP_LICENSE_URL>). The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](<SOURCEMATION_LINK>).
