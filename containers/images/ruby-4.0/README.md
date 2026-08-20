# Ruby 4.0 packaged by Sourcemation

An open source purely object-oriented programming language with a focus on
simplicity and readability. Ruby 4.0 introduces performance improvements, YJIT
optimizations, and modernized language features.

This Ruby distribution is built from official source distributions by the
Sourcemation automation team. It is based on the `sourcemation/debian-13-slim`
base image, providing a highly optimized, clean, and secure environment.

## Usage

Run a temporary container with the Ruby REPL (`irb`) (don't forget the
`-it` argument).

```bash
docker run --rm -it sourcemation/ruby-4.0:latest
```

### Advanced usage examples

Example: create a Gemfile for a Ruby project, in your current directory:

```bash
docker run --rm -v "${PWD}:/your-project" -w "/your-project" sourcemation/ruby-4.0:latest bundle init
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/bundle/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
GEM_HOME="/usr/local/bundle"
BUNDLE_APP_CONFIG="/usr/local/bundle"
APP_VERSION="4.0.6"
APP_NAME="ruby-4.0"
```

This image exposes no ports by default.

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We welcome your contributions! If you have new feature requests, want to report
a bug, or wish to submit a pull request with your code or an image request, you
can do so via the Sourcemation GitHub repository for this image.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/Sourcemation/images/issues/new/choose)
- [Submit a pull request](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/ruby-4.0` image is not affiliated with
Yukihiro Matsumoto and the Ruby Community [the Ruby
Community](https://www.ruby-lang.org/en/community/). The respective
entities own the trademarks mentioned in the offering. The
`sourcemation/ruby-4.0` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation
platform](https://www.sourcemation.com).

For more information, check out the [overview of
Ruby](https://www.ruby-lang.org/en/about/) page.

### Licenses

The base license for the solution (Ruby) is the [Ruby
License](https://www.ruby-lang.org/en/about/license.txt). The licenses
for each component shipped as part of this image can be found on [the
image's appropriate Sourcemation
entry](https://www.sourcemation.com).
