# Angular packaged by Sourcemation

Angular is one of the most popular JavaScript frameworks. Its performance,
along with the ability to handle complex enterprise applications make it a top
choice for building Single Page Applications.

This Angular distribution is provided by the upstream developers, hosted at
[registry.npmjs.org](https://registry.npmjs.org/).

The image uses Sourcemation independent image stack as its base, which is a
minimal Debian-based image with a small footprint, built from scratch. Also
the default version of NodeJS is Node.js 24 which is the current active LTS.


## Usage

Run a temporary container with the Angular CLI serving the project in your
current directory:

```
docker run --rm -p 3000:3000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/angular:latest ng serve
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

This image exposes the following ports:

- 3000 : the default NodeJS' builtin HTTP server port used by Angular

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)


**Disclaimer:** The `sourcemation/angular` image is not affiliated with Google
LLC. The respective companies and organisations own the trademarks mentioned in
the offering. The `sourcemation/angular` image is a separate project and is
maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [Sourcemation
platform](https://www.sourcemation.com/products/0af955c3-bc56-4592-a769-744bb9b3a7b9/deployments).

For more information, check out the [overview of Angular
CLI](https://angular.dev/tools/cli) page.

### Licenses

The base license for the solution (Angular) is the [MIT
License](https://github.com/angular/angular-cli/blob/main/LICENSE). The
licenses for each component shipped as part of this image can be found on [the
image's appropriate Sourcemation
entry](https://www.sourcemation.com/products/0af955c3-bc56-4592-a769-744bb9b3a7b9/deployments).
