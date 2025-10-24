# Golang 1.24 packaged by SourceMation

Go (Golang) is a statically typed, compiled programming language designed at
Google. Its simplicity, efficiency, and concurrency support make it ideal for
building scalable and high-performance applications.

This Golang distribution is packed from fresh official Google builds by the
SourceMation automation team. The version is 1.24.X and it's regularly updated
to the latest patch version. For user convenience, the `go` toolchain is
pre-installed and ready to use.

The base image is the latest, at the time of the build,
`sourcemation/debian-13-slim` image. It's gives you fully independent and
self-contained Golang environment, that is regularly updated and patched.
Lastly the build process takes advantage of cryptographic signatures to ensure
that the source code is not tampered with.

## Usage

Run a temporary container with the Golang version check:

```bash
docker run --rm -it sourcemation/golang-1.24:latest go version
```

To run the shell in the container, use the following command:

```bash
docker run --rm -it sourcemation/golang-1.24:latest /bin/bash
```

### Advanced usage examples

Run a simple "Hello, World!" Go program from the current directory, with the
port 8080 forwarded:

```bash
docker run --rm -p 8080:8080 -v "${PWD}:/app" -w "/app" -it sourcemation/golang-1.24:latest sh -c 'go run main.go'
```

Build a Go binary from the current directory and run it, this time with podman:

```bash
podman run --rm -p 8080:8080 -v "${PWD}:/app" -w "/app" -it sourcemation/golang-1.24:latest sh -c 'go build -o myapp && ./myapp'
```

## Most important environment variables

This image uses the following environment variables:

```
PATH=/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
GOPATH=/go
GOLANG_VERSION=1.24.X # example: 1.24.1
GOTOOLCHAIN=local
```

## Ports

This image does not expose any ports. However, you can expose the ports you
need by using the `-p` option, setting up the ports manually, or with
kubernetes or docker-compose. You can also create an image with the ports
exposed by default.

## Contributions and Issue Reporting

Contributions are welcome! Propose new features by creating issues or submit
pull requests on the SourceMation GitHub repository.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)


**Disclaimer:** The `sourcemation/golang-1.24` image is not affiliated with the
Go project or Google. The respective companies and organisations own the
trademarks mentioned in the offering. The `sourcemation/golang-1.24` image is a
separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of our images and its components might be found
on the [SourceMation platform](https://www.sourcemation.com/).

However, not all images have a risk analysis report yet. If need risk report
for you images, have any questions, please contact us.

### Licenses

The base license for the solution (Golang) is the [Go
License](https://golang.org/LICENSE).
