# Hugo Container on Debian 12 Slim packed by SourceMation

This image, `sourcemation/hugo`, is built on a minimal Debian base to provide
**Hugo** environment (extended+withdeploy) with Sass/Dart and NodeJS. Hugo is
one of the world's most popular open-source static site generators, famous for
its incredible speed and flexibility. Written in Go, it takes content files
like markdown and uses powerful templating to render a complete,
ready-to-deploy website in a fraction of a second.

Maintained by the SourceMation automation team, this Hugo distribution is
regularly updated to ensure it's current, secure, and compact. It's built on a
minimal Debian Slim base, and cryptographic signatures are used during the
build process to guarantee the integrity of all source code and packages.

## Usage

This image is intended for building static websites using Hugo static site generator.

**Example for a local, non-production test:**

To create a new project:

```bash
mkdir my_website_src && docker run -u "$(id -u):$(id -g)" --rm -v ./my_website_src:/src:Z sourcemation/hugo hugo new site /src
```

This will create `my_website_src` on your host with default hugo project layout, with current user's ownership.

To live-run Hugo server with this project (for development):

```bash
docker run -u "$(id -u):$(id -g)" --rm -v ./my_website_src:/src:Z -p 1313:1313 sourcemation/hugo
```

This is a shorthand for:
```bash
docker run -u "$(id -u):$(id -g)" --rm -v ./my_website_src:/src:Z -p 1313:1313 sourcemation/hugo hugo server -D --bind 0.0.0.0
```

This default runs Hugo server (drafts included) in a container, mapping port `1313` to the default Hugo port `1313` and binds it to 0.0.0.0.
Please remember to mount `./my_website_src` so that hugo has content to work with.

To build Hugo website:

```bash
docker run -u "$(id -u):$(id -g)" --rm -v ./my_website_src:/src:Z sourcemation/hugo hugo build
```

## Image tags and versions

The `sourcemation/hugo` image itself comes in flavor: `debian-12`.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image is typically configured by mounting your files into it.

- Mount your website sources to `/src`.

This image exposes the following ports: 

- 1313 - Hugo server port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/hugo` image is not affiliated with Hugo. The respective companies and
organisations own the trademarks mentioned in the offering. The `sourcemation/hugo` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation platform](https://sourcemation.com).

For more information, check out [project page](https://gohugo.io).

### Licenses

The base license for Hugo is [Apache 2.0 License](https://gohugo.io/about/license/)
The licenses for each component shipped as
part of this image can be found on [SourceMation](https://sourcemation.com).
