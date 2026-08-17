# NodeJS 26 with Yarn Classic packed by Sourcemation

Leveraging its cross-platform nature and scalable architecture, Node.js® serves
as a powerful JavaScript runtime, facilitating the development of a wide
spectrum of applications, from simple command-line tools to complex
conferencing solutions, all thanks to its vibrant community and extensive
collection of modules.


This particular NodeJS distribution is built upon the
`sourcemation/debian-13-slim` base image and integrates Node.js version 26
along with Yarn Classic, specifically version `1.22.XX`.


**This image is optimized for build reproducibility and contains the packages
needed to compile NodeJS, providing developers with all tools needed in more advanced
NodeJS development - thus it's not a super small image.**

## NodeJS 26 new features

Node.js 26 introduces several significant improvements and modern capabilities:

- **Temporal API Enabled by Default**: The standard `Temporal` API is now stable and enabled globally, providing a modern, immutable, and time-zone-aware alternative to the legacy `Date` object.
- **V8 Engine 14.6**: Brings new ECMAScript capabilities like Map Upsert Helpers (`Map.prototype.getOrInsert`) and Iterator Sequencing (`Iterator.concat`).
- **Stable TypeScript Type Stripping**: Built-in TypeScript type erasure is now fully stable, allowing direct execution of TypeScript files without external transpilers.
- **Undici 8.0**: Improved performance and HTTP/2 handling for the native `fetch()` library.
- **Enhanced Permissions**: The new `permission.drop` API allows running processes to drop their own security privileges dynamically.

## Usage

Launch a temporary container equipped with the NodeJS REPL (remember to include the -it flags).

```bash
docker run --rm -it sourcemation/nodejs-26:latest
```

### Advanced usage examples

Deploy the content of your current directory as a NodeJS project utilizing npm.

```bash
docker run --rm -p 3000:3000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/nodejs-26:latest npm run start
```

Deploy the contents of the current directory with your NodeJS project using
yarn.

```bash
docker run --rm -p 3000:3000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/nodejs-26:latest yarn start
```

## Environment Vars, Ports, Volumes

This image employs the following environment variables:

```
NODEJS_VERSION=26.YY.ZZ
YARN_VERSION=1.22.XX
```

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

Disclaimer: The sourcemation/nodejs image operates independently and is not
affiliated with the [OpenJS Foundation](https://openjsf.org/). All trademarks
mentioned belong to their respective owners. This sourcemation/nodejs image is
a distinct project maintained by [Sourcemation](https://sourcemation.com).

## Extra notes
### Image and its components Risk Analysis report

A comprehensive risk analysis report detailing the image and its components can
be accessed on the [Sourcemation platform](https://www.sourcemation.com/).


For further details, explore the [overview of NodeJS®](https://nodejs.org/)
page.

# Licenses

The fundamental license governing NodeJS is the [MIT License, alongside ASL 2.0, ISC, and BSD where applicable](https://github.com/nodejs/node/blob/main/LICENSE).
