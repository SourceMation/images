# Ruby packaged by SourceMation

An open source purely object-oriented programming language with a focus on
simplicity and readability.

This Ruby distribution is provided by the downstream Rocky Linux 9
packaging team in the version respective to that system (3.0.7).

## Usage

Run a temporary container with the Ruby REPL (`irb`) (don't forget the
`-it` argument).

```
docker run --rm -it sourcemation/ruby:latest
```

### Advanced usage examples

Example: create a Gemfile for a Ruby project, in your current directory:

```
docker run --rm -v "${PWD}:/your-project" -w "/your-project" sourcemation/ruby:latest bundle init
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
APP_VERSION="3.0.7"
APP_NAME="ruby"
```

This image exposes the following ports: 

- 8000 : the default Rails server port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues](https://github.com/SourceMation/containers/issues/new)
[Creating pull
requests](https://github.com/SourceMation/containers/compare)

**Disclaimer:** The `sourcemation/ruby` image is not affiliated with
Yukihiro Matsumoto and the Ruby Community [the Ruby
Community](https://www.ruby-lang.org/en/community/). The respective
entities own the trademarks mentioned in the offering. The
`sourcemation/ruby` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://www.sourcemation.com/products/cceb8a81-f637-401f-9d6c-83584df8c517/deployments).

For more information, check out the [overview of
Ruby](https://www.ruby-lang.org/en/about/) page.

### Licenses

The base license for the solution (Ruby) is the [Ruby
License](https://www.ruby-lang.org/en/about/license.txt). The licenses
for each component shipped as part of this image can be found on [the
image's appropriate SourceMation
entry](https://www.sourcemation.com/products/cceb8a81-f637-401f-9d6c-83584df8c517/deployments).

