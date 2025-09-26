# Hugo Container on Debian 12 Slim packed by SourceMation

This image, `sourcemation/hugo`, is built on a minimal Debian base to provide **Hugo** environment (extended+withdeploy). Hugo is one of the world's most popular open-source static site generators, famous for its incredible speed and flexibility. Written in Go, it takes content files like markdown and uses powerful templating to render a complete, ready-to-deploy website in a fraction of a second.

Maintained by the SourceMation automation team, this Hugo distribution is regularly updated to ensure it's current, secure, and compact. It's built on a minimal Debian Slim base, and cryptographic signatures are used during the build process to guarantee the integrity of all source code and packages.

-----

## Core Features

  * **Blazing-Fast Performance:** Its world-class build speed accelerates development and delivers an incredibly fast user experience, which is crucial for SEO and visitor retention.
  * **Flexible Content & Data Modeling:** Its powerful templating engine provides unparalleled flexibility, allowing any design to be implemented and content to be pulled from local files or external APIs.
  * **Unmatched Security & Scalability:** By generating a static site with no live database, it offers incredible security and can be hosted on a global CDN to handle massive traffic at a very low cost.

-----

## Operational Use

This image is intended for building static websites using Hugo static site generator.

**Example for a local, non-production test:**

Running

```bash
docker run --rm -v my_website_src:/src:Z -p 1313:1313 sourcemation/hugo
```

is a shorthand for:

```bash
docker run --rm -v my_website_src:/src:Z -p 1313:1313 sourcemation/hugo server -D --bind 0.0.0.0 --baseURL /
```

The default runs Hugo server (drafts included) in a container, mapping port `1313` to the default Hugo port `1313` and binds it to 0.0.0.0, setting baseURL for easy dev access.
Please remember to mount `my_website_src` (preferably, utilizing the `:Z` flag) so that hugo has content to work with.

To override these defaults, please provide arguments in full, e.g.
```bash
docker run --rm sourcemation/hugo version
```

will just print the version.

-----

## Configuration via Volume Mounts

This container is typically configured by mounting your files into it.

  * **Your project:** Mount your website sources to `/src`.

-----

## Port Exposure
Hugo image exposes port **1313**.


## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/hugo` image is not affiliated with Hugo. The respective companies and
organisations own the trademarks mentioned in the offering. The `sourcemation/hugo` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### More Information
For more information on Hugo, check out [their website](https://gohugo.io).

### Licenses

The base license for Hugo is [Apache 2.0 License](https://gohugo.io/about/license/)
