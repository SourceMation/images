# NodeJS 20 with Yarn Classic packed by SourceMation

Node.js is a powerful and adaptable JavaScript runtime that's used to build all
sorts of applications, from simple command-line tools to complex conferencing
systems. Its popularity comes from its vast collection of modules and
widespread use.


This particular version of Node.js is built on the `sourcemation/debian-12-slim`
base image. It includes Node.js version 20 and Yarn Classic (version 1.22.XX).

## Usage

Run a temporary container with the NodeJS REPL (don't forget the `-it` flags).

```bash
docker run --rm -it sourcemation/nodejs-20:latest
```

### Advanced usage examples

Serve the contents of the current directory with your NodeJS project using npm.

```bash
docker run --rm -p 3000:3000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/nodejs-20:latest npm run start
```

Serve the contents of the current directory with your NodeJS project using
yarn.

```bash
docker run --rm -p 3000:3000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/nodejs-20:latest yarn start
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
NODEJS_VERSION=20.YY.ZZ
YARN_VERSION=1.22.XX
```


## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)


Disclaimer: The sourcemation/nodejs image is not affiliated with the
[OpenJS Foundation](https://openjsf.org/). The respective companies and
organisations own the trademarks mentioned in the offering. The
sourcemation/nodejs image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes
### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation platform](https://www.sourcemation.com/)


For more information, check out the [overview of NodeJS®](https://nodejs.org/)
page.

## Licenses

The base license for the solution (NodeJS) is the [MIT License, among ASL 2.0,
ISC and BSD where
appropriate](https://github.com/nodejs/node/blob/main/LICENSE).
