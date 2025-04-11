# Erlang packaged by SourceMation

Erlang is a functional programming language designed for building massively
scalable, distributed, fault-tolerant systems with high availability
requirements.


This Docker image provides a clean, lightweight installation of Erlang built
from source on Debian 12 Slim. It includes the latest stable OpenSSL compiled
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
APP_VERSION="27.3.2"
PATH=/opt/erlang/bin:/opt/openssl/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

## Contributing and Issues

We’d love for you to contribute! You can request new features by creating an
issue or submitting a pull request with your contribution to this image on the
SourceMation GitHub repository.


- [Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)


**Disclaimer:** The `sourcemation/erlang` image is not affiliated with
the Ericsson. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/erlang` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

### Licenses

The base license for the solution (Erlang) is the
[Apache License
2.0](https://raw.githubusercontent.com/erlang/otp/refs/heads/master/LICENSE.txt).


The OpenSSL licence is [Apache License
2.0](https://raw.githubusercontent.com/openssl/openssl/refs/heads/master/LICENSE.txt).


The Debian licence is the  [GNU General Public License
v3.0](https://raw.githubusercontent.com/bibledit/debian/refs/heads/main/LICENSE).
