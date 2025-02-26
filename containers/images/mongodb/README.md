# MongoDB packaged by SourceMation

MongoDB is a high-performant, easily scalable NoSQL database management system.
Its flexibility makes it a perfect choice for use cases ranging from handling
web application contents to big data processing.

This MongoDB distribution (Community Edition) is provided by MongoDB,
Inc., packaged as part of a Rocky Linux 9 image by
[SourceMation](https://sourcemation.com).

## Usage

Run a temporary container with the `mongod` server:  
Note: for this self-managed deployment, the recommended ulimit settings
have been provided as per the [official upstream
recommendations](https://www.mongodb.com/docs/manual/reference/ulimit/).

```
docker run --rm --ulimit nofile=64000:64000 --ulimit nproc=64000:64000 -it sourcemation/mongodb:latest
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
HOME="/home/mongodb"
APP_VERSION="8.0.1"
APP_NAME="mongodb"
```

This image exposes the following ports: 

- 27017 : the primary `mongod` daemon port (Note that sharded cluster
  support is beyond the scope of this Dockerfile)

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues](https://github.com/SourceMation/containers/issues/new)
[Creating pull
requests](https://github.com/SourceMation/containers/compare)

**Disclaimer:** The `sourcemation/mongodb` image is not affiliated with
MongoDB, Inc. The respective entities own the trademarks mentioned in
the offering. The `sourcemation/mongodb` image is a separate project and
is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://www.sourcemation.com/products/b95ab2de-202b-45f2-a2a3-086e64968979/deployments).

For more information, check out the [overview of
MongoDB®](https://www.mongodb.com/company/what-is-mongodb) page.

### Licenses

The base license for the solution (MongoDB) is the [Server Side Public
License (SSPL)
v1](https://www.mongodb.com/licensing/server-side-public-license) The
licenses for each component shipped as part of this image can be found
on [the image's appropriate SourceMation
entry](https://www.sourcemation.com/products/b95ab2de-202b-45f2-a2a3-086e64968979/deployments).

