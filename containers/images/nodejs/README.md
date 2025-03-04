# NodeJS packaged by SourceMation

Node.js® is a cross-platform, scalable JavaScript engine. Accompanied by its
popularity, and rich module collection, it lets you build various tools,
ranging from simple command-line applications to conferencing platforms.

This NodeJS distribution is provided by the downstream Rocky Linux 9 packaging
team in the version respective to that system (in particular, the `nodejs:20`
module, providing version 20.16).

## Usage

Run a temporary container with the NodeJS REPL (don't forget the `-it`
argument).

```
docker run --rm -it sourcemation/nodejs:latest
```

### Advanced usage examples

Serve the contents of the current directory with your NodeJS project.

```
docker run --rm -p 3000:3000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/nodejs:latest npm run start
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

This image exposes the following ports:

- 3000 : the default NodeJS' builtin HTTP server port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/nodejs` image is not affiliated with the
[OpenJS Foundation](https://openjsf.org/). The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/nodejs` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation
platform](https://www.sourcemation.com/products/429046c0-5dcd-4b05-af53-0074be75cd01/deployments).

For more information, check out the [overview of NodeJS®](https://nodejs.org/)
page.

### Licenses

The base license for the solution (NodeJS) is the [MIT License, among ASL 2.0,
ISC and BSD where
appropriate](https://github.com/nodejs/node/blob/main/LICENSE). The licenses
for each component shipped as part of this image can be found on [the image's
appropriate SourceMation
entry](https://www.sourcemation.com/products/429046c0-5dcd-4b05-af53-0074be75cd01/deployments).
