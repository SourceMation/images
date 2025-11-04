# NodeJS 24 with Yarn Classic packed by Sourcemation

Leveraging its cross-platform nature and scalable architecture, Node.js® serves
as a powerful JavaScript runtime, facilitating the development of a wide
spectrum of applications, from simple command-line tools to complex
conferencing solutions, all thanks to its vibrant community and extensive
collection of modules.


This particular NodeJS distribution is built upon the
`sourcemation/debian-13-slim` base image and integrates Node.js version 24
along with Yarn Classic, specifically version `1.22.XX`.


**This image is optimized for build reproducibility and contains the packages
needed to compile NodeJS, providing developers with all tools needed in more advanced
NodeJS development - thus it's not a super small image.**

## Usage

Launch a temporary container equipped with the NodeJS REPL (remember to include the -it flags).

```bash
docker run --rm -it sourcemation/nodejs-24:latest
```

### Advanced usage examples

Deploy the content of your current directory as a NodeJS project utilizing npm.

```bash
docker run --rm -p 3000:3000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/nodejs-24:latest npm run start
```

Deploy the contents of the current directory with your NodeJS project using
yarn.

```bash
docker run --rm -p 3000:3000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/nodejs-24:latest yarn start
```

## Environment Vars, Ports, Volumes

This image employs the following environment variables:

```
NODEJS_VERSION=24.YY.ZZ
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

The fundamental license governing NodeJS is the [MIT License, alongside ASL
2.0, ISC, and BSD where
applicable](https://github.com/nodejs/node/blob/main/LICENSE).
