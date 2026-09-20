# Golang 1.27 packaged by Sourcemation

Go (Golang) is a statically typed, compiled programming language developed by
Google. Its simplicity, performance, and robust concurrency features make it perfect for
creating scalable and high-performance applications.

This Golang distribution is packaged from fresh official Google releases by the
Sourcemation automation team. The version is 1.27.X and receives regular updates
to the latest patch version. For developer convenience, the complete `go` toolchain is
pre-installed and ready to use.

The base image is the most recent, at the time of the build,
`sourcemation/debian-13-slim` image. This provides you with a fully independent and
self-contained Golang environment, that is consistently updated and patched.
Additionally, the build process leverages cryptographic signatures to ensure
that the source code remains untampered.

## Go 1.27 new features

Go 1.27 introduces several significant improvements and new features that enhance developer productivity and application performance:

- **Generic Methods**: Concrete methods can now declare their own standalone type parameters, independent of the receiver type, allowing generic operations to live directly on types.
- **Struct Literal Keys**: Keys in struct literals can now be any valid field selector for the struct type, allowing direct initialization of fields in nested or embedded structs.
- **Generalized Function Type Inference**: Function type inference is generalized to apply in all assignment contexts (composite literals, type conversions, and channel sends).
- **Native UUID Support**: The standard library now natively supports generating and parsing UUIDs.
- **Redesigned JSON Processing (`encoding/json/v2`)**: A major redesign that provides configurable options, stricter/safer defaults, and significantly faster unmarshaling.
- **Post-Quantum Cryptography (`crypto/mldsa`)**: Implements the ML-DSA post-quantum digital-signature scheme (FIPS 204), integrated into `crypto/x509` and `crypto/tls`.
- **Size-Specialized Memory Allocation**: Size-specialized routines for objects smaller than 80 bytes reduce allocation overhead by up to 30%, yielding free runtime performance improvements.
- **Toolchain Updates**: `go test` now runs the `stdversion` check by default, reporting uses of standard library symbols too new for the declared `go.mod` version.

These updates make Go 1.27 an excellent choice for modern cloud-native applications, microservices, and high-performance systems.

## Usage

Run a temporary container with the Golang version check:

```bash
docker run --rm -it sourcemation/golang-1.27:latest go version
```

To run the shell in the container, use the following command:

```bash
docker run --rm -it sourcemation/golang-1.27:latest /bin/bash
```

### Advanced usage examples

Run a simple "Hello, World!" Go program from the current directory, with the
port 8080 forwarded:

```bash
docker run --rm -p 8080:8080 -v "${PWD}:/app" -w "/app" -it sourcemation/golang-1.27:latest sh -c 'go run main.go'
```

Build a Go binary from the current directory and run it, this time with podman:

```bash
podman run --rm -p 8080:8080 -v "${PWD}:/app" -w "/app" -it sourcemation/golang-1.27:latest sh -c 'go build -o myapp && ./myapp'
```

## Most important environment variables

This image uses the following environment variables:

```
PATH=/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
GOPATH=/go
GOLANG_VERSION=1.27.X # example: 1.27.1
GOTOOLCHAIN=local
```

## Ports

This image does not expose any ports. However, you can expose the ports you
need by using the `-p` option, setting up the ports manually, or with
kubernetes or docker-compose. You can also create an image with the ports
exposed by default.

## Contributions and Issue Reporting

Contributions are welcome! Propose new features by creating issues or submit
pull requests on the Sourcemation GitHub repository.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)


**Disclaimer:** The `sourcemation/golang-1.27` image is not affiliated with the
Go project or Google. The respective companies and organisations own the
trademarks mentioned in the offering. The `sourcemation/golang-1.27` image is a
separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of our images and its components might be found
on the [Sourcemation platform](https://www.sourcemation.com/).

However, not all images have a risk analysis report yet. If you need risk report
for your images or have any questions, please contact us.

### Licenses

The base license for the solution (Golang) is the [Go
License](https://golang.org/LICENSE).
