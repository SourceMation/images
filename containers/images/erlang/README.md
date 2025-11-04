# Erlang packaged by Sourcemation

Erlang is a functional programming language designed for building massively
scalable, distributed, fault-tolerant systems with high availability
requirements.


This Docker image provides a clean, lightweight installation of Erlang built
from source on Debian 13 Slim. It includes the latest stable OpenSSL compiled
from the source to ensure maximum security and performance.

## Usage

Run a temporary container with the Erlang

```
docker run --rm -it sourcemation/erlang
```

### Advanced usage examples (running an erlang app)

```
docker run --rm -it -v $(pwd):/app sourcemation/erlang erl -pa /app/ebin
```

## Environment Vars

This image uses the following environment variables:

```
APP_NAME="erlang"
APP_VERSION="28.1.1"
PATH=/opt/erlang/bin:/opt/openssl/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

## Contributing and Issues

We welcome your contributions! If you have new feature requests, want to report
a bug, or wish to submit a pull request with your code or an image request, you
can do so via the Sourcemation GitHub repository for this image.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/Sourcemation/images/issues/new/choose)
- [Submit a pull request](https://github.com/Sourcemation/images/compare)


**Disclaimer:** The `sourcemation/erlang` image is not affiliated with
the Ericsson. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/erlang` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

### Licenses

The base license for the solution (Erlang) is the
[Apache License
2.0](https://raw.githubusercontent.com/erlang/otp/refs/heads/master/LICENSE.txt).


The OpenSSL licence is [Apache License
2.0](https://raw.githubusercontent.com/openssl/openssl/refs/heads/master/LICENSE.txt).


The Debian licence is the  [GNU General Public License
v3.0](https://raw.githubusercontent.com/bibledit/debian/refs/heads/main/LICENSE).
